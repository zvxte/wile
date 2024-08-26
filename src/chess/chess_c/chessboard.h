#pragma once

#include "color.h"
#include "position.h"
#include "status.h"

typedef struct Chessboard {
    Position_t position;
} Chessboard_t;

Status_t chessboard_init_from_fen(char *fen, Chessboard_t *chessboard);

Status_t chessboard_move_uci(Chessboard_t *chessboard, char *uci_move);

Status_t chessboard_convert_san_to_uci(Chessboard_t *chessboard, char *san_move,
                                       char *uci_move);
Status_t chessboard_convert_uci_to_san(Chessboard_t *chessboard, char *uci_move,
                                       char *san_move);

char *chessboard_get_fen(Chessboard_t *chessboard);
Color_t chessboard_get_color(Chessboard_t *chessboard);
