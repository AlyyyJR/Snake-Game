# ============================================================
# FICHIER : game.py
# Projet  : Snake Game
# Auteur  : Aly KONATE
# ============================================================
# Classe principale orchestrant la boucle de jeu pygame.
#
# Responsabilités :
#   - Initialiser pygame, la fenêtre et le mixer audio
#   - Gérer les événements clavier (déplacement, IA, musique)
#   - Mettre à jour l'état du jeu (mouvement, collisions, score)
#   - Dessiner la grille, le serpent, la pomme et les overlays de texte
#   - Exécuter la boucle principale à 7 FPS
#
# Constantes :
#   - GRID_WIDTH / GRID_HEIGHT : dimensions de la grille (30×20 cellules)
#   - CELL_SIZE                : taille d'une cellule en pixels (20)
#   - BACKGROUND_COLOR         : couleur de fond (gris clair)
#
# Touches :
#   - ↑ ↓ ← → : déplacer le serpent (mode humain)
#   - A        : basculer entre mode humain et mode IA
#   - M        : mettre en pause / reprendre la musique
#
# Dépendances :
#   - pygame, snake.Snake, food.Food, ai.SnakeAI
# ============================================================

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
    """
    Orchestrateur principal du Snake Game.

    Initialise tous les composants (fenêtre, audio, serpent, nourriture, IA)
    et gère la boucle de jeu pygame : événements → mise à jour → rendu.
    """

    def __init__(self):
        """
        Initialise pygame, la fenêtre, le mixer audio et tous les objets du jeu.

        - Charge et joue en boucle la musique d'ambiance (canary.ogg).
        - Crée un serpent, une pomme et une instance d'IA.
        - Démarre en mode humain (ai_mode = False).
        """
        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("../assets/canary.ogg")  # Charger la musique
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1)  # Jouer en boucle
        self.screen = pygame.display.set_mode((GRID_WIDTH * CELL_SIZE, GRID_HEIGHT * CELL_SIZE))
        pygame.display.set_caption("Snake Game 🐍")
        self.clock = pygame.time.Clock()
        self.running = True

        # Initialisation des entités du jeu
        self.snake = Snake()
        self.food = Food(GRID_WIDTH, GRID_HEIGHT)
        self.score = 0

        # Intelligence artificielle (désactivée par défaut)
        self.ai = SnakeAI(self.snake, self.food, GRID_WIDTH, GRID_HEIGHT)
        self.ai_mode = False  # Mode humain par défaut

    def handle_events(self):
        """
        Gère les événements pygame (fermeture, clavier).

        Événements traités :
          - QUIT           : ferme la fenêtre et arrête la boucle
          - K_UP/DOWN/LEFT/RIGHT : change la direction du serpent (mode humain)
          - K_a            : bascule entre mode humain et mode IA
          - K_m            : pause / reprise de la musique
        """
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
                elif event.key == pygame.K_a:  # Touche "A" : basculer le mode IA
                    self.ai_mode = not self.ai_mode
                    print("Mode IA activé" if self.ai_mode else "Mode Humain activé")
                elif event.key == pygame.K_m:  # Touche "M" : pause/reprise musique
                    if pygame.mixer.music.get_busy():
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()

    def update(self):
        """
        Met à jour l'état du jeu pour chaque tick.

        Séquence :
          1. Si le mode IA est actif, demande à l'IA la meilleure direction.
          2. Déplace le serpent.
          3. Vérifie si la tête est sur la pomme → grow() + relocate() + score++.
          4. Vérifie les collisions mur/corps → arrête la boucle si game over.
        """
        if self.ai_mode:
            self.snake.change_direction(self.ai.get_best_move())

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
        """
        Dessine le quadrillage de la grille en gris foncé sur l'écran.

        Itère sur toutes les cellules et dessine le contour de chaque case.
        """
        for x in range(0, GRID_WIDTH * CELL_SIZE, CELL_SIZE):
            for y in range(0, GRID_HEIGHT * CELL_SIZE, CELL_SIZE):
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(self.screen, (150, 150, 150), rect, 1)

    def draw(self):
        """
        Effectue le rendu complet d'une frame.

        Ordre de dessin :
          1. Remplir le fond (gris clair).
          2. Dessiner le quadrillage.
          3. Dessiner le serpent et la pomme.
          4. Afficher le score et le mode courant (Humain / IA) en overlay.
          5. Rafraîchir l'affichage (flip).
        """
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
        """
        Boucle principale du jeu, cadencée à 7 FPS.

        Exécute en boucle : handle_events → update → draw.
        Arrête pygame proprement à la fin de la partie.
        """
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(7)
        pygame.quit()
