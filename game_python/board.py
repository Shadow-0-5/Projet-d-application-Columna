import pygame

# Gère le plateau de jeu
# Deplacements + verifications des coups possibles

# NOTE : case de 100 x 100 pixels + 10 de bordures,


class Board:
    def __init__(self, screen: pygame.Surface):
        # une initialisation début de game
        self.screen = screen

        self.dalles = []
        for i in range(6):
            self.dalles.append([])
            for j in range(6):
                self.dalles[i].append(1)

        self.white_pawns = [(2, 0), (2, 3), (0, 5), (5, 4)]
        self.black_pawns = [(0, 1), (3, 2), (3, 5), (5, 0)]
        self.board_image = pygame.image.load("img/board.jpg")
        self.dalle_images = [
            pygame.image.load(f"img/dalle{i}.jpg") for i in range(1, 6)
        ]
        self.black_pawns_image = pygame.image.load("img/pion_noir.png")
        self.white_pawns_image = pygame.image.load("img/pion_blanc.png")

    # une fonction display -> affiche le plateau, dalles et pion
    def display(self):
        self.screen.blit(self.board_image, (0, 0))
        for y in range(len(self.dalles)):
            for x in range(len(self.dalles[y])):
                self.screen.blit(
                    self.dalle_images[self.dalles[y][x]-1], (20 + 100 * x, 20 + 100 * y)
                )
        for i in self.white_pawns:
            self.screen.blit(self.white_pawns_image, (35+100*i[1], 35+100*i[0]))
        for i in self.black_pawns:
            self.screen.blit(self.black_pawns_image, (35+100*i[1], 35+100*i[0]))

    # une sous fonction qui vérifie la possibilité du mouvement
    def available_mouv(sefl):
        pass

    # une fonction qui déplace un pion
    # déplace une pile de dalle
    def mouv_piece(self):
        pass
