# ============================================================
# FICHIER : snake.py
# Projet  : Snake Game
# Auteur  : Aly KONATE
# ============================================================
# Classe représentant le serpent contrôlé par le joueur ou l'IA.
#
# Attributs :
#   - body      : liste de tuples (x, y) représentant les segments
#   - direction : direction actuelle ("UP", "DOWN", "LEFT", "RIGHT")
#   - growing   : flag indiquant si le serpent doit grandir au prochain tick
#
# Méthodes :
#   - move()             : déplace le serpent d'une case selon sa direction
#   - grow()             : active le flag de croissance
#   - check_collision()  : détecte les collisions avec les murs et le corps
#   - draw()             : dessine chaque segment sur l'écran pygame
#   - change_direction() : change la direction en empêchant le demi-tour
#
# Dépendances :
#   - pygame
# ============================================================

import pygame

# Constantes
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Snake:
    """
    Représente le serpent du jeu.

    Le serpent est modélisé comme une liste de tuples (x, y) en coordonnées
    de grille. La tête est toujours body[0]. À chaque tick, le serpent insère
    une nouvelle tête et supprime la queue, sauf si growing == True.
    """

    def __init__(self):
        """
        Initialise le serpent avec 3 segments au centre de la grille.

        Position de départ : (10,10), (9,10), (8,10) — direction initiale : RIGHT.
        """
        self.body = [(10, 10), (9, 10), (8, 10)]  # Positions initiales du serpent
        self.direction = "RIGHT"  # Direction de départ
        self.growing = False

    def move(self):
        """
        Déplace le serpent d'une case dans la direction courante.

        Insère une nouvelle tête en tête de liste et supprime la queue,
        sauf si le flag growing est activé (alors la queue est conservée
        pour simuler la croissance), puis réinitialise growing à False.
        """
        head_x, head_y = self.body[0]

        # Déplacement basé sur la direction
        if self.direction == "UP":
            new_head = (head_x, head_y - 1)
        elif self.direction == "DOWN":
            new_head = (head_x, head_y + 1)
        elif self.direction == "LEFT":
            new_head = (head_x - 1, head_y)
        elif self.direction == "RIGHT":
            new_head = (head_x + 1, head_y)

        self.body.insert(0, new_head)  # Ajouter la nouvelle tête
        if not self.growing:
            self.body.pop()
        self.growing = False

    def grow(self):
        """
        Active le flag de croissance pour le prochain appel à move().

        Appelée lorsque le serpent mange une pomme. Au prochain déplacement,
        la queue ne sera pas supprimée, augmentant ainsi la taille du serpent.
        """
        self.growing = True

    def check_collision(self, width, height):
        """
        Vérifie si la tête du serpent entre en collision avec un mur ou son corps.

        :param width:  largeur de la grille (en cellules)
        :param height: hauteur de la grille (en cellules)
        :return: True si collision détectée (game over), False sinon
        """
        head_x, head_y = self.body[0]

        # Collision avec les murs
        if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
            return True

        # Collision avec soi-même
        if (head_x, head_y) in self.body[1:]:
            return True

        return False

    def draw(self, screen):
        """
        Dessine chaque segment du serpent en vert sur l'écran pygame.

        :param screen: surface pygame sur laquelle dessiner
        """
        for segment in self.body:
            pygame.draw.rect(
                screen,
                GREEN,
                (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )

    def change_direction(self, new_direction):
        """
        Change la direction du serpent en empêchant le demi-tour (180°).

        :param new_direction: nouvelle direction souhaitée ("UP", "DOWN", "LEFT", "RIGHT")

        Si la nouvelle direction est opposée à la direction actuelle, elle est ignorée
        pour éviter que le serpent ne se retourne sur lui-même instantanément.
        """
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        # Empêcher un demi-tour
        if new_direction != opposite_directions.get(self.direction, ""):
            self.direction = new_direction
