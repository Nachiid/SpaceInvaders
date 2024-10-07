### README (English)

# Space Invaders - Python Game

## Description

This is a Python implementation of the classic **Space Invaders** arcade game. The player controls a spaceship (the Defender) and must destroy waves of alien invaders before they reach the bottom of the screen or destroy the ship. The player can move the ship left and right, as well as shoot at enemies. The game tracks scores and includes a simple system for lives.

## Features

- **Player-controlled Defender**: The player can move the ship left and right and shoot projectiles at the alien invaders.
- **Alien Fleet**: Aliens move horizontally and drop down after reaching the edge. They shoot projectiles towards the player.
- **Score System**: Points are awarded for each alien destroyed. The game also saves the player's score.
- **Lives System**: The player starts with 3 lives. If all lives are lost or aliens reach the bottom, the game is over.
- **Game States**: Displays "Game Over" or "Victory" messages depending on the player's performance.

## File Structure

- `SpaceInvaders.py` - Main game logic and initialization.
- `Game.py` - Controls the game state, movement of aliens, bullets, and interactions.
- `Fleet.py` - Manages alien fleet movement and shooting.
- `Alien.py` - Defines the behavior and attributes of alien invaders.
- `Defender.py` - Represents the player's ship.
- `Bullet.py` - Handles bullet firing and collision detection.
- `Score.py` - Tracks the player's score and saves it to a file.
- `Resultats.py` - Stores and manages the results and high scores.

## Prerequisites

- Python 3.x
- Tkinter (typically pre-installed with Python)

## How to Play

1. Clone or download the repository.
2. Make sure all necessary image files (`alien2.png`, `rk1.png`, `heartF.gif`, `explosion.gif`) are in the same directory as the Python script.
3. Run the game:
    ```bash
    python SpaceInvaders.py
    ```
4. Enter your name and start playing:
    - **Left Arrow**: Move the defender left.
    - **Right Arrow**: Move the defender right.
    - **Space Bar**: Shoot.

## Score System

- Scores are based on the number of aliens destroyed.
- The game stores the player’s score in `LastScore.json` and updates the list of high scores in `AllResults.json`.

## Authors

- EL OMARI Mohammed Hachim
- NACHID Aymen

---

### README (French)

# Space Invaders - Jeu Python

## Description

Ceci est une implémentation en Python du jeu d'arcade classique **Space Invaders**. Le joueur contrôle un vaisseau spatial (le Défenseur) et doit détruire des vagues d'envahisseurs extraterrestres avant qu'ils n'atteignent le bas de l'écran ou ne détruisent le vaisseau. Le joueur peut déplacer le vaisseau à gauche et à droite, ainsi que tirer sur les ennemis. Le jeu suit les scores et inclut un simple système de vies.

## Fonctionnalités

- **Défenseur contrôlé par le joueur** : Le joueur peut déplacer le vaisseau à gauche et à droite et tirer des projectiles sur les envahisseurs aliens.
- **Flotte d'Aliens** : Les aliens se déplacent horizontalement et descendent après avoir atteint le bord. Ils tirent des projectiles vers le joueur.
- **Système de Score** : Des points sont attribués pour chaque alien détruit. Le jeu enregistre également le score du joueur.
- **Système de Vies** : Le joueur commence avec 3 vies. Si toutes les vies sont perdues ou si les aliens atteignent le bas, la partie est terminée.
- **États du Jeu** : Affiche des messages "Game Over" ou "Victory" selon la performance du joueur.

## Structure des Fichiers

- `SpaceInvaders.py` - Logique principale du jeu et initialisation.
- `Game.py` - Contrôle l'état du jeu, le mouvement des aliens, des projectiles et les interactions.
- `Fleet.py` - Gère les mouvements et les tirs de la flotte d'aliens.
- `Alien.py` - Définit le comportement et les attributs des envahisseurs aliens.
- `Defender.py` - Représente le vaisseau du joueur.
- `Bullet.py` - Gère les tirs et la détection de collision.
- `Score.py` - Suivi du score du joueur et sauvegarde dans un fichier.
- `Resultats.py` - Stocke et gère les résultats et les meilleurs scores.

## Prérequis

- Python 3.x
- Tkinter (généralement pré-installé avec Python)

## Comment Jouer

1. Clonez ou téléchargez le dépôt.
2. Assurez-vous que tous les fichiers d'image nécessaires (`alien2.png`, `rk1.png`, `heartF.gif`, `explosion.gif`) sont dans le même répertoire que le script Python.
3. Exécutez le jeu :
    ```bash
    python SpaceInvaders.py
    ```
4. Entrez votre nom et commencez à jouer :
    - **Flèche gauche** : Déplacer le défenseur à gauche.
    - **Flèche droite** : Déplacer le défenseur à droite.
    - **Barre d'espace** : Tirer.

## Système de Score

- Les scores sont basés sur le nombre d'aliens détruits.
- Le jeu enregistre le score du joueur dans `LastScore.json` et met à jour la liste des meilleurs scores dans `AllResults.json`.

## Auteurs

- EL OMARI Mohammed Hachim
- NACHID Aymen
