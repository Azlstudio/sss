# GTA San Andreas Multiplayer Prototype

Prototipo funcional de un servidor y cliente multijugador para GTA San Andreas. Permite que múltiples jugadores en la misma red WiFi se conecten y sincricen sus posiciones en tiempo real.

## Características

- ✅ Servidor UDP que maneja múltiples conexiones
- ✅ Cliente que se conecta al servidor
- ✅ Sincronización de posiciones de jugadores
- ✅ Protocolo de networking personalizado
- ✅ Soporte para hasta 32 jugadores simultáneos
- ⏳ Inyección en GTA San Andreas (en desarrollo)

## Estructura del Proyecto

```
.
├── include/
│   └── protocol.h          # Definición del protocolo compartido
├── src/
│   ├── server/
│   │   └── server.cpp      # Servidor multijugador
│   ├── client/
│   │   └── client.cpp      # Cliente multijugador
│   └── inject/
│       └── (DLL injection code)
├── CMakeLists.txt          # Build configuration
└── build.bat               # Script de compilación (Windows)
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

### 1. Iniciar el Servidor

```bash
sa_server.exe
```

El servidor escuchará en `127.0.0.1:8888` (o en toda la red local `0.0.0.0:8888`)

### 2. Conectar Cliente(s)

En otra terminal/PC en la misma red:

```bash
sa_client.exe
```

El cliente se conectará automáticamente al servidor en `127.0.0.1:8888` y simulará movimiento.

## Protocolo de Networking

### Tipos de Paquetes

- `PKT_CONNECT` - Conexión inicial del cliente
- `PKT_DISCONNECT` - Desconexión del cliente
- `PKT_PLAYER_UPDATE` - Actualización de posición/rotación
- `PKT_PLAYER_JOINED` - Notificación de jugador conectado
- `PKT_PLAYER_LEFT` - Notificación de jugador desconectado
- `PKT_SPAWN` - Spawn de jugador

## Próximos Pasos

1. **Inyección en GTA SA**: Crear DLL que se inyecta en GTA SA
2. **Captura de Datos**: Hook de memoria para capturar posición real del jugador
3. **Renderizado**: Mostrar otros jugadores en el juego
4. **Sincronización de Acciones**: Disparos, golpes, etc.
5. **Persistencia**: Base de datos para cuentas de jugadores

## Configuración para Red WiFi Local

Para conectar desde otra PC en la misma WiFi:

1. Encontrar IP del servidor: `ipconfig`
2. Modificar `client.cpp` para usar esa IP
3. Recompilar

Ejemplo: Si el servidor está en IP `192.168.1.100`:

```cpp
client.Connect("192.168.1.100", "Player1");
```

---

**Estado:** Prototipo Funcional v0.1
