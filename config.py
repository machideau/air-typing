"""
Configuration centralisée pour Air-Typing
Tous les paramètres de l'application sont définis ici
"""

# ==================== PARAMÈTRES WEBCAM ====================
CAMERA_INDEX = 0
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
TARGET_FPS = 60

# ==================== PARAMÈTRES MEDIAPIPE ====================
MODEL_PATH = 'hand_landmarker.task'
NUM_HANDS = 2
MIN_DETECTION_CONFIDENCE = 0.5
MIN_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5

# ==================== PARAMÈTRES DE GESTES ====================
PINCH_THRESHOLD = 35  # Distance en pixels pour détecter un pincement
HOVER_SMOOTHING = 0.7  # Lissage du curseur (0-1, plus élevé = plus lisse)

# ==================== LAYOUT DU CLAVIER ====================
KEYBOARD_LAYOUTS = {
    'QWERTY': [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "<-"],
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";", "'", "ENTER"],
        ["SHIFT", "Z", "X", "C", "V", "B", "N", "M", ",", ".", "/", "SHIFT"],
        [" "]
    ],
    'AZERTY': [
        ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "-", "=", "<-"],
        ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "[", "]"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M", "'", "ENTER"],
        ["SHIFT", "W", "X", "C", "V", "B", "N", ",", ";", ".", "/", "SHIFT"],
        [" "]
    ]
}

DEFAULT_LAYOUT = 'QWERTY'

# ==================== PARAMÈTRES VISUELS ====================
# Tailles des touches (ajustées pour remplir la fenêtre 720p)
KEY_WIDTH = 75
KEY_HEIGHT = 75
KEY_SPACING = 85
KEY_START_X = 40
KEY_START_Y = 180
SPACE_KEY_WIDTH = 500  # Barre espace large
BACKSPACE_KEY_WIDTH = 110
SHIFT_KEY_WIDTH = 120
ENTER_KEY_WIDTH = 120

# Tailles de police
FONT_SIZE_NORMAL = 50
FONT_SIZE_BIG = 80
FONT_SIZE_SMALL = 30

# Bordures et arrondis
KEY_BORDER_RADIUS = 12
TEXT_BOX_BORDER_RADIUS = 15
KEY_BORDER_THICKNESS_NORMAL = 2
KEY_BORDER_THICKNESS_HOVER = 4
KEY_BORDER_THICKNESS_PRESSED = 6

# Curseur
CURSOR_OUTER_RADIUS = 20
CURSOR_INNER_RADIUS = 2
CURSOR_THICKNESS = 2

# Zone de texte
TEXT_BOX_X = 100
TEXT_BOX_Y = 50
TEXT_BOX_WIDTH = 1080
TEXT_BOX_HEIGHT = 100
TEXT_BOX_PADDING = 30

THEMES = {
    'simple_dark': {
        'name': 'Dark Theme',
        'background': (20, 20, 20),           # Solid dark grey
        'key_normal': (60, 60, 60),           # Solid grey
        'key_hover': (100, 100, 100),         # Lighter grey
        'key_pressed': (0, 120, 215),         # Solid blue
        'text': (255, 255, 255),              # White
        'text_box_bg': (30, 30, 30),
        'text_box_border': (200, 200, 200),
        'cursor': (0, 255, 0),                # Bright green
        'status_bar': (40, 40, 40),
        'particle': (200, 200, 200)
    }
}

DEFAULT_THEME = 'simple_dark'

# ==================== PARAMÈTRES AUDIO ====================
ENABLE_SOUND = True
SOUND_VOLUME = 0.5  # 0.0 à 1.0

# ==================== PARAMÈTRES DE SAUVEGARDE ====================
AUTO_SAVE = True
SAVE_FILE = 'typed_text.txt'
SAVE_INTERVAL = 30  # Secondes

# ==================== PARAMÈTRES D'ANIMATION ====================
ENABLE_ANIMATIONS = True
PARTICLE_COUNT = 5
PARTICLE_LIFETIME = 30  # Frames
GLOW_INTENSITY = 0.5  # 0.0 à 1.0

# ==================== PARAMÈTRES DE DEBUG ====================
SHOW_FPS = True
SHOW_HAND_LANDMARKS = False
DEBUG_MODE = False

# ==================== PARAMÈTRES STATISTIQUES ====================
ENABLE_STATS = True
STATS_WPM_WINDOW = 60  # Fenêtre de calcul WPM en secondes
STATS_POSITION_X = 100
STATS_POSITION_Y = 170
STATS_FONT_SIZE = 25

# ==================== PARAMÈTRES GESTES AVANCÉS ====================
ENABLE_ADVANCED_GESTURES = True
GESTURE_COOLDOWN = 1.0  # Secondes entre deux gestes
SWIPE_THRESHOLD = 150  # Pixels pour détecter un swipe
HANDS_TOGETHER_THRESHOLD = 100  # Distance pour mains jointes

# ==================== ZONES INTELLIGENTES DU CLAVIER ====================
ENABLE_SMART_ZONES = False
LEFT_ZONE_COLOR_TINT = (-10, -5, 15)  # Teinte bleutée
RIGHT_ZONE_COLOR_TINT = (15, 5, -10)  # Teinte orangée
ZONE_OPACITY = 0.3  # Opacité de la coloration

# ==================== MODE ENTRAÎNEMENT ====================
TRAINING_MODE_ENABLED = False  # Désactivé par défaut
TRAINING_PHRASES_FILE = 'data/training_phrases.json'
TRAINING_MIN_ACCURACY = 90  # Pourcentage minimum pour passer au niveau suivant

# ==================== PRÉDICTION DE TEXTE ====================
ENABLE_TEXT_PREDICTION = True
MAX_PREDICTIONS = 3  # Nombre de suggestions
PREDICTION_MIN_CHARS = 2  # Caractères minimum avant suggestion
WORDS_DICTIONARY_FR = 'data/words_fr.json'
WORDS_DICTIONARY_EN = 'data/words_en.json'

# ==================== MULTI-LANGUES ====================
DEFAULT_LANGUAGE = 'FR'
AVAILABLE_LANGUAGES = ['FR', 'EN', 'ES']

# Layouts étendus avec caractères spéciaux
KEYBOARD_LAYOUTS_EXTENDED = {
    'FR': [
        ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "<-"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
        ["W", "X", "C", "V", "B", "N", ",", ";", ".", " "]
    ],
    'EN': [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<-"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", " "]
    ],
    'ES': [
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<-"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", "Ñ"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", " "]
    ]
}

# ==================== EFFETS VISUELS AVANCÉS ====================
ENABLE_TRAIL_EFFECT = True
TRAIL_LENGTH = 10  # Nombre de positions dans la traînée
TRAIL_FADE_SPEED = 0.1

ENABLE_COMBO_SYSTEM = True
COMBO_TIMEOUT = 2.0  # Secondes sans frappe pour réinitialiser combo
COMBO_MULTIPLIER_THRESHOLD = 5  # Frappes pour activer multiplicateur

ENABLE_ENERGY_WAVES = True
WAVE_EXPANSION_SPEED = 5  # Pixels par frame
WAVE_MAX_RADIUS = 50

# ==================== OPTIMISATION VITESSE ====================
FAST_MODE = False  # Mode rapide (réduit seuils)
FAST_MODE_PINCH_THRESHOLD = 30  # Réduit de 35 à 30
ENABLE_TAP_MODE = False  # Mode tap (proximité au lieu de pincement)
TAP_PROXIMITY_THRESHOLD = 40  # Distance doigt-touche pour tap

# ==================== CALIBRATION ====================
USER_PREFERENCES_FILE = 'data/user_preferences.json'
DEFAULT_SENSITIVITY = 50  # 0-100
DEFAULT_KEYBOARD_SCALE = 100  # Pourcentage

# ==================== HISTORIQUE & SNIPPETS ====================
HISTORY_FILE = 'data/history.json'
HISTORY_MAX_ENTRIES = 100
SNIPPETS_FILE = 'data/snippets.json'
ENABLE_AUTO_COPY = False  # Copie automatique vers presse-papier
