#include <stdio.h>

#include "../status.h"
#include "../string.h"

void test_string_to_u16() {
    char *string = "626212";
    u16 value;
    Status_t status = string_to_u16(string, &value);
    if (status != STATUS_SUCCESS || value != (u16)626212) {
        printf("FAILED: test_string_to_u16\n");
    }
}

int main() {
    test_string_to_u16();
    return 0;
}
