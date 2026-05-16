#include "gta_memory.h"
#include <TlHelp32.h>
#include <iostream>

GTAMemory::GTAMemory() : processHandle(nullptr), baseAddress(0) {}

GTAMemory::~GTAMemory() {
    if (processHandle) {
        CloseHandle(processHandle);
    }
}

bool GTAMemory::Initialize() {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) return false;

    PROCESSENTRY32 pe32{};
    pe32.dwSize = sizeof(PROCESSENTRY32);

    if (Process32First(snapshot, &pe32)) {
        do {
            if (wcscmp(pe32.szExeFile, L"gta_sa.exe") == 0) {
                processHandle = OpenProcess(PROCESS_VM_READ | PROCESS_VM_WRITE,
                                          FALSE, pe32.th32ProcessID);
                if (!processHandle) break;

                HMODULE modules[256];
                DWORD needed;
                if (EnumProcessModules(processHandle, modules, sizeof(modules), &needed)) {
                    baseAddress = (uintptr_t)modules[0];
                }

                CloseHandle(snapshot);
                return processHandle != nullptr;
            }
        } while (Process32Next(snapshot, &pe32));
    }

    CloseHandle(snapshot);
    return false;
}

bool GTAMemory::ReadMemory(uintptr_t address, void* buffer, size_t size) {
    if (!processHandle) return false;

    SIZE_T bytesRead;
    return ReadProcessMemory(processHandle, (void*)address, buffer, size, &bytesRead)
           && bytesRead == size;
}

bool GTAMemory::WriteMemory(uintptr_t address, const void* data, size_t size) {
    if (!processHandle) return false;

    SIZE_T bytesWritten;
    return WriteProcessMemory(processHandle, (void*)address, (void*)data, size, &bytesWritten)
           && bytesWritten == size;
}

Vector3 GTAMemory::GetPlayerPosition() {
    Vector3 pos = {0, 0, 0};

    uintptr_t playerPed = 0;
    if (!ReadMemory(baseAddress + PLAYER_PED_OFFSET, &playerPed, sizeof(playerPed))) {
        return pos;
    }

    float posData[3];
    if (ReadMemory(playerPed + PLAYER_POS_OFFSET, posData, sizeof(posData))) {
        pos = {posData[0], posData[1], posData[2]};
    }

    return pos;
}

float GTAMemory::GetPlayerHealth() {
    float health = 100.0f;

    uintptr_t playerPed = 0;
    if (!ReadMemory(baseAddress + PLAYER_PED_OFFSET, &playerPed, sizeof(playerPed))) {
        return health;
    }

    ReadMemory(playerPed + PLAYER_HEALTH_OFFSET, &health, sizeof(health));
    return health;
}

Vector3 GTAMemory::GetPlayerRotation() {
    return {0, 0, 0};
}

uint32_t GTAMemory::GetPlayerModel() {
    return 0;
}

void GTAMemory::SetPlayerPosition(const Vector3& pos) {
    uintptr_t playerPed = 0;
    if (!ReadMemory(baseAddress + PLAYER_PED_OFFSET, &playerPed, sizeof(playerPed))) {
        return;
    }

    float posData[3] = {pos.x, pos.y, pos.z};
    WriteMemory(playerPed + PLAYER_POS_OFFSET, posData, sizeof(posData));
}

void GTAMemory::SetPlayerHealth(float health) {
    uintptr_t playerPed = 0;
    if (!ReadMemory(baseAddress + PLAYER_PED_OFFSET, &playerPed, sizeof(playerPed))) {
        return;
    }

    WriteMemory(playerPed + PLAYER_HEALTH_OFFSET, &health, sizeof(health));
}
