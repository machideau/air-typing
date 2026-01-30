"""
Module de statistiques de frappe
Calcule WPM, précision, temps de session et autres métriques
"""

import time
from typing import List, Dict
from datetime import datetime


class StatsTracker:
    """Tracker de statistiques de frappe en temps réel"""
    
    def __init__(self):
        """Initialise le tracker de statistiques"""
        self.session_start = time.time()
        self.total_chars = 0
        self.total_words = 0
        self.keystrokes = []  # Liste de (timestamp, char)
        self.errors = 0
        self.backspaces = 0
        
        # Pour calcul WPM sur fenêtre glissante
        self.wpm_window = 60  # Secondes
        
    def track_keystroke(self, char: str):
        """
        Enregistre une frappe
        
        Args:
            char: Caractère tapé
        """
        timestamp = time.time()
        self.keystrokes.append((timestamp, char))
        
        if char == "<-":
            self.backspaces += 1
        else:
            self.total_chars += 1
            
            # Compter les mots (espace = nouveau mot)
            if char == " ":
                self.total_words += 1
    
    def calculate_wpm(self) -> float:
        """
        Calcule les mots par minute sur une fenêtre glissante
        
        Returns:
            WPM (mots par minute)
        """
        current_time = time.time()
        
        # Filtrer les frappes dans la fenêtre
        recent_keystrokes = [
            (t, c) for t, c in self.keystrokes
            if current_time - t <= self.wpm_window
        ]
        
        if not recent_keystrokes:
            return 0.0
        
        # Compter les caractères (hors backspace)
        char_count = sum(1 for _, c in recent_keystrokes if c != "<-")
        
        # Calculer le temps écoulé
        time_elapsed = current_time - recent_keystrokes[0][0]
        
        if time_elapsed < 1:
            return 0.0
        
        # WPM = (caractères / 5) / (temps en minutes)
        # Standard: 1 mot = 5 caractères
        words = char_count / 5
        minutes = time_elapsed / 60
        
        return words / minutes if minutes > 0 else 0.0
    
    def get_accuracy(self) -> float:
        """
        Calcule la précision (pourcentage de frappes sans erreur)
        
        Returns:
            Précision en pourcentage (0-100)
        """
        total_keystrokes = len(self.keystrokes)
        
        if total_keystrokes == 0:
            return 100.0
        
        # Précision = (total - backspaces) / total * 100
        accuracy = ((total_keystrokes - self.backspaces) / total_keystrokes) * 100
        return max(0.0, min(100.0, accuracy))
    
    def get_session_time(self) -> float:
        """
        Retourne le temps de session en secondes
        
        Returns:
            Temps écoulé en secondes
        """
        return time.time() - self.session_start
    
    def get_session_time_formatted(self) -> str:
        """
        Retourne le temps de session formaté
        
        Returns:
            Temps formaté (MM:SS)
        """
        elapsed = int(self.get_session_time())
        minutes = elapsed // 60
        seconds = elapsed % 60
        return f"{minutes:02d}:{seconds:02d}"
    
    def get_stats_summary(self) -> Dict:
        """
        Retourne un résumé de toutes les statistiques
        
        Returns:
            Dictionnaire avec toutes les stats
        """
        return {
            'wpm': self.calculate_wpm(),
            'accuracy': self.get_accuracy(),
            'total_chars': self.total_chars,
            'total_words': self.total_words,
            'backspaces': self.backspaces,
            'session_time': self.get_session_time(),
            'session_time_formatted': self.get_session_time_formatted(),
            'total_keystrokes': len(self.keystrokes)
        }
    
    def reset_session(self):
        """Réinitialise toutes les statistiques"""
        self.session_start = time.time()
        self.total_chars = 0
        self.total_words = 0
        self.keystrokes.clear()
        self.errors = 0
        self.backspaces = 0
    
    def get_keystroke_history(self, seconds: int = 10) -> List[tuple]:
        """
        Retourne l'historique des frappes récentes
        
        Args:
            seconds: Nombre de secondes à récupérer
            
        Returns:
            Liste de (timestamp, char)
        """
        current_time = time.time()
        return [
            (t, c) for t, c in self.keystrokes
            if current_time - t <= seconds
        ]
