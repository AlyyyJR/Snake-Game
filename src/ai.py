import random

class SnakeAI:
    def __init__(self, snake, food, grid_width, grid_height):
        self.snake = snake
        self.food = food
        self.grid_width = grid_width
        self.grid_height = grid_height

    def is_safe_move(self, direction):
        """Vérifie si un mouvement ne mène pas à une collision."""
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
        if (new_head in self.snake.body) or (new_head[0] < 0 or new_head[0] >= self.grid_width) or (new_head[1] < 0 or new_head[1] >= self.grid_height):
            return False 
        
        return True

    def get_best_move(self):
        """Détermine le meilleur mouvement en évitant les collisions."""
        head_x, head_y = self.snake.body[0]
        food_x, food_y = self.food.position

        # Liste des mouvements possibles classés par priorité
        directions = []
        
        if food_x > head_x:
            directions.append("RIGHT")
        elif food_x < head_x:
            directions.append("LEFT")

        if food_y > head_y:
            directions.append("DOWN")
        elif food_y < head_y:
            directions.append("UP")

        # Vérifier si ces directions sont sûres, sinon choisir une autre
        safe_moves = [move for move in directions if self.is_safe_move(move)]

        if safe_moves:
            return safe_moves[0]  # Prendre la meilleure direction possible
        
        # Si aucune direction n’est sûre, choisir une direction aléatoire qui ne tue pas
        all_moves = ["UP", "DOWN", "LEFT", "RIGHT"]
        random.shuffle(all_moves) 
        for move in all_moves:
            if self.is_safe_move(move):
                return move
        
        return "UP" 