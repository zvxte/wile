#include "types.h"

Square_t square_create_from_file_rank(File_t file, Rank_t rank) {
  return (Square_t)((rank << 3) + file);
}
