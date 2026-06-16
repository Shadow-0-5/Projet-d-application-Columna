# Gère le fonctionnement d'un joueur
# Joue les coups

from board import Board


PROFONDEUR = 1

class Player:
    def __init__(self, color, IA=False):
        self.IA = IA
        self.color = color

    def take_action(self, board):
        _, action = self.tour_max(board, -10000, 10000, PROFONDEUR)
        return action
    

    def tour_max(self, board : Board, alpha, beta, profondeur):
        if profondeur == 0:
            return self.evaluate_position(board)

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
            return self.evaluate_position(board)-20

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

