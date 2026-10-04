#include <stdio.h>

static int factorial(int n) {
    int result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main(void) {
    printf("n    n!\n");
    for (int n = 0; n <= 20; n += 4) {
        printf("%-4d %d\n", n, factorial(n));
    }
    return 0;
}
