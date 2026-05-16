# Integrated Launcher Guide - GTA San Andreas Multiplayer

## Concepto

El launcher **automáticamente inicia GTA San Andreas en background** y lo integra dentro de la interfaz del launcher. El usuario nunca ve una ventana separada de GTA - todo funciona dentro del launcher.

## Arquitectura

```
Launcher (GTASALauncher.exe)
    │
    ├─ GameHost (gestiona proceso GTA SA)
    │   ├─ StartGameInBackground()    → Inicia GTA sin ventana visible
    │   ├─ EmbedGameWindow()          → Integra ventana de GTA en el launcher
    │   ├─ InjectMultiplayerDLL()     → Inyecta DLL del multiplayer
    │   └─ ConnectToServer()          → Conecta a servidor
    │
    └─ MainWindowIntegrated
        ├─ Barra lateral izquierda (navegación)
        ├─ Barra lateral derecha (chat + info)
        └─ Centro: Ventana de GTA San Andreas incrustada
```

## Flujo de Ejecución

### 1. Inicio del Launcher
```
Usuario ejecuta GTASALauncher.exe
    ↓
Launcher verifica GTA San Andreas instalado
    ↓
GameHost inicia GTA en background (sin ventana visible)
    ↓
GTA se mantiene ejecutándose esperando comandos
    ↓
Launcher muestra interfaz con overlay "Selecciona servidor"
```

### 2. Conectarse a Servidor
```
Usuario selecciona servidor en launcher
    ↓
Usuario hace click en "Conectar"
    ↓
GameHost incrusta ventana de GTA en el launcher
    ↓
GameHost inyecta DLL del multiplayer en GTA
    ↓
DLL se conecta al servidor
    ↓
GTA muestra el mundo de multiplayer
    ↓
Usuario está jugando dentro del launcher
```

### 3. Cerrar Sesión / Cambiar Servidor
```
Usuario hace click en "Salir del Juego"
    ↓
Overlay "Selecciona servidor" reaparece
    ↓
GTA sigue ejecutándose en background
    ↓
Usuario puede seleccionar otro servidor
    ↓
Vuelve al paso 2
```

## Componentes Clave

### GameHost.cs

**Responsabilidades:**
- Iniciar GTA San Andreas sin ventana visible
- Encontrar la ventana de GTA
- Integrar (embed) la ventana en el launcher usando Windows API
- Inyectar la DLL del multiplayer
- Gestionar la conexión a servidor

**Métodos principales:**

```csharp
// Inicia GTA en background
StartGameInBackground(string gtaSAPath)

// Integra ventana de GTA en el launcher
EmbedGameWindow(IntPtr parentHandle, int x, int y, int width, int height)

// Inyecta DLL en GTA
InjectMultiplayerDLL(string dllPath)

// Conecta a servidor
ConnectToServer(string ip, ushort port, string dllPath)

// Para de forma segura
StopGame()
```

**Windows API Utilizada:**
- `SetParent()` - Hace que la ventana de GTA sea hijo del launcher
- `ShowWindow()` - Muestra/oculta la ventana
- `MoveWindow()` - Redimensiona y posiciona la ventana
- `VirtualAllocEx()` - Asigna memoria en GTA
- `WriteProcessMemory()` - Escribe en memoria de GTA
- `CreateRemoteThread()` - Ejecuta código en GTA (para cargar DLL)

### MainWindowIntegrated.xaml

**Layout:**
```
┌────────────────────────────────────────────────────┐
│ SA MULTIPLAYER                                      │
├────────────────────────────────────────────────────┤
│         │                                          │
│  Navegación                                        │
│  • Home                                            │
│  • Servidores                                      │
│  • Favoritos                                       │
│  • Config                                          │
│         │                                          │
│  Estado │  ├─ Servidor Info                       │
│  Ping   │  │                                       │
│  Status │  ├─ Chat                                │
│         │  │  [Mensaje 1]                         │
│         │  │  [Mensaje 2]                         │
│         │  │  Input: ____                         │
│         │  │                                       │
│         │  ├─ Jugadores                           │
│         │  │  Player1 (Nivel 45)                  │
│         │  │  Player2 (Nivel 32)                  │
│         │  │                                       │
│         │  ├─ GTA WINDOW (incrustado)             │
│         │  │                                       │
│         │  │  [Mundo de GTA aquí]                 │
│         │  │                                       │
└────────────────────────────────────────────────────┘
```

**Áreas:**

1. **Left Sidebar (280px)**
   - Logo y título
   - Estado actual (Conectado/Desconectado)
   - Navegación (Home, Servidores, Favoritos, Config)
   - Botones de control (Salir, Reportar)

2. **Right Sidebar (350px)**
   - Información del servidor actual
   - Sistema de chat
   - Lista de jugadores conectados

3. **Center Area**
   - Ventana de GTA San Andreas incrustada
   - Barra de estado superior (F1 para UI, ESC para opciones)
   - Overlay cuando no hay servidor conectado

## Proceso de Embedding

### Paso 1: Encontrar ventana de GTA
```cpp
IntPtr hWnd = FindWindow(null, "GTA: San Andreas");
```

### Paso 2: Cambiar estilos de ventana
```cpp
SetWindowLong(hWnd, GWL_STYLE, WS_CHILD);  // Hace que sea ventana hijo
```

### Paso 3: Establecer padre
```cpp
SetParent(hWnd, launcherWindowHandle);  // El launcher es el padre
```

### Paso 4: Redimensionar y posicionar
```cpp
MoveWindow(hWnd, 0, 0, width, height, true);  // Rellena el área
```

## Inyección de DLL

Cuando el usuario se conecta a un servidor:

1. **Obtener handle del proceso GTA**
   ```cpp
   IntPtr hProcess = gameProcess.Handle;
   ```

2. **Asignar memoria para la ruta de DLL**
   ```cpp
   IntPtr allocMemAddress = VirtualAllocEx(hProcess, IntPtr.Zero, 
       dllPath.Length + 1, 0x1000, 0x04);
   ```

3. **Escribir ruta de DLL en esa memoria**
   ```cpp
   WriteProcessMemory(hProcess, allocMemAddress, dllPath, 
       dllPath.Length, out _);
   ```

4. **Obtener dirección de LoadLibraryA**
   ```cpp
   IntPtr loadLibAddr = GetProcAddress(
       GetModuleHandle("kernel32.dll"), "LoadLibraryA");
   ```

5. **Crear thread remoto para ejecutar LoadLibraryA**
   ```cpp
   IntPtr hThread = CreateRemoteThread(hProcess, IntPtr.Zero, 0, 
       loadLibAddr, allocMemAddress, 0, IntPtr.Zero);
   ```

6. **Esperar a que se cargue**
   ```cpp
   WaitForSingleObject(hThread, 5000);
   ```

La DLL se carga y ejecuta el código `DllMain` que conecta al servidor.

## Ventajas

✅ **Experiencia Unificada**: Todo en una ventana  
✅ **Fácil de Usar**: No hay ventanas flotantes  
✅ **Siempre Listo**: GTA está en background, conexión rápida  
✅ **Chat Integrado**: Chatear sin alt-tab  
✅ **Info en Tiempo Real**: Ver stats sin salir del juego  
✅ **Cambiar Servidor**: Fácil transición entre servidores  

## Requisitos

- **Windows 7+** (compatible con API de Windows)
- **.NET Framework 4.7.2+** (para WPF)
- **GTA San Andreas** instalado
- Permisos administrativos (para inyectar DLL)

## Configuración

En `MainWindowIntegrated.xaml.cs`:

```csharp
// Ruta de GTA San Andreas
string gtaSAPath = "C:\\Program Files (x86)\\Rockstar Games\\GTA San Andreas\\gta_sa.exe";

// Ruta de DLL a inyectar
string dllPath = "sa_inject.dll";
```

## Troubleshooting

### "No se pudo encontrar ventana de GTA"
- GTA tardó mucho en abrir
- Título de ventana diferente (versión diferente)
- **Solución**: Aumentar timeout en `StartGameInBackground()`

### "No se pudo inyectar DLL"
- Falta permisos administrativos
- Ruta de DLL incorrecta
- **Solución**: Ejecutar launcher como admin

### Ventana de GTA se ve "rara"
- Resolución incorrecta
- Modo ventana no soportado
- **Solución**: Configurar GTA SA en "Windowed Mode"

## Próximos Pasos

- [ ] Integración con controlador (joystick)
- [ ] Captura de entrada del usuario (mouse + teclado)
- [ ] Sincronización de audio
- [ ] Screenshots dentro del launcher
- [ ] Recording de gameplay
- [ ] Streaming directo desde launcher

---

**Versión**: 2.0 - Integrated Launcher  
**Tipo**: WPF Application (C#)  
**Requisitos**: .NET Framework 4.7.2+, Windows 7+  
**Estado**: En desarrollo
