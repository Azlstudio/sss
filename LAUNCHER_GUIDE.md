# Launcher - GTA San Andreas Multiplayer

## Overview

Launcher profesional y moderno para conectarse a servidores de GTA San Andreas Multiplayer.

**Características:**
- ✅ Interfaz moderna y elegante (Dark Mode)
- ✅ Búsqueda y filtrado de servidores
- ✅ Sistema de favoritos
- ✅ Historial de recientes
- ✅ Conectar con doble click
- ✅ Panel de administración para dueños
- ✅ Customización de servidor (banner, logo, tags)
- ✅ Estadísticas de servidor
- ✅ Sistema de rating y votaciones

## Estructura

```
src/launcher/
├── MainWindow.xaml           # Ventana principal con navegación
├── MainWindow.xaml.cs        # Code-behind
├── ServerData.cs             # Modelo de datos (servidor, usuario, filtros)
└── Pages/
    ├── HomePage.xaml         # Página de inicio (servidores destacados)
    ├── HomePage.xaml.cs
    ├── ServersPage.xaml      # Búsqueda y lista de servidores
    ├── ServersPage.xaml.cs
    ├── FavoritesPage.xaml    # Servidores favoritos
    ├── FavoritesPage.xaml.cs
    ├── RecentPage.xaml       # Servidores recientes
    ├── RecentPage.xaml.cs
    ├── SettingsPage.xaml     # Configuración de usuario
    ├── SettingsPage.xaml.cs
    ├── AdminPanel.xaml       # Panel de administración de servidor
    └── AdminPanel.xaml.cs
```

## Interfaz

### Navegación Lateral (Left Sidebar)
```
SA MULTIPLAYER
├── 🏠 Home
├── 🔍 Buscar Servidores
├── ⭐ Favoritos
├── 🕐 Recientes
├─────────────────
├── ➕ Mi Servidor
├── ⚙️ Panel Admin
├─────────────────
└── ⚙️ Configuración
```

### Páginas Principales

#### 1. Home
- **Servidor Destacado**: Mostrado en grande (highest rated)
- **Recomendados**: Top 3 servidores
- **Double-Click para conectar**: Conexión rápida
- **Stats**: Jugadores, ping, rating

#### 2. Búsqueda de Servidores
- **Filtros**:
  - Modo de juego (RP, TDM, Sandbox)
  - Número de jugadores (Vacío, Pocas personas, Lleno)
  - Estado (En línea, Sin conexión)
  - Ordenar por (Jugadores, Ping, Rating, Nombre)
  
- **Lista de Servidores**:
  - Nombre y descripción
  - Tags (RP, Economia, etc)
  - Jugadores en línea / Máximo
  - Ping (latencia)
  - Rating con número de votos
  - Botón ⭐ para agregar a favoritos
  - Botón "Conectar"

#### 3. Favoritos
- Lista de servidores guardados
- Quick-access para servidores favoritos
- Remover de favoritos fácilmente

#### 4. Recientes
- Historial de últimos servidores visitados
- Ordenados por fecha (más reciente primero)
- Máximo 10 recientes guardados

#### 5. Configuración
- Cambiar nombre de usuario
- Seleccionar tema (Oscuro/Claro)
- Seleccionar idioma
- Conectar automáticamente
- Habilitar notificaciones

#### 6. Panel de Administrador
- **Para dueños de servidor**:
  - Configuración del servidor (nombre, descripción)
  - Editar game mode
  - Subir banner y logo
  - Editar tags
  - Establecer máximo de jugadores
  - Ver estadísticas (visitas, en línea, rating)
  - Listar jugadores conectados

## Flujo de Uso

### Conectarse a un Servidor

**Opción 1: Doble-Click**
1. Ir a Home o Buscar Servidores
2. Hacer doble-click en un servidor
3. Se abre la DLL de inyección automáticamente

**Opción 2: Botón Conectar**
1. Seleccionar servidor
2. Click en botón "Conectar"
3. Se abre la DLL de inyección automáticamente

### Agregar a Favoritos
1. En lista de servidores
2. Click en botón ⭐
3. Servidor guardado en favoritos
4. Ver en sección "Favoritos"

### Gestionar Servidor (Admin)
1. Click en "Panel Admin"
2. Editar información del servidor
3. Cambiar banner, logo, tags
4. Ver estadísticas y jugadores
5. Click en "Guardar Cambios"

## Datos de Servidor

### ServerData
```csharp
ServerId              // ID único
Name                  // Nombre del servidor
Description           // Descripción breve
IP                    // IP del servidor
Port                  // Puerto
Owner                 // Dueño del servidor
MaxPlayers            // Máximo de jugadores
CurrentPlayers        // Jugadores conectados
Tags[]                // Tags (RP, PvP, etc)
GameMode              // Tipo de juego
BannerUrl             // URL del banner
LogoUrl               // URL del logo
PingMs                // Latencia en ms
CreatedDate           // Fecha de creación
IsOnline              // Si está en línea
Rating                // Rating 0-5 estrellas
RatingCount           // Número de votos
IsFavorite            // Si está en favoritos
```

### UserSettings
```csharp
Username              // Nombre del jugador
AccountId             // ID de cuenta
FavoriteServers[]     // IDs de favoritos
RecentServers[]       // IDs de recientes (máx 10)
Theme                 // "Dark" o "Light"
AutoConnect           // Conectar automáticamente
Language              // "ES" o "EN"
EnableNotifications   // Notificaciones
EnableSounds          // Sonidos
MasterVolume          // 0-100
```

## Diseño Visual

### Colores
- **Fondo Oscuro**: #1E1E1E
- **Panel Oscuro**: #252526
- **Borde**: #3E3E42
- **Primario (Azul)**: #007ACC
- **Verde (Conectado)**: #00FF00
- **Amarillo (Advertencia)**: #FFFF00
- **Dorado (Rating)**: #FFD700
- **Texto Principal**: #FFFFFF
- **Texto Secundario**: #999999

### Tipografía
- **Títulos**: 18-24px, Bold, Blanco
- **Subtítulos**: 14-16px, Regular, Blanco
- **Texto Normal**: 12-13px, Regular, Gris claro
- **Etiquetas**: 9-10px, Regular, Gris

### Controles
- Botones primarios: Azul (#007ACC)
- Botones secundarios: Gris oscuro (#2D2D30)
- TextBox: Gris (#3E3E42)
- Bordes: Gris (#3E3E42)
- Hover effects: Transparencia + brightness

## Tecnología

- **Lenguaje**: C# (.NET Framework 4.7.2+)
- **UI Framework**: WPF (Windows Presentation Foundation)
- **Patrón**: MVVM (con data binding)
- **Base de Datos**: (Local) JSON / SQL (propuesto)

## Próximas Mejoras

- [ ] Integración con API de servidores
- [ ] Sistema de autenticación con cuenta
- [ ] Descargar y actualizar GTA SA automáticamente
- [ ] Instalador del launcher
- [ ] Update automático del launcher
- [ ] Notificaciones de push (servidores favoritos)
- [ ] Chat de comunidad
- [ ] Historial de estadísticas personales
- [ ] Themes personalizados
- [ ] Soporte para mods

## Build

```bash
# Compilar en Visual Studio 2022
# O desde línea de comandos:
msbuild Launcher.sln /p:Configuration=Release

# Ejecutable en:
bin/Release/GTASALauncher.exe
```

---

**Versión**: 1.0  
**Estado**: Interfaz Completa - Backend pendiente  
**Plataforma**: Windows (.NET Framework)
