#include "types.h"
#include <stdio.h>

Bitboard_t bitboard_create_from_square(Square_t square) {
  return (Bitboard_t)0b1 << square;
};

void bitboard_print(Bitboard_t bitboard) {
  printf("+---+---+---+---+---+---+---+---+\n");
  for (int rank = RANK_8; rank >= RANK_1; rank--) {
    for (int file = FILE_A; file <= FILE_H; file++) {
      Square_t square = square_create_from_file_rank(file, rank);
      printf("| %c ", bitboard >> square & 1 ? 'X' : ' ');
    }
    printf("| %d\n", rank + 1);
    printf("+---+---+---+---+---+---+---+---+\n");
  }
  printf("  a   b   c   d   e   f   g   h\n");
};
