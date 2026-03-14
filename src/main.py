# ============================================================
# FICHIER : main.py
# Projet  : Snake Game
# Auteur  : Aly KONATE
# ============================================================
# Point d'entrée du programme.
#
# Instancie la classe Game et lance la boucle principale via game.run().
# Ce fichier doit être exécuté depuis le répertoire src/ afin que les
# imports relatifs (snake, food, ai) et le chemin audio (../assets/)
# soient résolus correctement.
#
# Lancement :
#   cd src && python main.py
# ============================================================

from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()
