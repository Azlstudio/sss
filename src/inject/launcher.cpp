#include <Windows.h>
#include <TlHelp32.h>
#include <cstdio>
#include <cstring>

bool InjectDLL(const char* dllPath, const char* processName) {
    HANDLE snapshot = CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0);
    if (snapshot == INVALID_HANDLE_VALUE) {
        printf("Error: No se pudo crear snapshot de procesos\n");
        return false;
    }

    PROCESSENTRY32 pe32{};
    pe32.dwSize = sizeof(PROCESSENTRY32);
    DWORD targetPID = 0;

    if (Process32First(snapshot, &pe32)) {
        do {
            if (wcscmp(pe32.szExeFile, (const wchar_t*)processName) == 0) {
                targetPID = pe32.th32ProcessID;
                break;
            }
        } while (Process32Next(snapshot, &pe32));
    }

    CloseHandle(snapshot);

    if (targetPID == 0) {
        printf("Error: Proceso %s no encontrado. Asegurate de que GTA SA esta abierto.\n", processName);
        return false;
    }

    printf("Proceso encontrado: PID %d\n", targetPID);

    HANDLE hProcess = OpenProcess(PROCESS_CREATE_THREAD | PROCESS_QUERY_INFORMATION |
                                  PROCESS_VM_OPERATION | PROCESS_VM_WRITE |
                                  PROCESS_VM_READ, FALSE, targetPID);

    if (!hProcess) {
        printf("Error: No se pudo abrir el proceso\n");
        return false;
    }

    // Allocate memory for DLL path
    size_t dllPathLen = strlen(dllPath) + 1;
    LPVOID pDllPath = VirtualAllocEx(hProcess, nullptr, dllPathLen,
                                     MEM_COMMIT | MEM_RESERVE, PAGE_READWRITE);

    if (!pDllPath) {
        printf("Error: No se pudo asignar memoria\n");
        CloseHandle(hProcess);
        return false;
    }

    // Write DLL path to target process
    if (!WriteProcessMemory(hProcess, pDllPath, (void*)dllPath, dllPathLen, nullptr)) {
        printf("Error: No se pudo escribir ruta de DLL\n");
        VirtualFreeEx(hProcess, pDllPath, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return false;
    }

    // Get address of LoadLibraryA
    HMODULE hKernel32 = GetModuleHandleA("kernel32.dll");
    LPVOID pLoadLibraryA = (LPVOID)GetProcAddress(hKernel32, "LoadLibraryA");

    if (!pLoadLibraryA) {
        printf("Error: No se pudo obtener LoadLibraryA\n");
        VirtualFreeEx(hProcess, pDllPath, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return false;
    }

    // Create remote thread to load DLL
    HANDLE hThread = CreateRemoteThread(hProcess, nullptr, 0,
                                        (LPTHREAD_START_ROUTINE)pLoadLibraryA,
                                        pDllPath, 0, nullptr);

    if (!hThread) {
        printf("Error: No se pudo crear thread remoto\n");
        VirtualFreeEx(hProcess, pDllPath, 0, MEM_RELEASE);
        CloseHandle(hProcess);
        return false;
    }

    printf("Esperando inyeccion...\n");
    WaitForSingleObject(hThread, INFINITE);

    VirtualFreeEx(hProcess, pDllPath, 0, MEM_RELEASE);
    CloseHandle(hThread);
    CloseHandle(hProcess);

    printf("DLL inyectada exitosamente!\n");
    return true;
}

int main() {
    printf("=== GTA San Andreas Multiplayer Launcher ===\n\n");
    printf("Asegurate de que GTA San Andreas esta abierto...\n");
    printf("Presiona cualquier tecla para continuar...\n\n");
    getchar();

    char dllPath[MAX_PATH];
    GetCurrentDirectoryA(MAX_PATH, dllPath);
    strcat_s(dllPath, "\\sa_inject.dll");

    printf("Ruta de DLL: %s\n", dllPath);

    if (!InjectDLL(dllPath, "gta_sa.exe")) {
        printf("Error: Inyeccion fallida\n");
        getchar();
        return 1;
    }

    printf("Puedes cerrar esta ventana.\n");
    printf("La UI deberia aparecer en el juego (F1 para mostrar/ocultar)\n");
    getchar();

    return 0;
}
