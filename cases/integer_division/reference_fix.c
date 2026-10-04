#include <stdio.h>

static double average(const int *values, int n) {
    int total = 0;
    for (int i = 0; i < n; i++) {
        total += values[i];
    }
    return (double)total / n;
}

int main(void) {
    int grades[4] = {7, 8, 9, 9};
    printf("Average: %.2f\n", average(grades, 4));
    return 0;
}
