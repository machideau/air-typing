# 🚀 Guide de Démarrage Rapide - Air-Typing

## Installation Express

### 1. Installer les dépendances
```bash
# Activer l'environnement virtuel
env\Scripts\activate

# Installer les packages
pip install -r requirements.txt
```

### 2. Lancer l'application
```bash
python main.py
```

## Premiers Pas

### Utilisation Basique
1. **Levez votre main** devant la webcam (paume visible)
2. **Déplacez votre index** pour contrôler le curseur
3. **Pincez** (rapprochez index et pouce) pour cliquer sur une touche

### Raccourcis Essentiels
- `T` : Changer de thème
- `S` : Sauvegarder le texte
- `ESC` : Quitter

## Personnalisation Rapide

### Changer la sensibilité du clic
Éditez `config.py` :
```python
PINCH_THRESHOLD = 40  # Plus facile à cliquer
```

### Désactiver le son
Éditez `config.py` :
```python
ENABLE_SOUND = False
```

### Changer la caméra
Éditez `config.py` :
```python
CAMERA_INDEX = 1  # Essayez 0, 1, 2...
```

## Problèmes Courants

### La webcam ne s'ouvre pas
→ Changez `CAMERA_INDEX` dans `config.py`

### Détection imprécise
→ Améliorez l'éclairage de votre pièce

### Erreur d'import
→ Vérifiez que l'environnement virtuel est activé

## Plus d'Informations

Consultez le [README.md](README.md) complet pour tous les détails !
