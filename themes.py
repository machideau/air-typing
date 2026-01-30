"""
Thèmes de couleurs pour Air-Typing
Définit tous les thèmes visuels disponibles
"""

# Ce fichier peut être importé pour accéder aux thèmes
# Les thèmes sont déjà définis dans config.py
# Ce fichier est fourni pour une extension future facile

from config import THEMES, DEFAULT_THEME

__all__ = ['THEMES', 'DEFAULT_THEME']


def get_theme(theme_name: str) -> dict:
    """
    Récupère un thème par son nom
    
    Args:
        theme_name: Nom du thème
        
    Returns:
        Dictionnaire du thème ou thème par défaut si non trouvé
    """
    return THEMES.get(theme_name, THEMES[DEFAULT_THEME])


def list_themes() -> list:
    """
    Liste tous les thèmes disponibles
    
    Returns:
        Liste des noms de thèmes
    """
    return list(THEMES.keys())


def create_custom_theme(name: str, colors: dict) -> dict:
    """
    Crée un thème personnalisé
    
    Args:
        name: Nom du thème
        colors: Dictionnaire des couleurs
        
    Returns:
        Thème créé
        
    Example:
        >>> custom = create_custom_theme('ocean', {
        ...     'background': (0, 20, 40),
        ...     'key_normal': (100, 200, 255),
        ...     'key_hover': (0, 150, 255),
        ...     'key_pressed': (255, 200, 0),
        ...     'text': (255, 255, 255),
        ...     'text_box_bg': (0, 30, 60),
        ...     'text_box_border': (0, 150, 255),
        ...     'cursor': (0, 200, 255),
        ...     'status_bar': (0, 40, 80),
        ...     'particle': (0, 200, 255)
        ... })
    """
    required_keys = [
        'background', 'key_normal', 'key_hover', 'key_pressed',
        'text', 'text_box_bg', 'text_box_border', 'cursor',
        'status_bar', 'particle'
    ]
    
    # Vérifier que toutes les clés sont présentes
    for key in required_keys:
        if key not in colors:
            raise ValueError(f"Clé manquante dans le thème: {key}")
    
    theme = colors.copy()
    theme['name'] = name
    
    return theme
