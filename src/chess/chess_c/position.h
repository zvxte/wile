#pragma once

#include "bitboard.h"
#include "castling_rights.h"
#include "color.h"
#include "move.h"
#include "square.h"
#include "status.h"
#include "types.h"

typedef struct Position {
    Bitboard_t occupancy;

    Bitboard_t white_pawns;
    Bitboard_t white_knights;
    Bitboard_t white_bishops;
    Bitboard_t white_rooks;
    Bitboard_t white_queens;
    Bitboard_t white_king;

    Bitboard_t black_pawns;
    Bitboard_t black_knights;
    Bitboard_t black_bishops;
    Bitboard_t black_rooks;
    Bitboard_t black_queens;
    Bitboard_t black_king;

    Color_t color;
    CastlingRights_t castling_rights;
    Square_t en_passant_square;
    u16 halfmove_clock;
    u16 fullmove_counter;
} Position_t;

Position_t position_init();
Position_t position_init_empty();
Status_t position_init_from_fen(char *fen, Position_t *position);
Status_t position_move(Position_t *position, Move_t *move);
