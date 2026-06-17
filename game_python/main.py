# Boucle principale du jeu

# Gère la fenetre pygame + evenements (clic -> vers case choisie)

import threading
import random
import pygame

pygame.init()

from board import Board
from player import Player
from math import floor


class Main:
    def __init__(self):
        self.screen = pygame.display.set_mode((620, 620))
        self.launched = True
        self.clock = pygame.time.Clock()
        self.selected_case = None

        self.board = Board(self.screen)
        self.player_white = Player("white", True, profondeur=1)
        self.player_black = Player("black")

        self.current_player = random.choice([self.player_black, self.player_white])
        self.current_action = "pawn"  # pawn / slab

        self.surface_selected = pygame.Surface((100, 100), pygame.SRCALPHA)
        self.surface_selected.fill((0, 255, 0, 70))

        self.all_moves_possible = self.board.get_all_pawns_move(self.current_player.color)
        self.previous_move = None
        self.previous_stack = None

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.launched = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.current_player and not self.current_player.IA:
                    self.handle_click(*(pygame.mouse.get_pos()))
            


    def handle_click(self, x, y):
        if x < 10 or x > 610 or y < 10 or y > 610: return
        next_case = (floor((y - 10) / 100), floor((x - 10) / 100))
        if not self.selected_case:
            if self.current_action == "pawn":
                if self.current_player.color == "white" and next_case in self.board.white_pawns or self.current_player.color == "black" and next_case in self.board.black_pawns:
                    self.selected_case = next_case

            else:
                if next_case not in self.board.white_pawns and next_case not in self.board.black_pawns and self.board.dalles[next_case[0]][next_case[1]] > 0:
                    self.selected_case = next_case
            
        else:
            if self.board.available_mouv(self.selected_case, next_case, self.current_player.color):
                self.board.move(self.selected_case, next_case)
                if self.current_action == "pawn":
                    self.current_action = "slab"
                    self.previous_move = (self.selected_case, next_case)
                    self.previous_stack = None
                    self.all_moves_possible = self.board.get_all_slabs_stack()
                    if not self.all_moves_possible:
                        print(self.board.get_result())
                        self.current_player = None

                else:
                    self.current_action = "pawn"
                    self.current_player = self.player_white if self.current_player == self.player_black else self.player_black
                    self.previous_stack = (self.selected_case, next_case)
                    self.all_moves_possible = self.board.get_all_pawns_move(self.current_player.color)
                    if not self.all_moves_possible:
                        print(self.board.get_result())
                        self.current_player = None

            self.selected_case = None

    def update(self):
        if self.current_player and self.current_player.IA:
            if not self.current_player.is_calculating:
                if self.current_player.action:
                    self.previous_move, self.previous_stack = self.current_player.action
                    self.board.move(self.previous_move[0], self.previous_move[1])
                    self.all_moves_possible = self.board.get_all_slabs_stack()
                    if not self.all_moves_possible:
                        print(self.board.get_result())
                        self.current_player = None
                        return
                    self.board.move(self.previous_stack[0], self.previous_stack[1])
                    self.current_player.action = None
                    self.current_player = self.player_white if self.current_player == self.player_black else self.player_black
                    self.all_moves_possible = self.board.get_all_pawns_move(self.current_player.color)
                    if not self.all_moves_possible:
                        print(self.board.get_result())
                        self.current_player = None
                    
                else:
                    self.current_player.is_calculating = True
                    thread_bot = threading.Thread(target=self.current_player.take_action, args=(self.board,))
                    thread_bot.start()

    def display(self):
        self.screen.fill("black")
        self.board.display()
        if self.selected_case:
            self.screen.blit(self.surface_selected, (10+100*self.selected_case[1], 10+100*self.selected_case[0]))
            if self.all_moves_possible:
                for move in self.all_moves_possible:
                    if self.selected_case == move[0]:
                        pygame.draw.circle(self.screen, (122,122,122), (move[1][1]*100+60, move[1][0]*100+60), 5)
        
        if self.previous_move:
            pygame.draw.line(self.screen, (0,50,200), (self.previous_move[0][1]*100+60, self.previous_move[0][0]*100+60), (self.previous_move[1][1]*100+60, self.previous_move[1][0]*100+60), 3)
        if self.previous_stack:
            pygame.draw.line(self.screen, (200,50,0), (self.previous_stack[0][1]*100+60, self.previous_stack[0][0]*100+60), (self.previous_stack[1][1]*100+60, self.previous_stack[1][0]*100+60), 3)
        
        pygame.display.flip()

    def run(self):
        print(self.current_player.color)
        while self.launched:
            self.handle_events()
            self.display()
            self.update()
            self.clock.tick(60)


main = Main()
main.run()
pygame.quit()
