#include <stdio.h>

static int binary_search(const int *a, int n, int key) {
    int lo = 0;
    int hi = n - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        if (a[mid] == key) {
            return mid;
        } else if (a[mid] < key) {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    return -1;
}

int main(void) {
    int sorted[] = {2, 5, 8, 12, 16, 23, 38, 56, 72, 91};
    int n = (int)(sizeof sorted / sizeof sorted[0]);
    int keys[] = {2, 23, 91, 7, 56, 72};
    for (int i = 0; i < 6; i++) {
        printf("search %d -> %d\n", keys[i], binary_search(sorted, n, keys[i]));
    }
    int single[] = {42};
    printf("search 42 in single -> %d\n", binary_search(single, 1, 42));
    return 0;
}
