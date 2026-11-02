
import pygame

from game import Game

def main():
    try:
        pygame.init()
        Game().run()
    finally:
        pygame.quit()

if __name__ == "__main__":
    main()
