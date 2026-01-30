"""
Composants d'interface utilisateur
Contient les éléments visuels réutilisables
"""

import pygame
import math
import random
from typing import Optional, Tuple, List
import config


class TextBox:
    """Zone de texte avec effet glassmorphism"""
    
    def __init__(self):
        """Initialise la zone de texte"""
        self.x = config.TEXT_BOX_X
        self.y = config.TEXT_BOX_Y
        self.w = config.TEXT_BOX_WIDTH
        self.h = config.TEXT_BOX_HEIGHT
        
    def draw(self, screen: pygame.Surface, text: str, theme: dict, font: pygame.font.Font):
        """
        Dessine la zone de texte avec glassmorphism
        
        Args:
            screen: Surface Pygame
            text: Texte à afficher
            theme: Thème de couleurs
            font: Police pour le texte
        """
        # Fond glassmorphism avec blur simulé
        bg_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        
        # Check if theme color has alpha
        theme_bg = theme['text_box_bg']
        if len(theme_bg) == 4:
            bg_color = theme_bg
        else:
            bg_color = theme_bg + (220,)  # Default opacity if not specified
            
        pygame.draw.rect(
            bg_surface,
            bg_color,
            (0, 0, self.w, self.h),
            border_radius=config.TEXT_BOX_BORDER_RADIUS
        )
        screen.blit(bg_surface, (self.x, self.y))
        
        # Glow externe
        glow_surface = pygame.Surface((self.w + 10, self.h + 10), pygame.SRCALPHA)
        
        theme_border = theme['text_box_border']
        if len(theme_border) == 4:
             # If border has alpha, use a fraction of it for glow, or fixed low alpha
             glow_color = theme_border[:3] + (30,)
        else:
             glow_color = theme_border + (30,)
             
        pygame.draw.rect(
            glow_surface,
            glow_color,
            (0, 0, self.w + 10, self.h + 10),
            border_radius=config.TEXT_BOX_BORDER_RADIUS + 2
        )
        screen.blit(glow_surface, (self.x - 5, self.y - 5))
        
        # Contour lumineux
        pygame.draw.rect(
            screen,
            theme['text_box_border'],
            (self.x, self.y, self.w, self.h),
            3,
            border_radius=config.TEXT_BOX_BORDER_RADIUS
        )
        
        # Texte avec défilement si trop long
        text_surface = font.render(text, True, theme['text'])
        
        # Calculer la position pour que le texte soit visible
        text_x = self.x + config.TEXT_BOX_PADDING
        if text_surface.get_width() > self.w - config.TEXT_BOX_PADDING * 2:
            # Décaler vers la gauche si trop long
            text_x = self.x + self.w - config.TEXT_BOX_PADDING - text_surface.get_width()
        
        text_y = self.y + (self.h - text_surface.get_height()) // 2
        
        # Ombre du texte
        text_shadow = font.render(text, True, (0, 0, 0))
        screen.blit(text_shadow, (text_x + 2, text_y + 2))
        
        # Texte principal
        screen.blit(text_surface, (text_x, text_y))


class StatusBar:
    """Barre d'état affichant les informations système"""
    
    def __init__(self):
        """Initialise la barre d'état"""
        self.fps = 0
        self.theme_name = ""
        
    def update(self, fps: float, theme_name: str):
        """
        Met à jour les informations
        
        Args:
            fps: FPS actuel
            theme_name: Nom du thème actuel
        """
        self.fps = fps
        self.theme_name = theme_name
        
    def draw(self, screen: pygame.Surface, theme: dict, font: pygame.font.Font):
        """
        Dessine la barre d'état
        
        Args:
            screen: Surface Pygame
            theme: Thème de couleurs
            font: Police pour le texte
        """
        if not config.SHOW_FPS:
            return
        
        # Fond
        bar_height = 40
        bg_surface = pygame.Surface((config.WINDOW_WIDTH, bar_height), pygame.SRCALPHA)
        
        theme_status = theme['status_bar']
        if len(theme_status) == 4:
            bg_color = theme_status
        else:
            bg_color = theme_status + (150,)
            
        bg_surface.fill(bg_color)
        screen.blit(bg_surface, (0, config.WINDOW_HEIGHT - bar_height))
        
        # Texte FPS
        fps_text = f"FPS: {int(self.fps)}"
        fps_surface = font.render(fps_text, True, theme['text'])
        screen.blit(fps_surface, (10, config.WINDOW_HEIGHT - bar_height + 10))
        
        # Texte thème
        theme_text = f"Thème: {self.theme_name}"
        theme_surface = font.render(theme_text, True, theme['text'])
        screen.blit(
            theme_surface,
            (config.WINDOW_WIDTH - theme_surface.get_width() - 10,
             config.WINDOW_HEIGHT - bar_height + 10)
        )
        
        # Instructions
        instructions = "ESC: Menu | T: Changer thème | S: Sauvegarder"
        inst_surface = font.render(instructions, True, theme['text'])
        inst_x = (config.WINDOW_WIDTH - inst_surface.get_width()) // 2
        screen.blit(inst_surface, (inst_x, config.WINDOW_HEIGHT - bar_height + 10))


class Particle:
    """Particule pour les effets visuels"""
    
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        """
        Initialise une particule
        
        Args:
            x: Position X initiale
            y: Position Y initiale
            color: Couleur de la particule
        """
        self.x = float(x)
        self.y = float(y)
        self.color = color
        
        # Vélocité aléatoire
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(1, 3)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # Durée de vie
        self.lifetime = config.PARTICLE_LIFETIME
        self.max_lifetime = config.PARTICLE_LIFETIME
        
    def update(self):
        """Met à jour la particule"""
        self.x += self.vx
        self.y += self.vy
        self.lifetime -= 1
        
        # Ralentir progressivement
        self.vx *= 0.95
        self.vy *= 0.95
        
    def is_alive(self) -> bool:
        """Retourne True si la particule est encore vivante"""
        return self.lifetime > 0
    
    def draw(self, screen: pygame.Surface):
        """Dessine la particule"""
        # Alpha basé sur la durée de vie restante
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        size = int(5 * (self.lifetime / self.max_lifetime))
        
        if size > 0:
            particle_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            color_with_alpha = self.color + (alpha,)
            pygame.draw.circle(particle_surface, color_with_alpha, (size, size), size)
            screen.blit(particle_surface, (int(self.x) - size, int(self.y) - size))


class ParticleSystem:
    """Système de particules pour les effets visuels"""
    
    def __init__(self):
        """Initialise le système de particules"""
        self.particles: List[Particle] = []
        
    def emit(self, x: int, y: int, color: Tuple[int, int, int], count: int = None):
        """
        Émet des particules
        
        Args:
            x: Position X
            y: Position Y
            color: Couleur des particules
            count: Nombre de particules (optionnel)
        """
        if not config.ENABLE_ANIMATIONS:
            return
        
        count = count or config.PARTICLE_COUNT
        for _ in range(count):
            self.particles.append(Particle(x, y, color))
    
    def update(self):
        """Met à jour toutes les particules"""
        for particle in self.particles:
            particle.update()
        
        # Supprimer les particules mortes
        self.particles = [p for p in self.particles if p.is_alive()]
    
    def draw(self, screen: pygame.Surface):
        """Dessine toutes les particules"""
        for particle in self.particles:
            particle.draw(screen)
    
    def clear(self):
        """Supprime toutes les particules"""
        self.particles.clear()


class Cursor:
    """Curseur visuel pour le doigt"""
    
    def __init__(self):
        """Initialise le curseur"""
        self.pulse = 0  # Pour l'animation de pulsation
        
    def update(self):
        """Met à jour l'animation du curseur"""
        self.pulse = (self.pulse + 0.1) % (2 * math.pi)
    
    def draw(self, screen: pygame.Surface, pos: Tuple[int, int], theme: dict, clicking: bool = False):
        """
        Dessine le curseur (version par défaut - main droite)
        
        Args:
            screen: Surface Pygame
            pos: Position (x, y)
            theme: Thème de couleurs
            clicking: True si en train de cliquer
        """
        self.draw_right(screen, pos, theme, clicking)
    
    def draw_left(self, screen: pygame.Surface, pos: Tuple[int, int], theme: dict, clicking: bool = False):
        """
        Dessine le curseur de la main gauche
        
        Args:
            screen: Surface Pygame
            pos: Position (x, y)
            theme: Thème de couleurs
            clicking: True si en train de cliquer
        """
        x, y = pos
        # Couleur légèrement modifiée pour la main gauche (plus bleutée)
        base_color = theme['cursor']
        color = tuple(min(255, max(0, c + offset)) for c, offset in zip(base_color, (-20, -10, 20)))
        
        self._draw_cursor_shape(screen, x, y, color, clicking, "L")
    
    def draw_right(self, screen: pygame.Surface, pos: Tuple[int, int], theme: dict, clicking: bool = False):
        """
        Dessine le curseur de la main droite
        
        Args:
            screen: Surface Pygame
            pos: Position (x, y)
            theme: Thème de couleurs
            clicking: True si en train de cliquer
        """
        x, y = pos
        # Couleur légèrement modifiée pour la main droite (plus orangée)
        base_color = theme['cursor']
        color = tuple(min(255, max(0, c + offset)) for c, offset in zip(base_color, (20, 10, -20)))
        
        self._draw_cursor_shape(screen, x, y, color, clicking, "R")
    
    def _draw_cursor_shape(self, screen: pygame.Surface, x: int, y: int, color: Tuple[int, int, int], 
                          clicking: bool, label: str):
        """
        Dessine la forme du curseur
        
        Args:
            screen: Surface Pygame
            x, y: Position
            color: Couleur du curseur
            clicking: True si en train de cliquer
            label: Label à afficher (L ou R)
        """
        # Rayon avec pulsation
        pulse_offset = int(math.sin(self.pulse) * 3)
        outer_radius = config.CURSOR_OUTER_RADIUS + pulse_offset
        
        # Cercle extérieur
        pygame.draw.circle(screen, color, (x, y), outer_radius, config.CURSOR_THICKNESS)
        
        # Point central
        pygame.draw.circle(screen, color, (x, y), config.CURSOR_INNER_RADIUS)
        
        # Effet de clic (cercle qui se rétrécit)
        if clicking:
            click_radius = outer_radius - 5
            pygame.draw.circle(screen, color, (x, y), click_radius, 1)
        
        # Lignes de visée (croix)
        line_length = 10
        pygame.draw.line(screen, color, (x - line_length, y), (x - 5, y), 1)
        pygame.draw.line(screen, color, (x + 5, y), (x + line_length, y), 1)
        pygame.draw.line(screen, color, (x, y - line_length), (x, y - 5), 1)
        pygame.draw.line(screen, color, (x, y + 5), (x, y + line_length), 1)
        
        # Label pour identifier la main
        font = pygame.font.Font(None, 20)
        label_surface = font.render(label, True, color)
        label_rect = label_surface.get_rect(center=(x, y - outer_radius - 10))
        screen.blit(label_surface, label_rect)


class StatsDisplay:
    """Affichage des statistiques de frappe"""
    
    def __init__(self):
        """Initialise l'affichage des stats"""
        self.x = config.STATS_POSITION_X
        self.y = config.STATS_POSITION_Y
        
    def draw(self, screen: pygame.Surface, stats: dict, theme: dict, font: pygame.font.Font):
        """
        Dessine les statistiques
        
        Args:
            screen: Surface Pygame
            stats: Dictionnaire des statistiques
            theme: Thème de couleurs
            font: Police pour le texte
        """
        if not config.ENABLE_STATS:
            return
        
        color = theme['text']
        y_offset = 0
        
        # WPM (plus gros)
        wpm_text = f"WPM: {int(stats['wpm'])}"
        wpm_font = pygame.font.Font(None, config.STATS_FONT_SIZE + 10)
        wpm_surface = wpm_font.render(wpm_text, True, theme['key_hover'])
        screen.blit(wpm_surface, (self.x, self.y + y_offset))
        y_offset += 30
        
        # Précision
        acc_text = f"Précision: {int(stats['accuracy'])}%"
        acc_surface = font.render(acc_text, True, color)
        screen.blit(acc_surface, (self.x, self.y + y_offset))
        y_offset += 25
        
        # Temps de session
        time_text = f"Temps: {stats['session_time_formatted']}"
        time_surface = font.render(time_text, True, color)
        screen.blit(time_surface, (self.x, self.y + y_offset))
        y_offset += 25
        
        # Caractères
        chars_text = f"Caractères: {stats['total_chars']}"
        chars_surface = font.render(chars_text, True, color)
        screen.blit(chars_surface, (self.x, self.y + y_offset))


class TrailEffect:
    """Effet de traînée derrière les curseurs"""
    
    def __init__(self):
        """Initialise l'effet de traînée"""
        self.left_trail = []
        self.right_trail = []
        
    def update(self, left_pos: Optional[Tuple[int, int]], right_pos: Optional[Tuple[int, int]]):
        """
        Met à jour les traînées
        
        Args:
            left_pos: Position curseur gauche
            right_pos: Position curseur droite
        """
        if not config.ENABLE_TRAIL_EFFECT:
            return
        
        # Ajouter positions actuelles
        if left_pos:
            self.left_trail.append(left_pos)
            if len(self.left_trail) > config.TRAIL_LENGTH:
                self.left_trail.pop(0)
        
        if right_pos:
            self.right_trail.append(right_pos)
            if len(self.right_trail) > config.TRAIL_LENGTH:
                self.right_trail.pop(0)
    
    def draw(self, screen: pygame.Surface, theme: dict):
        """
        Dessine les traînées
        
        Args:
            screen: Surface Pygame
            theme: Thème de couleurs
        """
        if not config.ENABLE_TRAIL_EFFECT:
            return
        
        self._draw_trail(screen, self.left_trail, theme['cursor'], -20, -10, 20)
        self._draw_trail(screen, self.right_trail, theme['cursor'], 20, 10, -20)
    
    def _draw_trail(self, screen: pygame.Surface, trail: List[Tuple[int, int]], 
                   base_color: Tuple[int, int, int], r_offset: int, g_offset: int, b_offset: int):
        """Dessine une traînée"""
        for i, pos in enumerate(trail):
            # Alpha basé sur la position dans la traînée
            alpha = int(255 * (i / len(trail)) * 0.5)
            size = int(3 + (i / len(trail)) * 5)
            
            # Couleur avec offset
            color = tuple(min(255, max(0, c + offset)) 
                         for c, offset in zip(base_color, (r_offset, g_offset, b_offset)))
            
            # Dessiner cercle semi-transparent
            trail_surface = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(trail_surface, color + (alpha,), (size, size), size)
            screen.blit(trail_surface, (pos[0] - size, pos[1] - size))


class ComboIndicator:
    """Indicateur de combo de frappes"""
    
    def __init__(self):
        """Initialise l'indicateur de combo"""
        self.combo_count = 0
        self.last_keystroke_time = 0
        self.combo_display_alpha = 0
        
    def update(self, keystroke_occurred: bool):
        """
        Met à jour le combo
        
        Args:
            keystroke_occurred: True si une frappe vient d'avoir lieu
        """
        if not config.ENABLE_COMBO_SYSTEM:
            return
        
        import time
        current_time = time.time()
        
        if keystroke_occurred:
            # Vérifier timeout
            if current_time - self.last_keystroke_time > config.COMBO_TIMEOUT:
                self.combo_count = 1
            else:
                self.combo_count += 1
            
            self.last_keystroke_time = current_time
            self.combo_display_alpha = 255
        else:
            # Fade progressif
            if current_time - self.last_keystroke_time > config.COMBO_TIMEOUT:
                self.combo_count = 0
                self.combo_display_alpha = max(0, self.combo_display_alpha - 5)
    
    def draw(self, screen: pygame.Surface, theme: dict):
        """
        Dessine l'indicateur de combo
        
        Args:
            screen: Surface Pygame
            theme: Thème de couleurs
        """
        if not config.ENABLE_COMBO_SYSTEM or self.combo_count < config.COMBO_MULTIPLIER_THRESHOLD:
            return
        
        # Position centrale en haut
        x = config.WINDOW_WIDTH // 2
        y = 100
        
        # Texte du combo
        font = pygame.font.Font(None, 60)
        combo_text = f"{self.combo_count}x COMBO!"
        
        # Couleur avec alpha
        color = theme['key_hover'] + (int(self.combo_display_alpha),)
        
        # Surface avec alpha
        text_surface = font.render(combo_text, True, theme['key_hover'])
        alpha_surface = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        alpha_surface.blit(text_surface, (0, 0))
        alpha_surface.set_alpha(int(self.combo_display_alpha))
        
        # Centrer
        text_rect = alpha_surface.get_rect(center=(x, y))
        screen.blit(alpha_surface, text_rect)


class EnergyWave:
    """Onde d'énergie lors de frappe rapide"""
    
    def __init__(self, x: int, y: int, color: Tuple[int, int, int]):
        """Initialise une onde d'énergie"""
        self.x = x
        self.y = y
        self.color = color
        self.radius = 0
        self.max_radius = config.WAVE_MAX_RADIUS
        self.alpha = 255
        
    def update(self):
        """Met à jour l'onde"""
        self.radius += config.WAVE_EXPANSION_SPEED
        self.alpha = int(255 * (1 - self.radius / self.max_radius))
    
    def is_alive(self) -> bool:
        """Retourne True si l'onde est encore visible"""
        return self.radius < self.max_radius
    
    def draw(self, screen: pygame.Surface):
        """Dessine l'onde"""
        if self.alpha > 0:
            wave_surface = pygame.Surface((self.max_radius * 2, self.max_radius * 2), pygame.SRCALPHA)
            color_with_alpha = self.color + (self.alpha,)
            pygame.draw.circle(wave_surface, color_with_alpha, 
                             (self.max_radius, self.max_radius), int(self.radius), 2)
            screen.blit(wave_surface, (self.x - self.max_radius, self.y - self.max_radius))


class EnergyWaveSystem:
    """Système de gestion des ondes d'énergie"""
    
    def __init__(self):
        """Initialise le système d'ondes"""
        self.waves: List[EnergyWave] = []
    
    def emit(self, x: int, y: int, color: Tuple[int, int, int]):
        """
        Émet une onde d'énergie
        
        Args:
            x: Position X
            y: Position Y
            color: Couleur de l'onde
        """
        if config.ENABLE_ENERGY_WAVES:
            self.waves.append(EnergyWave(x, y, color))
    
    def update(self):
        """Met à jour toutes les ondes"""
        for wave in self.waves:
            wave.update()
        
        # Supprimer les ondes mortes
        self.waves = [w for w in self.waves if w.is_alive()]
    
    def draw(self, screen: pygame.Surface):
        """Dessine toutes les ondes"""
        for wave in self.waves:
            wave.draw(screen)
