// ====TYPES_H==== //
#ifndef TYPES_H
#define TYPES_H

#include <stdint.h>

typedef uint64_t Bitboard_t;

typedef enum Square {
  SQUARE_A1, SQUARE_B1, SQUARE_C1, SQUARE_D1, SQUARE_E1, SQUARE_F1, SQUARE_G1, SQUARE_H1,
  SQUARE_A2, SQUARE_B2, SQUARE_C2, SQUARE_D2, SQUARE_E2, SQUARE_F2, SQUARE_G2, SQUARE_H2,
  SQUARE_A3, SQUARE_B3, SQUARE_C3, SQUARE_D3, SQUARE_E3, SQUARE_F3, SQUARE_G3, SQUARE_H3,
  SQUARE_A4, SQUARE_B4, SQUARE_C4, SQUARE_D4, SQUARE_E4, SQUARE_F4, SQUARE_G4, SQUARE_H4,
  SQUARE_A5, SQUARE_B5, SQUARE_C5, SQUARE_D5, SQUARE_E5, SQUARE_F5, SQUARE_G5, SQUARE_H5,
  SQUARE_A6, SQUARE_B6, SQUARE_C6, SQUARE_D6, SQUARE_E6, SQUARE_F6, SQUARE_G6, SQUARE_H6,
  SQUARE_A7, SQUARE_B7, SQUARE_C7, SQUARE_D7, SQUARE_E7, SQUARE_F7, SQUARE_G7, SQUARE_H7,
  SQUARE_A8, SQUARE_B8, SQUARE_C8, SQUARE_D8, SQUARE_E8, SQUARE_F8, SQUARE_G8, SQUARE_H8,
  SQUARE_NONE,
  SQUARE_MAX = 64,
} Square_t;

typedef enum Color {
  COLOR_WHITE,
  COLOR_BLACK,
} Color_t;

typedef enum Piece {
  PIECE_PAWN,
  PIECE_KNIGHT,
  PIECE_BISHOP,
  PIECE_ROOK,
  PIECE_QUEEN,
  PIECE_KING,
  PIECE_NONE,
} Piece_t;

typedef enum File : int {
  FILE_A,
  FILE_B,
  FILE_C,
  FILE_D,
  FILE_E,
  FILE_F,
  FILE_G,
  FILE_H,
} File_t;

typedef enum Rank : int {
  RANK_1,
  RANK_2,
  RANK_3,
  RANK_4,
  RANK_5,
  RANK_6,
  RANK_7,
  RANK_8,
} Rank_t;

typedef enum Direction {
  DIRECTION_UP = 8,
  DIRECTION_DOWN = -8,
  DIRECTION_LEFT = -1,
  DIRECTION_RIGHT = 1,
} Direction_t;

typedef enum CastlingRights {
  CASTLING_RIGHTS_NONE,
  CASTLING_RIGHTS_WHITE_KINGSIDE,
  CASTLING_RIGHTS_WHITE_QUEENSIDE,
  CASTLING_RIGHTS_BLACK_KINGSIDE = 4,
  CASTLING_RIGHTS_BLACK_QUEENSIDE = 8,
} CastlingRights_t;

typedef enum MoveType {
  MOVE_TYPE_PROMOTION,
  MOVE_TYPE_EN_PASSANT,
  MOVE_TYPE_CASTLING,
} MoveType_t;

typedef enum MoveSymbol {
  MOVE_SYMBOL_NONE,
  MOVE_SYMBOL_CHECK,
  MOVE_SYMBOL_MATE,
} MoveSymbol_t;

typedef struct Move {
  Square_t source_square;
  Square_t target_square;
  Piece_t promotion_piece;
  MoveType_t move_type;
  MoveSymbol_t move_symbol;
} Move_t;

typedef struct Position {
  Bitboard_t occupancy;

  Bitboard_t white_pawns;
  Bitboard_t white_knights;
  Bitboard_t white_bishops;
  Bitboard_t white_rooks;
  Bitboard_t white_queens;
  Bitboard_t white_king;

  Bitboard_t black_pawns;
  Bitboard_t black_knights;
  Bitboard_t black_bishops;
  Bitboard_t black_rooks;
  Bitboard_t black_queens;
  Bitboard_t black_king;

  Color_t active_color;
  CastlingRights_t castling_rights;
  Square_t en_passant_square;
  int halfmove_clock;
  int fullmove_number;
} Position_t;



Bitboard_t bitboard_create_from_square(Square_t square);
void bitboard_print(Bitboard_t bitboard);

Square_t square_create_from_file_rank(File_t file, Rank_t rank);

File_t file_create_from_char(char character);

Rank_t rank_create_from_char(char character);

Position_t position_create();
Position_t position_create_empty();
Position_t position_create_from_fen(const char *fen);
int position_move(Position_t *position, const Move_t *move);
char* position_get_fen(const Position_t *position);

#endif
// ====TYPES_H==== //
