#include <stdio.h>
#include <stdlib.h>

static void release(int *p) {
    free(p);
}

int main(void) {
    int *numbers = malloc(4 * sizeof(int));
    if (numbers == NULL) {
        return 1;
    }
    for (int i = 0; i < 4; i++) {
        numbers[i] = i * i;
    }
    printf("Last: %d\n", numbers[3]);
    release(numbers);
    return 0;
}
