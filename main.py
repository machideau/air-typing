"""
Air-Typing - Clavier Virtuel Contrôlé par Gestes
Version améliorée avec architecture modulaire

Auteur: machideau
GitHub: https://github.com/machideau/air-typing
"""

import cv2
import pygame
import numpy as np
import time
import os
from datetime import datetime

# Imports des modules personnalisés
import config
from utils import (
    HandDetector,
    VirtualKeyboard,
    TextBox,
    StatusBar,
    Cursor,
    ParticleSystem,
    AudioManager
)


class AirTypingApp:
    """Application principale Air-Typing"""
    
    def __init__(self):
        """Initialise l'application"""
        # Initialiser Pygame
        pygame.init()
        
        # Créer la fenêtre
        self.screen = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        pygame.display.set_caption("Air-Typing - Clavier Virtuel par Gestes")
        
        # Charger les polices
        self.font_normal = pygame.font.Font(None, config.FONT_SIZE_NORMAL)
        self.font_big = pygame.font.Font(None, config.FONT_SIZE_BIG)
        self.font_small = pygame.font.Font(None, config.FONT_SIZE_SMALL)
        
        # Initialiser les composants
        self.hand_detector = HandDetector()
        self.keyboard = VirtualKeyboard()
        self.text_box = TextBox()
        self.status_bar = StatusBar()
        self.cursor = Cursor()
        self.particle_system = ParticleSystem()
        self.audio_manager = AudioManager()
        
        # Initialiser la webcam
        self.cap = cv2.VideoCapture(config.CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.WINDOW_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.WINDOW_HEIGHT)
        
        # État de l'application
        self.running = True
        self.current_theme_name = config.DEFAULT_THEME
        self.current_theme = config.THEMES[self.current_theme_name]
        self.show_menu = False
        
        # FPS
        self.clock = pygame.time.Clock()
        self.fps = 0
        
        # Sauvegarde automatique
        self.last_save_time = time.time()
        
        # Charger le texte sauvegardé si existant
        self._load_saved_text()
    
    def _load_saved_text(self):
        """Charge le texte sauvegardé précédemment"""
        if os.path.exists(config.SAVE_FILE):
            try:
                with open(config.SAVE_FILE, 'r', encoding='utf-8') as f:
                    saved_text = f.read()
                    self.keyboard.set_text(saved_text)
                    print(f"Texte chargé depuis {config.SAVE_FILE}")
            except Exception as e:
                print(f"Erreur lors du chargement du texte: {e}")
    
    def _save_text(self):
        """Sauvegarde le texte actuel"""
        try:
            with open(config.SAVE_FILE, 'w', encoding='utf-8') as f:
                f.write(self.keyboard.get_text())
            print(f"Texte sauvegardé dans {config.SAVE_FILE}")
        except Exception as e:
            print(f"Erreur lors de la sauvegarde du texte: {e}")
    
    def _auto_save(self):
        """Sauvegarde automatique périodique"""
        if not config.AUTO_SAVE:
            return
        
        current_time = time.time()
        if current_time - self.last_save_time >= config.SAVE_INTERVAL:
            self._save_text()
            self.last_save_time = current_time
    
    def _cycle_theme(self):
        """Passe au thème suivant"""
        theme_names = list(config.THEMES.keys())
        current_index = theme_names.index(self.current_theme_name)
        next_index = (current_index + 1) % len(theme_names)
        self.current_theme_name = theme_names[next_index]
        self.current_theme = config.THEMES[self.current_theme_name]
        print(f"Thème changé: {self.current_theme['name']}")
    
    def _handle_events(self):
        """Gère les événements Pygame"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    # Menu ou quitter
                    self.running = False
                
                elif event.key == pygame.K_t:
                    # Changer de thème
                    self._cycle_theme()
                
                elif event.key == pygame.K_s:
                    # Sauvegarder manuellement
                    self._save_text()
                
                elif event.key == pygame.K_c:
                    # Effacer le texte
                    self.keyboard.clear_text()
                
                elif event.key == pygame.K_m:
                    # Toggle son
                    enabled = self.audio_manager.toggle()
                    print(f"Son: {'Activé' if enabled else 'Désactivé'}")
                
                elif event.key == pygame.K_l:
                    # Changer de layout
                    current_layout = self.keyboard.layout_name
                    new_layout = 'AZERTY' if current_layout == 'QWERTY' else 'QWERTY'
                    self.keyboard.change_layout(new_layout)
                    print(f"Layout changé: {new_layout}")
    
    def _process_frame(self):
        """Traite une frame de la webcam"""
        ret, frame = self.cap.read()
        if not ret:
            return None
        
        # Miroir et conversion
        frame = cv2.flip(frame, 1)
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        return img_rgb
    
    def _draw_background(self, frame_rgb):
        """Dessine le fond (webcam)"""
        # Convertir la frame en surface Pygame
        frame_surface = pygame.surfarray.make_surface(cv2.transpose(frame_rgb))
        self.screen.blit(frame_surface, (0, 0))
        
        # Overlay semi-transparent pour améliorer la lisibilité
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT), pygame.SRCALPHA)
        overlay.fill(self.current_theme['background'] + (50,))
        self.screen.blit(overlay, (0, 0))
    
    def run(self):
        """Boucle principale de l'application"""
        print("=== Air-Typing démarré ===")
        print("Contrôles:")
        print("  ESC: Quitter")
        print("  T: Changer de thème")
        print("  S: Sauvegarder le texte")
        print("  C: Effacer le texte")
        print("  M: Activer/Désactiver le son")
        print("  L: Changer de layout (QWERTY/AZERTY)")
        print("========================\n")
        
        while self.running:
            # Gérer les événements
            self._handle_events()
            
            # Traiter la frame
            frame_rgb = self._process_frame()
            if frame_rgb is None:
                break
            
            # Détecter les deux mains
            timestamp_ms = pygame.time.get_ticks()
            left_hand, right_hand, landmarks = self.hand_detector.detect(frame_rgb, timestamp_ms)
            
            # Dessiner le fond
            self._draw_background(frame_rgb)
            
            # Mettre à jour le clavier avec les deux mains
            typed_char = self.keyboard.update(
                left_hand['pos'], left_hand['clicking'],
                right_hand['pos'], right_hand['clicking']
            )
            
            # Jouer le son si une touche a été tapée
            if typed_char:
                self.audio_manager.play_key_sound(typed_char)
                # Émettre des particules pour la main qui a tapé
                # Vérifier quelle main a cliqué
                if left_hand['clicking'] and left_hand['pos']:
                    self.particle_system.emit(
                        left_hand['pos'][0],
                        left_hand['pos'][1],
                        self.current_theme['particle']
                    )
                if right_hand['clicking'] and right_hand['pos']:
                    self.particle_system.emit(
                        right_hand['pos'][0],
                        right_hand['pos'][1],
                        self.current_theme['particle']
                    )
            
            # Dessiner le clavier
            self.keyboard.draw(self.screen, self.current_theme, self.font_normal)
            
            # Dessiner la zone de texte
            self.text_box.draw(
                self.screen,
                self.keyboard.get_text(),
                self.current_theme,
                self.font_big
            )
            
            # Dessiner les deux curseurs
            self.cursor.update()
            if left_hand['detected'] and left_hand['pos']:
                self.cursor.draw_left(self.screen, left_hand['pos'], self.current_theme, left_hand['clicking'])
            if right_hand['detected'] and right_hand['pos']:
                self.cursor.draw_right(self.screen, right_hand['pos'], self.current_theme, right_hand['clicking'])
            
            # Mettre à jour et dessiner les particules
            self.particle_system.update()
            self.particle_system.draw(self.screen)
            
            # Dessiner la barre d'état
            self.status_bar.update(self.fps, self.current_theme['name'])
            self.status_bar.draw(self.screen, self.current_theme, self.font_small)
            
            # Dessiner les landmarks si debug activé
            if config.SHOW_HAND_LANDMARKS and landmarks:
                self._draw_landmarks(landmarks)
            
            # Mettre à jour l'affichage
            pygame.display.flip()
            
            # Contrôler le FPS
            self.clock.tick(config.TARGET_FPS)
            self.fps = self.clock.get_fps()
            
            # Sauvegarde automatique
            self._auto_save()
        
        # Nettoyage
        self.cleanup()
    
    def _draw_landmarks(self, landmarks_list):
        """Dessine les landmarks des mains pour le debug"""
        for hand_landmarks in landmarks_list:
            for landmark in hand_landmarks:
                x = int(landmark.x * config.WINDOW_WIDTH)
                y = int(landmark.y * config.WINDOW_HEIGHT)
                pygame.draw.circle(self.screen, (0, 255, 0), (x, y), 3)
    
    def cleanup(self):
        """Nettoie les ressources"""
        print("\n=== Fermeture de l'application ===")
        
        # Sauvegarder le texte
        self._save_text()
        
        # Libérer les ressources
        self.cap.release()
        self.hand_detector.close()
        pygame.quit()
        
        print("Application fermée proprement.")


def main():
    """Point d'entrée de l'application"""
    try:
        app = AirTypingApp()
        app.run()
    except KeyboardInterrupt:
        print("\nInterruption par l'utilisateur")
    except Exception as e:
        print(f"\nErreur fatale: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()