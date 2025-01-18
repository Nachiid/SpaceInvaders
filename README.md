### README

# English

# Space Invaders - Python Game

## Description

Space Invaders is a Python reimplementation of the classic arcade game. The player controls a spaceship (the Defender) and must destroy waves of alien invaders before they reach the bottom of the screen or destroy the ship.

The game features score tracking, a lives system, and immersive animations. However, custom font handling has some technical limitations (see below).

## Features

- **Defender Control**: The player can move the spaceship left and right and shoot projectiles at enemies.
- **Alien Fleet**: Aliens move horizontally, descend when they reach the screen edges, and shoot projectiles at the player.
- **Score System**: The game calculates points for each alien destroyed and saves scores in JSON files.
- **Lives System**: The player starts with 3 lives. The game ends if all lives are lost or aliens reach the bottom of the screen.
- **Game States**: The game displays a "Game Over" or "Victory" screen at the end of a session.

## Limitations

- **Custom Fonts**: Although the game uses a custom font (from a .ttf file), it is not consistently applied to all text in the game. This limitation is due to incompatibilities with the Tkinter module.

## Future Improvements

- **Executable Creation**: One of the next steps is to enable easy distribution of the game as an executable file, so it can be played without requiring Python installation.
- **Improved Font Handling**: Investigate alternatives to ensure consistent application of custom fonts.

## File Structure

- `SpaceInvaders.py` - Main file containing the overall game logic.
- `Game.py` - Manages game state, object movements, and interactions.
- `Fleet.py` - Controls alien movements and shooting.
- `Alien.py` - Defines the behavior and properties of the alien invaders.
- `Defender.py` - Represents the player-controlled spaceship.
- `Bullet.py` - Manages projectiles and collision detection.
- `Score.py` - Tracks and saves scores.
- `Resultats.py` - Manages results and leaderboards.
- `images/` - Contains the images required for the game (aliens, ships, explosions, etc.).
- `fonts/` - Contains custom font files.
- `donnee/` - Contains JSON files for storing scores and results.

## Prerequisites

- **Python 3.x**
- **Tkinter** (typically included with Python)
- **Pillow** (for image handling):
  ```bash
  pip install pillow
  ```

## Installation and Launch Instructions

1. Clone or download this repository.
2. Install the required dependencies using pip (see above).
3. Ensure the `images`, `fonts`, and `donnee` folders are in the same directory as `SpaceInvaders.py`.
4. Run the game using the following command:
   ```bash
   python SpaceInvaders.py
   ```

## Controls

- **Left Arrow**: Move the spaceship left.
- **Right Arrow**: Move the spaceship right.
- **Space Bar**: Shoot a projectile.

## Score System

- Points are awarded for each alien destroyed.
- Scores are saved in `donnee/LastScore.json`.
- Leaderboards are updated in `donnee/AllResults.json`.

## Authors

- **EL OMARI Mohammed Hachim**
- **NACHID Aymen**

---

Thank you for playing Space Invaders! Your suggestions and feedback are welcome to help improve the game.

-

# French

# Space Invaders - Jeu Python

## Description

Space Invaders est une réimplémentation Python du jeu d'arcade classique. Le joueur contrôle un vaisseau spatial (le Défenseur) et doit détruire des vagues d'envahisseurs extraterrestres avant qu'ils n'atteignent le bas de l'écran ou ne détruisent le vaisseau.

Le jeu propose un suivi des scores, un système de vies et des animations immersives. Cependant, la gestion des polices personnalisées présente quelques limitations techniques (voir plus bas).

## Fonctionnalités

- **Contrôle du Défenseur** : Le joueur peut déplacer le vaisseau à gauche et à droite et tirer des projectiles sur les ennemis.
- **Flotte d'Aliens** : Les aliens se déplacent horizontalement, descendent lorsqu'ils atteignent les bords de l'écran, et tirent des projectiles vers le joueur.
- **Système de Score** : Le jeu calcule les points gagnés pour chaque alien détruit et sauvegarde les scores dans des fichiers JSON.
- **Système de Vies** : Le joueur commence avec 3 vies. La partie est terminée si toutes les vies sont perdues ou si les aliens atteignent le bas de l'écran.
- **États du Jeu** : Le jeu affiche un écran "Game Over" ou "Victory" à la fin d'une partie.

## Limitations

- **Polices personnalisées** : Bien que le jeu utilise une police personnalisée (à partir d'un fichier .ttf), celle-ci n'est pas toujours appliquée comme prévu à tous les textes dans le jeu. Cette limitation est due à des incompatibilités avec le module Tkinter.

## Améliorations futures

- **Création d'un exécutable** : L'une des prochaines étapes est de permettre la distribution facile du jeu sous forme d'exécutable, afin qu'il puisse être joué sans installer Python.
- **Amélioration de la gestion des polices** : Investiguer des alternatives pour garantir une application cohérente des polices personnalisées.

## Structure des Fichiers

- `SpaceInvaders.py` - Fichier principal contenant la logique globale du jeu.
- `Game.py` - Gère l'état du jeu, les mouvements des objets et les interactions.
- `Fleet.py` - Contrôle les mouvements et tirs des aliens.
- `Alien.py` - Définit le comportement et les propriétés des envahisseurs.
- `Defender.py` - Représente le vaisseau spatial du joueur.
- `Bullet.py` - Gère les projectiles et la détection de collisions.
- `Score.py` - Suivi et sauvegarde des scores.
- `Resultats.py` - Gère les résultats et classements.
- `images/` - Contient les images nécessaires pour le jeu (aliens, vaisseaux, explosions, etc.).
- `fonts/` - Contient les fichiers de polices personnalisées.
- `donnee/` - Contient les fichiers JSON pour enregistrer les scores et résultats.

## Prérequis

- **Python 3.x**
- **Tkinter** (généralement inclus avec Python)
- **Pillow** (pour la gestion des images) :
  ```bash
  pip install pillow
  ```

## Instructions d'Installation et de Lancement

1. Clonez ou téléchargez ce dépôt.
2. Installez les dépendances nécessaires avec pip (voir ci-dessus).
3. Assurez-vous que les dossiers `images`, `fonts`, et `donnee` sont présents dans le même répertoire que `SpaceInvaders.py`.
4. Lancez le jeu avec la commande suivante :
   ```bash
   python SpaceInvaders.py
   ```

## Contrôles

- **Flèche gauche** : Déplacer le vaisseau vers la gauche.
- **Flèche droite** : Déplacer le vaisseau vers la droite.
- **Barre d'espace** : Tirer un projectile.

## Système de Score

- Les points sont attribués pour chaque alien détruit.
- Les scores sont enregistrés dans `donnee/LastScore.json`.
- Les classements sont mis à jour dans `donnee/AllResults.json`.

## Auteurs

- **EL OMARI Mohammed Hachim**
- **NACHID Aymen**

---

Merci d'avoir joué à Space Invaders ! Vos suggestions et commentaires sont les bienvenus pour améliorer le jeu.
