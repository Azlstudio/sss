#include <Windows.h>
#include <thread>
#include <winsock2.h>
#include "gta_memory.h"
#include "ui.h"
#include "../../include/protocol.h"

#pragma comment(lib, "ws2_32.lib")

class InjectClient {
private:
    GTAMemory gtaMemory;
    GameUI ui;
    SOCKET socket;
    sockaddr_in serverAddr;
    uint32_t playerID = 0;
    bool connected = false;
    bool running = true;
    PlayerData localPlayer;
    std::map<uint32_t, RemotePlayer> remotePlayers;

public:
    InjectClient() : socket(INVALID_SOCKET) {
        memset(&serverAddr, 0, sizeof(serverAddr));
    }

    bool Initialize() {
        // Initialize GTA Memory Access
        if (!gtaMemory.Initialize()) {
            MessageBoxA(nullptr, "Error: No se pudo acceder a GTA San Andreas",
                       "Error", MB_OK | MB_ICONERROR);
            return false;
        }

        // Initialize Networking
        WSADATA wsaData;
        if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
            return false;
        }

        socket = ::socket(AF_INET, SOCK_DGRAM, IPPROTO_UDP);
        if (socket == INVALID_SOCKET) {
            return false;
        }

        serverAddr.sin_family = AF_INET;
        serverAddr.sin_port = htons(SERVER_PORT);
        serverAddr.sin_addr.s_addr = inet_addr("127.0.0.1");

        // Connect to server
        memset(&localPlayer, 0, sizeof(localPlayer));
        strncpy_s(localPlayer.name, "SAPlayer", sizeof(localPlayer.name) - 1);
        localPlayer.modelID = 0;
        localPlayer.position = {0, 0, 0};
        localPlayer.health = 100.0f;

        Packet connectPkt{};
        connectPkt.type = PKT_CONNECT;
        connectPkt.data = localPlayer;

        if (sendto(socket, (char*)&connectPkt, sizeof(Packet), 0,
                   (sockaddr*)&serverAddr, sizeof(serverAddr)) != SOCKET_ERROR) {
            connected = true;
            ui.SetConnectionStatus("Conectado");
        } else {
            connected = false;
            ui.SetConnectionStatus("Error de conexion");
        }

        return true;
    }

    void NetworkLoop() {
        char buffer[PACKET_SIZE];
        sockaddr_in addr{};
        int addrLen = sizeof(addr);

        u_long mode = 1;
        ioctlsocket(socket, FIONBIO, &mode);

        while (running) {
            int recvLen = recvfrom(socket, buffer, PACKET_SIZE, 0,
                                  (sockaddr*)&addr, &addrLen);

            if (recvLen > 0) {
                Packet* pkt = (Packet*)buffer;
                HandleNetworkPacket(pkt);
            }

            std::this_thread::sleep_for(std::chrono::milliseconds(10));
        }
    }

    void GameLoop() {
        while (running) {
            // Read local player data from GTA memory
            localPlayer.position = gtaMemory.GetPlayerPosition();
            localPlayer.health = gtaMemory.GetPlayerHealth();

            // Send position update to server
            if (connected && playerID != 0) {
                Packet updatePkt{};
                updatePkt.type = PKT_PLAYER_UPDATE;
                updatePkt.playerID = playerID;
                updatePkt.data = localPlayer;

                sendto(socket, (char*)&updatePkt, sizeof(Packet), 0,
                       (sockaddr*)&serverAddr, sizeof(serverAddr));
            }

            // Update remote players in GTA world
            UpdateRemotePlayersInGame();

            // Render UI
            ui.RenderPlayerInfo(localPlayer.position, localPlayer.health);

            std::this_thread::sleep_for(std::chrono::milliseconds(100));
        }
    }

    void HandleNetworkPacket(Packet* pkt) {
        switch (pkt->type) {
            case PKT_CONNECT:
                playerID = pkt->playerID;
                ui.SetConnectionStatus("Conectado");
                break;

            case PKT_PLAYER_UPDATE: {
                if (pkt->playerID != playerID) {
                    RemotePlayer remote;
                    remote.id = pkt->playerID;
                    remote.name = pkt->data.name;
                    remote.position = pkt->data.position;
                    remote.health = pkt->data.health;
                    remote.visible = true;

                    float dx = remote.position.x - localPlayer.position.x;
                    float dy = remote.position.y - localPlayer.position.y;
                    float dz = remote.position.z - localPlayer.position.z;
                    remote.distance = sqrt(dx*dx + dy*dy + dz*dz);

                    remotePlayers[pkt->playerID] = remote;
                    ui.UpdateRemotePlayer(remote);
                }
                break;
            }

            case PKT_PLAYER_JOINED:
                ui.AddChatMessage("[SERVER] " + std::string(pkt->data.name) + " se unio");
                ui.SetPlayerCount(remotePlayers.size() + 1);
                break;

            case PKT_PLAYER_LEFT:
                ui.AddChatMessage("[SERVER] Un jugador se fue");
                remotePlayers.erase(pkt->playerID);
                ui.SetPlayerCount(remotePlayers.size() + 1);
                break;
        }
    }

    void UpdateRemotePlayersInGame() {
        for (const auto& [id, player] : remotePlayers) {
            if (player.distance < 300.0f) {
                // Would spawn/update player ped in GTA here
                // This requires creating a ped and synchronizing position
            }
        }
    }

    void Shutdown() {
        running = false;

        if (connected && playerID != 0) {
            Packet disconnectPkt{};
            disconnectPkt.type = PKT_DISCONNECT;
            disconnectPkt.playerID = playerID;
            sendto(socket, (char*)&disconnectPkt, sizeof(Packet), 0,
                   (sockaddr*)&serverAddr, sizeof(serverAddr));
        }

        if (socket != INVALID_SOCKET) {
            closesocket(socket);
        }
        WSACleanup();
    }
};

InjectClient* g_pInjectClient = nullptr;

DWORD WINAPI MainThread(LPVOID lpParam) {
    g_pInjectClient = new InjectClient();

    if (!g_pInjectClient->Initialize()) {
        delete g_pInjectClient;
        return 0;
    }

    std::thread networkThread(&InjectClient::NetworkLoop, g_pInjectClient);
    std::thread gameThread(&InjectClient::GameLoop, g_pInjectClient);

    networkThread.join();
    gameThread.join();

    g_pInjectClient->Shutdown();
    delete g_pInjectClient;

    return 0;
}

BOOL APIENTRY DllMain(HMODULE hModule, DWORD ul_reason_for_call, LPVOID lpReserved) {
    switch (ul_reason_for_call) {
        case DLL_PROCESS_ATTACH: {
            DisableThreadLibraryCalls(hModule);
            HANDLE hThread = CreateThread(nullptr, 0, MainThread, nullptr, 0, nullptr);
            if (hThread) CloseHandle(hThread);
            break;
        }

        case DLL_PROCESS_DETACH:
            if (g_pInjectClient) {
                g_pInjectClient->Shutdown();
                delete g_pInjectClient;
            }
            break;
    }

    return TRUE;
}
