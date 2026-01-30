"""
Module du clavier virtuel
Gère l'affichage, les interactions et la logique du clavier
"""

import pygame
from typing import List, Optional, Tuple
import config


class Key:
    """Représente une touche du clavier virtuel"""
    
    def __init__(self, x: int, y: int, char: str, w: int = None, h: int = None):
        """
        Initialise une touche
        
        Args:
            x: Position X
            y: Position Y
            char: Caractère de la touche
            w: Largeur (optionnel, utilise config par défaut)
            h: Hauteur (optionnel, utilise config par défaut)
        """
        self.x = x
        self.y = y
        self.char = char
        self.w = w or config.KEY_WIDTH
        self.h = h or config.KEY_HEIGHT
        
        # État de la touche
        self.is_hovered = False
        self.is_pressed = False
        
        # Animation
        self.press_animation = 0  # 0 à 1
        
    def update(self, cursor_pos: Optional[Tuple[int, int]], clicking: bool) -> bool:
        """
        Met à jour l'état de la touche
        
        Args:
            cursor_pos: Position du curseur (x, y) ou None
            clicking: État du clic
            
        Returns:
            True si la touche a été cliquée
        """
        was_pressed = self.is_pressed
        self.is_hovered = False
        
        if cursor_pos:
            if self.x < cursor_pos[0] < self.x + self.w and self.y < cursor_pos[1] < self.y + self.h:
                self.is_hovered = True
                self.is_pressed = clicking
            else:
                self.is_pressed = False
        else:
            self.is_pressed = False
        
        # Animation de pression
        if self.is_pressed:
            self.press_animation = min(1.0, self.press_animation + 0.2)
        else:
            self.press_animation = max(0.0, self.press_animation - 0.15)
        
        
        # Retourne True si la touche vient d'être pressée (changement d'état)
        # Simplifié: on déclenche dès qu'on appuie, pas besoin d'attendre le relâchement
        result = not was_pressed and self.is_pressed and self.is_hovered
        if result:
            print(f"DEBUG Key '{self.char}': TRIGGERED!")
        return result
    
    def draw(self, screen: pygame.Surface, theme: dict, font: pygame.font.Font):
        """
        Dessine la touche avec effet glassmorphism
        
        Args:
            screen: Surface Pygame
            theme: Dictionnaire du thème de couleurs
            font: Police pour le texte
        """
        # Déterminer la couleur et l'épaisseur
        if self.is_pressed:
            color = theme['key_pressed']
            thickness = config.KEY_BORDER_THICKNESS_PRESSED
        elif self.is_hovered:
            color = theme['key_hover']
            thickness = config.KEY_BORDER_THICKNESS_HOVER
        else:
            color = theme['key_normal']
            thickness = config.KEY_BORDER_THICKNESS_NORMAL
        
        # Effet de pression (légère réduction de taille)
        offset = int(self.press_animation * 4)
        draw_rect = (
            self.x + offset,
            self.y + offset,
            self.w - offset * 2,
            self.h - offset * 2
        )
        
        # Ombre portée (si pressé ou survolé)
        if self.is_hovered or self.is_pressed:
            shadow_offset = 3 if self.is_pressed else 5
            shadow_rect = (
                draw_rect[0] + shadow_offset,
                draw_rect[1] + shadow_offset,
                draw_rect[2],
                draw_rect[3]
            )
            shadow_surface = pygame.Surface((draw_rect[2], draw_rect[3]), pygame.SRCALPHA)
            shadow_color = (0, 0, 0, 80)
            pygame.draw.rect(
                shadow_surface,
                shadow_color,
                (0, 0, draw_rect[2], draw_rect[3]),
                border_radius=config.KEY_BORDER_RADIUS
            )
            screen.blit(shadow_surface, (shadow_rect[0], shadow_rect[1]))
        
        # Fond glassmorphism (semi-transparent)
        if self.press_animation > 0 or self.is_hovered:
            alpha = int(100 + (self.press_animation * 100))
            # Handle RGBA colors by taking only the first 3 components (RGB)
            rgb = color[:3]
            fill_color = tuple(int(c * 0.4) for c in rgb) + (alpha,)
            glass_surface = pygame.Surface((draw_rect[2], draw_rect[3]), pygame.SRCALPHA)
            pygame.draw.rect(
                glass_surface,
                fill_color,
                (0, 0, draw_rect[2], draw_rect[3]),
                border_radius=config.KEY_BORDER_RADIUS
            )
            screen.blit(glass_surface, (draw_rect[0], draw_rect[1]))
        
        # Dessiner le contour avec glow si survolé
        if self.is_hovered:
            # Glow externe
            glow_surface = pygame.Surface((draw_rect[2] + 10, draw_rect[3] + 10), pygame.SRCALPHA)
            # Handle RGBA by taking RGB parts and adding fixed alpha
            glow_color = color[:3] + (50,)
            pygame.draw.rect(
                glow_surface,
                glow_color,
                (0, 0, draw_rect[2] + 10, draw_rect[3] + 10),
                border_radius=config.KEY_BORDER_RADIUS + 2
            )
            screen.blit(glow_surface, (draw_rect[0] - 5, draw_rect[1] - 5))
        
        # Contour principal
        pygame.draw.rect(
            screen,
            color,
            draw_rect,
            thickness,
            border_radius=config.KEY_BORDER_RADIUS
        )
        
        # Dessiner le texte avec ombre
        label = self._get_label()
        
        # Ombre du texte
        text_shadow = font.render(label, True, (0, 0, 0))
        shadow_rect = text_shadow.get_rect(
            center=(self.x + self.w // 2 + 2, self.y + self.h // 2 + 2)
        )
        screen.blit(text_shadow, shadow_rect)
        
        # Texte principal
        text_surface = font.render(label, True, color)
        text_rect = text_surface.get_rect(
            center=(self.x + self.w // 2, self.y + self.h // 2)
        )
        screen.blit(text_surface, text_rect)
    
    def _get_label(self) -> str:
        """Retourne le label à afficher sur la touche"""
        if self.char == "<-":
            return "BS"
        elif self.char == " ":
            return "SPACE"
        elif self.char == "SHIFT":
            return "⇧"
        elif self.char == "ENTER":
            return "↵"
        else:
            return self.char


class VirtualKeyboard:
    """Clavier virtuel complet"""
    
    def __init__(self, layout_name: str = None):
        """
        Initialise le clavier virtuel
        
        Args:
            layout_name: Nom du layout (QWERTY, AZERTY, etc.)
        """
        self.layout_name = layout_name or config.DEFAULT_LAYOUT
        self.keys: List[Key] = []
        self.typed_text = ""
        # Tracking séparé pour chaque main
        self.last_clicked_char_left = ""
        self.last_clicked_char_right = ""
        # État du Shift
        self.shift_active = False
        
        # Créer les touches
        self._create_keys()
        
    def _create_keys(self):
        """Crée toutes les touches du clavier"""
        layout = config.KEYBOARD_LAYOUTS[self.layout_name]
        
        for i, row in enumerate(layout):
            # Position X cumulative pour cette rangée
            current_x = config.KEY_START_X
            
            for j, char in enumerate(row):
                # Largeur spéciale pour certaines touches
                if char == " ":
                    w = config.SPACE_KEY_WIDTH
                elif char == "<-":
                    w = config.BACKSPACE_KEY_WIDTH
                elif char == "SHIFT":
                    w = config.SHIFT_KEY_WIDTH
                elif char == "ENTER":
                    w = config.ENTER_KEY_WIDTH
                else:
                    w = config.KEY_WIDTH
                
                # Position Y basée sur la rangée
                y = config.KEY_SPACING * i + config.KEY_START_Y
                
                # Créer la touche à la position X actuelle
                self.keys.append(Key(current_x, y, char, w=w))
                
                # Incrémenter X pour la prochaine touche
                # Ajouter la largeur de la touche actuelle + un petit espacement
                current_x += w + 10  # 10 pixels d'espacement entre les touches
    
    def update(self, cursor_pos_left: Optional[Tuple[int, int]], clicking_left: bool,
               cursor_pos_right: Optional[Tuple[int, int]], clicking_right: bool) -> Optional[str]:
        """
        Met à jour le clavier avec deux curseurs
        
        Args:
            cursor_pos_left: Position du curseur main gauche
            clicking_left: État du clic main gauche
            cursor_pos_right: Position du curseur main droite
            clicking_right: État du clic main droite
            
        Returns:
            Caractère tapé ou None (peut être plusieurs si clics simultanés)
        """
        typed_chars = []
        
        # Traiter chaque main séparément
        for key in self.keys:
            # Main gauche
            if key.update(cursor_pos_left, clicking_left):
                if key.char != self.last_clicked_char_left or not clicking_left:
                    char = self._process_key_press(key)
                    if char:
                        typed_chars.append(char)
                    self.last_clicked_char_left = key.char
            
            # Main droite (réinitialiser l'état hover/pressed pour la deuxième vérification)
            # Sauvegarder l'état actuel
            saved_hover = key.is_hovered
            saved_pressed = key.is_pressed
            
            if key.update(cursor_pos_right, clicking_right):
                # Vérifier que ce n'est pas la même touche que la main gauche
                if key.char != self.last_clicked_char_right or not clicking_right:
                    # Éviter de taper deux fois si les deux mains sont sur la même touche
                    if key.char != self.last_clicked_char_left or not clicking_left:
                        char = self._process_key_press(key)
                        if char:
                            typed_chars.append(char)
                    self.last_clicked_char_right = key.char
            
            # Combiner les états hover/pressed des deux mains pour l'affichage
            key.is_hovered = saved_hover or key.is_hovered
            key.is_pressed = saved_pressed or key.is_pressed
        
        # Réinitialiser le tracking si on ne clique plus
        if not clicking_left:
            self.last_clicked_char_left = ""
        if not clicking_right:
            self.last_clicked_char_right = ""
        
        # Retourner le premier caractère tapé (ou None)
        return typed_chars[0] if typed_chars else None
    
    def _process_key_press(self, key: Key) -> Optional[str]:
        """
        Traite l'appui sur une touche
        
        Args:
            key: Touche pressée
            
        Returns:
            Caractère tapé ou None
        """
        # Gestion des touches spéciales
        if key.char == "SHIFT":
            # Toggle shift
            self.shift_active = not self.shift_active
            return None
        elif key.char == "ENTER":
            # Nouvelle ligne
            self.typed_text += "\n"
            return "\n"
        elif key.char == "<-":
            # Backspace
            if self.typed_text:
                self.typed_text = self.typed_text[:-1]
                return "<-"
        else:
            # Caractère normal - appliquer shift si actif
            char = key.char
            if self.shift_active:
                char = self._apply_shift(char)
                # Désactiver shift après utilisation (comportement standard)
                self.shift_active = False
            
            self.typed_text += char
            return char
        return None
    
    def _apply_shift(self, char: str) -> str:
        """
        Applique la transformation Shift à un caractère
        
        Args:
            char: Caractère à transformer
            
        Returns:
            Caractère transformé
        """
        # Mapping des transformations Shift
        shift_map = {
            '1': '!', '2': '@', '3': '#', '4': '$', '5': '%',
            '6': '^', '7': '&', '8': '*', '9': '(', '0': ')',
            '-': '_', '=': '+', '[': '{', ']': '}',
            ';': ':', "'": '"', ',': '<', '.': '>', '/': '?'
        }
        
        # Si c'est une lettre, mettre en majuscule
        if char.isalpha():
            return char.upper()
        # Si c'est dans le mapping, retourner le symbole
        elif char in shift_map:
            return shift_map[char]
        else:
            return char
    
    def draw(self, screen: pygame.Surface, theme: dict, font: pygame.font.Font):
        """
        Dessine le clavier
        
        Args:
            screen: Surface Pygame
            theme: Thème de couleurs
            font: Police pour les touches
        """
        # Dessiner les zones intelligentes si activées
        if config.ENABLE_SMART_ZONES:
            self._draw_smart_zones(screen, theme)
        
        for key in self.keys:
            key.draw(screen, theme, font)
    
    def _draw_smart_zones(self, screen: pygame.Surface, theme: dict):
        """
        Dessine les zones intelligentes (gauche/droite)
        
        Args:
            screen: Surface Pygame
            theme: Thème de couleurs
        """
        if not self.keys:
            return
        
        # Trouver les limites du clavier
        min_x = min(k.x for k in self.keys)
        max_x = max(k.x + k.w for k in self.keys)
        min_y = min(k.y for k in self.keys)
        max_y = max(k.y + k.h for k in self.keys)
        
        # Point milieu
        mid_x = (min_x + max_x) // 2
        
        # Zone gauche (bleutée)
        left_zone_width = mid_x - min_x
        left_zone_height = max_y - min_y
        
        left_surface = pygame.Surface((left_zone_width, left_zone_height), pygame.SRCALPHA)
        left_color = theme['cursor']
        # Ensure we only use RGB for tint calculation if cursor becomes RGBA
        left_color_rgb = left_color[:3]
        left_tint = tuple(min(255, max(0, c + offset)) 
                         for c, offset in zip(left_color_rgb, config.LEFT_ZONE_COLOR_TINT))
        left_tint_alpha = left_tint + (int(255 * config.ZONE_OPACITY),)
        left_surface.fill(left_tint_alpha)
        screen.blit(left_surface, (min_x, min_y))
        
        # Zone droite (orangée)
        right_zone_width = max_x - mid_x
        right_zone_height = max_y - min_y
        
        right_surface = pygame.Surface((right_zone_width, right_zone_height), pygame.SRCALPHA)
        right_color = theme['cursor']
        # Ensure we only use RGB for tint calculation
        right_color_rgb = right_color[:3]
        right_tint = tuple(min(255, max(0, c + offset)) 
                          for c, offset in zip(right_color_rgb, config.RIGHT_ZONE_COLOR_TINT))
        right_tint_alpha = right_tint + (int(255 * config.ZONE_OPACITY),)
        right_surface.fill(right_tint_alpha)
        screen.blit(right_surface, (mid_x, min_y))
    
    def get_text(self) -> str:
        """Retourne le texte tapé"""
        return self.typed_text
    
    def set_text(self, text: str):
        """Définit le texte tapé"""
        self.typed_text = text
    
    def clear_text(self):
        """Efface tout le texte"""
        self.typed_text = ""
    
    def change_layout(self, layout_name: str):
        """
        Change le layout du clavier
        
        Args:
            layout_name: Nom du nouveau layout
        """
        if layout_name in config.KEYBOARD_LAYOUTS:
            self.layout_name = layout_name
            self.keys.clear()
            self._create_keys()
