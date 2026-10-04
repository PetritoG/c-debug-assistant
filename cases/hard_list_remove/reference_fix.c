#include <stdio.h>
#include <stdlib.h>

typedef struct Node {
    int value;
    struct Node *next;
} Node;

static Node *push_front(Node *head, int value) {
    Node *n = malloc(sizeof *n);
    if (n == NULL) {
        exit(1);
    }
    n->value = value;
    n->next = head;
    return n;
}

static Node *remove_value(Node *head, int value) {
    Node *prev = NULL;
    for (Node *cur = head; cur != NULL; prev = cur, cur = cur->next) {
        if (cur->value == value) {
            if (prev == NULL) {
                head = cur->next;
            } else {
                prev->next = cur->next;
            }
            free(cur);
            return head;
        }
    }
    return head;
}

static void print_list(const Node *head) {
    for (const Node *c = head; c != NULL; c = c->next) {
        printf("%d ", c->value);
    }
    printf("\n");
}

static void free_list(Node *head) {
    while (head != NULL) {
        Node *next = head->next;
        free(head);
        head = next;
    }
}

int main(void) {
    Node *list = NULL;
    for (int i = 1; i <= 5; i++) {
        list = push_front(list, i * 10);
    }
    print_list(list);
    list = remove_value(list, 30);
    print_list(list);
    list = remove_value(list, 50);
    print_list(list);
    free_list(list);
    return 0;
}
