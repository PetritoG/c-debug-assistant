#include <stdio.h>

#define N 3

typedef struct {
    const char *owner;
    int cents;
} Account;

static int transfer(Account *from, Account *to, int cents) {
    from->cents -= cents;
    if (from->cents < 0) {
        return 0;
    }
    to->cents += cents;
    return 1;
}

static void report(const Account *accts, int n) {
    for (int i = 0; i < n; i++) {
        printf("%-6s %4d.%02d\n", accts[i].owner, accts[i].cents / 100, accts[i].cents % 100);
    }
}

int main(void) {
    Account accts[N] = {{"alice", 10000}, {"bob", 2550}, {"carol", 0}};
    struct {
        int from;
        int to;
        int cents;
    } ops[] = {
        {0, 1, 2500}, {1, 2, 10000}, {2, 0, 500}, {1, 2, 5050}, {0, 2, 7500}, {0, 1, 1},
    };
    int count = (int)(sizeof ops / sizeof ops[0]);
    for (int i = 0; i < count; i++) {
        int ok = transfer(&accts[ops[i].from], &accts[ops[i].to], ops[i].cents);
        printf("transfer %d: %s -> %s %d cents: %s\n", i + 1, accts[ops[i].from].owner,
               accts[ops[i].to].owner, ops[i].cents, ok ? "ok" : "rejected");
    }
    report(accts, N);
    return 0;
}
