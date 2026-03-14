# ============================================================
# FICHIER : ai.py
# Projet  : Snake Game
# Auteur  : Aly KONATE
# ============================================================
# Module d'intelligence artificielle pour le serpent.
#
# Implémente une IA gloutonne (greedy) qui dirige le serpent vers
# la nourriture en priorité, tout en évitant les collisions immédiates
# (murs et corps). En cas d'impasse, une direction sûre aléatoire est choisie.
#
# Attributs :
#   - snake       : référence à l'objet Snake courant
#   - food        : référence à l'objet Food courant
#   - grid_width  : largeur de la grille (en cellules)
#   - grid_height : hauteur de la grille (en cellules)
#
# Méthodes :
#   - is_safe_move()  : vérifie si une direction ne mène pas à une collision
#   - get_best_move() : retourne la meilleure direction vers la nourriture
#
# Dépendances :
#   - random (pour le fallback aléatoire)
# ============================================================

import random

class SnakeAI:
    """
    Intelligence artificielle gloutonne pour contrôler le serpent.

    Stratégie :
      1. Calculer la direction vers la nourriture (horizontal, puis vertical).
      2. Filtrer les directions sûres (sans collision immédiate).
      3. Si aucune direction vers la nourriture n'est sûre, choisir une
         direction aléatoire parmi les directions sûres restantes.
      4. En ultime recours (serpent encerclé), retourner "UP" par défaut.
    """

    def __init__(self, snake, food, grid_width, grid_height):
        """
        Initialise l'IA avec les références au serpent, à la nourriture et à la grille.

        :param snake:       instance de Snake à contrôler
        :param food:        instance de Food à cibler
        :param grid_width:  largeur de la grille en cellules
        :param grid_height: hauteur de la grille en cellules
        """
        self.snake = snake
        self.food = food
        self.grid_width = grid_width
        self.grid_height = grid_height

    def is_safe_move(self, direction):
        """
        Vérifie si le mouvement dans la direction donnée est sûr.

        Calcule la position de la prochaine tête et vérifie qu'elle ne sort
        pas de la grille et ne chevauche pas le corps du serpent.

        :param direction: direction à tester ("UP", "DOWN", "LEFT", "RIGHT")
        :return: True si le mouvement est sûr, False sinon
        """
        head_x, head_y = self.snake.body[0]

        if direction == "UP":
            new_head = (head_x, head_y - 1)
        elif direction == "DOWN":
            new_head = (head_x, head_y + 1)
        elif direction == "LEFT":
            new_head = (head_x - 1, head_y)
        elif direction == "RIGHT":
            new_head = (head_x + 1, head_y)
        else:
            return False

        # Vérifier les collisions avec le mur et le corps du serpent
        if (
            new_head in self.snake.body
            or new_head[0] < 0
            or new_head[0] >= self.grid_width
            or new_head[1] < 0
            or new_head[1] >= self.grid_height
        ):
            return False

        return True

    def get_best_move(self):
        """
        Détermine la meilleure direction pour rapprocher le serpent de la nourriture.

        Algorithme glouton :
          - Construit une liste de directions préférées vers la nourriture
            (horizontal en premier, puis vertical).
          - Filtre les directions sûres (is_safe_move).
          - Retourne la première direction sûre vers la nourriture.
          - Si aucune n'est sûre, tire au sort parmi toutes les directions sûres.
          - En dernier recours, retourne "UP".

        :return: direction choisie ("UP", "DOWN", "LEFT", "RIGHT")
        """
        head_x, head_y = self.snake.body[0]
        food_x, food_y = self.food.position

        # Liste des mouvements préférés classés par priorité (vers la nourriture)
        directions = []

        if food_x > head_x:
            directions.append("RIGHT")
        elif food_x < head_x:
            directions.append("LEFT")

        if food_y > head_y:
            directions.append("DOWN")
        elif food_y < head_y:
            directions.append("UP")

        # Filtrer les directions sûres parmi les directions préférées
        safe_moves = [move for move in directions if self.is_safe_move(move)]

        if safe_moves:
            return safe_moves[0]  # Prendre la meilleure direction possible

        # Fallback : choisir une direction aléatoire qui ne tue pas
        all_moves = ["UP", "DOWN", "LEFT", "RIGHT"]
        random.shuffle(all_moves)
        for move in all_moves:
            if self.is_safe_move(move):
                return move

        # Dernier recours : UP (serpent probablement encerclé)
        return "UP"
