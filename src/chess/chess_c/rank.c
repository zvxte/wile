#include "types.h"

Rank_t rank_create_from_char(char character) {
  return (Rank_t)(character - '1');
};

Rank_t rank_create_from_square(Square_t square) {
  return (Rank_t)(square >> 3);
};

char rank_to_char(Rank_t rank) { return (char)(rank + '1'); };
