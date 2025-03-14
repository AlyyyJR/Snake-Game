import pygame
from snake import Snake
from food import Food
from ai import SnakeAI

# Constantes du jeu
GRID_WIDTH = 30
GRID_HEIGHT = 20
CELL_SIZE = 20
BACKGROUND_COLOR = (200, 200, 200)
WHITE = (255, 255, 255)

class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("../assets/canary.ogg")  # Charger la musique
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Jouer en boucle
        self.screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        pygame.display.set_caption("Snake Game 🐍")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialisation du jeu
        self.snake = Snake()
        self.food = Food(GRID_WIDTH, GRID_HEIGHT)
        self.score = 0

        # Activation/Désactivation de l'IA
        self.ai = SnakeAI(self.snake, self.food, GRID_WIDTH, GRID_HEIGHT)
        self.ai_mode = False  # Mode humain par défaut

    def handle_events(self):
        """Gère les événements clavier pour contrôler le serpent."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.snake.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    self.snake.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    self.snake.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    self.snake.change_direction("RIGHT")
                elif event.key == pygame.K_a:  # Touche "A" pour activer/désactiver l'IA
                    self.ai_mode = not self.ai_mode
                    print("Mode IA activé" if self.ai_mode else "Mode Humain activé")
                elif event.key == pygame.K_m:  # Touche "M" pour gérer la musique
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

    def update(self):
        """Met à jour l'état du jeu (mouvement, collision, score)."""
        if self.ai_mode:
            self.snake.change_direction(self.ai.get_best_move())  # IA - Choix de la meilleure direction

        self.snake.move()

        # Vérification de collision avec la nourriture
        if self.snake.body[0] == self.food.position:
            self.snake.grow()
            self.food.relocate(self.snake.body)
            self.score += 1

        # Vérification de collision avec le mur ou soi-même
        if self.snake.check_collision(GRID_WIDTH, GRID_HEIGHT):
            self.running = False 

    def draw_grid(self):
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (150, 150, 150), rect, 1)

    def draw(self):
        """Dessine l'écran du jeu avec quadrillage."""
        self.screen.fill(BACKGROUND_COLOR)
        self.draw_grid() 
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Affichage du score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Affichage du mode (Humain ou IA)
        mode_text = font.render("Mode: IA" if self.ai_mode else "Mode: Humain", True, WHITE)
        self.screen.blit(mode_text, (10, 40))

        pygame.display.flip()

    def run(self):
        """Boucle principale du jeu."""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(7) 
        pygame.quit()