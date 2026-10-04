#include <stdio.h>

int main(void) {
    int values[4] = {3, 8, 1, 6};
    int max;
    for (int i = 0; i < 4; i++) {
        if (values[i] > max) {
            max = values[i];
        }
    }
    printf("Max: %d\n", max);
    return 0;
}
