"""
Module de détection des mains avec MediaPipe
Gère la détection, le tracking et l'analyse des gestes
"""

import cv2
import mediapipe as mp
import math
from typing import Optional, Tuple, List
import config
import numpy as np


class HandDetector:
    """Détecteur de mains utilisant MediaPipe"""
    
    def __init__(self):
        """Initialise le détecteur de mains"""
        # Initialize MediaPipe Tasks
        self.BaseOptions = mp.tasks.BaseOptions
        self.HandLandmarker = mp.tasks.vision.HandLandmarker
        self.HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
        self.VisionRunningMode = mp.tasks.vision.RunningMode
        
        # Create hand landmarker instance
        options = self.HandLandmarkerOptions(
            base_options=self.BaseOptions(model_asset_path=config.MODEL_PATH),
            running_mode=self.VisionRunningMode.VIDEO,
            num_hands=config.NUM_HANDS,
            min_hand_detection_confidence=config.MIN_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=config.MIN_PRESENCE_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        
        self.landmarker = self.HandLandmarker.create_from_options(options)
        
        # Smoothing pour le curseur
        self.prev_cursor_pos = None
        self.smoothing = config.HOVER_SMOOTHING
        
    def detect(self, frame: np.ndarray, timestamp_ms: int) -> Tuple[Optional[Tuple[int, int]], bool, List]:
        """
        Détecte les mains dans une frame
        
        Args:
            frame: Frame RGB (numpy array)
            timestamp_ms: Timestamp en millisecondes
            
        Returns:
            Tuple contenant:
            - Position du curseur (x, y) ou None
            - État du clic (True/False)
            - Liste des landmarks pour le debug
        """
        # Convert to MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        
        # Process
        results = self.landmarker.detect_for_video(mp_image, timestamp_ms)
        
        cursor_pos = None
        clicking = False
        all_landmarks = []
        
        if results.hand_landmarks:
            for hand_lms in results.hand_landmarks:
                all_landmarks.append(hand_lms)
                
                # Index 8 = Index Finger Tip, 4 = Thumb Tip
                idx_x = int(hand_lms[8].x * config.WINDOW_WIDTH)
                idx_y = int(hand_lms[8].y * config.WINDOW_HEIGHT)
                
                # Appliquer le lissage
                if self.prev_cursor_pos is not None:
                    idx_x = int(self.smoothing * self.prev_cursor_pos[0] + (1 - self.smoothing) * idx_x)
                    idx_y = int(self.smoothing * self.prev_cursor_pos[1] + (1 - self.smoothing) * idx_y)
                
                cursor_pos = (idx_x, idx_y)
                self.prev_cursor_pos = cursor_pos
                
                # Détecter le pincement
                thumb_x = int(hand_lms[4].x * config.WINDOW_WIDTH)
                thumb_y = int(hand_lms[4].y * config.WINDOW_HEIGHT)
                distance = math.hypot(idx_x - thumb_x, idx_y - thumb_y)
                
                if distance < config.PINCH_THRESHOLD:
                    clicking = True
                    
                # On prend seulement la première main pour le curseur
                break
        else:
            # Réinitialiser le lissage si aucune main détectée
            self.prev_cursor_pos = None
        
        return cursor_pos, clicking, all_landmarks
    
    def get_finger_position(self, hand_landmarks, finger_tip_index: int) -> Tuple[int, int]:
        """
        Obtient la position d'un doigt spécifique
        
        Args:
            hand_landmarks: Landmarks de la main
            finger_tip_index: Index du bout du doigt (4=pouce, 8=index, etc.)
            
        Returns:
            Position (x, y) en pixels
        """
        x = int(hand_landmarks[finger_tip_index].x * config.WINDOW_WIDTH)
        y = int(hand_landmarks[finger_tip_index].y * config.WINDOW_HEIGHT)
        return (x, y)
    
    def calculate_distance(self, pos1: Tuple[int, int], pos2: Tuple[int, int]) -> float:
        """
        Calcule la distance euclidienne entre deux points
        
        Args:
            pos1: Position (x, y) du premier point
            pos2: Position (x, y) du second point
            
        Returns:
            Distance en pixels
        """
        return math.hypot(pos1[0] - pos2[0], pos1[1] - pos2[1])
    
    def close(self):
        """Ferme le détecteur et libère les ressources"""
        self.landmarker.close()
