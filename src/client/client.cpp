#include "../../include/protocol.h"
#include <iostream>
#include <winsock2.h>
#include <thread>
#include <cstring>

#pragma comment(lib, "ws2_32.lib")

class GameClient {
private:
    SOCKET socket;
    sockaddr_in serverAddr;
    uint32_t playerID;
    PlayerData localPlayer;
    bool connected;

public:
    GameClient() : socket(INVALID_SOCKET), playerID(0), connected(false) {}

    bool Connect(const char* serverIP, const char* playerName) {
        WSADATA wsaData;
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
            std::cerr << "WSAStartup failed\n";
            return false;
        }

        socket = ::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
        if (socket == INVALID_SOCKET) {
            std::cerr << "Socket creation failed\n";
            WSACleanup();
            return false;
        }

        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(SERVER_PORT);
        serverAddr.sin_addr.s_addr = inet_addr(serverIP);

        memset(&localPlayer, 0, sizeof(localPlayer));
        strncpy_s(localPlayer.name, playerName, sizeof(localPlayer.name) - 1);
        localPlayer.modelID = 0;
        localPlayer.position = {0, 0, 0};
        localPlayer.rotation = {0, 0, 0};
        localPlayer.health = 100.0f;

        Packet connectPkt{};
        connectPkt.type = PKT_CONNECT;
        connectPkt.data = localPlayer;

        if (sendto(socket, (char*)&connectPkt, sizeof(Packet), 0,
                   (sockaddr*)&serverAddr, sizeof(serverAddr)) == SOCKET_ERROR) {
            std::cerr << "Failed to send connect packet\n";
            return false;
        }

        std::cout << "Connected to server: " << serverIP << ":" << SERVER_PORT << "\n";
        std::cout << "Player name: " << playerName << "\n";
        connected = true;

        std::thread recvThread(&GameClient::ReceiveLoop, this);
        recvThread.detach();

        return true;
    }

    void ReceiveLoop() {
        char buffer[PACKET_SIZE];
        sockaddr_in addr{};
        int addrLen = sizeof(addr);

        while (connected) {
            int recvLen = recvfrom(socket, buffer, PACKET_SIZE, 0,
                                  (sockaddr*)&addr, &addrLen);

            if (recvLen > 0) {
                Packet* pkt = (Packet*)buffer;
                HandlePacket(pkt);
            }
        }
    }

    void HandlePacket(const Packet* pkt) {
        switch (pkt->type) {
            case PKT_CONNECT:
                playerID = pkt->playerID;
                std::cout << "Assigned player ID: " << playerID << "\n";
                break;

            case PKT_PLAYER_UPDATE:
                if (pkt->playerID != playerID) {
                    std::cout << "Player " << pkt->playerID << " at ("
                             << pkt->data.position.x << ", "
                             << pkt->data.position.y << ", "
                             << pkt->data.position.z << ")\n";
                }
                break;

            case PKT_PLAYER_JOINED:
                std::cout << "Player joined: " << pkt->data.name << "\n";
                break;

            case PKT_PLAYER_LEFT:
                std::cout << "Player left: ID " << pkt->playerID << "\n";
                break;
        }
    }

    void UpdatePosition(float x, float y, float z) {
        if (!connected) return;

        localPlayer.position = {x, y, z};

        Packet updatePkt{};
        updatePkt.type = PKT_PLAYER_UPDATE;
        updatePkt.playerID = playerID;
        updatePkt.data = localPlayer;

        sendto(socket, (char*)&updatePkt, sizeof(Packet), 0,
               (sockaddr*)&serverAddr, sizeof(serverAddr));
    }

    void SimulateMovement() {
        std::cout << "\n=== Simulating player movement ===\n";
        for (int i = 0; i < 10; i++) {
            float x = 100.0f + (i * 10.0f);
            float y = 200.0f + (i * 5.0f);
            float z = 10.0f;

            UpdatePosition(x, y, z);
            std::cout << "Sent position: (" << x << ", " << y << ", " << z << ")\n";

            std::this_thread::sleep_for(std::chrono::milliseconds(500));
        }
    }

    void Disconnect() {
        if (!connected) return;

        Packet disconnectPkt{};
        disconnectPkt.type = PKT_DISCONNECT;
        disconnectPkt.playerID = playerID;

        sendto(socket, (char*)&disconnectPkt, sizeof(Packet), 0,
               (sockaddr*)&serverAddr, sizeof(serverAddr));

        connected = false;

        if (socket != INVALID_SOCKET) {
            closesocket(socket);
        }
        WSACleanup();

        std::cout << "Disconnected from server\n";
    }

    ~GameClient() {
        Disconnect();
    }
};

int main() {
    GameClient client;

    std::cout << "=== GTA San Andreas Multiplayer Client ===\n";
    std::cout << "Connecting to server...\n";

    if (!client.Connect("127.0.0.1", "Player1")) {
        std::cerr << "Failed to connect\n";
        return 1;
    }

    std::this_thread::sleep_for(std::chrono::seconds(1));

    client.SimulateMovement();

    std::cout << "\nPress Enter to disconnect...\n";
    std::cin.get();

    client.Disconnect();

    return 0;
}
