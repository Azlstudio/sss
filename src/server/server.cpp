#include "../../include/protocol.h"
#include <iostream>
#include <winsock2.h>
#include <thread>
#include <vector>
#include <mutex>
#include <map>

#pragma comment(lib, "ws2_32.lib")

struct ConnectedPlayer {
    uint32_t id;
    SOCKET socket;
    PlayerData data;
    bool active;
};

class GameServer {
private:
    SOCKET serverSocket;
    std::vector<ConnectedPlayer> players;
    std::mutex playersMutex;
    uint32_t nextPlayerID = 1;

public:
    GameServer() : serverSocket(INVALID_SOCKET) {}

    bool Initialize() {
        WSADATA wsaData;
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
            std::cerr << "WSAStartup failed\n";
            return false;
        }

        serverSocket = socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
        if (serverSocket == INVALID_SOCKET) {
            std::cerr << "Socket creation failed\n";
            WSACleanup();
            return false;
        }

        sockaddr_in serverAddr{};
        serverAddr.sin_family = AF_INET;
        serverAddr.sin_addr.s_addr = htonl(INADDR_ANY);
        serverAddr.sin_port = htons(SERVER_PORT);

        if (bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
            std::cerr << "Bind failed: " << WSAGetLastError() << "\n";
            closesocket(serverSocket);
            WSACleanup();
            return false;
        }

        std::cout << "Server initialized on port " << SERVER_PORT << "\n";
        return true;
    }

    void Run() {
        std::cout << "Server running... Waiting for connections\n";

        char buffer[PACKET_SIZE];
        sockaddr_in clientAddr{};
        int clientAddrLen = sizeof(clientAddr);

        while (true) {
            int recvLen = recvfrom(serverSocket, buffer, PACKET_SIZE, 0,
                                  (sockaddr*)&clientAddr, &clientAddrLen);

            if (recvLen == SOCKET_ERROR) {
                continue;
            }

            Packet* pkt = (Packet*)buffer;
            HandlePacket(pkt, clientAddr);
        }
    }

    void HandlePacket(Packet* pkt, sockaddr_in clientAddr) {
        std::lock_guard<std::mutex> lock(playersMutex);

        switch (pkt->type) {
            case PKT_CONNECT: {
                uint32_t playerID = nextPlayerID++;
                pkt->playerID = playerID;

                std::cout << "Player connected: " << pkt->data.name
                         << " (ID: " << playerID << ")\n";

                ConnectedPlayer player;
                player.id = playerID;
                player.data = pkt->data;
                player.active = true;
                players.push_back(player);

                BroadcastPacket(*pkt, nullptr);
                break;
            }

            case PKT_PLAYER_UPDATE: {
                for (auto& p : players) {
                    if (p.id == pkt->playerID) {
                        p.data = pkt->data;
                        BroadcastPacket(*pkt, nullptr);
                        break;
                    }
                }
                break;
            }

            case PKT_DISCONNECT: {
                players.erase(
                    std::remove_if(players.begin(), players.end(),
                        [&](const ConnectedPlayer& p) { return p.id == pkt->playerID; }),
                    players.end()
                );
                std::cout << "Player disconnected: ID " << pkt->playerID << "\n";
                BroadcastPacket(*pkt, nullptr);
                break;
            }
        }
    }

    void BroadcastPacket(const Packet& pkt, sockaddr_in* exclude) {
        for (const auto& player : players) {
            if (exclude && player.id == *(uint32_t*)exclude) continue;

            char buffer[PACKET_SIZE];
            memcpy(buffer, &pkt, sizeof(Packet));
        }
    }

    void Shutdown() {
        if (serverSocket != INVALID_SOCKET) {
            closesocket(serverSocket);
        }
        WSACleanup();
    }
};

int main() {
    GameServer server;
    if (!server.Initialize()) {
        return 1;
    }

    server.Run();
    server.Shutdown();
    return 0;
}
