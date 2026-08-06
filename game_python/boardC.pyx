from libc.math cimport sqrt
from libc.stdio cimport printf

cdef int is_in_white(Board *board, Coords pos) noexcept nogil:
    cdef int i
    for i in range(4):
        if board.white_pawns[i].y == pos.y and board.white_pawns[i].x == pos.x:
            return 1
    return 0

cdef int is_in_black(Board *board, Coords pos) noexcept nogil:
    cdef int i
    for i in range(4):
        if board.black_pawns[i].y == pos.y and board.black_pawns[i].x == pos.x:
            return 1
    return 0

cdef int is_pawn(Board *board, Coords pos) noexcept nogil:
    cdef int i
    for i in range(4):
        if board.white_pawns[i].y == pos.y and board.white_pawns[i].x == pos.x or board.black_pawns[i].y == pos.y and board.black_pawns[i].x == pos.x:
            return 1
    return 0

cdef int make_move(Board *board, Move move) noexcept nogil:
    """Effectue le mouvement sur le plateau\n
    Retourne le nombre de dalles deplacées"""
    cdef int i, nb_dalles
    for i in range(4):
        if board.white_pawns[i].y == move.start.y and board.white_pawns[i].x == move.start.x:
            board.white_pawns[i].y = move.end.y
            board.white_pawns[i].x = move.end.x
            return 0
        if board.black_pawns[i].y == move.start.y and board.black_pawns[i].x == move.start.x:
            board.black_pawns[i].y = move.end.y
            board.black_pawns[i].x = move.end.x
            return 0

    nb_dalles = board.slabs[move.start.y][move.start.x]
    board.slabs[move.end.y][move.end.x] += nb_dalles
    board.slabs[move.start.y][move.start.x] = 0
    return nb_dalles

cdef void undo_move(Board *board, Move move, int nb_dalles) noexcept nogil:
    """Annule le mouvement du plateau"""
    cdef int i
    if nb_dalles == 0:
        for i in range(4):
            if board.white_pawns[i].y == move.end.y and board.white_pawns[i].x == move.end.x:
                board.white_pawns[i].y = move.start.y
                board.white_pawns[i].x = move.start.x
                return 
            if board.black_pawns[i].y == move.end.y and board.black_pawns[i].x == move.end.x:
                board.black_pawns[i].y = move.start.y
                board.black_pawns[i].x = move.start.x
                return 
    else:
        board.slabs[move.end.y][move.end.x] -= nb_dalles
        board.slabs[move.start.y][move.start.x] = nb_dalles

cdef int get_all_pawns_move(Board *board, int color, Move all_moves[16]) noexcept nogil:
    """Ecrit tous les coups de pions possibles dans la liste 'all_moves'\n
    Retourne le nombre de coups trouvés"""
    cdef int i, offset = 0
    if color == 0:
        for i in range(4):
            offset += get_one_pawn_move(board, board.white_pawns[i], all_moves+offset)
    else:
        for i in range(4):
            offset += get_one_pawn_move(board, board.black_pawns[i], all_moves+offset)
    return offset

cdef int get_one_pawn_move(Board *board, Coords pawn, Move all_moves[4]) noexcept nogil:
    """Ecrit tous les coups du pion possibles dans la liste 'all_moves'\n
    Retourne le nombre de coups trouvés"""
    # deplacement a droite
    cdef int i, offset = 0
    cdef Coords pos
    for i in range(pawn.x+1, 6):
        if board.slabs[pawn.y][i] != 0:
            pos.y = pawn.y
            pos.x = i
            if not is_pawn(board, pos):
                all_moves[offset].start.y = pawn.y
                all_moves[offset].start.x = pawn.x
                all_moves[offset].end.y = pawn.y
                all_moves[offset].end.x = i
                offset += 1
            break
    # deplacement a gauche
    for i in range(pawn.x-1, -1, -1):
        if board.slabs[pawn.y][i] != 0:
            pos.y = pawn.y
            pos.x = i
            if not is_pawn(board, pos):
                all_moves[offset].start.y = pawn.y
                all_moves[offset].start.x = pawn.x
                all_moves[offset].end.y = pawn.y
                all_moves[offset].end.x = i
                offset += 1
            break
    # deplacement en bas
    for i in range(pawn.y+1, 6):
        if board.slabs[i][pawn.x] != 0:
            pos.y = i
            pos.x = pawn.x
            if not is_pawn(board, pos):
                all_moves[offset].start.y = pawn.y
                all_moves[offset].start.x = pawn.x
                all_moves[offset].end.y = i
                all_moves[offset].end.x = pawn.x
                offset += 1
            break
    # deplacement en haut
    for i in range(pawn.y-1, -1, -1):
        if board.slabs[i][pawn.x] != 0:
            pos.y = i
            pos.x = pawn.x
            if not is_pawn(board, pos):
                all_moves[offset].start.y = pawn.y
                all_moves[offset].start.x = pawn.x
                all_moves[offset].end.y = i
                all_moves[offset].end.x = pawn.x
                offset += 1
            break
            
    return offset

cdef int get_all_slabs_stack(Board *board, Move all_moves[112]) noexcept nogil:
    """Ecrit tous les coups de dalles possibles dans la liste 'all_moves'\n
    Retourne le nombre de coups trouvés"""
    cdef int y, x, nb_dalles, offset=0
    cdef Coords pos
    for y in range(6):
        for x in range(6):
            pos.y = y
            pos.x = x
            if board.slabs[y][x] == 0 or is_pawn(board, pos): continue
            nb_dalles = board.slabs[y][x]
            # deplacement a doite
            for i in range(x+1, 6):
                if board.slabs[y][i] != 0:
                    pos.y = y
                    pos.x = i
                    if not is_pawn(board, pos) and nb_dalles + board.slabs[y][i] <= 5:
                        all_moves[offset].start.y = y
                        all_moves[offset].start.x = x
                        all_moves[offset].end.y = y
                        all_moves[offset].end.x = i
                        offset += 1
                    break
            # deplacement a gauche
            for i in range(x-1, -1, -1):
                if board.slabs[y][i] != 0:
                    pos.y = y
                    pos.x = i
                    if not is_pawn(board, pos) and nb_dalles + board.slabs[y][i] <= 5:
                        all_moves[offset].start.y = y
                        all_moves[offset].start.x = x
                        all_moves[offset].end.y = y
                        all_moves[offset].end.x = i
                        offset += 1
                    break
            # deplacement en bas
            for i in range(y+1, 6):
                if board.slabs[i][x] != 0:
                    pos.y = i
                    pos.x = x
                    if not is_pawn(board, pos) and nb_dalles + board.slabs[i][x] <= 5:
                        all_moves[offset].start.y = y
                        all_moves[offset].start.x = x
                        all_moves[offset].end.y = i
                        all_moves[offset].end.x = x
                        offset += 1
                    break
            # deplacement en haut
            for i in range(y-1, -1, -1):
                if board.slabs[i][x] != 0:
                    pos.y = i
                    pos.x = x
                    if not is_pawn(board, pos) and nb_dalles + board.slabs[i][x] <= 5:
                        all_moves[offset].start.y = y
                        all_moves[offset].start.x = x
                        all_moves[offset].end.y = i
                        all_moves[offset].end.x = x
                        offset += 1
                    break
    return offset

cdef int get_result(Board *board, int color_turn) noexcept nogil:
    """Retourne la couleur du gagnant (0 ou 1)"""
    cdef int current_white_stack = 0 
    cdef int current_black_stack = 0
    cdef int i, j

    for i in range(5,1, -1):
        for j in range(4):
            if board.slabs[board.white_pawns[j].y][board.white_pawns[j].x] == i: 
                current_white_stack += 1 
            if board.slabs[board.black_pawns[j].y][board.black_pawns[j].x] == i: 
                current_black_stack += 1

        if current_white_stack == current_black_stack: 
            current_white_stack = 0 
            current_black_stack = 0
            continue
        elif current_black_stack > current_white_stack : 
            return 1
        
        return 0
    
    return 1 if color_turn == 0 else 0

cdef int get_voisins(Board *board, Coords pos, Coords all_neighbours[4]) noexcept nogil:
    """Ecrit tous les voisins de la case 'pos' dans la liste 'all_neighbours'\n
    Retourne le nombre de voisins trouvés"""
    cdef int i, offset=0

    # Droite
    for i in range(pos.x + 1, 6):
        if board.slabs[pos.y][i] != 0:
            all_neighbours[offset].y = pos.y
            all_neighbours[offset].x = i
            offset += 1
            break  
    # Gauche
    for i in range(pos.x - 1, -1, -1):
        if board.slabs[pos.y][i] != 0:
            all_neighbours[offset].y = pos.y
            all_neighbours[offset].x = i
            offset += 1
            break  
    # Bas
    for i in range(pos.y + 1, 6):
        if board.slabs[i][pos.x] != 0:
            all_neighbours[offset].y = i
            all_neighbours[offset].x = pos.x
            offset += 1
            break  
    # Haut
    for i in range(pos.y - 1, -1, -1):
        if board.slabs[i][pos.x] != 0:
            all_neighbours[offset].y = i
            all_neighbours[offset].x = pos.x
            offset += 1
            break  

    return offset

cdef void calcul_dist(Board *board, Coords goal, Coords *pos, int *dists, int len_pos) noexcept nogil:
    cdef int i, j
    if is_pawn(board, goal):
        for i in range(len_pos):
            dists[i] = -1
    
    cdef int distances[6][6]
    for i in range(6):
        for j in range(6):
            distances[i][j] = -1
    distances[goal.y][goal.x] = 0
    cdef int actual_dist = 1

    cdef Coords open_list[36]
    open_list[0].y = goal.y
    open_list[0].x = goal.x
    cdef int offset=0, size_step=1, size_next_step=0

    cdef Coords all_neighbours[4]
    cdef int len_neighbours
    while size_step:
        for i in range(size_step):
            len_neighbours = get_voisins(board, open_list[offset+i], all_neighbours)
            for j in range(len_neighbours):
                if distances[all_neighbours[j].y][all_neighbours[j].x] == -1:
                    distances[all_neighbours[j].y][all_neighbours[j].x] = actual_dist
                    if not is_pawn(board, all_neighbours[j]):
                        open_list[offset+size_step+size_next_step].y = all_neighbours[j].y
                        open_list[offset+size_step+size_next_step].x = all_neighbours[j].x
                        size_next_step += 1
        offset += size_step
        size_step = size_next_step
        size_next_step = 0
        actual_dist += 1
    
    for i in range(len_pos):
        dists[i] = distances[pos[i].y][pos[i].x]
    
    

cdef double CalculMobility(Board *board, Coords pos, float gamma) noexcept nogil:
    cdef int i, j
    cdef int distances[6][6]
    for i in range(6):
        for j in range(6):
            distances[i][j] = -1
    distances[pos.y][pos.x] = 0
    cdef int actual_dist = 1
    cdef double score = 0
    cdef Coords open_list[36]
    open_list[0].y = pos.y
    open_list[0].x = pos.x
    cdef int offset=0, size_step=1, size_next_step=0
    cdef Coords all_neighbours[4]
    cdef int len_neighbours
    while size_step:
        for i in range(size_step):
            len_neighbours = get_voisins(board, open_list[offset+i], all_neighbours)
            for j in range(len_neighbours):
                if distances[all_neighbours[j].y][all_neighbours[j].x] == -1:
                    distances[all_neighbours[j].y][all_neighbours[j].x] = actual_dist
                    open_list[offset+size_step+size_next_step].y = all_neighbours[j].y
                    open_list[offset+size_step+size_next_step].x = all_neighbours[j].x
                    size_next_step += 1

        score += gamma**(actual_dist-1) * sqrt(<double>size_next_step)

        offset += size_step
        size_step = size_next_step
        size_next_step = 0
        actual_dist += 1
    return score
        

  