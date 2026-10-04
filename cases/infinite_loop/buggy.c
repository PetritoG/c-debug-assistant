#include <stdio.h>

int main(void) {
    int data[5] = {4, 9, 16, 25, 36};
    int i = 0;
    int found = -1;
    while (i < 5) {
        if (data[i] == 25) {
            found = i;
            break;
        }
    }
    printf("Found at index %d\n", found);
    return 0;
}
