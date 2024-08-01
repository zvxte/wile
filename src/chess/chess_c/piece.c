#include "types.h"

char piece_to_char(Piece_t piece) {
  // clang-format off
  switch (piece) {
    case PIECE_WHITE_PAWN: return 'P';
    case PIECE_WHITE_KNIGHT: return 'N';
    case PIECE_WHITE_BISHOP: return 'B';
    case PIECE_WHITE_ROOK: return 'R';
    case PIECE_WHITE_QUEEN: return 'Q';
    case PIECE_WHITE_KING: return 'K';
  
    case PIECE_BLACK_PAWN: return 'p';
    case PIECE_BLACK_KNIGHT: return 'n';
    case PIECE_BLACK_BISHOP: return 'b';
    case PIECE_BLACK_ROOK: return 'r';
    case PIECE_BLACK_QUEEN: return 'q';
    case PIECE_BLACK_KING: return 'k';
    
    default: return ' ';
  }
  // clang-format on
};
