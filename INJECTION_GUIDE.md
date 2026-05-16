# GTA San Andreas Multiplayer - DLL Injection Guide

## Componentes

### 1. **sa_inject.dll** - DLL que se inyecta en GTA SA
- Accede a memoria del juego
- Captura posición del jugador en tiempo real
- Se conecta al servidor multiplayer
- Renderiza UI en-game

### 2. **sa_launcher.exe** - Launcher que inyecta la DLL
- Encuentra el proceso de GTA SA
- Inyecta sa_inject.dll
- Facilita la comunicación con el servidor

### 3. **UI In-Game**
- Interfaz con:
  - Estado de conexión (esquina superior izquierda)
  - Lista de jugadores (derecha)
  - Chat multiplayer (inferior)
  - Mini-mapa con posiciones (esquina inferior derecha)
  - Información del jugador (salud, posición)

## Cómo Usar

### Paso 1: Compilar

```bash
build.bat
```

Esto creará:
- `build\Release\sa_server.exe`
- `build\Release\sa_client.exe`
- `build\Release\sa_inject.dll`
- `build\Release\sa_launcher.exe`

### Paso 2: Iniciar Servidor

```bash
sa_server.exe
```

El servidor escuchará en puerto 8888.

### Paso 3: Abrir GTA San Andreas

Abre el juego GTA San Andreas normalmente.

### Paso 4: Inyectar DLL

Ejecuta el launcher:

```bash
sa_launcher.exe
```

El programa te pedirá que presiones una tecla, luego buscará el proceso de GTA SA y cargará la DLL.

### Paso 5: ¡Jugar Multijugador!

La UI aparecerá en el juego. Verás:
- Tu posición y salud
- Otros jugadores conectados
- Chat de jugadores
- Ping y estado de conexión

## Controles

- **F1** - Mostrar/Ocultar UI
- **T** - Chat
- **M** - Mini-mapa
- **P** - Lista de jugadores

## Estructura de Datos

### Captura de Memoria

```cpp
// Offsets de GTA San Andreas v1.0
PLAYER_PED = 0xB6F5F0        // Puntero al jugador actual
PLAYER_POS = 0x4C             // Posición (X, Y, Z) dentro del PED
PLAYER_HEALTH = 0x540         // Salud del jugador
PLAYER_MODEL = 0x22           // Modelo del jugador
```

### Comunicación de Red

La DLL se comunica con el servidor usando el protocolo UDP definido en `protocol.h`:

```cpp
struct PlayerData {
    uint32_t playerID;
    char name[32];
    Vector3 position;      // Posición en el mundo
    Vector3 rotation;      // Rotación (pitch, yaw, roll)
    uint32_t modelID;      // Modelo de skin
    float health;          // Salud del jugador
};
```

## Sincronización

- **Update Rate**: 100ms (10 updates por segundo)
- **Packet Type**: UDP con ~256 bytes por paquete
- **Broadcast**: Servidor envía updates a todos los clientes

## Troubleshooting

### Problema: "Proceso gta_sa.exe no encontrado"
- **Solución**: Asegúrate de que GTA San Andreas está abierto antes de ejecutar el launcher

### Problema: "No se pudo abrir el proceso"
- **Solución**: Ejecuta sa_launcher.exe como administrador

### Problema: La DLL no se carga
- **Solución**: Verifica que sa_inject.dll esté en el mismo directorio que sa_launcher.exe

### Problema: No se ve la UI
- **Solución**: Presiona F1 para mostrar la interfaz

### Problema: No se conecta al servidor
- **Solución**: 
  - Verifica que sa_server.exe esté corriendo
  - Verifica la IP del servidor en `inject.cpp` (línea ~77)
  - Asegúrate de que el puerto 8888 está abierto en el firewall

## Arquitectura de Red

```
GTA San Andreas (sa_inject.dll)
    |
    | UDP Port 8888
    |
Game Server (sa_server.exe)
    |
    | Broadcast a todos los clientes
    |
Otros Clientes (sa_inject.dll)
```

## Próximas Características

- [ ] Sincronización de animaciones
- [ ] Sincronización de vehículos
- [ ] Sistema de equipos (Cops vs Robbers)
- [ ] Poder crear salas privadas
- [ ] Persistencia de datos en DB
- [ ] Base de datos de jugadores
- [ ] Sistema de ranks y niveles
- [ ] Sistema de dinero/economía

## Nota Legal

Este es un proyecto educativo. El reverse engineering de GTA San Andreas se hace con fines educativos.

---

**Versión**: 0.2 - Injection Implementation
**Última actualización**: 2026-05-16
