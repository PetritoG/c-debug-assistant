#include <stdio.h>
#include <string.h>

static const char *find_name(const char *names[], int n, const char *prefix) {
    for (int i = 0; i < n; i++) {
        if (strncmp(names[i], prefix, strlen(prefix)) == 0) {
            return names[i];
        }
    }
    return NULL;
}

int main(void) {
    const char *names[] = {"alice", "bob", "carol"};
    const char *found = find_name(names, 3, "da");
    if (found == NULL) {
        printf("No name found\n");
    } else {
        printf("Found name of length %zu\n", strlen(found));
    }
    return 0;
}
