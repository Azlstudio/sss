# UI Design - GTA San Andreas Multiplayer

## Overview

La interfaz es diseñada para ser **no-intrusiva** y **funcional** durante el gameplay.
Inspirada en interfaces modernas, pero optimizada para GTA San Andreas.

## Layouts

### 1. Status Bar (Arriba-Izquierda)
```
╔════════════════════════════════════╗
║ Ping: 45ms | Jugadores: 12 | [●] ║
║ Estado: Conectado                  ║
╚════════════════════════════════════╝
```

- **Verde**: Conectado (Ping < 100ms)
- **Amarillo**: Advertencia (Ping 100-200ms)
- **Rojo**: Crítico (Ping > 200ms o desconectado)

### 2. Player List (Derecha)
```
╔═══════════════════════════════════╗
║ JUGADORES (12)                    ║
├───────────────────────────────────┤
║ Player1 [ID:1]    Salud: 100%    ║
║ Player2 [ID:2]    Salud: 87%     ║
║ Player3 [ID:3]    Salud: 45%     ║
║ ...                               ║
║ Distancia: 250m                   ║
╚═══════════════════════════════════╝
```

**Colores por Salud:**
- Verde: > 75%
- Amarillo: 50-75%
- Naranja: 25-50%
- Rojo: < 25%

### 3. Chat Window (Abajo-Centro)
```
╔════════════════════════════════════════════╗
║ [12:34] Player1: Hola a todos!            ║
║ [12:35] Player2: Como estan?              ║
║ [SYSTEM] Player3 se unio al servidor      ║
│────────────────────────────────────────────│
│ Escribe aquí...                            │
╚════════════════════════════════════════════╝
```

**Tipos de mensajes:**
- `[CHAT]` - Mensajes normales
- `[SISTEMA]` - Eventos del servidor
- `[ADVERTENCIA]` - Información importante

### 4. Mini-Map (Abajo-Derecha)
```
╔═══════════════════════════════════╗
║         MINI-MAPA                 ║
║    ▲                              ║
║    ⚪ (TU)                         ║
║    •  • (Otros Jugadores)        ║
║    📍 Waypoint                    ║
│                                   │
│ Escala: 1:1000                    ║
╚═══════════════════════════════════╝
```

**Elementos:**
- ⚪ Blanco = Tú
- 🔴 Rojo = Enemigos cercanos
- 🟢 Verde = Aliados (si hay teams)
- 📍 Amarillo = Waypoint

### 5. Player Info (Abajo-Izquierda)
```
┌─────────────────────────────────┐
│ POSICIÓN: X: 2048.50 Y: 1950.75 │
│           Z: 10.50              │
│ SALUD: ▓▓▓▓▓▓▓▓░░ 80%          │
│ ARMADURA: ▓▓▓▓░░░░░░ 40%        │
│ ARMA: Deagle [7/30]             │
│ PING: 45ms                       │
└─────────────────────────────────┘
```

## Controles de Teclado

| Tecla | Función |
|-------|---------|
| **F1** | Mostrar/Ocultar UI |
| **T** | Abrir Chat |
| **M** | Toggle Mini-mapa |
| **P** | Toggle Lista de Jugadores |
| **L** | Mostrar/Ocultar Logs |
| **Esc** | Cerrar ventanas activas |

## Temas

### Dark Mode (Por Defecto)
- Fondo: Negro semi-transparente (#000000AA)
- Texto: Blanco (#FFFFFF)
- Acentos: Naranja (#FF8800)
- Bordes: Gris (#444444)

### Light Mode (Alternativo)
- Fondo: Gris claro semi-transparente (#FFFFFFCC)
- Texto: Negro (#000000)
- Acentos: Azul (#0088FF)
- Bordes: Negro (#111111)

## Animaciones

### Transiciones
- **Fade In/Out**: 200ms
- **Slide**: 300ms
- **Hover Effects**: 100ms

### Pulso de Estado
- Conectado: Pulso verde suave cada 1s
- Desconectado: Pulso rojo cada 500ms
- Crítico: Pulso rojo cada 250ms

## Indicadores

### Conexión
```
● CONECTADO       (Verde, pulsante)
● RECONECTANDO    (Amarillo, rápido)
● DESCONECTADO    (Rojo, pulsante)
```

### Salud
```
█████████░ 90% (Verde)
███████░░░ 70% (Verde)
█████░░░░░ 50% (Amarillo)
██░░░░░░░░ 20% (Rojo)
```

## Accesibilidad

- **Contraste Alto**: Mínimo 4.5:1 ratio
- **Tamaño Mínimo de Texto**: 12px
- **Tooltips**: Al pasar el mouse
- **Atajos de Teclado**: Todas las acciones disponibles

## Performance

- **FPS Impact**: < 5% del rendimiento del juego
- **Memory Usage**: < 50MB
- **Update Rate**: 60 FPS (sincronizado con el juego)

---

**Diseñador**: Claude Code
**Versión**: 1.0
**Inspiración**: Interfaces modernas + GTA UI
