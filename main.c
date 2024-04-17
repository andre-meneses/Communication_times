// main.c
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <unistd.h>

int main() {
    pid_t pid = fork();

    if (pid == 0) {
        // Executa o servidor
        char *argv[] = { "servidor", NULL };
        execvp("./servidor", argv);
        perror("execvp failed");
        return EXIT_FAILURE;
    } else {
        // Dorme por um segundo para dar tempo do servidor iniciar
        sleep(1);

        // Executa o cliente
        char *argv[] = { "cliente", NULL };
        execvp("./cliente", argv);
        perror("execvp failed");
        return EXIT_FAILURE;
    }

    // Aguarda o processo do servidor finalizar
    wait(NULL);
    return 0;
}

