#include "position.h"
#include "bitboard.h"
#include "castling_rights.h"
#include "color.h"
#include "file.h"
#include "rank.h"
#include "square.h"
#include "status.h"
#include "string.h"

Position_t position_init() {
    return (Position_t){
        .occupancy = bitboard_init_from_value(0xFFFF00000000FFFF),

        .white_pawns = bitboard_init_from_value(0xFF << 8),
        .white_knights = bitboard_init_from_value(0x42),
        .white_bishops = bitboard_init_from_value(0x24),
        .white_rooks = bitboard_init_from_value(0x81),
        .white_queens = bitboard_init_from_value(0x8),
        .white_king = bitboard_init_from_value(0x10),

        .black_pawns = bitboard_init_from_value((u64)0xFF << 48),
        .black_knights = bitboard_init_from_value((u64)0x42 << 56),
        .black_bishops = bitboard_init_from_value((u64)0x24 << 56),
        .black_rooks = bitboard_init_from_value((u64)0x81 << 56),
        .black_queens = bitboard_init_from_value((u64)0x8 << 56),
        .black_king = bitboard_init_from_value((u64)0x10 << 56),

        .color = COLOR_WHITE,
        .castling_rights = 0xF,
        .en_passant_square = SQUARE_NONE,
        .halfmove_clock = 0,
        .fullmove_counter = 1,
    };
};

Position_t position_init_empty() {
    return (Position_t){
        .occupancy = bitboard_init_from_value(0),

        .white_pawns = bitboard_init_from_value(0),
        .white_knights = bitboard_init_from_value(0),
        .white_bishops = bitboard_init_from_value(0),
        .white_rooks = bitboard_init_from_value(0),
        .white_queens = bitboard_init_from_value(0),
        .white_king = bitboard_init_from_value(0),

        .black_pawns = bitboard_init_from_value(0),
        .black_knights = bitboard_init_from_value(0),
        .black_bishops = bitboard_init_from_value(0),
        .black_rooks = bitboard_init_from_value(0),
        .black_queens = bitboard_init_from_value(0),
        .black_king = bitboard_init_from_value(0),

        .color = COLOR_WHITE,
        .castling_rights = 0,
        .en_passant_square = SQUARE_NONE,
        .halfmove_clock = 0,
        .fullmove_counter = 1,
    };
}

Status_t position_init_from_fen(char *fen, Position_t *position) {
    if (!fen || !position) {
        return STATUS_ERROR;
    }

    char *character = fen;

    *position = position_init_empty();

    // PIECE PLACEMENT //
    for (Rank_t rank = RANK_8; rank >= RANK_1; rank--) {
        for (File_t file = FILE_A; file <= FILE_H; file++) {
            if (*character >= '1' && *character <= '8') {
                file += (*character - '0') - 1;
                character++;
                continue;
            }

            Square_t square = square_init_from_file_and_rank(file, rank);
            switch (*character) { // clang-format off
                case 'P': bitboard_set_square(&position->white_pawns, square); break;
                case 'p': bitboard_set_square(&position->black_pawns, square); break;
                case 'N': bitboard_set_square(&position->white_knights, square); break;
                case 'n': bitboard_set_square(&position->black_knights, square); break;
                case 'B': bitboard_set_square(&position->white_bishops, square); break;
                case 'b': bitboard_set_square(&position->black_bishops, square); break;
                case 'R': bitboard_set_square(&position->white_rooks, square); break;
                case 'r': bitboard_set_square(&position->black_rooks, square); break;
                case 'Q': bitboard_set_square(&position->white_queens, square); break;
                case 'q': bitboard_set_square(&position->black_queens, square); break;
                case 'K': bitboard_set_square(&position->white_king, square); break;
                case 'k': bitboard_set_square(&position->black_king, square); break;
                default: return STATUS_ERROR;
            } // clang-format on
            bitboard_set_square(&position->occupancy, square);

            character++;
        }
        character++;
    }
    character--;

    if (*character == '\0') {
        return STATUS_SUCCESS;
    }
    character++;

    // COLOR //
    switch (*character) { // clang-format off
        case 'w': position->color = COLOR_WHITE; break;
        case 'b': position->color = COLOR_BLACK; break;
        default: return STATUS_ERROR;
    } // clang-format on
    character++;

    if (*character == '\0') {
        return STATUS_SUCCESS;
    }
    character++;

    // CASTLING RIGHTS //
    for (u8 i = 0; i < 4; i++) {
        if (*character == '-') {
            character++;
            break;
        } else if (!*character || *character == ' ') {
            break;
        }

        switch (*character) { // clang-format off
            case 'K': position->castling_rights |= CASTLING_RIGHTS_WHITE_KINGSIDE; break;
            case 'Q': position->castling_rights |= CASTLING_RIGHTS_WHITE_QUEENSIDE; break;
            case 'k': position->castling_rights |= CASTLING_RIGHTS_BLACK_KINGSIDE; break;
            case 'q': position->castling_rights |= CASTLING_RIGHTS_BLACK_QUEENSIDE; break;
            default: return STATUS_ERROR;
        } // clang-format on
        character++;
    }

    if (*character == '\0') {
        return STATUS_SUCCESS;
    }
    character++;

    // EN PASSANT SQUARE //
    if (*character >= 'a' && *character <= 'h') {
        File_t file = file_init_from_char(*character);
        character++;
        if (*character >= '1' && *character <= '8') {
            Rank_t rank = rank_init_from_char(*character);
            Square_t en_passant_square =
                square_init_from_file_and_rank(file, rank);
            position->en_passant_square = en_passant_square;
        }
    }
    character++;

    if (*character == '\0') {
        return STATUS_SUCCESS;
    }
    character++;
    // HALFMOVE CLOCK //
    u16 halfmove_clock;
    Status_t halfmove_clock_status = string_to_u16(character, &halfmove_clock);
    if (halfmove_clock_status != STATUS_SUCCESS) {
        return STATUS_ERROR;
    }
    position->halfmove_clock = halfmove_clock;
    character++;

    if (*character == '\0') {
        return STATUS_SUCCESS;
    }
    character++;

    // FULLMOVE COUNTER //
    u16 fullmove_counter;
    Status_t fullmove_counter_status =
        string_to_u16(character, &fullmove_counter);
    if (fullmove_counter_status != STATUS_SUCCESS) {
        return STATUS_ERROR;
    }
    position->fullmove_counter = fullmove_counter;

    return STATUS_SUCCESS;
};
