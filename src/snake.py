import pygame

# Constantes
CELL_SIZE = 20
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

class Snake:
    def __init__(self):
        self.body = [(10, 10), (9, 10), (8, 10)]  # Positions initiales du serpent
        self.direction = "RIGHT"  # Direction de départ
        self.growing = False

    def move(self):
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
        self.growing = True

    def check_collision(self, width, height):
        head_x, head_y = self.body[0]

        # Collision avec les murs
        if head_x < 0 or head_x >= width or head_y < 0 or head_y >= height:
            return True

        # Collision avec soi-même
        if (head_x, head_y) in self.body[1:]:
            return True

        return False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, GREEN, (segment[0] * CELL_SIZE, segment[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))

    def change_direction(self, new_direction):
        opposite_directions = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        # Empêcher un demi-tour
        if new_direction != opposite_directions.get(self.direction, ""):
            self.direction = new_direction