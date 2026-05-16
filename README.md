# GTA San Andreas Multiplayer Prototype

Prototipo funcional de un servidor y cliente multijugador para GTA San Andreas. Permite que múltiples jugadores en la misma red WiFi se conecten y sincricen sus posiciones en tiempo real.

## Características

- ✅ Servidor UDP que maneja múltiples conexiones
- ✅ Cliente que se conecta al servidor
- ✅ Sincronización de posiciones de jugadores
- ✅ Protocolo de networking personalizado
- ✅ Soporte para hasta 32 jugadores simultáneos
- ✅ DLL Injection en GTA San Andreas
- ✅ Interfaz gráfica in-game profesional
- ✅ Captura de datos de memoria del juego
- ✅ Mini-mapa, chat, y lista de jugadores

## Estructura del Proyecto

```
.
├── include/
│   └── protocol.h              # Protocolo de networking
├── src/
│   ├── server/
│   │   └── server.cpp          # Servidor UDP multijugador
│   ├── client/
│   │   └── client.cpp          # Cliente de prueba
│   └── inject/
│       ├── inject.cpp          # DLL principal (se ejecuta en GTA SA)
│       ├── launcher.cpp        # Inyector de DLL
│       ├── gta_memory.h/cpp    # Acceso a memoria de GTA SA
│       └── ui.h/cpp            # Interfaz gráfica in-game
├── CMakeLists.txt              # Build configuration
├── build.bat                   # Script de compilación
├── INJECTION_GUIDE.md          # Guía de inyección
└── UI_DESIGN.md                # Diseño de la interfaz
```

## Requisitos

- Visual Studio 2022 (o compatible)
- CMake 3.20+
- Windows SDK

## Compilación

### Windows (Recomendado)

1. Ejecutar `build.bat`
2. Los ejecutables se crearán en `build/Release/`

### Manual

```bash
mkdir build
cd build
cmake -G "Visual Studio 17 2022" ..
cmake --build . --config Release
```

## Uso

### Opción 1: Servidor + Cliente Standalone

```bash
# Terminal 1 - Servidor
sa_server.exe

# Terminal 2 - Cliente
sa_client.exe
```

### Opción 2: Inyección en GTA San Andreas (Recomendado)

```bash
# Terminal 1 - Servidor
sa_server.exe

# GTA San Andreas - Abre el juego normalmente

# Terminal 2 - Launcher (Inyector)
sa_launcher.exe
```

La DLL se inyectará automáticamente y la UI aparecerá en el juego.

**Controles:**
- **F1** - Mostrar/Ocultar UI
- **T** - Chat
- **M** - Mini-mapa
- **P** - Lista de jugadores

## Protocolo de Networking

### Tipos de Paquetes

- `PKT_CONNECT` - Conexión inicial del cliente
- `PKT_DISCONNECT` - Desconexión del cliente
- `PKT_PLAYER_UPDATE` - Actualización de posición/rotación
- `PKT_PLAYER_JOINED` - Notificación de jugador conectado
- `PKT_PLAYER_LEFT` - Notificación de jugador desconectado
- `PKT_SPAWN` - Spawn de jugador

## Próximos Pasos

- [ ] **Renderizado de Jugadores**: Crear peds para otros jugadores en el mapa
- [ ] **Sincronización de Vehículos**: Sincronizar uso de vehículos
- [ ] **Sincronización de Animaciones**: Animar acciones (disparos, golpes, etc)
- [ ] **Sistema de Salas**: Crear salas/servidores privados
- [ ] **Base de Datos**: Persistencia de datos de jugadores
- [ ] **Sistema de Equipos**: Implementar modos Cops vs Robbers, TDM
- [ ] **Voz**: Comunicación de voz en-game
- [ ] **Antitrampas**: Sistema de detección de hackers

## Configuración para Red WiFi Local

Para conectar desde otra PC en la misma WiFi:

1. Encontrar IP del servidor: `ipconfig`
2. Modificar `client.cpp` para usar esa IP
3. Recompilar

Ejemplo: Si el servidor está en IP `192.168.1.100`:

```cpp
client.Connect("192.168.1.100", "Player1");
```

## Documentación Adicional

- [**INJECTION_GUIDE.md**](INJECTION_GUIDE.md) - Guía completa de inyección y troubleshooting
- [**UI_DESIGN.md**](UI_DESIGN.md) - Diseño detallado de la interfaz
- [**QUICKSTART.md**](QUICKSTART.md) - Inicio rápido del servidor/cliente

## Componentes Clave

| Componente | Descripción |
|-----------|-----------|
| `sa_server.exe` | Servidor UDP que sincroniza jugadores |
| `sa_client.exe` | Cliente de prueba (no necesario si usas la DLL) |
| `sa_launcher.exe` | Inyector de DLL en GTA SA |
| `sa_inject.dll` | DLL que se ejecuta en GTA SA |

## API de Red

```cpp
// Todos los paquetes usan UDP
#define SERVER_PORT 8888
#define PACKET_SIZE 256
#define MAX_PLAYERS 32

// Estructura de datos de jugador
struct PlayerData {
    uint32_t playerID;
    char name[32];
    Vector3 position;        // X, Y, Z
    Vector3 rotation;        // Pitch, Yaw, Roll
    uint32_t modelID;        // Skin del jugador
    float health;            // 0-100
};
```

---

**Estado:** Prototipo Funcional v0.2 - DLL Injection & UI Completa
**Última actualización:** 2026-05-16
**Versión:** 0.2.0
