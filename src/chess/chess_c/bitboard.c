#include "types.h"
#include <stdio.h>

void bitboard_print(Bitboard_t bitboard) {
  printf("+---+---+---+---+---+---+---+---+\n");
  for (Rank_t rank = RANK_8; rank >= RANK_1; rank--) {
    for (File_t file = FILE_A; file <= FILE_H; file++) {
      Square_t square = square_from_file_rank(file, rank);
      printf("| %c ", bitboard >> square & 1 ? 'X' : ' ');
    }
    printf("| %d\n", rank + 1);
    printf("+---+---+---+---+---+---+---+---+\n");
  }
  printf("  a   b   c   d   e   f   g   h\n");
};
