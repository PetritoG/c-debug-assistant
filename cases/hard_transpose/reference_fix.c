#include <stdio.h>

static void transpose(const int *src, int *dst, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            dst[j * rows + i] = src[i * cols + j];
        }
    }
}

static void print_matrix(const int *m, int rows, int cols) {
    for (int i = 0; i < rows; i++) {
        for (int j = 0; j < cols; j++) {
            printf("%3d", m[i * cols + j]);
        }
        printf("\n");
    }
}

int main(void) {
    int square[9] = {1, 2, 3, 4, 5, 6, 7, 8, 9};
    int square_t[9];
    transpose(square, square_t, 3, 3);
    printf("3x3 transposed:\n");
    print_matrix(square_t, 3, 3);

    int wide[6] = {1, 2, 3, 4, 5, 6};
    int wide_t[6];
    transpose(wide, wide_t, 2, 3);
    printf("2x3 transposed (now 3x2):\n");
    print_matrix(wide_t, 3, 2);
    return 0;
}
