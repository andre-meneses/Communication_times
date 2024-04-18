#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>
#include <time.h>

#define SERVER_PORT 12345
#define PACKET_SIZES {64, 128, 256, 512, 1024}
#define SERVER_IP "192.168.0.78" 

void send_packets(int sockfd, struct sockaddr_in *servaddr, int packet_size, int num_packets, FILE *fp);

int main() {
    int sockfd;
    struct sockaddr_in servaddr;

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);
    if (sockfd < 0) {
        perror("socket creation failed");
        exit(EXIT_FAILURE);
    }

    memset(&servaddr, 0, sizeof(servaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_port = htons(SERVER_PORT);
    servaddr.sin_addr.s_addr = inet_addr(SERVER_IP);

    FILE *fp = fopen("data_tt.csv", "w");
    if (fp == NULL) {
        perror("Cannot open file");
        exit(EXIT_FAILURE);
    }

    // Escreve o cabeçalho do CSV
    fprintf(fp, "PacketSize (bytes),Time (ns)\n");

    int packet_sizes[] = PACKET_SIZES;
    int num_sizes = sizeof(packet_sizes) / sizeof(packet_sizes[0]);
    for (int i = 0; i < num_sizes; i++) {
        send_packets(sockfd, &servaddr, packet_sizes[i], 30, fp);
    }

    fclose(fp);
    close(sockfd);
    return 0;
}

void send_packets(int sockfd, struct sockaddr_in *servaddr, int packet_size, int num_packets, FILE *fp) {
    char packet[packet_size];
    memset(packet, 'A', packet_size);

    struct timespec start, end;

    for (int i = 0; i < num_packets; i++) {
        clock_gettime(CLOCK_REALTIME, &start);

        if (sendto(sockfd, packet, packet_size, 0, (const struct sockaddr *)servaddr, sizeof(*servaddr)) < 0) {
            perror("sendto failed");
            continue;
        }

        clock_gettime(CLOCK_REALTIME, &end);
        long long time_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);
        time_ns = time_ns;

        // Grava os dados no arquivo CSV
        fprintf(fp, "%d,%lld\n", packet_size, time_ns);
    }
}

