#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char key[16];
    int value;
} Entry;

static int parse_config(char *text, Entry *out, int max) {
    int n = 0;
    for (char *tok = strtok(text, ";"); tok != NULL && n < max; tok = strtok(NULL, ";")) {
        char *eq = strchr(tok, '=');
        if (eq == NULL) {
            continue;
        }
        *eq = '\0';
        strncpy(out[n].key, tok, sizeof out[n].key - 1);
        out[n].key[sizeof out[n].key - 1] = '\0';
        out[n].value = atoi(eq + 1);
        n++;
    }
    return n;
}

int main(void) {
    char config[] = "width=80;height=24;depth=8;invalid;scale=3";
    Entry entries[8];
    int n = parse_config(config, entries, 8);
    printf("parsed %d entries\n", n);
    for (int i = 0; i < n; i++) {
        printf("%s -> %d\n", entries[i].key, entries[i].value);
    }
    return 0;
}
