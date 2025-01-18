"""
Space Invaders - Classes Principales
----------------------------------
Auteurs: NACHID AYMEN - EL OMARI MOHAMMED HACHIM

Ce module contient les classes principales qui gèrent:
- L'interface utilisateur initiale (SpaceInvaders)
- La logique principale du jeu (Game)
- La flotte d'aliens et leur comportement (Fleet)
"""

import tkinter as tk
from tkinter import *
import tkinter.font as font
from PIL import Image, ImageTk
import json
import random as rd
import time


class SpaceInvaders(object):
    """
    Classe principale qui initialise l'interface du jeu et gère le démarrage de la partie.
    Gère la fenêtre principale et l'écran de saisie du pseudo du joueur.
    """

    def __init__(self):
        # Configuration de la fenêtre principale
        self.root = tk.Tk()
        self.root.title("Space Invaders")

        # le chemin de la police personnalisée
        font_path = "fonts/PressStart2P-Regular.ttf"
        try:
            self.custom_font = font.Font(file=font_path, size=14)
        except Exception as e:
            print(f"Erreur de chargement de la police : {e}")
            self.custom_font = font.Font(family="Arial", size=14)

        # Désactivation du redimensionnement de la fenêtre
        self.root.resizable(0, 0)

        # Création du frame principal
        self.frame = tk.Frame(self.root)
        self.frame.pack(side="top", fill="both")

        # Initialisation du jeu avec la police personnalisée
        self.game = Game(self.frame, self.custom_font)

    def play(self):
        """
        Initialise l'interface de saisie du pseudo et démarre le jeu.
        Configure les événements de validation et lance la boucle principale.
        """
        def lancer(event):
            # Désactive l'entrée après validation
            self.input_name.config(state='disabled')
            self.game.score.set_name(
                self.input_name.get())  # Enregistre le pseudo
            # Configure les contrôles
            self.root.bind("<Key>", self.game.stop_def)
            self.game.start_animation()  # Démarre l'animation du jeu

        # Configuration de l'interface de saisie du pseudo
        Lname = Label(
            self.frame,
            text="Enter Votre Pseudo : ",
            font=self.custom_font)
        Lname.pack(side=TOP)
        self.input_name = Entry(self.frame, bd=5, font=self.custom_font)
        self.input_name.pack()
        self.input_name.focus_set()
        self.input_name.bind('<Return>', lancer)

        # Lancement de la boucle principale
        self.root.mainloop()


class Game(object):
    """
    Classe principale du jeu qui gère:
    - Le canvas et ses dimensions
    - Les interactions entre les composants (defender, fleet, score)
    - La logique de jeu (victoire/défaite)
    - L'animation et les mises à jour
    """

    def __init__(self, frame, custom_font):
        # Initialisation des attributs principaux
        self.frame = frame
        self.custom_font = custom_font
        self.fleet = Fleet()
        self.defender = Defender()
        self.score = Score()

        # Configuration des dimensions du canvas
        self.canvas_height = self.fleet.get_height()
        self.canvas_width = self.fleet.get_width()

        # Configuration du fond du jeu
        original_image = Image.open("images/earth.gif")
        resized_image = original_image.resize(
            (self.canvas_width, self.canvas_height),
            Image.Resampling.LANCZOS
        )
        self.background_image = ImageTk.PhotoImage(resized_image)

        # Création et configuration du canvas
        self.canvas = tk.Canvas(
            self.frame,
            width=self.canvas_width,
            height=self.canvas_height
        )
        self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_image)
        self.canvas.pack(padx=5, pady=5, side="bottom")

        # Installation des éléments du jeu
        self.defender.install_in(self.canvas)
        self.defender.display_defender_lifes(self.canvas)
        self.fleet.install_in(self.canvas)

    def stop_def(self, event):
        """
        Gère les contrôles du joueur (déplacements et tirs).

        Args:
            event: L'événement clavier capturé
        """
        xcond = self.defender.xi

        # Gestion des déplacements gauche/droite
        if event.keysym == 'Left':
            if xcond - self.defender.move_delta > 0:
                self.defender.xi -= self.defender.move_delta
                self.defender.move_in(self.canvas, -self.defender.move_delta)
        elif event.keysym == 'Right':
            if xcond + self.defender.move_delta < self.defender.canvas_width:
                self.defender.xi += self.defender.move_delta
                self.defender.move_in(self.canvas, self.defender.move_delta)
        # Gestion du tir
        elif event.keysym == 'space':
            if len(self.fleet.aliens_fleet) != 0 and self.defender.lifes > 0:
                self.defender.fire(self.canvas)

    def Bienvenue(self):
        """Affiche le message de bienvenue avec le pseudo du joueur"""
        text1 = f"Bonjour : '{self.score.name}'"
        label = Label(
            self.canvas,
            text=text1,
            bg="Black",
            fg="white",
            font=self.custom_font
        )
        self.canvas.create_window(110, 25, window=label)

    def affiche_score(self):
        """Configure et affiche le score actuel du joueur"""
        self.score_actuel = StringVar()
        score_label = Label(
            self.canvas,
            textvariable=self.score_actuel,
            bg="black",
            fg="white",
            font=self.custom_font
        )
        self.score_actuel.set(f"score : {self.score.get_points()}")
        self.canvas.create_window(1050, 25, window=score_label)

    def saveFile(self):
        """Sauvegarde les scores dans les fichiers de données"""
        self.score.delai = int(time.time()) - self.score.start_time
        self.score.toFile("donnees/LastScore.json")
        lastScore = self.score.fromFile("donnees/LastScore.json")
        self.resultats = Resultats.fromFile("donnees/AllResults.json")
        self.resultats.ajout(lastScore)
        self.resultats.toFile("donnees/AllResults.json")

    def game_over(self):
        """Gère la fin de partie en cas de défaite"""
        self.score.winning = False
        self.saveFile()

        last_score = self.score.fromFile("donnees/LastScore.json")
        w = int(self.canvas.cget("width")) // 2
        h = int(self.canvas.cget("height")) // 2

        # Supprimer les éléments existants du canvas
        self.canvas.delete("all")

        # Charger et redimensionner l'image de fond 'game_over.jpg'
        original_image = Image.open("images/game_over.jpg")
        resized_image = original_image.resize(
            (self.canvas_width, self.canvas_height),  # Taille du canvas
            Image.Resampling.LANCZOS
        )
        self.background_go = ImageTk.PhotoImage(
            resized_image)  # Conserver la référence

        # Ajouter l'image de fond sur le canvas
        self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_go
        )

        # Message de défaite
        defeat_message = (
            f"Game Over !\n\n"
            f"Score : {last_score.points}\n\n"
            f"Time alive : {last_score.delai} s"
        )

        # Afficher le texte au centre de l'écran
        self.canvas.create_text(
            w, h,
            text=defeat_message,
            fill="white",
            font=self.custom_font,
            anchor="center"
        )

    def victoire(self):
        """Gère la fin de partie en cas de victoire"""
        self.score.winning = True
        self.saveFile()

        last_score = self.score.fromFile("donnees/LastScore.json")
        w = int(self.canvas.cget("width")) // 2
        h = int(self.canvas.cget("height")) // 3

        # Supprimer les éléments existants du canvas
        self.canvas.delete("all")

        # Charger et redimensionner l'image de fond 'victory.jpg'
        # Remplacez cette image par celle que vous souhaitez
        original_image = Image.open("images/victory.jpg")
        resized_image = original_image.resize(
            (self.canvas_width, self.canvas_height),  # Taille du canvas
            Image.Resampling.LANCZOS
        )
        self.background_victory = ImageTk.PhotoImage(
            resized_image)  # Conserver la référence

        # Ajouter l'image de fond sur le canvas
        self.canvas.create_image(
            0, 0, anchor=tk.NW, image=self.background_victory
        )

        # Message de victoire
        victory_message = (
            f"You Won !   "
            f"Score : {last_score.points}     "
            f"Time alive : {last_score.delai} s"
        )

        # Afficher le texte au centre de l'écran
        self.canvas.create_text(
            w, h,
            text=victory_message,
            fill="white",
            font=self.custom_font,
            anchor="center"
        )

    def start_animation(self):
        """Initialise et démarre l'animation du jeu"""
        self.Bienvenue()
        self.affiche_score()
        self.fleet.previous_shoot_time = float(time.time())
        self.animation()

    def animation(self):
        """
        Boucle principale d'animation du jeu.
        Gère les mouvements, collisions et mises à jour de l'état du jeu.
        """
        self.score_actuel.set(f"score : {self.score.get_points()}")

        if len(self.fleet.aliens_fleet) != 0:
            x1, y1, x2, y2 = self.canvas.bbox("alien")

            # Vérifie si les aliens n'ont pas atteint le defender
            if (y2 <= int(self.canvas.cget("height")) - self.defender.height
                    and self.defender.lifes > 0):
                # Met à jour tous les éléments du jeu
                self.defender.move_bullet(self.canvas)
                self.defender.manage_defender_touched_by(
                    self.canvas, self.fleet)
                self.fleet.move_aliens_bullets(self.canvas)
                self.fleet.move_in(self.canvas)
                self.fleet.manage_touched_aliens_by(
                    self.canvas, self.defender, self.score)
                self.fleet.install_aliens_bullets(self.canvas)
                self.fleet.animation_aliens_img(self.canvas)

                # Continue l'animation
                self.canvas.after(50, self.animation)
            else:
                self.game_over()
        else:
            self.victoire()


# -------------------Fleet-------------------------
class Fleet(object):
    """
    Classe qui gère la flotte d'aliens.
    - Contient les paramètres relatifs à la taille de la flotte
    - Gère le déplacement des aliens
    - Gère le tir des aliens
    - Détecte les collisions entre les projectiles et les aliens
    """

    def __init__(self):
        # Initialisation des attributs liés à la flotte
        self.width = 1220  # Largeur de la zone de la flotte
        self.height = 600  # Hauteur de la zone de la flotte

        # Configuration du nombre d'aliens dans la flotte
        self.aliens_lines = 5  # Nombre de lignes d'aliens
        self.aliens_columns = 6  # Nombre de colonnes d'aliens
        self.aliens_inner_gap = 10  # Espacement entre les aliens
        fleet_size = self.aliens_lines * self.aliens_columns
        # Liste pour stocker les aliens
        self.aliens_fleet = [None] * fleet_size

        # Déplacements des aliens
        self.alien_x_delta = 5  # Delta de déplacement horizontal des aliens
        self.alien_y_delta = 15  # Delta de déplacement vertical des aliens

        # Gestion de l'animation
        self.animation_start_time = float(
            time.time())  # Temps du début de l'animation

        # Paramètres liés aux tirs des aliens
        self.temps_ecart = 1  # Temps d'écart entre les tirs
        self.previous_shoot_time = None  # Temps du dernier tir
        self.max_fired_bullets = 5  # Nombre maximum de projectiles tirés simultanément
        self.aliens_fired_bullets = []  # Liste des projectiles tirés par les aliens

    def get_width(self):
        """Retourne la largeur de la flotte."""
        return self.width

    def get_height(self):
        """Retourne la hauteur de la flotte."""
        return self.height

    def install_in(self, canvas):
        """
        Installe la flotte d'aliens sur le canevas au départ.

        Args:
            canvas: Le canevas où les aliens seront placés
        """
        x, y = 50, 75  # Position initiale des aliens
        pos = 0  # Index pour positionner chaque alien
        for i in range(0, self.aliens_lines):
            for j in range(0, self.aliens_columns):
                alien = Alien()  # Création d'un nouvel alien
                self.aliens_fleet[pos] = alien.install_in(
                    canvas, x, y)  # Placement de l'alien
                pos += 1
                # Déplacement de l'aliens en horizontal
                x += self.aliens_inner_gap + alien.alien_width
            x = 50  # Remise à zéro de la position en X
            # Déplacement de la ligne d'aliens vers le bas
            y += self.aliens_inner_gap + alien.alien_height

    def move_in(self, canvas):
        """
        Gère le déplacement des aliens sur le canevas.

        Args:
            canvas: Le canevas où les aliens se déplacent
        """
        if len(self.aliens_fleet) != 0:
            # Vérification des bords du canevas pour faire rebondir les aliens
            x1, y1, x2, y2 = canvas.bbox("alien")
            if x2 >= int(canvas.cget("width")
                         ):  # Si les aliens atteignent le bord droit
                self.alien_x_delta = -self.alien_x_delta  # Inverser la direction horizontale
                dy = self.alien_y_delta  # Déplacer les aliens vers le bas
            elif x1 <= 0:  # Si les aliens atteignent le bord gauche
                self.alien_x_delta = -self.alien_x_delta  # Inverser la direction horizontale
                dy = self.alien_y_delta  # Déplacer les aliens vers le bas
            else:
                dy = 0  # Si l'animation ne touche pas les bords, les aliens ne descendent pas

            # Déplacer chaque alien en fonction des nouvelles valeurs de delta
            for i in range(0, len(self.aliens_fleet)):
                self.aliens_fleet[i].move_in(canvas, self.alien_x_delta, dy)

    def manage_touched_aliens_by(self, canvas, defender, score):
        """
        Gère les aliens touchés par les projectiles du défenseur.

        Args:
            canvas: Le canevas où se trouve la flotte d'aliens
            defender: Le défenseur qui tire des projectiles
            score: L'objet de gestion du score
        """
        sortir1 = False
        sortir2 = False
        for i in range(len(self.aliens_fleet)):  # Parcours des aliens
            x1, y1, x2, y2 = canvas.bbox(
                self.aliens_fleet[i].id)  # Coordonnées de l'alien
            overlapped = canvas.find_overlapping(
                x1, y1, x2, y2)  # Vérification des chevauchements
            if len(overlapped) > 1:  # Si un projectile touche un alien
                for j in range(len(defender.fired_bullets)
                               ):  # Parcours des projectiles du défenseur
                    for k in range(len(overlapped)):
                        # Collision détectée
                        if defender.fired_bullets[j].id == overlapped[k]:
                            self.effet_boom(
                                canvas, defender.fired_bullets[j])  # Effet de l'explosion
                            self.aliens_fleet[i].touched_by(
                                canvas, defender.fired_bullets[j])  # Alien touché
                            score.refresh_score(
                                time.time())  # Mise à jour du score
                            # Suppression du projectile
                            del defender.fired_bullets[j]
                            del self.aliens_fleet[i]  # Suppression de l'alien
                            sortir1 = True
                            sortir2 = True
                            break
                    if sortir2:
                        break
                if sortir1:
                    break

    def install_aliens_bullets(self, canvas):
        """
        Installe les projectiles tirés par les aliens.

        Args:
            canvas: Le canevas où les projectiles sont installés
        """
        if len(self.aliens_fleet) != 0:
            # Limite sur le nombre de projectiles
            if len(self.aliens_fired_bullets) < self.max_fired_bullets:
                # Choix aléatoire d'un alien
                choix = rd.randint(0, len(self.aliens_fleet) - 1)
                x, y = canvas.coords(
                    self.aliens_fleet[choix].id)  # Coordonnées de l'alien
                self.aliens_fire(canvas, x, y)  # L'alien tire un projectile

    def aliens_fire(self, canvas, x, y):
        """
        Permet à un alien de tirer un projectile.

        Args:
            canvas: Le canevas où le projectile est tiré
            x: Coordonnée X de l'alien
            y: Coordonnée Y de l'alien
        """
        if float(time.time(
        )) - self.previous_shoot_time >= self.temps_ecart:  # Vérification de l'écart de temps
            bullet = Bullet("alien")  # Création d'un projectile
            bullet = bullet.install_aliens_bullets(
                canvas, x, y)  # Installation du projectile
            # Ajout du projectile à la liste des projectiles tirés
            self.aliens_fired_bullets.append(bullet)
            # Mise à jour du temps du dernier tir
            self.previous_shoot_time = float(time.time())

    def move_aliens_bullets(self, canvas):
        """
        Déplace les projectiles tirés par les aliens.

        Args:
            canvas: Le canevas où les projectiles se déplacent
        """
        for i in range(0, len(self.aliens_fired_bullets)):
            x1, y1, x2, y2 = canvas.bbox(
                self.aliens_fired_bullets[i].id)  # Coordonnées du projectile
            if y1 > int(canvas.cget("height")
                        ):  # Si le projectile dépasse le bas du canevas
                # Suppression du projectile
                canvas.delete(self.aliens_fired_bullets[i].id)
                # Suppression du projectile de la liste
                del self.aliens_fired_bullets[i]
                break
            else:
                self.aliens_fired_bullets[i].move_in(
                    canvas)  # Déplacement du projectile

    def animation_aliens_img(self, canvas):
        """
        Anime l'image des aliens.

        Args:
            canvas: Le canevas où les images des aliens sont affichées
        """
        temps = float(time.time())  # Temps actuel
        if temps - self.animation_start_time > 1:  # Rafraîchissement toutes les secondes
            self.animation_start_time = temps
            for i in range(len(self.aliens_fleet)):
                # Rafraîchissement des images des aliens
                self.aliens_fleet[i].refresh_img(canvas)

    def effet_boom(self, canvas, projectile):
        """
        Crée l'effet visuel de l'explosion lorsque les projectiles touchent un alien.

        Args:
            canvas: Le canevas où l'effet est affiché
            projectile: Le projectile qui a causé l'explosion
        """
        self.boom = PhotoImage(
            file="images/boom.gif")  # Chargement de l'image de l'explosion
        x1, y1, x2, y2 = canvas.bbox(
            projectile.id)  # Coordonnées du projectile
        # Position de l'explosion (centre du projectile)
        x, y = x1 + (x2 - x1) / 2, y1 + (y2 - y1) / 2
        boom = canvas.create_image(
            x, y, image=self.boom, tags="boom")  # Affichage de l'explosion
        # Suppression de l'effet après 45 ms
        canvas.after(45, canvas.delete, boom)

# ------------- Alien ---------------#


class Alien(object):
    """
    Classe représentant un alien dans le jeu.
    Gère l'affichage, le déplacement et les interactions avec les projectiles.
    """

    def __init__(self):
        # Initialisation des attributs de l'alien
        self.id = None  # Identifiant de l'image de l'alien sur le canevas
        self.alive = True  # Indique si l'alien est toujours vivant
        self.alien = PhotoImage(file="images/alien.png")  # Image de l'alien
        self.alien_width = self.alien.width()  # Largeur de l'image de l'alien
        self.alien_height = self.alien.height()  # Hauteur de l'image de l'alien

    def get_width(self):
        """Retourne la largeur de l'image de l'alien."""
        return self.alien_width

    def get_height(self):
        """Retourne la hauteur de l'image de l'alien."""
        return self.alien_height

    def install_in(self, canvas, x, y):
        """
        Installe l'alien sur le canevas à une position donnée.

        Args:
            canvas: Le canevas où l'alien sera installé
            x: Position X de l'alien
            y: Position Y de l'alien

        Retourne:
            L'objet alien après avoir été installé sur le canevas.
        """
        self.id = canvas.create_image(
            x, y, image=self.alien, tags="alien")  # Création de l'image de l'alien
        return self  # Retourne l'instance de l'alien

    def move_in(self, canvas, dx, dy):
        """
        Déplace l'alien sur le canevas en fonction des deltas.

        Args:
            canvas: Le canevas où l'alien est déplacé
            dx: Déplacement horizontal
            dy: Déplacement vertical
        """
        canvas.move(self.id, dx, dy)  # Déplace l'alien de dx et dy

    def touched_by(self, canvas, projectile):
        """
        Gère l'impact d'un projectile avec l'alien.

        Args:
            canvas: Le canevas où les objets sont gérés
            projectile: Le projectile qui touche l'alien

        Supprime l'alien et le projectile du canevas et marque l'alien comme mort.
        """
        canvas.delete(projectile.id)  # Suppression du projectile du canevas
        canvas.delete(self.id)  # Suppression de l'alien du canevas
        self.alive = False  # Marque l'alien comme mort

    def refresh_img(self, canvas):
        """
        Anime l'alien en changeant son image (changement temporaire d'image pour l'animation).

        Args:
            canvas: Le canevas où l'image de l'alien est modifiée
        """
        if (self.alien.cget("file") ==
                "images/alien.png"):  # Si l'image actuelle est celle de l'alien
            # Change l'image de l'alien en celle d'un "rocket"
            self.alien = PhotoImage(file="images/rocket.png")
            # Mise à jour de l'image sur le canevas
            canvas.itemconfigure(self.id, image=self.alien)
            # Restaure l'image d'origine de l'alien
            self.alien = PhotoImage(file="images/alien.png")
            # Mise à jour de l'image sur le canevas
            canvas.itemconfigure(self.id, image=self.alien)

# ------------- Defender ---------------#


class Defender(object):
    """
    Classe représentant le défenseur dans le jeu, qui contrôle les déplacements du joueur,
    les tirs et la gestion des vies.
    """

    def __init__(self):
        # Initialisation des attributs du défenseur
        self.defender_img = PhotoImage(
            file="images/rocket.png")  # Image du défenseur
        # Image représentant une vie
        self.life_img = PhotoImage(file="images/heart.gif")
        self.boom = PhotoImage(file="images/boom.gif")  # Image de l'explosion
        self.width = self.defender_img.width()  # Largeur de l'image du défenseur
        self.height = self.defender_img.height()  # Hauteur de l'image du défenseur

        # Hauteur du canevas basée sur la flotte
        self.canvas_height = Fleet().get_height()
        # Largeur du canevas basée sur la flotte
        self.canvas_width = Fleet().get_width()

        self.id = None  # Identifiant de l'image du défenseur sur le canevas
        self.lifes = 3  # Nombre de vies du défenseur
        # Position initiale en X du défenseur (centré)
        self.xi = self.canvas_width // 2 - self.width
        # Position initiale en Y du défenseur (en bas)
        self.yi = self.canvas_height - self.height
        # Distance de déplacement du défenseur par mouvement
        self.move_delta = self.width / 2

        self.max_fired_bullets = 8  # Nombre maximal de projectiles que le défenseur peut tirer
        self.fired_bullets = []  # Liste des projectiles tirés par le défenseur

    def get_height(self):
        """Retourne la hauteur de l'image du défenseur."""
        return self.height

    def get_width(self):
        """Retourne la largeur de l'image du défenseur."""
        return self.width

    def install_in(self, canvas):
        """
        Installe l'image du défenseur sur le canevas.

        Args:
            canvas: Le canevas sur lequel le défenseur sera affiché
        """
        self.id = canvas.create_image(
            self.xi,
            self.yi,
            image=self.defender_img,
            tags="defender")

    def display_defender_lifes(self, canvas):
        """
        Affiche les vies du défenseur sur le canevas sous forme de cœurs.

        Args:
            canvas: Le canevas sur lequel les vies seront affichées
        """
        width = self.life_img.width()  # Largeur de l'image représentant une vie
        height = self.life_img.height()  # Hauteur de l'image représentant une vie
        inner_gap = width / 2  # Espace entre les vies

        # Positionnement des vies en haut à gauche
        x = int(canvas.cget("width")) / 2 - (width) * 3 / 2 - inner_gap
        y = height * 3 / 4
        for i in range(self.lifes):  # Affiche chaque vie
            life = canvas.create_image(x, y, image=self.life_img, tags="lifes")
            x += width + inner_gap  # Décalage horizontal pour la prochaine vie

    def move_in(self, canvas, dx):
        """
        Déplace le défenseur sur le canevas.

        Args:
            canvas: Le canevas sur lequel le défenseur sera déplacé
            dx: Le déplacement horizontal du défenseur
        """
        canvas.move(self.id, dx, 0)  # Déplace le défenseur horizontalement

    def fire(self, canvas):
        """
        Permet au défenseur de tirer un projectile, s'il n'a pas atteint le nombre maximal de projectiles.

        Args:
            canvas: Le canevas sur lequel le projectile sera tiré
        """
        if len(self.fired_bullets) < self.max_fired_bullets:  # Vérifie si le nombre de projectiles est en dessous du max
            # Crée un nouveau projectile pour le défenseur
            bullet = Bullet("defender")
            # Installe le projectile sur le canevas
            bullet = bullet.install_in(canvas)
            # Ajoute le projectile à la liste des projectiles tirés
            self.fired_bullets.append(bullet)

    def move_bullet(self, canvas):
        """
        Déplace tous les projectiles tirés par le défenseur sur le canevas.

        Args:
            canvas: Le canevas sur lequel les projectiles seront déplacés
        """
        for i in range(0, len(self.fired_bullets)
                       ):  # Parcourt tous les projectiles tirés
            # Récupère les coordonnées du projectile
            x1, y1, x2, y2 = canvas.bbox(self.fired_bullets[i].id)
            if y1 < 0:  # Si le projectile sort du canevas par le haut
                # Supprime le projectile du canevas
                canvas.delete(self.fired_bullets[i].id)
                del self.fired_bullets[i]  # Supprime le projectile de la liste
                break
            else:
                # Déplace le projectile vers le haut
                self.fired_bullets[i].move_in(canvas)

    def manage_defender_touched_by(self, canvas, fleet):
        """
        Gère le cas où le défenseur est touché par un projectile de la flotte d'aliens.

        Args:
            canvas: Le canevas sur lequel les objets sont gérés
            fleet: L'objet flotte contenant les projectiles d'aliens
        """
        x1, y1, x2, y2 = canvas.bbox(
            self.id)  # Récupère les coordonnées du défenseur
        # Vérifie les objets qui se chevauchent avec le défenseur
        overlapped = canvas.find_overlapping(x1, y1, x2, y2)
        if len(
                overlapped) > 1:  # Si un objet (en dehors du défenseur) chevauche le défenseur
            sortir = False
            for i in range(len(overlapped)):
                for j in range(len(fleet.aliens_fired_bullets)
                               ):  # Parcourt tous les projectiles d'aliens
                    # Si le projectile touche le défenseur
                    if overlapped[i] == fleet.aliens_fired_bullets[j].id:
                        self.lifes -= 1  # Réduit le nombre de vies du défenseur
                        # Applique un effet d'explosion
                        self.touched_by(canvas)
                        # Supprime le projectile de la flotte
                        canvas.delete(fleet.aliens_fired_bullets[j].id)
                        # Supprime le projectile de la liste
                        del fleet.aliens_fired_bullets[j]
                        # Récupère toutes les vies affichées
                        all_lifes = canvas.find_withtag("lifes")
                        # Supprime la dernière vie
                        canvas.delete(all_lifes[-1])
                        sortir = True
                        break
                if sortir:
                    break

    def touched_by(self, canvas):
        """
        Gère l'effet d'explosion lorsque le défenseur est touché.

        Args:
            canvas: Le canevas sur lequel l'effet d'explosion sera affiché
        """
        x, y = canvas.coords(self.id)  # Récupère les coordonnées du défenseur
        self.boom_effect(canvas, x, y)  # Applique l'effet d'explosion

    def boom_effect(self, canvas, x, y):
        """
        Crée un effet d'explosion au niveau des coordonnées spécifiées.

        Args:
            canvas: Le canevas sur lequel l'effet d'explosion sera affiché
            x: Position X de l'explosion
            y: Position Y de l'explosion
        """
        boom = canvas.create_image(
            x, y, image=self.boom, tags="boom")  # Crée l'image de l'explosion
        # Supprime l'explosion après 45ms
        canvas.after(45, canvas.delete, boom)


# ------------- Bullet ---------------#
class Bullet(object):
    """
    Classe représentant un projectile (tiré soit par le défenseur soit par un alien).
    Le projectile peut être déplacé et affiché sur le canevas.
    """

    def __init__(self, shooter):
        """
        Initialisation d'un projectile selon le tireur (défenseur ou alien).

        Args:
            shooter: Indique si le tireur est le défenseur ou un alien ("defender" ou "alien")
        """
        self.shooter = shooter
        self.id = None
        if self.shooter == "defender":  # Si le projectile est tiré par le défenseur
            self.radius = 10  # Rayon du projectile
            self.color = "red"  # Couleur du projectile
            self.speed = 8  # Vitesse de déplacement du projectile
        elif self.shooter == "alien":  # Si le projectile est tiré par un alien
            self.radius = 9  # Rayon du projectile
            self.color = "white"  # Couleur du projectile
            self.speed = 3  # Vitesse de déplacement du projectile

    def install_in(self, canvas):
        """
        Installe un projectile tiré par le défenseur sur le canevas.

        Args:
            canvas: Le canevas où le projectile sera affiché.

        Returns:
            self: Le projectile installé.
        """
        if self.shooter == "defender":  # Si le projectile est tiré par le défenseur
            # Récupère la largeur et hauteur du défenseur
            w, h = Defender().get_width(), Defender().get_height()
            # Récupère les coordonnées du défenseur
            x, y = canvas.coords("defender")
            x, y = x - w / 4, y - h  # Calcule la position du projectile au-dessus du défenseur
            r = self.radius  # Rayon du projectile
            # Crée le projectile sous forme d'ovale
            self.id = canvas.create_oval(x, y, x + r, y + r, fill=self.color)
            return self

    def install_aliens_bullets(self, canvas, x, y):
        """
        Installe un projectile tiré par un alien sur le canevas.

        Args:
            canvas: Le canevas où le projectile sera affiché.
            x, y: Les coordonnées du projectile.

        Returns:
            self: Le projectile installé.
        """
        if self.shooter == "alien":  # Si le projectile est tiré par un alien
            r = self.radius  # Rayon du projectile
            # Crée le projectile sous forme d'ovale
            self.id = canvas.create_oval(x, y, x + r, y + r, fill=self.color)
            # Place le projectile au-dessus des autres éléments
            canvas.tag_raise(self.id)
            return self

    def move_in(self, canvas):
        """
        Déplace le projectile sur le canevas en fonction du tireur.

        Args:
            canvas: Le canevas sur lequel le projectile sera déplacé.
        """
        if self.shooter == "defender":  # Si le projectile est tiré par le défenseur
            # Déplace le projectile vers le haut
            canvas.move(self.id, 0, -self.speed)
        elif self.shooter == "alien":  # Si le projectile est tiré par un alien
            # Déplace le projectile vers le bas
            canvas.move(self.id, 0, self.speed)

# ------------- Score ---------------#


class Score(object):
    """
    Classe représentant le score du joueur, gère les points, le nom du joueur,
    et l'enregistrement du score dans un fichier.
    """

    def __init__(self):
        """
        Initialisation du score avec un nom et un délai de jeu.
        """
        self.name = None  # Nom du joueur
        self.points = 0  # Points du joueur
        self.winning = False  # Indicateur si le joueur a gagné
        self.delai = None  # Délai pour calculer le score
        # Temps de départ pour le calcul du score
        self.start_time = int(time.time())
        # Délai recommandé pour les points (en secondes)
        self.delai_recommended = 2 * 60

    def get_points(self):
        """Retourne les points du joueur."""
        return self.points

    def set_name(self, Nname):
        """Définit le nom du joueur."""
        self.name = Nname

    def refresh_score(self, end_time):
        """
        Met à jour le score du joueur en fonction du temps écoulé.

        Args:
            end_time: Temps de fin du jeu.
        """
        temps = int(end_time)  # Convertit le temps de fin en entier
        if self.delai_recommended - \
                (temps - self.start_time) > 0:  # Si le temps restant est positif
            self.points += self.delai_recommended - \
                (temps - self.start_time)  # Ajoute des points
        else:  # Si le temps est écoulé
            self.points += 10  # Ajoute un bonus de 10 points

    def toFile(self, file):
        """
        Sauvegarde les données du score dans un fichier JSON.

        Args:
            file: Le chemin du fichier où sauvegarder les données.
        """
        f = open(file, "w")  # Ouvre le fichier en mode écriture
        json.dump(self.__dict__, f)  # Sauvegarde l'objet sous forme JSON
        f.close()  # Ferme le fichier

    @classmethod
    def fromFile(cls, file):
        """
        Charge les données du score depuis un fichier JSON.

        Args:
            file: Le chemin du fichier à charger.

        Returns:
            snew: Un objet Score chargé des données du fichier.
        """
        try:
            f = open(file, "r")  # Tente d'ouvrir le fichier en mode lecture
        except FileNotFoundError:  # Si le fichier est introuvable
            print("Fichier introuvable")
            snew = Score()  # Crée un nouveau score par défaut
        else:
            d = json.load(f)  # Charge les données JSON depuis le fichier
            snew = Score()  # Crée un nouvel objet Score
            snew.name = d["name"]  # Assigne le nom du joueur
            snew.points = d["points"]  # Assigne les points du joueur
            snew.delai = d["delai"]  # Assigne le délai
            snew.winning = d["winning"]  # Assigne si le joueur a gagné
            f.close()  # Ferme le fichier
        finally:
            return snew  # Retourne l'objet Score chargé

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères du score.

        Returns:
            str: Représentation sous forme de chaîne du score.
        """
        return str(self.name) + " -> " + \
            str(self.points)  # Affiche le nom et le score

# ------------- Les Resultats ---------------#


class Resultats(object):
    def __init__(self):
        """
        Initialisation de la classe Resultats. Initialise une liste vide pour stocker les scores.
        """
        self.lesResultats = [
        ]  # Liste vide qui contiendra les résultats (scores) du jeu

    def get_resultats(self):
        """
        Retourne la liste des résultats enregistrés.

        Returns:
            list: La liste des résultats (scores).
        """
        return self.lesResultats

    def ajout(self, score):
        """
        Ajoute un score à la liste des résultats.

        Args:
            score: Un objet Score à ajouter à la liste.
        """
        self.lesResultats.append(score)

    def __str__(self):
        """
        Retourne une représentation sous forme de chaîne de caractères de tous les résultats.

        Returns:
            str: Les résultats sous forme de chaîne (affiche chaque score ou "Pas de score enregistré").
        """
        try:
            # Initialise la chaîne avec le premier score
            ch = str(self.lesResultats[0])
            for elt in self.lesResultats[1:]:
                # Ajoute chaque score suivant à la chaîne
                ch = ch + " , " + str(elt)
            return ch
        except IndexError:
            return "Pas de score enregistré"  # Si la liste des résultats est vide

    def toFile(self, file):
        """
        Sauvegarde les résultats dans un fichier JSON.

        Args:
            file: Le chemin du fichier où sauvegarder les résultats.
        """
        f = open(file, "w")  # Ouvre le fichier en mode écriture
        tmp = []  # Liste temporaire pour stocker les scores sous forme de dictionnaires
        for s in self.lesResultats:
            dic = {}  # Dictionnaire pour chaque score
            dic["name"] = s.name
            dic["points"] = s.points
            dic["delai"] = s.delai
            dic["winning"] = s.winning
            tmp.append(dic)  # Ajoute le dictionnaire à la liste temporaire
        json.dump(tmp, f)  # Sauvegarde la liste dans le fichier au format JSON
        f.close()  # Ferme le fichier

    @classmethod
    def fromFile(cls, file):
        """
        Charge les résultats à partir d'un fichier JSON et les transforme en objets Score.

        Args:
            file: Le chemin du fichier à charger.

        Returns:
            Resultats: Un objet Resultats contenant les scores chargés du fichier.
        """
        try:
            f = open(file, "r")  # Ouvre le fichier en mode lecture
        except FileNotFoundError:
            print("Ce fichier n'existe pas")  # Si le fichier n'existe pas
            res = Resultats()  # Crée un objet Resultats vide
            res.lesResultats = []  # Liste vide de résultats
        else:
            tmp = json.load(f)  # Charge les données JSON depuis le fichier
            liste = []  # Liste pour stocker les objets Score
            for d in tmp:
                sc = Score()  # Crée un objet Score
                sc.name = d["name"]
                sc.points = d["points"]
                sc.delai = d["delai"]
                sc.winning = d["winning"]
                liste.append(sc)  # Ajoute chaque score à la liste
            res = Resultats()  # Crée un objet Resultats
            res.lesResultats = liste  # Assigne la liste des scores à l'objet Resultats
            f.close()  # Ferme le fichier
        finally:
            return res  # Retourne l'objet Resultats chargé


toto = SpaceInvaders()
toto.play()
