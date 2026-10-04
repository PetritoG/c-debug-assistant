#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *data = malloc(3 * sizeof(int));
    if (data == NULL) {
        return 1;
    }
    data[0] = 10;
    data[1] = 20;
    data[2] = 30;
    int sum = data[0] + data[1] + data[2];
    printf("Sum: %d, first: %d\n", sum, data[0]);
    free(data);
    return 0;
}
