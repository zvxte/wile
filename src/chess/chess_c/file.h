#pragma once

#include "types.h"

typedef enum File : i8 {
    FILE_A,
    FILE_B,
    FILE_C,
    FILE_D,
    FILE_E,
    FILE_F,
    FILE_G,
    FILE_H,
} File_t;

File_t file_init_from_char(char character);
