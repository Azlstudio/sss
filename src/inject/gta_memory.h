#pragma once
#include <cstdint>
#include <Windows.h>
#include "../../include/protocol.h"

class GTAMemory {
private:
    HANDLE processHandle;
    uintptr_t baseAddress;

    static constexpr uintptr_t PLAYER_PED_OFFSET = 0xB6F5F0;
    static constexpr uintptr_t PLAYER_POS_OFFSET = 0x4C;
    static constexpr uintptr_t PLAYER_HEALTH_OFFSET = 0x540;

public:
    GTAMemory();
    ~GTAMemory();

    bool Initialize();
    bool ReadMemory(uintptr_t address, void* buffer, size_t size);
    bool WriteMemory(uintptr_t address, const void* data, size_t size);

    Vector3 GetPlayerPosition();
    float GetPlayerHealth();
    Vector3 GetPlayerRotation();
    uint32_t GetPlayerModel();

    void SetPlayerPosition(const Vector3& pos);
    void SetPlayerHealth(float health);

    uintptr_t GetBaseAddress() const { return baseAddress; }
};
