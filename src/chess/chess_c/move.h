#pragma once

#include "square.h"
#include "piece.h"

typedef struct Move {
    Square_t source_square;
    Square_t target_square;
    Piece_t piece;
    Piece_t promotion_piece;
} Move_t;
