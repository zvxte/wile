#include "stdio.h"

#include "bitboard.h"
#include "square.h"

Bitboard_t bitboard_init_from_value(u64 value) {
    return (Bitboard_t){.value = value};
};

void bitboard_set_square(Bitboard_t *bitboard, Square_t square) {
    bitboard->value |= (u64)1 << square;
};

void bitboard_set_bitboard(Bitboard_t *source_bitboard,
                           Bitboard_t *target_bitboard) {
    source_bitboard->value |= target_bitboard->value;
};

void bitboard_print(Bitboard_t *bitboard) {
    printf("+---+---+---+---+---+---+---+---+\n");
    for (Rank_t rank = RANK_8; rank >= RANK_1; rank--) {
      for (File_t file = FILE_A; file <= FILE_H; file++) {
        Square_t square = square_init_from_file_and_rank(file, rank);
        printf("| %c ", bitboard->value >> square & 1 ? 'X' : ' ');
      }
      printf("| %d\n", rank + 1);
      printf("+---+---+---+---+---+---+---+---+\n");
    }
    printf("  a   b   c   d   e   f   g   h\n");
};
