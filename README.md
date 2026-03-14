# Snake Game

> Jeu Snake classique développé en Python avec **pygame**, incluant un mode IA glouton et une ambiance sonore.

---

## Présentation

Snake Game est une réinterprétation du jeu arcade classique Snake. Le joueur dirige un serpent qui grandit à chaque pomme mangée, et la partie se termine lorsque le serpent heurte un mur ou son propre corps.

Le projet intègre un **mode intelligence artificielle** basculable en cours de jeu : l'IA gloutonne (greedy) dirige automatiquement le serpent vers la nourriture en évitant les collisions immédiates.

---

## Objectifs

- Maîtriser la **boucle de jeu pygame** (init → events → update → render → clock)
- Implémenter la **logique de déplacement** et de **détection de collision**
- Concevoir une **IA greedy** simple mais efficace pour un jeu en grille
- Séparer les responsabilités en plusieurs modules (Snake, Food, AI, Game)
- Intégrer l'audio avec **pygame.mixer**

---

## Stack technique

| Composant       | Technologie        | Rôle                                      |
|-----------------|--------------------|-------------------------------------------|
| Langage         | Python 3.x         | Langage principal                         |
| Moteur graphique| pygame             | Rendu 2D, gestion des événements, audio   |
| IA              | Algorithme glouton | Navigation automatique vers la nourriture |
| Audio           | pygame.mixer       | Lecture de la musique d'ambiance (OGG)    |

---

## Structure du projet

```
Snake-Game/
├── src/
│   ├── main.py          # Point d'entrée — instancie et lance Game
│   ├── game.py          # Boucle principale pygame (events / update / draw)
│   ├── snake.py         # Classe Snake (corps, déplacement, collision, dessin)
│   ├── food.py          # Classe Food (position aléatoire, dessin, relocalisation)
│   └── ai.py            # Classe SnakeAI (algorithme glouton)
├── assets/
│   └── canary.ogg       # Musique d'ambiance jouée en boucle
└── requirements.txt     # Dépendances Python (pygame)
```

---

## Architecture

```
main.py
  └── Game
        ├── Snake          ← corps, direction, collision, dessin
        ├── Food           ← position aléatoire, relocalisation
        └── SnakeAI        ← meilleur coup glouton
              ├── is_safe_move()   → vérifie mur + corps
              └── get_best_move()  → dirige vers la pomme
```

### Flux d'une frame (7 FPS)

```
handle_events()
  ├── QUIT → stop
  ├── ↑↓←→ → snake.change_direction()
  ├── A → basculer ai_mode
  └── M → pause/reprise musique

update()
  ├── [IA] snake.change_direction(ai.get_best_move())
  ├── snake.move()
  ├── collision nourriture → snake.grow() + food.relocate() + score++
  └── collision mur/corps → running = False

draw()
  ├── fond gris + quadrillage
  ├── snake.draw() + food.draw()
  └── overlay : Score + Mode (Humain/IA)
```

---

## Intelligence artificielle

### Stratégie gloutonne

L'IA (`SnakeAI.get_best_move()`) applique l'algorithme suivant à chaque tick :

1. **Directions préférées** : calculer les directions qui rapprochent la tête de la pomme (horizontal, puis vertical).
2. **Filtrage de sécurité** : vérifier avec `is_safe_move()` que la case suivante ne dépasse pas la grille et ne chevauche pas le corps.
3. **Sélection** : prendre la première direction sûre vers la nourriture.
4. **Fallback** : si aucune direction vers la pomme n'est sûre, choisir aléatoirement parmi les directions sûres restantes.
5. **Dernier recours** : retourner `"UP"` si le serpent est entièrement encerclé.

```
Exemple de décision :
  Tête : (10, 8)   Pomme : (14, 5)
  → food_x > head_x  → préfère RIGHT
  → food_y < head_y  → préfère UP
  → is_safe_move("RIGHT") = True  → choisit RIGHT
```

### Limites de l'IA

L'algorithme glouton ne planifie pas à long terme. Il peut s'enfermer dans une impasse si le serpent est très long. Une extension possible serait d'implémenter un **BFS (pathfinding)** pour garantir un chemin jusqu'à la nourriture.

---

## Contrôles

| Touche    | Action                              |
|-----------|-------------------------------------|
| `↑` `↓` `←` `→` | Déplacer le serpent (mode humain) |
| `A`       | Basculer mode Humain ↔ IA           |
| `M`       | Mettre en pause / reprendre la musique |

---

## Installation & lancement

### Prérequis

- Python 3.8+
- pip

### Étapes

```bash
# 1. Cloner le dépôt
git clone https://github.com/alyyyjr/Projet-Github.git
cd Projet-Github/Snake-Game

# 2. Installer les dépendances
pip install -r requirements.txt

# 3. Lancer le jeu depuis le répertoire src/
cd src
python main.py
```

> Le jeu doit être lancé depuis `src/` pour que le chemin `../assets/canary.ogg` soit résolu correctement.

---

## Dépendances

| Package | Version | Rôle                    |
|---------|---------|-------------------------|
| pygame  | ≥ 2.0   | Moteur graphique et audio |

---

## Paramètres configurables

| Constante        | Valeur par défaut | Description                   |
|------------------|-------------------|-------------------------------|
| `GRID_WIDTH`     | 30                | Largeur de la grille (cellules)|
| `GRID_HEIGHT`    | 20                | Hauteur de la grille (cellules)|
| `CELL_SIZE`      | 20 px             | Taille d'une cellule           |
| `clock.tick(7)`  | 7 FPS             | Vitesse du jeu                 |
| `set_volume(0.5)`| 50 %              | Volume de la musique           |

---

## Modules et responsabilités

| Module      | Classe     | Responsabilité principale                            |
|-------------|------------|------------------------------------------------------|
| `snake.py`  | `Snake`    | Corps, direction, déplacement, collision, dessin     |
| `food.py`   | `Food`     | Position aléatoire, dessin, relocalisation hors-corps|
| `ai.py`     | `SnakeAI`  | Algorithme glouton, vérification sécurité            |
| `game.py`   | `Game`     | Boucle pygame, événements, rendu, orchestration      |
| `main.py`   | —          | Point d'entrée                                       |

---

## Auteur

**Aly KONATE** - Projet personnel