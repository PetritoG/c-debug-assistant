#include <stdio.h>
#include <string.h>

static void set_name(char *dest, const char *src) {
    strcpy(dest, src);
}

int main(void) {
    char name[16];
    set_name(name, "Margaret");
    printf("Name: %s\n", name);
    return 0;
}
