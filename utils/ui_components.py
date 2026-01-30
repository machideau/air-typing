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
        Dessine la zone de texte
        
        Args:
            screen: Surface Pygame
            text: Texte à afficher
            theme: Thème de couleurs
            font: Police pour le texte
        """
        # Fond semi-transparent
        bg_surface = pygame.Surface((self.w, self.h), pygame.SRCALPHA)
        bg_color = theme['text_box_bg'] + (200,)  # Ajouter alpha
        pygame.draw.rect(
            bg_surface,
            bg_color,
            (0, 0, self.w, self.h),
            border_radius=config.TEXT_BOX_BORDER_RADIUS
        )
        screen.blit(bg_surface, (self.x, self.y))
        
        # Contour
        pygame.draw.rect(
            screen,
            theme['text_box_border'],
            (self.x, self.y, self.w, self.h),
            2,
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
        bg_color = theme['status_bar'] + (150,)
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
