# Boucle principale du jeu

# Gère la fenetre pygame + evenements (clic -> vers case choisie)

import random
import pygame
pygame.init()

from board import Board
from player import Player

class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((620,620))
        self.launched = True
        self.clock = pygame.time.Clock()

        self.board = Board(self.screen)
        self.player_white = Player("white")
        self.player_black = Player("black")

        self.current_player = random.choice([self.player_black, self.player_white])

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.launched = False

    def display(self):
        self.screen.fill("black")
        self.board.display()
        pygame.display.flip()

    def run(self):
        while self.launched:
            self.handle_events()
            self.display()
            self.clock.tick(60)

    
main = Main()
main.run()
pygame.quit()