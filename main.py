import pygame
from setting import *
from scenes.menu import Menu
from run_game import run_game
from scenes.credits_screen import CreditsScreen

def main():
    pygame.init()

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    pygame.display.set_caption(TITLE)
    
    credits = CreditsScreen(screen)
    menu = Menu(screen)

    running = True

    while running:
        option = menu.run()

        if option == "start":
            result = run_game(screen)

            if result == "exit":
                running = False

        elif option == "settings":
            print("Configurações ainda não implementadas")

        elif option == "credits":
            credits.run()

        elif option == "exit":
            running = False

    pygame.quit()


if __name__ == "__main__":
    main()