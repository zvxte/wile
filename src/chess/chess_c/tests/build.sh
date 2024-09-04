#!/bin/bash

# POSITION
gcc -o "test_position.o" "test_position.c" "../position.c" "../position.h" \
"../status.h" "../bitboard.c" "../bitboard.h" "../file.c" "../file.h" \
"../rank.c" "../rank.h" "../square.c" "../square.h" "../string.c" "../string.h"
if [ $? -ne 0 ]; then
    echo "test_position failed to compile"
fi

# STRING
gcc -o "test_string.o" "test_string.c" "../string.c" "../string.h" "../status.h"
if [ $? -ne 0 ]; then
    echo "test_string failed to compile"
fi
