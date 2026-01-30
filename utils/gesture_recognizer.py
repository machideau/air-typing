"""
Module de reconnaissance de gestes avancés
Détecte paume ouverte, pouce levé, swipe, mains jointes, etc.
"""

import math
from typing import Optional, Tuple, List
import config


class GestureRecognizer:
    """Reconnaisseur de gestes avancés"""
    
    def __init__(self):
        """Initialise le reconnaisseur de gestes"""
        self.left_hand_history = []  # Historique positions main gauche
        self.right_hand_history = []  # Historique positions main droite
        self.history_length = 10  # Nombre de frames à garder
        
        # Cooldowns pour éviter détections multiples
        self.last_gesture_time = {}
        self.gesture_cooldown = 1.0  # Secondes
        
    def update_history(self, left_hand: dict, right_hand: dict):
        """
        Met à jour l'historique des positions
        
        Args:
            left_hand: Données main gauche
            right_hand: Données main droite
        """
        if left_hand['detected'] and left_hand['pos']:
            self.left_hand_history.append(left_hand['pos'])
            if len(self.left_hand_history) > self.history_length:
                self.left_hand_history.pop(0)
        
        if right_hand['detected'] and right_hand['pos']:
            self.right_hand_history.append(right_hand['pos'])
            if len(self.right_hand_history) > self.history_length:
                self.right_hand_history.pop(0)
    
    def detect_open_palm(self, hand_landmarks) -> bool:
        """
        Détecte une paume ouverte (tous les doigts étendus)
        
        Args:
            hand_landmarks: Landmarks de la main
            
        Returns:
            True si paume ouverte détectée
        """
        if not hand_landmarks:
            return False
        
        # Indices des bouts de doigts
        finger_tips = [4, 8, 12, 16, 20]  # Pouce, Index, Majeur, Annulaire, Auriculaire
        # Indices des articulations de base
        finger_bases = [2, 5, 9, 13, 17]
        
        # Vérifier que tous les doigts sont étendus
        extended_count = 0
        for tip, base in zip(finger_tips, finger_bases):
            tip_y = hand_landmarks[tip].y
            base_y = hand_landmarks[base].y
            
            # Doigt étendu si le bout est au-dessus de la base
            if tip_y < base_y:
                extended_count += 1
        
        # Paume ouverte si au moins 4 doigts étendus
        return extended_count >= 4
    
    def detect_thumbs_up(self, hand_landmarks) -> bool:
        """
        Détecte un pouce levé
        
        Args:
            hand_landmarks: Landmarks de la main
            
        Returns:
            True si pouce levé détecté
        """
        if not hand_landmarks:
            return False
        
        # Pouce étendu
        thumb_tip = hand_landmarks[4]
        thumb_base = hand_landmarks[2]
        
        # Autres doigts repliés
        finger_tips = [8, 12, 16, 20]
        finger_bases = [5, 9, 13, 17]
        
        # Pouce vers le haut
        thumb_extended = thumb_tip.y < thumb_base.y
        
        # Autres doigts repliés
        fingers_closed = 0
        for tip, base in zip(finger_tips, finger_bases):
            if hand_landmarks[tip].y > hand_landmarks[base].y:
                fingers_closed += 1
        
        return thumb_extended and fingers_closed >= 3
    
    def detect_swipe_horizontal(self, hand_type: str = 'right') -> Optional[str]:
        """
        Détecte un swipe horizontal (gauche ou droite)
        
        Args:
            hand_type: 'left' ou 'right'
            
        Returns:
            'left', 'right' ou None
        """
        history = self.right_hand_history if hand_type == 'right' else self.left_hand_history
        
        if len(history) < 5:
            return None
        
        # Calculer le déplacement horizontal
        start_x = history[0][0]
        end_x = history[-1][0]
        displacement = end_x - start_x
        
        # Seuil de swipe (pixels)
        swipe_threshold = 150
        
        if displacement > swipe_threshold:
            return 'right'
        elif displacement < -swipe_threshold:
            return 'left'
        
        return None
    
    def detect_hands_together(self, left_hand: dict, right_hand: dict) -> bool:
        """
        Détecte si les deux mains sont proches (jointes)
        
        Args:
            left_hand: Données main gauche
            right_hand: Données main droite
            
        Returns:
            True si mains jointes
        """
        if not (left_hand['detected'] and right_hand['detected']):
            return False
        
        if not (left_hand['pos'] and right_hand['pos']):
            return False
        
        # Calculer la distance entre les deux mains
        distance = math.hypot(
            left_hand['pos'][0] - right_hand['pos'][0],
            left_hand['pos'][1] - right_hand['pos'][1]
        )
        
        # Seuil de proximité (pixels)
        proximity_threshold = 100
        
        return distance < proximity_threshold
    
    def detect_fist(self, hand_landmarks) -> bool:
        """
        Détecte un poing fermé
        
        Args:
            hand_landmarks: Landmarks de la main
            
        Returns:
            True si poing fermé
        """
        if not hand_landmarks:
            return False
        
        # Tous les doigts repliés
        finger_tips = [8, 12, 16, 20]  # Sans le pouce
        finger_bases = [5, 9, 13, 17]
        
        closed_count = 0
        for tip, base in zip(finger_tips, finger_bases):
            if hand_landmarks[tip].y > hand_landmarks[base].y:
                closed_count += 1
        
        return closed_count >= 3
    
    def detect_peace_sign(self, hand_landmarks) -> bool:
        """
        Détecte le signe de la paix (index et majeur levés)
        
        Args:
            hand_landmarks: Landmarks de la main
            
        Returns:
            True si peace sign détecté
        """
        if not hand_landmarks:
            return False
        
        # Index et majeur étendus
        index_extended = hand_landmarks[8].y < hand_landmarks[5].y
        middle_extended = hand_landmarks[12].y < hand_landmarks[9].y
        
        # Autres doigts repliés
        ring_closed = hand_landmarks[16].y > hand_landmarks[13].y
        pinky_closed = hand_landmarks[20].y > hand_landmarks[17].y
        
        return index_extended and middle_extended and ring_closed and pinky_closed
    
    def can_trigger_gesture(self, gesture_name: str) -> bool:
        """
        Vérifie si un geste peut être déclenché (cooldown)
        
        Args:
            gesture_name: Nom du geste
            
        Returns:
            True si le geste peut être déclenché
        """
        import time
        current_time = time.time()
        
        if gesture_name not in self.last_gesture_time:
            self.last_gesture_time[gesture_name] = current_time
            return True
        
        elapsed = current_time - self.last_gesture_time[gesture_name]
        if elapsed >= self.gesture_cooldown:
            self.last_gesture_time[gesture_name] = current_time
            return True
        
        return False
