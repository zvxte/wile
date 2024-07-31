#include "types.h"

File_t file_create_from_char(char character) {
  return (File_t)(character - 'a');
};

File_t file_create_from_square(Square_t square) {
  return (File_t)(square & 7);
};

char file_to_char(File_t file) { return (char)(file + 'a'); };
