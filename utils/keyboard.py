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
        
        # Retourne True si la touche vient d'être relâchée (clic complet)
        return was_pressed and not self.is_pressed and self.is_hovered
    
    def draw(self, screen: pygame.Surface, theme: dict, font: pygame.font.Font):
        """
        Dessine la touche
        
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
        
        # Dessiner le fond si pressé (effet de remplissage)
        if self.press_animation > 0:
            fill_color = tuple(int(c * 0.3) for c in color)
            pygame.draw.rect(
                screen,
                fill_color,
                draw_rect,
                border_radius=config.KEY_BORDER_RADIUS
            )
        
        # Dessiner le contour
        pygame.draw.rect(
            screen,
            color,
            draw_rect,
            thickness,
            border_radius=config.KEY_BORDER_RADIUS
        )
        
        # Dessiner le texte
        label = self._get_label()
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
        if key.char == "<-":
            # Backspace
            if self.typed_text:
                self.typed_text = self.typed_text[:-1]
                return "<-"
        else:
            # Caractère normal
            self.typed_text += key.char
            return key.char
        return None
    
    def draw(self, screen: pygame.Surface, theme: dict, font: pygame.font.Font):
        """
        Dessine le clavier
        
        Args:
            screen: Surface Pygame
            theme: Thème de couleurs
            font: Police pour les touches
        """
        for key in self.keys:
            key.draw(screen, theme, font)
    
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
