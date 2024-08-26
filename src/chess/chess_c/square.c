#include "square.h"
#include "file.h"
#include "rank.h"

Square_t square_init_from_file_and_rank(File_t file, Rank_t rank) {
    return (Square_t)(rank * 8 + file);
};
