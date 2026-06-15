# Boucle principale du jeu

# Gère la fenetre pygame + evenements (clic -> vers case choisie)

import random
import pygame

pygame.init()

from board import Board
from player import Player


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((620, 620))
        self.launched = True
        self.clock = pygame.time.Clock()
        self.selected_case = None

        self.board = Board(self.screen)
        self.player_white = Player("white")
        self.player_black = Player("black")

        self.current_player = random.choice([self.player_black, self.player_white])
        self.current_action = "pawn"  # pawn / slab

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_click(*(pygame.mouse.get_pos()))

    def handle_click(self, x, y):
        next_case = (round((x - 10) / 100), round((y - 10) / 100))
        if not self.selected_case:
            self.selected_case = next_case
        else:
            if self.board.available_mouv(self.selected_case, next_case):
                self.board.move(self.selected_case, next_case)
                if self.current_action == "pawn":
                    self.current_action = "slab"
                else:
                    self.current_action = "pawn"
                    self.current_player = (
                        self.player_white
                        if self.current_player == self.player_black
                        else self.player_black
                    )
            self.selected_case = None

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
