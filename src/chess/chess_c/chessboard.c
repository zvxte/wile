#include "chessboard.h"
#include "position.h"
#include "status.h"

Status_t chessboard_init_from_fen(char *fen, Chessboard_t *chessboard) {
    Position_t position;
    Status_t status = position_init_from_fen(fen, &position);
    chessboard->position = position;
    return status;
};
