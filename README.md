# ⌨️ Air-Typing - Clavier Virtuel Contrôlé par Gestes

Un clavier virtuel futuriste et moderne contrôlé par gestes de la main, construit avec **Computer Vision** et **Intelligence Artificielle**. Tapez dans les airs en utilisant simplement vos mains et une webcam !

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10.14-green.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

---

## ✨ Fonctionnalités

### 🎯 Détection Avancée
* **Suivi des Mains en Temps Réel** : Utilise MediaPipe pour suivre 21 points de repère de la main avec une précision exceptionnelle
* **Reconnaissance de Gestes Intelligente** : Détection du "pincement" (index + pouce) avec lissage pour une stabilité optimale
* **Support Multi-Mains** : Détecte jusqu'à 2 mains simultanément

### 🎨 Interface Moderne
* **4 Thèmes Visuels** : Sombre, Clair, Néon et Minimaliste
* **Animations Fluides** : Effets de pression, particules et transitions douces
* **Design Glassmorphism** : Interface semi-transparente avec effet de verre dépoli
* **Curseur Animé** : Curseur futuriste avec pulsation et croix de visée

### 🔊 Feedback Multi-Sensoriel
* **Sons Synthétiques** : Feedback audio pour chaque touche (bips personnalisés)
* **Effets Visuels** : Système de particules lors des clics
* **Retour Haptique Visuel** : Changement de couleur dynamique (Cyan → Magenta)

### ⚙️ Fonctionnalités Avancées
* **Sauvegarde Automatique** : Le texte est sauvegardé toutes les 30 secondes
* **Layouts Multiples** : Support QWERTY et AZERTY
* **Architecture Modulaire** : Code propre et maintenable
* **Barre d'État** : Affichage du FPS, thème actuel et raccourcis

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
| 👆 **Index levé** | Déplacer le curseur |
| 🤏 **Pincement** (Index + Pouce) | Cliquer sur une touche |
| ✋ **Main visible** | Activer le clavier |

### Raccourcis Clavier

| Touche | Action |
|--------|--------|
| `ESC` | Quitter l'application |
| `T` | Changer de thème (Sombre → Clair → Néon → Minimaliste) |
| `S` | Sauvegarder le texte manuellement |
| `C` | Effacer tout le texte |
| `M` | Activer/Désactiver le son |
| `L` | Changer de layout (QWERTY ↔ AZERTY) |

### Indicateurs Visuels

- 🔵 **Contour Cyan** : Touche survolée
- 🟣 **Contour Magenta** : Touche pressée
- ⭕ **Cercle Cyan** : Position du curseur (index)
- ✨ **Particules** : Effet lors des clics

---

## 📁 Structure du Projet

```
air-typing/
├── main.py                    # Application principale
├── config.py                  # Configuration centralisée
├── utils/                     # Modules utilitaires
│   ├── __init__.py
│   ├── hand_detector.py       # Détection des mains (MediaPipe)
│   ├── keyboard.py            # Clavier virtuel
│   ├── ui_components.py       # Composants UI (TextBox, Cursor, etc.)
│   └── audio_manager.py       # Gestionnaire audio
├── hand_landmarker.task       # Modèle MediaPipe
├── requirements.txt           # Dépendances Python
├── typed_text.txt            # Texte sauvegardé (généré automatiquement)
├── .gitignore
└── README.md
```

---

## ⚙️ Configuration

Tous les paramètres sont modifiables dans `config.py` :

### Paramètres Principaux
```python
# Webcam
CAMERA_INDEX = 0              # Index de la caméra
WINDOW_WIDTH = 1280           # Largeur de la fenêtre
WINDOW_HEIGHT = 720           # Hauteur de la fenêtre

# Détection
PINCH_THRESHOLD = 35          # Sensibilité du pincement (pixels)
HOVER_SMOOTHING = 0.7         # Lissage du curseur (0-1)

# Audio
ENABLE_SOUND = True           # Activer/désactiver le son
SOUND_VOLUME = 0.5            # Volume (0.0 - 1.0)

# Sauvegarde
AUTO_SAVE = True              # Sauvegarde automatique
SAVE_INTERVAL = 30            # Intervalle en secondes
```

---

## 🎨 Thèmes Disponibles

### 🌑 Sombre (Défaut)
Interface cyberpunk avec accents cyan et magenta sur fond noir

### ☀️ Clair
Design épuré avec accents bleu et violet sur fond blanc

### 💜 Néon
Style futuriste avec couleurs vives et effet glow

### ⚪ Minimaliste
Design ultra-épuré en noir et blanc

---

## 🐛 Dépannage

### ❌ Erreur : `ImportError: DLL load failed`
```bash
pip uninstall mediapipe
pip install mediapipe==0.10.14
```

### ❌ La webcam ne s'ouvre pas
- Vérifiez que votre webcam est connectée
- Essayez de changer `CAMERA_INDEX` dans `config.py` (0, 1, 2...)
- Fermez les autres applications utilisant la webcam

### ❌ Détection imprécise
- Améliorez l'éclairage de votre environnement
- Ajustez `PINCH_THRESHOLD` dans `config.py`
- Réduisez `HOVER_SMOOTHING` pour plus de réactivité

### ❌ Pas de son
- Vérifiez que `ENABLE_SOUND = True` dans `config.py`
- Installez `numpy` : `pip install numpy`
- Appuyez sur `M` pour activer le son

---

## 🔧 Technologies Utilisées

| Technologie | Version | Rôle |
|------------|---------|------|
| **Python** | 3.11+ | Langage principal |
| **OpenCV** | 4.10.0.84 | Capture webcam et traitement d'image |
| **MediaPipe** | 0.10.14 | Détection et tracking des mains |
| **Pygame-CE** | Latest | Interface graphique et rendu |
| **NumPy** | Latest | Calculs matriciels et génération audio |

---

## 📝 Améliorations Futures

- [ ] Support de gestes supplémentaires (swipe, zoom)
- [ ] Mode d'entraînement pour améliorer la précision
- [ ] Export du texte en différents formats (PDF, DOCX)
- [ ] Support de la dictée vocale combinée
- [ ] Mode multi-utilisateurs
- [ ] Application mobile (iOS/Android)

---

## 📄 Licence

Ce projet est sous licence MIT. Libre d'utilisation pour des projets personnels et commerciaux.

---

## 👤 Auteur

**machideau**
- GitHub: [@machideau](https://github.com/machideau)
- Projet: [air-typing](https://github.com/machideau/air-typing)

---

## 🙏 Remerciements

- **Google MediaPipe** pour la technologie de détection des mains
- **OpenCV** pour le traitement d'image en temps réel
- **Pygame Community Edition** pour le rendu graphique performant

---

## 🌟 Contribuer

Les contributions sont les bienvenues ! N'hésitez pas à :
1. Fork le projet
2. Créer une branche (`git checkout -b feature/AmazingFeature`)
3. Commit vos changements (`git commit -m 'Add AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrir une Pull Request

---

**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile sur GitHub !**

**🎥 [Voir la Démo Vidéo](#)** | **📸 [Captures d'Écran](#)**