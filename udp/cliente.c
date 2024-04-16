// cliente.c
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

void send_packets(int sockfd, struct sockaddr_in *servaddr, int packet_size, int num_packets);

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
    servaddr.sin_addr.s_addr = inet_addr("127.0.0.1");

    int packet_sizes[] = PACKET_SIZES;
    int num_sizes = sizeof(packet_sizes) / sizeof(packet_sizes[0]);
    for (int i = 0; i < num_sizes; i++) {
        send_packets(sockfd, &servaddr, packet_sizes[i], 30);
    }

    close(sockfd);
    return 0;
}

void send_packets(int sockfd, struct sockaddr_in *servaddr, int packet_size, int num_packets) {
    char packet[packet_size];
    memset(packet, 'A', packet_size);

    struct timespec start, end;
    long long total_time = 0;

    for (int i = 0; i < num_packets; i++) {
        clock_gettime(CLOCK_REALTIME, &start);

        if (sendto(sockfd, packet, packet_size, 0, (const struct sockaddr *)servaddr, sizeof(*servaddr)) < 0) {
            perror("sendto failed");
            continue;
        }

        clock_gettime(CLOCK_REALTIME, &end);
        long long time_ns = (end.tv_sec - start.tv_sec) * 1000000000LL + (end.tv_nsec - start.tv_nsec);
        total_time += time_ns;

        printf("Packet size: %d bytes, Time taken: %lld ns\n", packet_size, time_ns);
    }

    long long average_time = total_time / num_packets;
    printf("Average time for packet size %d bytes: %lld ns\n", packet_size, average_time);
}

