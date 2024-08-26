#include <stdio.h>

#include "../position.h"
#include "../status.h"

void test_position_init_from_fen() {
    Position_t position;
    Status_t status;

    status = position_init_from_fen(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1", &position);
    if (status != STATUS_SUCCESS) {
        printf("FAILED: position_init_from_fen\n");
    }

    status = position_init_from_fen(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0", &position);
    if (status != STATUS_SUCCESS) {
        printf("FAILED: position_init_from_fen\n");
    }

    status = position_init_from_fen(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq -", &position);
    if (status != STATUS_SUCCESS) {
        printf("FAILED: position_init_from_fen\n");
    }

    status = position_init_from_fen(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq", &position);
    if (status != STATUS_SUCCESS) {
        printf("FAILED: position_init_from_fen\n");
    }

    status = position_init_from_fen(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w", &position);
    if (status != STATUS_SUCCESS) {
        printf("FAILED: position_init_from_fen\n");
    }

    status = position_init_from_fen(
        "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR", &position);
    if (status != STATUS_SUCCESS) {
        printf("FAILED: position_init_from_fen\n");
    }
}

int main() {
    test_position_init_from_fen();
    return 0;
}
