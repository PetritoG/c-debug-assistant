#include <stdio.h>

#define CAP 4

typedef struct {
    int data[CAP];
    int top;
} Stack;

static void stack_init(Stack *s) {
    s->top = 0;
}

static int stack_push(Stack *s, int v) {
    if (s->top >= CAP) {
        return 0;
    }
    s->data[s->top++] = v;
    return 1;
}

static int stack_pop(Stack *s, int *out) {
    if (s->top == 0) {
        return 0;
    }
    *out = s->data[--s->top];
    return 1;
}

int main(void) {
    Stack s;
    stack_init(&s);
    for (int v = 10; v <= 60; v += 10) {
        if (stack_push(&s, v)) {
            printf("pushed %d\n", v);
        } else {
            printf("push %d failed: stack full\n", v);
        }
    }
    int x;
    while (stack_pop(&s, &x)) {
        printf("popped %d\n", x);
    }
    return 0;
}
