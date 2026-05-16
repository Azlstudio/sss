# Quick Start Guide

## En Windows

### Terminal 1 - Servidor
```bash
cd build\Release
sa_server.exe
```

### Terminal 2 - Cliente 1
```bash
cd build\Release
sa_client.exe
```

### Terminal 3 - Cliente 2 (en la misma WiFi)
Cambiar IP en client.cpp:
```cpp
client.Connect("192.168.1.100", "Player2");  // IP del servidor
```
Luego compilar y ejecutar `sa_client.exe`

## Flujo de Conexión

1. **Servidor inicia** - Escucha en puerto 8888
2. **Cliente se conecta** - Envía paquete PKT_CONNECT
3. **Servidor asigna ID** - Envía ID de jugador
4. **Cliente actualiza posición** - Envía PKT_PLAYER_UPDATE cada 500ms
5. **Servidor broadcast** - Envía updates a todos los clientes
6. **Clientes reciben** - Sincronizan posiciones de otros jugadores

## Testing

Abrir 3 terminales:

**Terminal 1:**
```bash
sa_server.exe
```
Output: "Server running... Waiting for connections"

**Terminal 2:**
```bash
sa_client.exe
```
Output: "Assigned player ID: 1"

**Terminal 3:**
```bash
sa_client.exe
```
Output: "Assigned player ID: 2"

Verás en todas las terminales las posiciones sincronizadas.

## Problema: Conexión Rechazada?

- ¿Firewall bloqueando puerto 8888?
- ¿IP correcta? (127.0.0.1 para localhost)
- ¿Server corriendo?

