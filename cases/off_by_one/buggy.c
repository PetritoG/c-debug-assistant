#include <stdio.h>

int main(void) {
    int scores[5] = {90, 85, 70, 100, 65};
    int total = 0;
    for (int i = 0; i <= 5; i++) {
        total += scores[i];
    }
    printf("Total: %d\n", total);
    return 0;
}
