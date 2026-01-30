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
        ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P", "<-"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", " "]
    ],
    'AZERTY': [
        ["A", "Z", "E", "R", "T", "Y", "U", "I", "O", "P", "<-"],
        ["Q", "S", "D", "F", "G", "H", "J", "K", "L", "M"],
        ["W", "X", "C", "V", "B", "N", ",", ";", ".", " "]
    ]
}

DEFAULT_LAYOUT = 'QWERTY'

# ==================== PARAMÈTRES VISUELS ====================
# Tailles des touches
KEY_WIDTH = 80
KEY_HEIGHT = 80
KEY_SPACING = 110
KEY_START_X = 100
KEY_START_Y = 250
SPACE_KEY_WIDTH = 250  # Plus large pour faciliter le clic
BACKSPACE_KEY_WIDTH = 120  # Plus large pour faciliter le clic

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

# ==================== THÈMES DE COULEURS ====================
THEMES = {
    'dark': {
        'name': 'Sombre',
        'background': (0, 0, 0),
        'key_normal': (200, 200, 200),
        'key_hover': (0, 255, 255),      # Cyan
        'key_pressed': (255, 0, 255),    # Magenta
        'text': (255, 255, 255),
        'text_box_bg': (0, 0, 0),
        'text_box_border': (0, 255, 255),
        'cursor': (0, 255, 255),
        'status_bar': (100, 100, 100),
        'particle': (0, 255, 255)
    },
    'light': {
        'name': 'Clair',
        'background': (255, 255, 255),
        'key_normal': (100, 100, 100),
        'key_hover': (0, 120, 255),      # Bleu
        'key_pressed': (138, 43, 226),   # Violet
        'text': (0, 0, 0),
        'text_box_bg': (245, 245, 245),
        'text_box_border': (0, 120, 255),
        'cursor': (0, 120, 255),
        'status_bar': (200, 200, 200),
        'particle': (0, 120, 255)
    },
    'neon': {
        'name': 'Néon',
        'background': (10, 0, 20),
        'key_normal': (255, 0, 255),
        'key_hover': (0, 255, 255),
        'key_pressed': (255, 255, 0),    # Jaune
        'text': (0, 255, 255),
        'text_box_bg': (20, 0, 40),
        'text_box_border': (255, 0, 255),
        'cursor': (0, 255, 255),
        'status_bar': (50, 0, 100),
        'particle': (255, 0, 255)
    },
    'minimal': {
        'name': 'Minimaliste',
        'background': (250, 250, 250),
        'key_normal': (50, 50, 50),
        'key_hover': (100, 100, 100),
        'key_pressed': (0, 0, 0),
        'text': (0, 0, 0),
        'text_box_bg': (255, 255, 255),
        'text_box_border': (50, 50, 50),
        'cursor': (0, 0, 0),
        'status_bar': (230, 230, 230),
        'particle': (100, 100, 100)
    }
}

DEFAULT_THEME = 'dark'

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
