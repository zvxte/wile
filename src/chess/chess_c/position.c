#include "types.h"
#include <ctype.h>
#include <stdlib.h>
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

Position_t position_from_fen(const char *fen) {
  // TODO: validate legality of received fen
  char fen_inner[128];
  strncpy(fen_inner, fen, 127);
  fen_inner[127] = '\0';
  fen = NULL;

  Position_t position = position_create_empty();
  char *character = fen_inner;

  // ====PIECE PLACEMENT==== //
  for (Rank_t rank = RANK_8; rank >= RANK_1; rank--) {
    for (File_t file = FILE_A; file <= FILE_H;) {
      Square_t square = square_from_file_rank(file, rank);
      // Bitboard_t bitboard = bitboard_create_from_square(square);
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
        case 'P': bitboard_set(&position.white_pawns, square); break;
        case 'p': bitboard_set(&position.black_pawns, square); break;
        case 'N': bitboard_set(&position.white_knights, square); break;
        case 'n': bitboard_set(&position.black_knights, square); break;
        case 'B': bitboard_set(&position.white_bishops, square); break;
        case 'b': bitboard_set(&position.black_bishops, square); break;
        case 'R': bitboard_set(&position.white_rooks, square); break;
        case 'r': bitboard_set(&position.black_rooks, square); break;
        case 'Q': bitboard_set(&position.white_queens, square); break;
        case 'q': bitboard_set(&position.black_queens, square); break;
        case 'K': bitboard_set(&position.white_king, square); break;
        case 'k': bitboard_set(&position.black_king, square); break;
        // Invalid FEN characters will be skipped
        default: character++; continue;
      }
      // clang-format on
      bitboard_set(&position.occupancy, square);

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
      case 'K': castling_rights_set(&position.castling_rights, CASTLING_RIGHTS_WHITE_KINGSIDE); break;
      case 'Q': castling_rights_set(&position.castling_rights, CASTLING_RIGHTS_WHITE_QUEENSIDE); break;
      case 'k': castling_rights_set(&position.castling_rights, CASTLING_RIGHTS_BLACK_KINGSIDE); break;
      case 'q': castling_rights_set(&position.castling_rights, CASTLING_RIGHTS_BLACK_QUEENSIDE); break;
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
    File_t file = file_from_char(maybe_file);
    Rank_t rank = rank_from_char(maybe_rank);
    position.en_passant_square = square_from_file_rank(file, rank);
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

char *position_get_fen(const Position_t *position) {
  char *fen = malloc(128 * sizeof(char));
  char *character = fen;

  // ====PIECE PLACEMENT==== //
  for (Rank_t rank = RANK_8; rank >= RANK_1; rank--) {
    for (File_t file = FILE_A; file <= FILE_H;) {
      Square_t square = square_from_file_rank(file, rank);
      Piece_t piece = position_get_piece(position, square);

      if (piece == PIECE_NONE) {
        int empty_counter = 0;
        while (piece == PIECE_NONE && file <= FILE_H) {
          file++;
          empty_counter++;
          square = square_from_file_rank(file, rank);
          piece = position_get_piece(position, square);
        }
        *character = empty_counter + '0';
      } else {
        *character = piece_to_char(piece);
        file++;
      }
      character++;
    }
    if (rank > RANK_1) {
      *character = '/';
      character++;
    }
  }
  *character = ' ';
  character++;

  // ====COLOR==== //
  *character = position->active_color == COLOR_BLACK ? 'b' : 'w';
  character++;
  *character = ' ';
  character++;

  // ====CASTLING RIGHTS==== //
  CastlingRights_t castling_rights = position->castling_rights;
  if (castling_rights == CASTLING_RIGHTS_NONE) {
    *character = '-';
    character++;
  } else {
    if (castling_rights & CASTLING_RIGHTS_WHITE_KINGSIDE) {
      *character = 'K';
      character++;
    }
    if (castling_rights & CASTLING_RIGHTS_WHITE_QUEENSIDE) {
      *character = 'Q';
      character++;
    }
    if (castling_rights & CASTLING_RIGHTS_BLACK_KINGSIDE) {
      *character = 'k';
      character++;
    }
    if (castling_rights & CASTLING_RIGHTS_BLACK_QUEENSIDE) {
      *character = 'q';
      character++;
    }
  }
  *character = ' ';
  character++;

  // ====EN PASSANT SQUARE==== //
  Square_t en_passant_square = position->en_passant_square;
  if (en_passant_square == SQUARE_NONE) {
    *character = '-';
    character++;
  } else {
    File_t file = file_from_square(en_passant_square);
    *character = file_to_char(file);
    character++;
    Rank_t rank = rank_from_square(en_passant_square);
    *character = rank_to_char(rank);
    character++;
  }
  *character = ' ';
  character++;

  // ====HALFMOVE CLOCK==== //
  int halfmove_clock = position->halfmove_clock;
  int length = 0;
  do {
    *character = (char)(halfmove_clock % 10 + '0');
    halfmove_clock /= 10;
    character++;
    length++;
  } while (halfmove_clock > 0);

  // Reverse numbers back to the right order
  char *first_character = character - length;
  char *last_character = character - 1;
  for (int i = 0; i < length / 2; i++) {
    char temp = *last_character;
    *last_character = *first_character;
    *first_character = temp;
    first_character++;
    last_character--;
  }
  *character = ' ';
  character++;

  // ====FULLMOVE NUMBER==== //
  int fullmove_number = position->fullmove_number;
  length = 0;
  do {
    *character = (char)(fullmove_number % 10 + '0');
    fullmove_number /= 10;
    character++;
    length++;
  } while (fullmove_number > 0);

  // Reverse numbers back to the right order
  first_character = character - length;
  last_character = character - 1;
  for (int i = 0; i < length / 2; i++) {
    char temp = *last_character;
    *last_character = *first_character;
    *first_character = temp;
    first_character++;
    last_character--;
  }

  *character = '\0';

  return fen;
};

void position_move(Position_t *position, const Move_t *move) {
  int is_capture =
      (position->occupancy & bitboard_from_square(move->target_square)) > 0;
  Square_t source_square = move->source_square;
  Square_t target_square = move->target_square;
  Piece_t piece = move->piece;

  // ====UPDATE SOURCE AND TARGET SQUARE==== //
  position_unset(position, source_square);
  position_unset(position, target_square);
  bitboard_set(&position->occupancy, target_square);

  // clang-format off
  switch (move->move_type == MOVE_TYPE_PROMOTION ? move->promotion_piece : piece) {
    case PIECE_WHITE_PAWN: bitboard_set(&position->white_pawns, target_square); break;
    case PIECE_WHITE_KNIGHT: bitboard_set(&position->white_knights, target_square); break;
    case PIECE_WHITE_BISHOP: bitboard_set(&position->white_bishops, target_square); break;
    case PIECE_WHITE_ROOK: bitboard_set(&position->white_rooks, target_square); break;
    case PIECE_WHITE_QUEEN: bitboard_set(&position->white_queens, target_square); break;
    case PIECE_WHITE_KING: bitboard_set(&position->white_king, target_square); break;
    case PIECE_BLACK_PAWN: bitboard_set(&position->black_pawns, target_square); break;
    case PIECE_BLACK_KNIGHT: bitboard_set(&position->black_knights, target_square); break;
    case PIECE_BLACK_BISHOP: bitboard_set(&position->black_bishops, target_square); break;
    case PIECE_BLACK_ROOK: bitboard_set(&position->black_rooks, target_square); break;
    case PIECE_BLACK_QUEEN: bitboard_set(&position->black_queens, target_square); break;
    case PIECE_BLACK_KING: bitboard_set(&position->black_king, target_square); break;
    default: break;
  }
  // clang-format on

  if (move->move_type == MOVE_TYPE_CASTLING) {
    if (piece == PIECE_WHITE_KING) {
      if (target_square == SQUARE_G1) {
        bitboard_unset(&position->white_rooks, SQUARE_H1);
        bitboard_set(&position->white_rooks, SQUARE_F1);
      } else if (target_square == SQUARE_C1) {
        bitboard_unset(&position->white_rooks, SQUARE_A1);
        bitboard_set(&position->white_rooks, SQUARE_D1);
      }
    } else if (piece == PIECE_BLACK_KING) {
      if (target_square == SQUARE_G8) {
        bitboard_unset(&position->black_rooks, SQUARE_H8);
        bitboard_set(&position->black_rooks, SQUARE_F8);
      } else if (target_square == SQUARE_C8) {
        bitboard_unset(&position->black_rooks, SQUARE_A8);
        bitboard_set(&position->black_rooks, SQUARE_D8);
      }
    }
  }

  // ====UPDATE ACTIVE COLOR==== //
  position->active_color =
      (position->active_color == COLOR_WHITE) ? COLOR_BLACK : COLOR_WHITE;

  // ====UPDATE CASTLING RIGHTS==== //
  // clang-format off
  switch (piece) {
    case PIECE_WHITE_KING: castling_rights_unset(&position->castling_rights, CASTLING_RIGHTS_WHITE_KINGSIDE | CASTLING_RIGHTS_WHITE_QUEENSIDE); break;
    case PIECE_BLACK_KING: castling_rights_unset(&position->castling_rights, CASTLING_RIGHTS_BLACK_KINGSIDE | CASTLING_RIGHTS_BLACK_QUEENSIDE); break;
    case PIECE_WHITE_ROOK:
      if (source_square == SQUARE_A1) castling_rights_unset(&position->castling_rights, CASTLING_RIGHTS_WHITE_QUEENSIDE);
      else if (source_square == SQUARE_H1) castling_rights_unset(&position->castling_rights, CASTLING_RIGHTS_WHITE_KINGSIDE);
      break;
    case PIECE_BLACK_ROOK:
      if (source_square == SQUARE_A8) castling_rights_unset(&position->castling_rights, CASTLING_RIGHTS_BLACK_QUEENSIDE);
      else if (source_square == SQUARE_H8) castling_rights_unset(&position->castling_rights, CASTLING_RIGHTS_BLACK_KINGSIDE);
      break;
    default: break;
  }
  // clang-format on

  // ====UPDATE EN PASSANT SQUARE==== //
  if (target_square == position->en_passant_square) {
    if (position->active_color == COLOR_WHITE) {
      bitboard_unset(&position->white_pawns,
                     position->en_passant_square + DIRECTION_UP);
      bitboard_unset(&position->occupancy,
                     position->en_passant_square + DIRECTION_UP);
    } else {
      bitboard_unset(&position->black_pawns,
                     position->en_passant_square + DIRECTION_DOWN);
      bitboard_unset(&position->occupancy,
                     position->en_passant_square + DIRECTION_DOWN);
    }
  }
  if (piece == PIECE_WHITE_PAWN &&
      target_square == source_square + 2 * DIRECTION_UP) {
    Bitboard_t maybe_black_pawns = (Bitboard_t)0b101 << (target_square - 1);
    if (position->black_pawns & maybe_black_pawns) {
      position->en_passant_square = source_square + DIRECTION_UP;
    }
  } else if (piece == PIECE_BLACK_PAWN &&
             target_square == source_square + 2 * DIRECTION_DOWN) {
    Bitboard_t maybe_white_pawns = (Bitboard_t)0b101 << (target_square - 1);
    if (position->white_pawns & maybe_white_pawns) {
      position->en_passant_square = source_square + DIRECTION_DOWN;
    }
  } else {
    position->en_passant_square = SQUARE_NONE;
  }

  // ====UPDATE HALFMOVE CLOCK==== //
  if (is_capture || piece == PIECE_WHITE_PAWN || piece == PIECE_BLACK_PAWN) {
    position->halfmove_clock = 0;
  } else {
    position->halfmove_clock++;
  }

  // ====UPDATE FULLMOVE NUMBER==== //
  if (position->active_color == COLOR_WHITE) {
    position->fullmove_number++;
  }
};

Piece_t position_get_piece(const Position_t *position, Square_t square) {
  Bitboard_t bitboard = bitboard_from_square(square);
  // clang-format off
  if (!(position->occupancy & bitboard)) return PIECE_NONE;
  if (position->white_pawns & bitboard) return PIECE_WHITE_PAWN;
  if (position->black_pawns & bitboard) return PIECE_BLACK_PAWN;
  if (position->white_knights & bitboard) return PIECE_WHITE_KNIGHT;
  if (position->black_knights & bitboard) return PIECE_BLACK_KNIGHT;
  if (position->white_bishops & bitboard) return PIECE_WHITE_BISHOP;
  if (position->black_bishops & bitboard) return PIECE_BLACK_BISHOP;
  if (position->white_rooks & bitboard) return PIECE_WHITE_ROOK;
  if (position->black_rooks & bitboard) return PIECE_BLACK_ROOK;
  if (position->white_queens & bitboard) return PIECE_WHITE_QUEEN;
  if (position->black_queens & bitboard) return PIECE_BLACK_QUEEN;
  if (position->white_king & bitboard) return PIECE_WHITE_KING;
  if (position->black_king & bitboard) return PIECE_BLACK_KING;
  // clang-format on
  return PIECE_NONE;
};

void position_unset(Position_t *position, Square_t square) {
  Bitboard_t bitboard = bitboard_from_square(square);
  position->occupancy &= ~bitboard;
  position->white_pawns &= ~bitboard;
  position->black_pawns &= ~bitboard;
  position->white_knights &= ~bitboard;
  position->black_knights &= ~bitboard;
  position->white_bishops &= ~bitboard;
  position->black_bishops &= ~bitboard;
  position->white_rooks &= ~bitboard;
  position->black_rooks &= ~bitboard;
  position->white_queens &= ~bitboard;
  position->black_queens &= ~bitboard;
  position->white_king &= ~bitboard;
  position->black_king &= ~bitboard;
};
