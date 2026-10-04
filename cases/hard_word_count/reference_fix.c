#include <stdio.h>
#include <string.h>

static int count_words(const char *s) {
    int count = 0;
    int in_word = 0;
    for (size_t i = 0; i < strlen(s); i++) {
        if (s[i] != ' ') {
            if (!in_word) {
                count++;
            }
            in_word = 1;
        } else {
            in_word = 0;
        }
    }
    return count;
}

int main(void) {
    const char *samples[] = {
        "hello world",
        "  leading and trailing  ",
        "one",
        "",
        "a  b   c",
        "   ",
    };
    for (int i = 0; i < 6; i++) {
        printf("\"%s\" -> %d words\n", samples[i], count_words(samples[i]));
    }
    return 0;
}
