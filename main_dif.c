// main.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
    // Executa o cliente
    char *argv[] = {"./cliente", NULL};
    execvp(argv[0], argv);
    perror("execvp failed");
    
    return EXIT_FAILURE;
}

