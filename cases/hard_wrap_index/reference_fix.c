#include <stdio.h>

#define SIZE 5

static int wrap(int index, int size) {
    return ((index % size) + size) % size;
}

static void rotate_print(const char *labels[], int start, int step) {
    int pos = start;
    for (int k = 0; k < 6; k++) {
        printf("%s ", labels[wrap(pos, SIZE)]);
        pos += step;
    }
    printf("\n");
}

int main(void) {
    const char *labels[SIZE] = {"A", "B", "C", "D", "E"};
    rotate_print(labels, 0, 2);
    rotate_print(labels, 3, -1);
    rotate_print(labels, 1, -3);
    return 0;
}
