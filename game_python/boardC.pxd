cdef struct Coords:
    int y
    int x

cdef struct Move:
    Coords start
    Coords end
    
cdef struct Board:
    int slabs[6][6]
    Coords white_pawns[4]
    Coords black_pawns[4]


cdef int make_move(Board *board, Move move) noexcept nogil
cdef void undo_move(Board *board, Move move, int nb_dalles) noexcept nogil
cdef int get_all_pawns_move(Board *board, int color, Move all_moves[16]) noexcept nogil
cdef int get_one_pawn_move(Board *board, Coords pawn, Move all_moves[4]) noexcept nogil
cdef int get_all_slabs_stack(Board *board, Move all_moves[112]) noexcept nogil
cdef int get_result(Board *board, int color_turn) noexcept nogil
cdef int get_voisins(Board *board, Coords pos, Coords all_neighbours[4]) noexcept nogil
cdef void calcul_dist(Board *board, Coords goal, Coords *pos, int *dists, int len_pos) noexcept nogil
cdef int is_in_white(Board *board, Coords pos) noexcept nogil
cdef int is_in_black(Board *board, Coords pos) noexcept nogil
cdef int is_pawn(Board *board, Coords pos) noexcept nogil
cdef double CalculMobility(Board *board, Coords pos, float gamma) noexcept nogil