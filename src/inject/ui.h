#pragma once
#include "../../include/protocol.h"
#include <vector>
#include <string>
#include <map>

struct RemotePlayer {
    uint32_t id;
    std::string name;
    Vector3 position;
    float health;
    float distance;
    bool visible;
};

class GameUI {
private:
    std::vector<RemotePlayer> remotePlayers;
    bool showUI = true;
    bool showChat = true;
    bool showMap = true;
    bool showPlayers = true;

    std::vector<std::string> chatMessages;
    std::string inputBuffer;
    std::string connectionStatus = "Disconnected";
    int playerCount = 0;
    float ping = 0.0f;

public:
    GameUI();
    ~GameUI();

    void Render();
    void RenderMainWindow();
    void RenderPlayerList();
    void RenderChat();
    void RenderMiniMap();
    void RenderConnectionStatus();
    void RenderPlayerInfo(const Vector3& localPos, float health);

    void UpdateRemotePlayer(const RemotePlayer& player);
    void AddChatMessage(const std::string& message);
    void SetConnectionStatus(const std::string& status);
    void SetPlayerCount(int count);
    void SetPing(float ms);

    void ToggleUI() { showUI = !showUI; }
    void ToggleChat() { showChat = !showChat; }
    void ToggleMap() { showMap = !showMap; }

    const std::vector<RemotePlayer>& GetRemotePlayers() const { return remotePlayers; }
    std::string GetInputBuffer() const { return inputBuffer; }
    void ClearInputBuffer() { inputBuffer.clear(); }
};
