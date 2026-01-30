# ⌨️ Air-Typing - Clavier Virtuel Contrôlé par Gestes

Un clavier virtuel futuriste et moderne contrôlé par gestes de la main, construit avec **Computer Vision** et **Intelligence Artificielle**. Tapez dans les airs en utilisant simplement vos mains et une webcam !

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Fonctionnalités

### 🎯 Détection Avancée
* **Suivi des Mains en Temps Réel** : Utilise MediaPipe pour suivre 21 points de repère de la main avec une précision exceptionnelle
* **Reconnaissance de Gestes Intelligente** : Détection du "pincement" (index + pouce) pour la frappe
* **Support Multi-Mains** : Tapez avec vos deux mains simultanément pour plus de rapidité

### ⌨️ Clavier Complet & Standard
* **Layout 5 Rangées** : Clavier rectangulaire standard incluant chiffres, lettres, et symboles
* **Fonctionnalité Shift Compète** : Bascule entre minuscules/majuscules et accès aux symboles spéciaux (!, @, #, etc.)
* **Touches Spéciales** : Support complet de ENTER, BACKSPACE, et SHIFT
* **Taille Optimisée** : Touches larges (75px) pour une frappe facile et précise

### 🎨 Interface Épurée
* **Thème "Simple Dark"** : Interface sombre à fort contraste pour une visibilité maximale
* **Fond Vidéo** : Voyez vos mains en temps réel derrière le clavier
* **Feedback Visuel** : Les touches s'illuminent lorsque vous les survolez (gris clair) et les pressez (bleu)

### ⚙️ Fonctionnalités Avancées
* **Sauvegarde Automatique** : Le texte est sauvegardé via geste ou raccourci
* **Layouts Multiples** : Support QWERTY et AZERTY
* **Saisie Réactive** : Déclenchement de la touche dès l'appui (pincement) pour une latence minimale

---

## 🚀 Installation Rapide

### Prérequis
- **Python 3.11+** ([Télécharger](https://www.python.org/downloads/))
- **Webcam** fonctionnelle
- **Windows / Mac / Linux**

### Installation en 3 Étapes

#### 1️⃣ Cloner le dépôt
```bash
git clone https://github.com/machideau/air-typing.git
cd air-typing
```

#### 2️⃣ Installer les dépendances
```bash
# Créer un environnement virtuel (recommandé)
python -m venv env

# Activer l'environnement
# Windows:
env\Scripts\activate
# Mac/Linux:
source env/bin/activate

# Installer les packages
pip install -r requirements.txt
```

#### 3️⃣ Télécharger le modèle MediaPipe
Le fichier `hand_landmarker.task` est déjà inclus dans le dépôt. Si absent :
- 🔗 [Télécharger hand_landmarker.task](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task)
- Placez-le dans le dossier `air-typing/`

---

## 🎮 Utilisation

### Lancer l'Application
```bash
python main.py
```

### Contrôles Gestuels

| Geste | Action |
|-------|--------|
| 👆 **Pincement** (Index + Pouce) | **Taper** sur une touche |
| ✌️ **Signe de Paix** (Index + Majeur levés) | **Effacer tout** le texte |
| 👍 **Pouce levé** | **Sauvegarder** le texte |
| ✋ **Index levé** | **Déplacer** le curseur sans cliquer |

### Raccourcis Clavier (Physique)

| Touche | Action |
|--------|--------|
| `ESC` | Quitter l'application |
| `S` | Sauvegarder le texte manuellement |
| `C` | Effacer tout le texte |
| `M` | Activer/Désactiver le son |
| `L` | Changer de layout (QWERTY ↔ AZERTY) |

---

## 📁 Structure du Projet

```
air-typing/
├── main.py                    # Application principale
├── config.py                  # Configuration centralisée (tailles, couleurs, layouts)
├── utils/                     # Modules utilitaires
│   ├── __init__.py
│   ├── hand_detector.py       # Détection des mains (MediaPipe)
│   ├── keyboard.py            # Logique du clavier et des touches
│   ├── gesture_recognizer.py  # Reconnaissance des gestes (Peace, Thumbs Up)
│   ├── ui_components.py       # Composants UI
│   └── audio_manager.py       # Gestionnaire audio
├── hand_landmarker.task       # Modèle MediaPipe
├── requirements.txt           # Dépendances Python
├── typed_text.txt             # Fichier de sortie du texte
└── README.md                  # Documentation
```

---

## ⚙️ Configuration

Vous pouvez ajuster les paramètres dans `config.py` :

```python
# Fenêtre
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# Clavier
KEY_WIDTH = 75           # Taille des touches
KEY_SPACING = 85         # Espacement
ENABLE_SMART_ZONES = False # Désactivé pour clarté visuelle

# Main
PINCH_THRESHOLD = 30     # Sensibilité du clic
```

---

## 🐛 Dépannage

### ❌ Erreur : `ImportError: DLL load failed`
```bash
pip uninstall mediapipe
pip install mediapipe==0.10.14
```

### ❌ La touche ne se déclenche pas
- Assurez-vous de bien "pincer" (toucher le bout de l'index avec le bout du pouce)
- Le déclenchement se fait **dès le contact** (appui) pour une meilleure réactivité

---

## 📄 Licence

Ce projet est sous licence MIT. Libre d'utilisation pour des projets personnels et commerciaux.

---

## 👤 Auteur

**machideau**
- GitHub: [@machideau](https://github.com/machideau)
- Projet: [air-typing](https://github.com/machideau/air-typing)