#include <stdio.h>

static long long factorial(int n) {
    long long result = 1;
    for (int i = 2; i <= n; i++) {
        result *= i;
    }
    return result;
}

int main(void) {
    printf("n    n!\n");
    for (int n = 0; n <= 20; n += 4) {
        printf("%-4d %lld\n", n, factorial(n));
    }
    return 0;
}
