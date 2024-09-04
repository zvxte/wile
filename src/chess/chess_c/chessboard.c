#include "chessboard.h"
#include "position.h"
#include "status.h"

Status_t chessboard_init_from_fen(char *fen, Chessboard_t *chessboard) {
    if (!fen || !chessboard) {
        return STATUS_ERROR;
    }

    Position_t position;
    Status_t status = position_init_from_fen(fen, &position);
    chessboard->position = position;
    return status;
};

Status_t chessboard_move_uci(Chessboard_t *chessboard, char *uci_move) {
    if (!chessboard || !uci_move) {
        return STATUS_ERROR;
    }
    // todo
    return STATUS_SUCCESS;
};
