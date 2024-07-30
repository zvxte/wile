#include "types.h"

Rank_t rank_create_from_char(char character) {
  return (Rank_t)(character - '1');
};
