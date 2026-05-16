#pragma once
#include <cstdint>
#include <cstring>

#define SERVER_PORT 8888
#define MAX_PLAYERS 32
#define PACKET_SIZE 256

enum PacketType : uint8_t {
    PKT_CONNECT = 1,
    PKT_DISCONNECT = 2,
    PKT_PLAYER_UPDATE = 3,
    PKT_PLAYER_JOINED = 4,
    PKT_PLAYER_LEFT = 5,
    PKT_SPAWN = 6
};

struct Vector3 {
    float x, y, z;
};

struct PlayerData {
    uint32_t playerID;
    char name[32];
    Vector3 position;
    Vector3 rotation;
    uint32_t modelID;
    float health;
};

struct Packet {
    PacketType type;
    uint32_t playerID;
    PlayerData data;
};

static_assert(sizeof(Packet) <= PACKET_SIZE, "Packet size too large");
