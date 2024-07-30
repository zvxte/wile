#include "types.h"
#include <ctype.h>
#include <string.h>

Position_t position_create() {
  return (Position_t){
      .occupancy = (Bitboard_t)0xFFFF00000000FFFF,

      .white_pawns = (Bitboard_t)0xFF << 8,
      .white_knights = (Bitboard_t)0x42,
      .white_bishops = (Bitboard_t)0x24,
      .white_rooks = (Bitboard_t)0x81,
      .white_queens = (Bitboard_t)0x8,
      .white_king = (Bitboard_t)0x10,

      .black_pawns = (Bitboard_t)0xFF << 48,
      .black_knights = (Bitboard_t)0x42 << 56,
      .black_bishops = (Bitboard_t)0x24 << 56,
      .black_rooks = (Bitboard_t)0x81 << 56,
      .black_queens = (Bitboard_t)0x8 << 56,
      .black_king = (Bitboard_t)0x10 << 56,

      .active_color = COLOR_WHITE,
      .castling_rights = 0xF,
      .en_passant_square = SQUARE_NONE,
      .halfmove_clock = 0,
      .fullmove_number = 1,
  };
}

Position_t position_create_empty() {
  return (Position_t){
      .occupancy = (Bitboard_t)0,

      .white_pawns = (Bitboard_t)0,
      .white_knights = (Bitboard_t)0,
      .white_bishops = (Bitboard_t)0,
      .white_rooks = (Bitboard_t)0,
      .white_queens = (Bitboard_t)0,
      .white_king = (Bitboard_t)0,

      .black_pawns = (Bitboard_t)0,
      .black_knights = (Bitboard_t)0,
      .black_bishops = (Bitboard_t)0,
      .black_rooks = (Bitboard_t)0,
      .black_queens = (Bitboard_t)0,
      .black_king = (Bitboard_t)0,

      .active_color = COLOR_WHITE,
      .castling_rights = 0x0,
      .en_passant_square = SQUARE_NONE,
      .halfmove_clock = 0,
      .fullmove_number = 1,
  };
};

Position_t position_create_from_fen(const char *fen) {
  char fen_inner[128] = {0};
  strncpy(fen_inner, fen, 127);
  fen_inner[127] = '\0';
  fen = NULL;

  Position_t position = position_create_empty();
  char *character = fen_inner;

  // ====PIECE PLACEMENT==== //
  for (int rank = RANK_8; rank >= RANK_1; rank -= 1) {
    for (int file = FILE_A; file <= FILE_H;) {
      Square_t square = square_create_from_file_rank(file, rank);
      Bitboard_t bitboard = bitboard_create_from_square(square);
      if (*character == '/') {
        character++;
        continue;
      }

      if (isdigit(*character)) {
        // Invalid FEN digits will behave as 8
        int digit = *character - '0';
        file += digit;
        character++;
        continue;
      }

      // clang-format off
      switch (*character) {
        case 'P': position.white_pawns |= bitboard; break;
        case 'p': position.black_pawns |= bitboard; break;
        case 'N': position.white_knights |= bitboard; break;
        case 'n': position.black_knights |= bitboard; break;
        case 'B': position.white_bishops |= bitboard; break;
        case 'b': position.black_bishops |= bitboard; break;
        case 'R': position.white_rooks |= bitboard; break;
        case 'r': position.black_rooks |= bitboard; break;
        case 'Q': position.white_queens |= bitboard; break;
        case 'q': position.black_queens |= bitboard; break;
        case 'K': position.white_king |= bitboard; break;
        case 'k': position.black_king |= bitboard; break;
        // Invalid FEN characters will be skipped
        default: character++; continue;
      }
      // clang-format on
      position.occupancy |= bitboard;

      file++;
      character++;
    }
  }
  character++;

  // ====COLOR==== //
  if (*character == 'b') {
    position.active_color = COLOR_BLACK;
  }
  character += 2;

  // ====CASTLING RIGHTS==== //
  while (*character && *character != ' ') {
    // clang-format off
    switch (*character) {
      case 'K': position.castling_rights |= CASTLING_RIGHTS_WHITE_KINGSIDE; break;
      case 'Q': position.castling_rights |= CASTLING_RIGHTS_WHITE_QUEENSIDE; break;
      case 'k': position.castling_rights |= CASTLING_RIGHTS_BLACK_KINGSIDE; break;
      case 'q': position.castling_rights |= CASTLING_RIGHTS_BLACK_QUEENSIDE; break;
    }
    // clang-format on

    character++;
  }
  character++;

  // ====EN PASSANT SQUARE==== //
  char maybe_file = *character;
  char maybe_rank = *(character + 1);
  if ((maybe_file >= 'a' && maybe_file <= 'h') &&
      (maybe_rank == '3' || maybe_rank == '6')) {
    File_t file = file_create_from_char(maybe_file);
    Rank_t rank = rank_create_from_char(maybe_rank);
    position.en_passant_square = square_create_from_file_rank(file, rank);
    character++;
  }
  character += 2;

  // ====HALFMOVE CLOCK==== //
  int halfmove_clock = 0;
  while (*character && *character != ' ') {
    if (isdigit(*character)) {
      halfmove_clock = halfmove_clock * 10 + (*character - 48);
    }
    character++;
  }
  position.halfmove_clock = halfmove_clock;
  character++;

  // ====FULLMOVE NUMBER==== //
  int fullmove_number = 0;
  while (*character && *character != ' ') {
    if (isdigit(*character)) {
      fullmove_number = fullmove_number * 10 + (*character - 48);
    }
    character++;
  }
  if (fullmove_number > position.fullmove_number) {
    position.fullmove_number = fullmove_number;
  }

  return position;
};
