# Gère le fonctionnement d'un joueur
# Joue les coups

from board import Board


PROFONDEUR = 1

# distance :  |   0   |   1   |   2   |   3   |   4+

# tour de 5 : |  55   |  36   |  15   |   10  |   0    
# tour de 4 : |  18   |  12   |   6   |   2   |   0
# tour de 3 : |   6   |   3   |   1   |   0   |   0   
# tour de 2 : |   2   |   1   |   0   |   0   |   0

POINTS_T5_D0 = 55
POINTS_T5_D1 = 36
POINTS_T5_D2 = 15
POINTS_T5_D3 = 10

POINTS_T4_D0 = 18
POINTS_T4_D1 = 12
POINTS_T4_D2 = 6
POINTS_T4_D3 = 2

POINTS_T3_D0 = 6
POINTS_T3_D1 = 3
POINTS_T3_D2 = 1
POINTS_T3_D3 = 0

POINTS_T2_D0 = 2
POINTS_T2_D1 = 1
POINTS_T2_D2 = 0
POINTS_T2_D3 = 0

class Player:
    def __init__(self, color, IA=False):
        self.IA = IA
        self.color = color

    def take_action(self, board):
        _, action = self.tour_max(board, -10000, 10000, PROFONDEUR)
        return action
    

    def tour_max(self, board : Board, alpha, beta, profondeur):
        if profondeur == 0:
            return (self.evaluate_position(board), None)

        all_moves_possible = board.get_all_pawns_move(self.color)
        u = None
        a = None
        for move in all_moves_possible:
            vboard = board.copy()
            vboard.move(move[0], move[1])
            all_stacks_possible = vboard.get_all_slabs_stack()
            for stack in all_stacks_possible:
                vvboard = vboard.copy()
                vvboard.move(stack[0], stack[1])
                u_min, _ = self.tour_min(vvboard, alpha, beta, profondeur-1)
                if not u or u_min > u:
                    a = (move, stack)
                    u = u_min
                if u >= beta:
                    return (u, a)
                alpha = max(alpha, u)
        return (u, a)




    def tour_min(self, board : Board, alpha, beta, profondeur):
        if profondeur == 0:
            return (self.evaluate_position(board)-20, None)

        color = "white" if self.color == "black" else "black"
        all_moves_possible = board.get_all_pawns_move(color)
        u = None
        a = None
        for move in all_moves_possible:
            vboard = board.copy()
            vboard.move(move[0], move[1])
            all_stacks_possible = vboard.get_all_slabs_stack()
            for stack in all_stacks_possible:
                vvboard = vboard.copy()
                vvboard.move(stack[0], stack[1])
                u_max, _ = self.tour_max(vvboard, alpha, beta, profondeur-1)
                if not u or u_max < u:
                    a = (move, stack)
                    u = u_max
                if u <= alpha:
                    return (u, a)
                beta = min(beta, u)
        return (u, a)

    def evaluate_position(self, board : Board):
        score = 0
        tour5 = []
        tour4 = []
        tour3 = []
        tour2 = []

        factor = 1 if self.color == "white" else -1

        for y in range(6):
            for x in range(6):
                if board.dalles[y][x] == 5 and (y, x) not in board.black_pawns and (y, x) not in board.white_pawns:
                    tour5.append((y, x))
                elif board.dalles[y][x] == 4 and (y, x) not in board.black_pawns and (y, x) not in board.white_pawns:
                    tour4.append((y, x))
                elif board.dalles[y][x] == 3 and (y, x) not in board.black_pawns and (y, x) not in board.white_pawns:
                    tour3.append((y, x))
                elif board.dalles[y][x] == 2 and (y, x) not in board.black_pawns and (y, x) not in board.white_pawns:
                    tour2.append((y, x))
        for liste in [board.white_pawns, board.black_pawns]:
            for pawn in liste:
                if board.dalles[pawn[0]][pawn[1]] == 5:
                    score += factor * POINTS_T5_D0

                elif board.dalles[pawn[0]][pawn[1]] == 4:
                    score += factor * POINTS_T4_D0
                    dist_min = None
                    for tour in tour5:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist_min or dist < dist_min):
                            dist_min = dist
                    if dist_min == 1:
                        score += factor * POINTS_T5_D1
                    elif dist_min == 2:
                        score += factor * POINTS_T5_D2
                    elif dist_min == 3:
                        score += factor * POINTS_T5_D3
                
                elif board.dalles[pawn[0]][pawn[1]] == 3:
                    score += factor * POINTS_T3_D0
                    dist5_min = None
                    dist4_min = None
                    for tour in tour5:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist5_min or dist < dist5_min):
                            dist5_min = dist
                    for tour in tour4:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist4_min or dist < dist4_min):
                            dist4_min = dist
                    if dist5_min == 1:
                        score += factor * POINTS_T5_D1
                    elif dist5_min == 2:
                        if dist4_min == 1:
                            score += factor * max(POINTS_T5_D2, POINTS_T4_D1)
                        else:
                            score += factor * POINTS_T5_D2
                    elif dist5_min == 3:
                        if dist4_min == 1:
                            score += factor * max(POINTS_T4_D1, POINTS_T5_D3)
                        elif dist4_min == 2:
                            score += factor * max(POINTS_T4_D2, POINTS_T5_D3)
                        else:
                            score += factor * POINTS_T5_D3
                    else:
                        if dist4_min == 1:
                            score += factor * POINTS_T4_D1
                        elif dist4_min == 2:
                            score += factor * POINTS_T4_D2
                        elif dist4_min == 3:
                            score += factor * POINTS_T4_D3
                
                elif board.dalles[pawn[0]][pawn[1]] == 2:
                    score += factor * POINTS_T2_D0
                    dist5_min = None
                    dist4_min = None
                    dist3_min = None
                    for tour in tour5:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist5_min or dist < dist5_min):
                            dist5_min = dist
                    for tour in tour4:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist4_min or dist < dist4_min):
                            dist4_min = dist
                    for tour in tour3:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist3_min or dist < dist3_min):
                            dist3_min = dist

                    if dist5_min == 1:
                        score += factor * POINTS_T5_D1
                    elif dist5_min == 2:
                        if dist4_min == 1:
                            score += factor * max(POINTS_T5_D2, POINTS_T4_D1)
                        else:
                            score += factor * POINTS_T5_D2
                    elif dist5_min == 3:
                        if dist4_min == 1:
                            score += factor * max(POINTS_T4_D1, POINTS_T5_D3)
                        elif dist4_min == 2:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T4_D2, POINTS_T5_D3)
                            else:
                                score += factor * max(POINTS_T4_D2, POINTS_T5_D3)
                        else:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T5_D3)
                            else:
                                score += factor * POINTS_T5_D3
                    else:
                        if dist4_min == 1:
                            score += factor * POINTS_T4_D1
                        elif dist4_min == 2:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T4_D2)
                            else:
                                score += factor * POINTS_T4_D2
                        elif dist4_min == 3:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T4_D3)
                            elif dist3_min == 2:
                                score += factor * max(POINTS_T3_D2, POINTS_T4_D3)
                            else:
                                score += factor * POINTS_T4_D3
                        else:
                            if dist3_min == 1:
                                score += factor * POINTS_T3_D1
                            elif dist3_min == 2:
                                score += factor * POINTS_T3_D2
                            elif dist3_min == 3:
                                score += factor * POINTS_T3_D3
                
                elif board.dalles[pawn[0]][pawn[1]] == 1:
                    dist5_min = None
                    dist4_min = None
                    dist3_min = None
                    dist2_min = None
                    for tour in tour5:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist5_min or dist < dist5_min):
                            dist5_min = dist
                    for tour in tour4:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist4_min or dist < dist4_min):
                            dist4_min = dist
                    for tour in tour3:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist3_min or dist < dist3_min):
                            dist3_min = dist
                    for tour in tour2:
                        dist = board.A_Star(pawn, tour)
                        if dist > 0 and (not dist2_min or dist < dist2_min):
                            dist2_min = dist

                    if dist5_min == 1:
                        score += factor * POINTS_T5_D1
                    elif dist5_min == 2:
                        if dist4_min == 1:
                            score += factor * max(POINTS_T5_D2, POINTS_T4_D1)
                        else:
                            score += factor * POINTS_T5_D2
                    elif dist5_min == 3:
                        if dist4_min == 1:
                            score += factor * max(POINTS_T4_D1, POINTS_T5_D3)
                        elif dist4_min == 2:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T4_D2, POINTS_T5_D3)
                            else:
                                score += factor * max(POINTS_T4_D2, POINTS_T5_D3)
                        else:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T5_D3)
                            elif dist3_min == 2:
                                if dist2_min == 1:
                                    score += factor * max(POINTS_T2_D1, POINTS_T3_D2, POINTS_T5_D3)
                                else:
                                    score += factor * max(POINTS_T3_D2, POINTS_T5_D3)
                            else:
                                if dist2_min == 1:
                                    score += factor * max(POINTS_T2_D1, POINTS_T5_D3)
                                elif dist2_min == 2:
                                    score += factor * max(POINTS_T2_D2, POINTS_T5_D3)
                                else:
                                    score += factor * POINTS_T5_D3
                    else:
                        if dist4_min == 1:
                            score += factor * POINTS_T4_D1
                        elif dist4_min == 2:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T4_D2)
                            else:
                                score += factor * POINTS_T4_D2
                        elif dist4_min == 3:
                            if dist3_min == 1:
                                score += factor * max(POINTS_T3_D1, POINTS_T4_D2)
                            elif dist3_min == 2:
                                if dist2_min == 1:
                                    score += factor * max(POINTS_T2_D1, POINTS_T3_D2, POINTS_T4_D3)
                                else:
                                    score += factor * max(POINTS_T3_D2, POINTS_T4_D3)
                            else:
                                if dist2_min == 1:
                                    score += factor * max(POINTS_T2_D1, POINTS_T4_D3)
                                elif dist2_min == 2:
                                    score += factor * max(POINTS_T2_D2, POINTS_T4_D3)
                                else:
                                    score += factor * POINTS_T4_D2
                        else:
                            if dist3_min == 1:
                                score += factor * POINTS_T3_D1
                            elif dist3_min == 2:
                                if dist2_min == 1:
                                    score += factor * max(POINTS_T3_D2, POINTS_T2_D1)
                                else:
                                    score += factor * POINTS_T3_D2
                            elif dist3_min == 3:
                                if dist2_min == 1:
                                    score += factor * max(POINTS_T3_D3, POINTS_T2_D1)
                                elif dist2_min == 2:
                                    score += factor * max(POINTS_T3_D3, POINTS_T2_D2)
                                else:
                                    score += factor * POINTS_T3_D3
                            else:
                                if dist2_min == 1:
                                    score += factor * POINTS_T2_D1
                                elif dist2_min == 2:
                                    score += factor * POINTS_T2_D2
                                elif dist2_min == 3:
                                    score += factor * POINTS_T2_D3
            factor *= -1
        return score

