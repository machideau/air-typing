# ⌨️ Air-Typing - Clavier Virtuel Contrôlé par Gestes

Un clavier virtuel futuriste contrôlé par gestes, construit avec **Computer Vision**. Ce projet permet de taper dans les airs en suivant les mouvements de la main et les "clics" des doigts (gestes de pincement) à l'aide d'une webcam.


## ✨ Fonctionnalités

* **Suivi des Mains en Temps Réel** : Utilise MediaPipe pour suivre 21 points de repère de la main à haute fréquence
* **Reconnaissance de Gestes** : Détection intelligente du "pincement" en calculant la distance euclidienne entre l'index et le pouce
* **Interface Holographique** : Overlay Pygame semi-transparent créant un effet de Réalité Augmentée (AR)
* **Clavier Complet** : Inclut A-Z, barre d'espace, et système de suppression (Backspace) fonctionnel
* **Retour Visuel Dynamique** : Changement de couleur (Cyan au survol, Magenta au clic) pour un feedback UX immersif

---

## 🚀 Technologies Utilisées

| Technologie | Version | Utilisation |
|------------|---------|-------------|
| **Python** | 3.11+ | Langage principal |
| **OpenCV** | 4.10.0.84 | Traitement d'image et capture webcam |
| **MediaPipe** | 0.10.14 | Détection et suivi des points de la main |
| **Pygame-CE** | Latest | Interface graphique et rendu |
| **NumPy** | Latest | Calculs matriciels |
| **Protobuf** | <5.0.0 | Sérialisation des données MediaPipe |

---

## 📦 Installation et Configuration

### Prérequis

- **Python 3.11** ou supérieur
- **Webcam** fonctionnelle
- **Windows** (testé sur Windows, adaptable pour Mac/Linux)
- **Fichier modèle MediaPipe** : `hand_landmarker.task` (doit être dans le même dossier que `main.py`)

### Étapes d'Installation

#### 1️⃣ Cloner le dépôt

```bash
git clone https://github.com/machideau/air-typing.git
cd air-typing
```

#### 2️⃣ Créer un environnement virtuel (Recommandé)

**Windows :**
```bash
py -3.11 -m venv env
env\Scripts\activate
```

**Mac/Linux :**
```bash
python3.11 -m venv env
source env/bin/activate
```

#### 3️⃣ Installer les dépendances

```bash
pip install -r requirements.txt
```

**Ou manuellement :**
```bash
pip install opencv-python==4.10.0.84 mediapipe==0.10.14 numpy protobuf<5.0.0 pygame-ce pygame msvc-runtime
```

#### 4️⃣ Télécharger le modèle MediaPipe

Le fichier `hand_landmarker.task` doit être présent dans le répertoire racine du projet. Si vous ne l'avez pas, téléchargez-le depuis :

🔗 [MediaPipe Hand Landmarker Model](https://storage.googleapis.com/mediapipe-models/hand_landmarker/hand_landmarker/float16/latest/hand_landmarker.task)

Placez-le dans le dossier `air-typing/` à côté de `main.py`.

---

## 🎮 Utilisation

### Lancer l'Application

```bash
python main.py
```

### Comment Utiliser le Clavier Virtuel

1. **Positionnement** : Placez votre main devant la webcam, paume visible
2. **Déplacer le Curseur** : Utilisez la pointe de votre **index** comme curseur pour survoler les touches
3. **Taper une Lettre** : Rapprochez votre **pouce** et votre **index** (geste de pincement) pour "cliquer" sur une touche
4. **Effacer** : Utilisez la touche **BS** (Backspace) en haut à droite pour supprimer des caractères
5. **Espace** : La touche **SPACE** en bas permet d'ajouter des espaces

### Indicateurs Visuels

- **Cercle Cyan** : Curseur de votre index
- **Contour Cyan** : Touche survolée
- **Contour Magenta** : Touche cliquée
- **Zone de Texte** : Affiche le texte tapé en temps réel

---

## 🛠 Structure du Projet

```
air-typing/
├── main.py                  # Application principale (boucle Pygame + logique MediaPipe)
├── hand_landmarker.task     # Modèle MediaPipe pour la détection des mains
├── requirements.txt         # Dépendances Python
├── .gitignore              # Fichiers à ignorer par Git
├── README.md               # Ce fichier
└── debug_*.py              # Scripts de débogage (optionnels)
```

---

## 🐛 Dépannage

### Problème : `ImportError: DLL load failed while importing _framework_bindings`

**Solution :**
```bash
pip uninstall mediapipe
pip install mediapipe==0.10.14
```

### Problème : La webcam ne s'ouvre pas

**Solution :**
- Vérifiez que votre webcam est connectée et fonctionnelle
- Essayez de changer l'index de la caméra dans `main.py` :
  ```python
  cap = cv2.VideoCapture(1)  # Essayez 0, 1, 2...
  ```

### Problème : `FileNotFoundError: hand_landmarker.task`

**Solution :**
- Téléchargez le modèle depuis le lien ci-dessus
- Placez-le dans le même dossier que `main.py`

### Problème : Détection des gestes imprécise

**Solution :**
- Améliorez l'éclairage de votre environnement
- Ajustez la distance entre votre main et la webcam
- Modifiez le seuil de détection dans `main.py` (ligne 119) :
  ```python
  if distance < 40:  # Augmentez ou diminuez cette valeur
  ```

---

## 📝 Améliorations Futures

- [ ] Ajout de sons de clic pour le feedback audio
- [ ] Support de plusieurs langues (AZERTY, QWERTZ)
- [ ] Mode sombre / clair
- [ ] Enregistrement automatique du texte tapé
- [ ] Détection de gestes supplémentaires (swipe pour effacer tout, etc.)
- [ ] Optimisation des performances pour des FPS plus élevés

---

## 📄 Licence

Ce projet est open source. Libre d'utilisation pour des projets personnels et éducatifs.

---

## 👤 Auteur

**machideau**
- GitHub: [@machideau](https://github.com/machideau)
- Projet: [air-typing](https://github.com/machideau/air-typing)

---

## 🙏 Remerciements

- **MediaPipe** par Google pour la technologie de suivi des mains
- **OpenCV** pour le traitement d'image
- **Pygame Community Edition** pour le rendu graphique

---

**⭐ Si ce projet vous plaît, n'hésitez pas à lui donner une étoile sur GitHub !**