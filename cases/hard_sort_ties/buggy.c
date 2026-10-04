#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    const char *name;
    int score;
} Player;

/* Highest score first; players with equal scores are ordered alphabetically. */
static int compare(const void *pa, const void *pb) {
    const Player *a = pa;
    const Player *b = pb;
    if (a->score != b->score) {
        return b->score - a->score;
    }
    return strcmp(b->name, a->name);
}

int main(void) {
    Player players[] = {
        {"mia", 80}, {"zoe", 95}, {"ben", 80}, {"ana", 95}, {"leo", 70}, {"kim", 80},
    };
    int n = (int)(sizeof players / sizeof players[0]);
    qsort(players, (size_t)n, sizeof players[0], compare);
    int rank = 1;
    for (int i = 0; i < n; i++) {
        if (i > 0 && players[i].score != players[i - 1].score) {
            rank = i + 1;
        }
        printf("%d. %s (%d)\n", rank, players[i].name, players[i].score);
    }
    return 0;
}
