"""
Gestionnaire audio pour les effets sonores
Utilise pygame.mixer pour jouer des sons
"""

import pygame
import os
from typing import Dict
import config


class AudioManager:
    """Gestionnaire des effets sonores"""
    
    def __init__(self):
        """Initialise le gestionnaire audio"""
        self.enabled = config.ENABLE_SOUND
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        
        if self.enabled:
            try:
                # Initialiser le mixer si pas déjà fait
                if not pygame.mixer.get_init():
                    pygame.mixer.init()
                
                # Définir le volume
                pygame.mixer.music.set_volume(config.SOUND_VOLUME)
                
                # Générer des sons synthétiques si pas de fichiers
                self._generate_sounds()
                
            except Exception as e:
                print(f"Erreur lors de l'initialisation audio: {e}")
                self.enabled = False
    
    def _generate_sounds(self):
        """Génère des sons synthétiques simples"""
        try:
            # Son de clic (bip court)
            self.sounds['click'] = self._create_beep(frequency=800, duration=50)
            
            # Son de backspace (bip plus grave)
            self.sounds['backspace'] = self._create_beep(frequency=400, duration=80)
            
            # Son de hover (bip très court et aigu)
            self.sounds['hover'] = self._create_beep(frequency=1200, duration=30)
            
        except Exception as e:
            print(f"Erreur lors de la génération des sons: {e}")
            self.enabled = False
    
    def _create_beep(self, frequency: int = 440, duration: int = 100) -> pygame.mixer.Sound:
        """
        Crée un son de bip synthétique
        
        Args:
            frequency: Fréquence en Hz
            duration: Durée en millisecondes
            
        Returns:
            pygame.mixer.Sound
        """
        import numpy as np
        
        sample_rate = 22050
        n_samples = int(sample_rate * duration / 1000)
        
        # Générer une onde sinusoïdale
        t = np.linspace(0, duration / 1000, n_samples)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Appliquer une enveloppe pour éviter les clics
        envelope = np.exp(-t * 10)
        wave = wave * envelope
        
        # Normaliser et convertir en 16-bit
        wave = np.int16(wave * 32767 * config.SOUND_VOLUME)
        
        # Créer un tableau stéréo
        stereo_wave = np.column_stack((wave, wave))
        
        # Créer le son
        sound = pygame.sndarray.make_sound(stereo_wave)
        return sound
    
    def play(self, sound_name: str):
        """
        Joue un son
        
        Args:
            sound_name: Nom du son à jouer
        """
        if not self.enabled:
            return
        
        if sound_name in self.sounds:
            try:
                self.sounds[sound_name].play()
            except Exception as e:
                print(f"Erreur lors de la lecture du son '{sound_name}': {e}")
    
    def play_key_sound(self, char: str):
        """
        Joue le son approprié pour une touche
        
        Args:
            char: Caractère de la touche
        """
        if char == "<-":
            self.play('backspace')
        else:
            self.play('click')
    
    def set_volume(self, volume: float):
        """
        Définit le volume global
        
        Args:
            volume: Volume (0.0 à 1.0)
        """
        if self.enabled:
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume)))
    
    def toggle(self):
        """Active/désactive le son"""
        self.enabled = not self.enabled
        return self.enabled
    
    def is_enabled(self) -> bool:
        """Retourne True si le son est activé"""
        return self.enabled
