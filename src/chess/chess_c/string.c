#include "status.h"
#include "types.h"

Status_t string_to_u16(char *character, u16 *number) {
    if (*character < '0' || *character > '9') {
        return STATUS_ERROR;
    }

    u16 result = 0;
    while (*character >= '0' && *character <= '9') {
        result *= 10;
        result += *character - '0';
        character++;
    }
    *number = result;

    return STATUS_SUCCESS;
};
