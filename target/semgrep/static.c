#include <stdio.h>
#include <string.h>

void copy_input(const char *input)
{
    char buffer[16];

    strcpy(buffer, input);

    printf("Copied: %s\n", buffer);
}

int main(int argc, char **argv) 
{
    if (argc < 2) {
        printf("Usage: %s <input>\n", argv[0]);
        return 1;
    }

    copy_input(argv[1]);

    return 0;
}