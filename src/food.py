# ============================================================
# FICHIER : food.py
# Projet  : Snake Game
# Auteur  : Aly KONATE
# ============================================================
# Classe représentant la nourriture (pomme) que le serpent doit manger.
#
# Attributs :
#   - grid_width  : largeur de la grille (en cellules)
#   - grid_height : hauteur de la grille (en cellules)
#   - position    : tuple (x, y) indiquant la position actuelle de la pomme
#
# Méthodes :
#   - generate_position() : génère une position aléatoire dans la grille
#   - draw()              : affiche la pomme sur l'écran pygame
#   - relocate()          : replace la pomme hors du corps du serpent
#
# Dépendances :
#   - pygame, random
# ============================================================

import pygame
import random

# Constantes
CELL_SIZE = 20
RED = (255, 0, 0)

class Food:
    """
    Représente la pomme que le serpent doit manger pour grandir.

    La pomme est placée aléatoirement dans la grille et se déplace à chaque
    fois qu'elle est mangée, en évitant les cases occupées par le serpent.
    """

    def __init__(self, grid_width, grid_height):
        """
        Initialise la nourriture avec une position aléatoire dans la grille.

        :param grid_width:  largeur de la grille en nombre de cellules
        :param grid_height: hauteur de la grille en nombre de cellules
        """
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.generate_position()

    def generate_position(self):
        """
        Génère une position aléatoire dans la grille.

        :return: tuple (x, y) avec x ∈ [0, grid_width-1] et y ∈ [0, grid_height-1]

        Note : cette méthode ne vérifie pas si la case est libre — utiliser
        relocate() pour garantir que la position ne chevauche pas le serpent.
        """
        x = random.randint(0, self.grid_width - 1)
        y = random.randint(0, self.grid_height - 1)
        return (x, y)

    def draw(self, screen):
        """
        Affiche la pomme en rouge sur l'écran pygame.

        :param screen: surface pygame sur laquelle dessiner
        """
        pygame.draw.rect(
            screen,
            RED,
            (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )

    def relocate(self, snake_body):
        """
        Replace la pomme à une position aléatoire non occupée par le serpent.

        Effectue une boucle jusqu'à trouver une case libre (non présente dans
        snake_body). Appelée après chaque consommation de la pomme.

        :param snake_body: liste de tuples (x, y) représentant les segments du serpent
        """
        while True:
            new_position = self.generate_position()
            if new_position not in snake_body:
                self.position = new_position
                break
