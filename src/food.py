import pygame
import random

# Constantes
CELL_SIZE = 20
RED = (255, 0, 0)

class Food:
    def __init__(self, grid_width, grid_height):
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.position = self.generate_position()

    def generate_position(self):
        """Génère une position aléatoire pour la pomme."""
        x = random.randint(0, self.grid_width - 1)
        y = random.randint(0, self.grid_height - 1)
        return (x, y)

    def draw(self, screen):
        """Affiche la pomme sur l'écran."""
        pygame.draw.rect(screen, RED, (self.position[0] * CELL_SIZE, self.position[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def relocate(self, snake_body):
        """Relocalise la pomme si elle apparaît sur le serpent."""
        while True:
            new_position = self.generate_position()
            if new_position not in snake_body:
                self.position = new_position
                break