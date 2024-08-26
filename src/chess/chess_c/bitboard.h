#pragma once

#include "square.h"
#include "types.h"

typedef struct Bitboard {
    u64 value;
} Bitboard_t;

Bitboard_t bitboard_init_from_value(u64 value);

void bitboard_set_square(Bitboard_t *bitboard, Square_t square);
void bitboard_set_bitboard(Bitboard_t *source_bitboard,
                           Bitboard_t *target_bitboard);

void bitboard_print(Bitboard_t *bitboard);
