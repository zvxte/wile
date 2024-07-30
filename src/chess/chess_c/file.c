#include "types.h"

File_t file_create_from_char(char character) {
  return (File_t)(character - 'a');
};
