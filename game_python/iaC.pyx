from boardC cimport *
cdef extern from "Hungarian.h" nogil:
    cdef cppclass HungarianAlgorithm:
        HungarianAlgorithm() except +
        double SolveStatique(double costMatrix[144])
from libc.math cimport sqrt, trunc
from libc.stdio cimport printf


cdef struct Action:
    Move move
    Move stack

cdef struct Evaluation:
    double value
    Action action


def test(list slabs, list white_pawns, list black_pawns, int color):
    cdef int i, j

    # Convertir les données python -> C
    cdef Board board

    # Dalles
    for i in range(6):
        for j in range(6):
            board.slabs[i][j] = slabs[i][j]

    # Pions
    for i in range(4):
        board.white_pawns[i].y = white_pawns[i][0]
        board.white_pawns[i].x = white_pawns[i][1]
        board.black_pawns[i].y = black_pawns[i][0]
        board.black_pawns[i].x = black_pawns[i][1]
    
    cdef Coords goal
    goal.y = 3
    goal.x = 3
    cdef Coords pos
    cdef int dists
    calcul_dist(&board, goal, &pos, &dists, 0)



def take_action(list slabs, list white_pawns, list black_pawns, int profondeur, int color):
    """Point d'entrée vers les calculs en C"""
    cdef int i, j

    # Convertir les données python -> C
    cdef Board board

    # Dalles
    for i in range(6):
        for j in range(6):
            board.slabs[i][j] = slabs[i][j]

    # Pions
    for i in range(4):
        board.white_pawns[i].y = white_pawns[i][0]
        board.white_pawns[i].x = white_pawns[i][1]
        board.black_pawns[i].y = black_pawns[i][0]
        board.black_pawns[i].x = black_pawns[i][1]
    
    # Calcul en C
    cdef Evaluation result_C
    tour_max(&result_C, &board, -10000, 10000, profondeur, color, True)
    print("\n", result_C.value)
    # On retourne le resultat en python
    move = ((result_C.action.move.start.y, result_C.action.move.start.x), (result_C.action.move.end.y, result_C.action.move.end.x))
    if result_C.action.stack.start.y == -1:
        stack = None
    else:
        stack = ((result_C.action.stack.start.y, result_C.action.stack.start.x), (result_C.action.stack.end.y, result_C.action.stack.end.x))
    final_action = (move, stack)
    
    return final_action


cdef void tour_max(Evaluation *res, Board *board, double alpha, double beta, int profondeur, int my_color, bint progression_bar) noexcept nogil:
    res.value = -999999
    if profondeur == 0:
        res.value = evaluate_pos(board, my_color)
        return 

    cdef Move all_moves_possible[16]
    cdef Move all_stacks_possible[112]
    cdef int len_moves, len_stacks, winner, nb_dalles
    cdef int i, j, k
    cdef Evaluation res_min
    cdef char bar[53]
    if progression_bar:
        bar[52] = '\0'
        bar[0] = '|'
        for i in range(1,51):
            bar[i] = ' '
        bar[51] = '|'
    cdef int indice_bar = 0, tmp
    len_moves = get_all_pawns_move(board, my_color, all_moves_possible)
    if len_moves == 0:
        winner = get_result(board, my_color)
        if winner == my_color:
            res.value = 10000
        else:
            res.value = -10000
        return  

    for i in range(len_moves):
        make_move(board, all_moves_possible[i])
        len_stacks = get_all_slabs_stack(board, all_stacks_possible)
        if len_stacks == 0:
            winner = get_result(board, my_color)
            if winner == my_color:
                res_min.value = 10000
            else:
                res_min.value = -10000
            if res_min.value > res.value:
                res.action.move.start.y = all_moves_possible[i].start.y
                res.action.move.start.x = all_moves_possible[i].start.x
                res.action.move.end.y = all_moves_possible[i].end.y
                res.action.move.end.x = all_moves_possible[i].end.x
                res.action.stack.start.y = -1
                res.value = res_min.value
            if res.value >= beta:
                undo_move(board, all_moves_possible[i], 0)
                return 
            if alpha < res.value:
                alpha = res.value
            undo_move(board, all_moves_possible[i], 0)
        else:
            for j in range(len_stacks):
                if progression_bar:
                    tmp = <int>trunc(50/len_moves * (i+(j+1)/len_stacks))
                    if indice_bar < tmp:
                        for k in range(indice_bar, tmp):
                            bar[k] = '-'
                        indice_bar = tmp
                    printf("\r%s",bar)

                nb_dalles = make_move(board, all_stacks_possible[j])
                tour_min(&res_min, board, alpha, beta, profondeur-1, my_color)
                undo_move(board, all_stacks_possible[j], nb_dalles)
                if res_min.value > res.value:
                    res.action.move.start.y = all_moves_possible[i].start.y
                    res.action.move.start.x = all_moves_possible[i].start.x
                    res.action.move.end.y = all_moves_possible[i].end.y
                    res.action.move.end.x = all_moves_possible[i].end.x
                    res.action.stack.start.y = all_stacks_possible[j].start.y
                    res.action.stack.start.x = all_stacks_possible[j].start.x
                    res.action.stack.end.y = all_stacks_possible[j].end.y
                    res.action.stack.end.x = all_stacks_possible[j].end.x
                    res.value = res_min.value
                if res.value >= beta:   
                    undo_move(board, all_moves_possible[i], 0)
                    return
                if alpha < res.value:
                    alpha = res.value
            undo_move(board, all_moves_possible[i], 0)
    return

cdef void tour_min(Evaluation *res, Board *board, double alpha, double beta, int profondeur, int my_color) noexcept nogil:
    cdef int opp_color = 0 if my_color == 1 else 1
    res.value = 999999
    if profondeur == 0:
        res.value = evaluate_pos(board, my_color)-20
        return 

    cdef Move all_moves_possible[16]
    cdef Move all_stacks_possible[112]
    cdef int len_moves, len_stacks, winner, nb_dalles
    cdef int i, j
    cdef Evaluation res_max
    len_moves = get_all_pawns_move(board, opp_color, all_moves_possible)
    if len_moves == 0:
        winner = get_result(board, opp_color)
        if winner == my_color:
            res.value = 10000
        else:
            res.value = -10000
        return

    for i in range(len_moves):
        make_move(board, all_moves_possible[i])
        len_stacks = get_all_slabs_stack(board, all_stacks_possible)
        if len_stacks == 0:
            winner = get_result(board, opp_color)
            if winner == my_color:
                res_max.value = 10000
            else:
                res_max.value = -10000
            if res_max.value < res.value:
                res.action.move.start.y = all_moves_possible[i].start.y
                res.action.move.start.x = all_moves_possible[i].start.x
                res.action.move.end.y = all_moves_possible[i].end.y
                res.action.move.end.x = all_moves_possible[i].end.x
                res.value = res_max.value
            if res.value <= alpha:
                undo_move(board, all_moves_possible[i], 0)
                return 
            if beta > res.value:
                beta = res.value
            undo_move(board, all_moves_possible[i], 0)
        else:
            for j in range(len_stacks):
                nb_dalles = make_move(board, all_stacks_possible[j])
                tour_max(&res_max, board, alpha, beta, profondeur-1, my_color, False)
                undo_move(board, all_stacks_possible[j], nb_dalles)
                if res_max.value < res.value:
                    res.action.move.start.y = all_moves_possible[i].start.y
                    res.action.move.start.x = all_moves_possible[i].start.x
                    res.action.move.end.y = all_moves_possible[i].end.y
                    res.action.move.end.x = all_moves_possible[i].end.x
                    res.action.stack.start.y = all_stacks_possible[j].start.y
                    res.action.stack.start.x = all_stacks_possible[j].start.x
                    res.action.stack.end.y = all_stacks_possible[j].end.y
                    res.action.stack.end.x = all_stacks_possible[j].end.x
                    res.value = res_max.value
                if res.value <= alpha:
                    undo_move(board, all_moves_possible[i], 0)
                    return
                if beta > res.value:
                    beta = res.value
            undo_move(board, all_moves_possible[i], 0)
    return


# distance :  |   0   |   1   |   2   |   3   |   4+

# tour de 5 : |  55   |  36   |  15   |   10  |   0    
# tour de 4 : |  18   |  12   |   6   |   2   |   0
# tour de 3 : |   6   |   3   |   1   |   0   |   0   
# tour de 2 : |   2   |   1   |   0   |   0   |   0

cdef double evaluate_pos(Board *board, int color) noexcept nogil:
    cdef double white_points[144]
    cdef double black_points[144]
    cdef double score=0.0
    cdef int i, y, x, tower_size
    cdef Coords pos
    cdef int dists[8]
    cdef Coords all_pawns[8]
    cdef HungarianAlgorithm HungAlgo
    for i in range(4):
        all_pawns[i] = board.white_pawns[i]
        all_pawns[i+4] = board.black_pawns[i]

    for y in range(6):
        for x in range(6):
            tower_size = board.slabs[y][x]
            if tower_size <= 1: 
                for i in range(4):
                    white_points[i + 4 *(y*6+x)] = 0
                    black_points[i + 4 *(y*6+x)] = 0
                continue
            pos.y = y
            pos.x = x

            calcul_dist(board, pos, all_pawns, dists, 8)
            for i in range(4):
                if dists[i] < 0 or dists[i] >= 4:
                    white_points[i + 4 *(y*6+x)] = 0
                
                elif dists[i] == 3:
                    if tower_size == 5:
                        white_points[i + 4 *(y*6+x)] = 10
                    elif tower_size == 4:
                        white_points[i + 4 *(y*6+x)] = 2
                    else:
                        white_points[i + 4 *(y*6+x)] = 0
                
                elif dists[i] == 2:
                    if tower_size == 5:
                        white_points[i + 4 *(y*6+x)] = 15
                    elif tower_size == 4:
                        white_points[i + 4 *(y*6+x)] = 6
                    elif tower_size == 3:
                        white_points[i + 4 *(y*6+x)] = 1
                    else:
                        white_points[i + 4 *(y*6+x)] = 0

                elif dists[i] == 1:
                    if tower_size == 5:
                        white_points[i + 4 *(y*6+x)] = 36
                    elif tower_size == 4:
                        white_points[i + 4 *(y*6+x)] = 12
                    elif tower_size == 3:
                        white_points[i + 4 *(y*6+x)] = 3
                    else:
                        white_points[i + 4 *(y*6+x)] = 1
                    
                else:
                    if tower_size == 5:
                        white_points[i + 4 *(y*6+x)] = 55
                    elif tower_size == 4:
                        white_points[i + 4 *(y*6+x)] = 18
                    elif tower_size == 3:
                        white_points[i + 4 *(y*6+x)] = 6
                    else:
                        white_points[i + 4 *(y*6+x)] = 2
                if dists[i+4] < 0 or dists[i+4] >= 4:
                    black_points[i + 4 *(y*6+x)] = 0
                
                elif dists[i+4] == 3:
                    if tower_size == 5:
                        black_points[i + 4 *(y*6+x)] = 10
                    elif tower_size == 4:
                        black_points[i + 4 *(y*6+x)] = 2
                    else:
                        black_points[i + 4 *(y*6+x)] = 0
                
                elif dists[i+4] == 2:
                    if tower_size == 5:
                        black_points[i + 4 *(y*6+x)] = 15
                    elif tower_size == 4:
                        black_points[i + 4 *(y*6+x)] = 6
                    elif tower_size == 3:
                        black_points[i + 4 *(y*6+x)] = 1
                    else:
                        black_points[i + 4 *(y*6+x)] = 0

                elif dists[i+4] == 1:
                    if tower_size == 5:
                        black_points[i + 4 *(y*6+x)] = 36
                    elif tower_size == 4:
                        black_points[i + 4 *(y*6+x)] = 12
                    elif tower_size == 3:
                        black_points[i + 4 *(y*6+x)] = 3
                    else:
                        black_points[i + 4 *(y*6+x)] = 1
                    
                else:
                    if tower_size == 5:
                        black_points[i + 4 *(y*6+x)] = 55
                    elif tower_size == 4:
                        black_points[i + 4 *(y*6+x)] = 18
                    elif tower_size == 3:
                        black_points[i + 4 *(y*6+x)] = 6
                    else:
                        black_points[i + 4 *(y*6+x)] = 2


    score += HungAlgo.SolveStatique(white_points)
    score -= HungAlgo.SolveStatique(black_points)
    cdef double mobility = 0
    for i in range(4):
        mobility += sqrt(CalculMobility(board, board.white_pawns[i], 0.5))
        mobility -= sqrt(CalculMobility(board, board.black_pawns[i], 0.5))
    mobility = 50*mobility
    score += mobility
    if color == 1:
        score = -score
    return score

