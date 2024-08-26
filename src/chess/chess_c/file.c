#include "file.h"

File_t file_init_from_char(char character) {
    return (File_t)(character - 'a');
};
