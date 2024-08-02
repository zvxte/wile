#include "types.h"
#include <string.h>

Move_t move_from_san_pawn(const Position_t *position, const char *san_move) {
  // TODO: validate legality of received move
  char san[8];
  strncpy(san, san_move, 7);
  san[7] = '\0';
  san_move = NULL;

  Color_t color = position->active_color;
  Piece_t piece = (color == COLOR_BLACK) ? PIECE_BLACK_PAWN : PIECE_WHITE_PAWN;
  MoveType_t move_type = MOVE_TYPE_NORMAL;
  char *character = san;

  File_t source_file = file_from_char(*character);
  if (*(character + 1) == 'x') {
    character += 2;
  }
  File_t target_file = file_from_char(*character);
  character++;
  Rank_t target_rank = rank_from_char(*character);

  Direction_t direction =
      (color == COLOR_BLACK) ? DIRECTION_UP : DIRECTION_DOWN;

  Rank_t source_rank =
      (direction == DIRECTION_UP) ? target_rank + 1 : target_rank - 1;

  // Pawn move by 2 squares
  if (target_rank == RANK_4 || target_rank == RANK_5) {
    Square_t maybe_pawn_square =
        square_from_file_rank(source_file, source_rank);
    Piece_t maybe_pawn = position_get_piece(position, maybe_pawn_square);
    if (maybe_pawn != piece) {
      (direction == DIRECTION_UP) ? source_rank++ : source_rank--;
    }
  }
  Square_t source_square = square_from_file_rank(source_file, source_rank);
  Square_t target_square = square_from_file_rank(target_file, target_rank);

  // Promotion
  Piece_t promotion_piece = PIECE_NONE;
  character++;
  if (*character == '=') {
    character++;
    // clang-format off
    switch (*character) {
      case 'Q': promotion_piece = PIECE_WHITE_QUEEN; break;
      case 'q': promotion_piece = PIECE_BLACK_QUEEN; break;
      case 'R': promotion_piece = PIECE_WHITE_ROOK; break;
      case 'r': promotion_piece = PIECE_BLACK_ROOK; break;
      case 'B': promotion_piece = PIECE_WHITE_BISHOP; break;
      case 'b': promotion_piece = PIECE_BLACK_BISHOP; break;
      case 'N': promotion_piece = PIECE_WHITE_KNIGHT; break;
      case 'n': promotion_piece = PIECE_BLACK_KNIGHT; break;
      default: break;
    }
    // clang-format on
    move_type = MOVE_TYPE_PROMOTION;
  }

  return (Move_t){
      .source_square = source_square,
      .target_square = target_square,
      .piece = piece,
      .promotion_piece = promotion_piece,
      .move_type = move_type,
  };
};

Move_t move_from_san(const Position_t *position, const char *san_move) {
  /*
  () - Mandatory, [] - Optional, || - Or

  ---Pawn move---
  [(File)x]  (File)  (Rank)  [=Piece]  [+ || #]

  ---Piece move---
  (Piece)  [File]  [Rank]  [x]  (File)  (Rank)  [+ || #]

  ---Castling---
  (O-O) || (O-O-O)
  */
  char first_character = san_move[0];
  if (first_character >= 'a' && first_character <= 'h') {
    return move_from_san_pawn(position, san_move);
  }

  return (Move_t){};
};
