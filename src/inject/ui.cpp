#include "ui.h"
#include <cmath>
#include <iomanip>
#include <sstream>

GameUI::GameUI() {
    chatMessages.push_back("[SERVER] Conectado al servidor multiplayer");
    chatMessages.push_back("[SYSTEM] Presiona F1 para mostrar/ocultar la UI");
}

GameUI::~GameUI() {}

void GameUI::Render() {
    if (!showUI) return;

    RenderConnectionStatus();
    if (showPlayers) RenderPlayerList();
    if (showChat) RenderChat();
    if (showMap) RenderMiniMap();
}

void GameUI::RenderConnectionStatus() {
    std::stringstream ss;
    ss << std::fixed << std::setprecision(1);
    ss << "Ping: " << ping << "ms | Jugadores: " << playerCount
       << " | Estado: " << connectionStatus;

    // Top-left corner status
}

void GameUI::RenderPlayerList() {
    std::stringstream title;
    title << "Jugadores Conectados (" << remotePlayers.size() << ")";

    // Player list window
    // Would use ImGui::Begin() and ImGui::End() here
    // This is pseudo-code for the UI structure

    for (const auto& player : remotePlayers) {
        std::stringstream ss;
        ss << player.name << " [" << player.id << "]";
        ss << " | Salud: " << (int)player.health << "%";
        ss << " | Distancia: " << (int)player.distance << "m";

        if (player.health < 30) {
            // Show as critical (red)
        }
    }
}

void GameUI::RenderChat() {
    // Chat window
    // Would display last 10 messages

    for (int i = std::max(0, (int)chatMessages.size() - 10);
         i < (int)chatMessages.size(); ++i) {
        // ImGui::TextWrapped(chatMessages[i].c_str());
    }

    // Input field for chat message
    // ImGui::InputText("##chat_input", &inputBuffer);
}

void GameUI::RenderMiniMap() {
    // Mini map in bottom-right
    // Shows local player position and nearby players
    // Grid-based with player icons

    // Local player at center
    // Red dots for nearby players
    // Text labels for names
}

void GameUI::RenderPlayerInfo(const Vector3& localPos, float health) {
    std::stringstream ss;
    ss << std::fixed << std::setprecision(2);
    ss << "Posicion: X:" << localPos.x << " Y:" << localPos.y
       << " Z:" << localPos.z;
    ss << " | Salud: " << (int)health << "%";

    // Bottom-left corner info
}

void GameUI::UpdateRemotePlayer(const RemotePlayer& player) {
    for (auto& p : remotePlayers) {
        if (p.id == player.id) {
            p.position = player.position;
            p.health = player.health;
            p.visible = player.visible;
            return;
        }
    }

    remotePlayers.push_back(player);
}

void GameUI::AddChatMessage(const std::string& message) {
    if (chatMessages.size() > 100) {
        chatMessages.erase(chatMessages.begin());
    }
    chatMessages.push_back(message);
}

void GameUI::SetConnectionStatus(const std::string& status) {
    connectionStatus = status;
}

void GameUI::SetPlayerCount(int count) {
    playerCount = count;
}

void GameUI::SetPing(float ms) {
    ping = ms;
}
