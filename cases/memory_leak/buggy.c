#include <stdio.h>
#include <stdlib.h>

static char *make_label(int id) {
    char *label = malloc(32);
    if (label == NULL) {
        return NULL;
    }
    snprintf(label, 32, "item-%d", id);
    return label;
}

int main(void) {
    for (int i = 1; i <= 3; i++) {
        char *label = make_label(i);
        if (label != NULL) {
            printf("%s\n", label);
        }
    }
    return 0;
}
