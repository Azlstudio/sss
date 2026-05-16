# GTAS Multiplayer - Guía de Scripting

## Introducción

El launcher de GTAS Multiplayer permite que **cualquier usuario cree scripts** usando **Lua**, un lenguaje de programación poderoso pero fácil de aprender.

## ¿Qué es un Script?

Un script es un archivo de código que extiende la funcionalidad del servidor. Puede hacer cosas como:
- Crear sistemas de dinero
- Implementar trabajos y oficios
- Crear gangs y facciones
- Añadir eventos especiales
- Modificar gameplay

## ¿Qué es Lua?

**Lua** es un lenguaje de programación ligero, rápido y fácil de aprender.

### Ejemplo Básico
```lua
-- Variables
local nombre = "Player1"
local dinero = 5000

-- Funciones
function saludar(person)
    print("Hola " .. person .. "!")
end

-- Llamar función
saludar(nombre)

-- Condicionales
if dinero > 1000 then
    print("Tienes mucho dinero")
else
    print("Necesitas más dinero")
end

-- Loops
for i = 1, 10 do
    print("Número: " .. i)
end

-- Tablas (arrays)
local jobs = {"Police", "Taxi", "Trucker"}
for _, job in ipairs(jobs) do
    print(job)
end
```

## Manifest vs Meta.xml

### Ventajas del Manifest sobre Meta.xml

| Característica | Meta.xml (MTA) | Manifest (GTAS) |
|---|---|---|
| Formato | XML | XML mejorado |
| Configuración | Limitada | Extensa |
| Anti-cheat | Genérico | Personalizable |
| Base de datos | No incluida | Integrada |
| Logging | Básico | Avanzado |
| Validación | Mínima | Completa |
| Dependencies | Básicas | Avanzadas |
| Exports | Sí | Mejorados |

### Manifest de GTAS

El **manifest.xml** reemplaza y mejora el meta.xml de MTA:

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest version="1.0">
    <info>
        <name>Mi Script</name>
        <author>MiNombre</author>
        <version>1.0.0</version>
        <description>Descripción del script</description>
        <type>gamemode</type>  <!-- gamemode, script, library -->
    </info>

    <!-- Scripts a cargar -->
    <scripts>
        <script>
            <file>scripts/server/main.lua</file>
            <type>server</type>
            <priority>1</priority>
        </script>
        <script>
            <file>scripts/client/main.lua</file>
            <type>client</type>
            <cache>true</cache>
        </script>
    </scripts>

    <!-- Funciones que exporta este script -->
    <exports>
        <export>
            <function>getPlayerMoney</function>
            <type>server</type>
        </export>
    </exports>

    <!-- Eventos personalizados -->
    <events>
        <event>
            <name>onPlayerMoneyChange</name>
            <type>server</type>
        </event>
    </events>

    <!-- Anti-cheat personalizado -->
    <security>
        <anti_cheat>
            <enabled>true</enabled>
            <level>2</level>
        </anti_cheat>
    </security>
</manifest>
```

## Estructura de un Script

### Carpetas Básicas

```
mi_script/
├── manifest.xml                    # Configuración
├── scripts/
│   ├── server/
│   │   ├── main.lua               # Lógica principal
│   │   └── commands.lua           # Comandos
│   └── client/
│       ├── hud.lua                # Interfaz
│       └── input.lua              # Entrada del usuario
├── models/                        # Modelos 3D
├── sounds/                        # Sonidos
├── images/                        # Imágenes
└── data/
    └── config.json               # Configuración
```

## Tipos de Scripts

### 1. **Gamemode** - Cambiar totalmente el gameplay
```lua
-- scripts/server/main.lua
function onPlayerJoin(player)
    outputChatBox(getPlayerName(player) .. " joined!", root)
    -- Lógica del gamemode
end
addEventHandler("onPlayerJoin", root, onPlayerJoin)
```

### 2. **Script** - Añadir funcionalidad
```lua
-- Ejemplo: Sistema de dinero
function getPlayerMoney(player)
    return getElementData(player, "money") or 0
end

function setPlayerMoney(player, amount)
    setElementData(player, "money", amount)
end
```

### 3. **Library** - Funciones reutilizables
```lua
-- scripts/shared/utils.lua
function formatNumber(n)
    return tostring(n):reverse():gsub("(%d%d%d)", "%1,"):reverse()
end

-- Otros scripts pueden usar esto:
-- local formatted = exports.mi_library:formatNumber(1000)  --> "1,000"
```

## Cómo Crear tu Primer Script

### Paso 1: Crear Carpeta
```bash
mkdir mi_primer_script
cd mi_primer_script
```

### Paso 2: Crear manifest.xml
```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest version="1.0">
    <info>
        <name>Mi Primer Script</name>
        <author>TuNombre</author>
        <version>1.0.0</version>
        <description>Mi primer script para GTAS</description>
        <type>script</type>
    </info>

    <scripts>
        <script>
            <file>scripts/server.lua</file>
            <type>server</type>
        </script>
        <script>
            <file>scripts/client.lua</file>
            <type>client</type>
        </script>
    </scripts>
</manifest>
```

### Paso 3: Crear scripts/server.lua
```lua
-- Script del servidor
function onPlayerJoin(player)
    outputChatBox("Welcome " .. getPlayerName(player) .. "!", root)
end
addEventHandler("onPlayerJoin", root, onPlayerJoin)
```

### Paso 4: Crear scripts/client.lua
```lua
-- Script del cliente
function onClientResourceStart()
    outputChatBox("Script loaded!", 0, 255, 0)
end
addEventHandler("onClientResourceStart", resourceRoot, onClientResourceStart)
```

### Paso 5: Instalar en el Launcher
1. Copiar carpeta a `launcher/scripts/mi_primer_script/`
2. El launcher detectará automáticamente el manifest.xml
3. Click en "Instalar" en el launcher
4. Script listo para usar

## Conceptos Clave

### 1. **Events** - Comunicación entre Server y Client

```lua
-- Server: Escuchar evento del cliente
function onPlayerLogin(username, password)
    local client = source  -- SIEMPRE confiable
    if validatePassword(username, password) then
        triggerClientEvent(client, "onLoginSuccess", client)
    end
end
addEventHandler("playerLogin", root, onPlayerLogin)

-- Client: Disparar evento hacia servidor
function loginButtonClick()
    local username = guiGetText(usernameBox)
    local password = guiGetText(passwordBox)
    triggerServerEvent("playerLogin", localPlayer, username, password)
end

-- Client: Escuchar respuesta del servidor
function onLoginSuccess()
    outputChatBox("Logged in successfully!", 0, 255, 0)
end
addEventHandler("onLoginSuccess", localPlayer, onLoginSuccess)
```

### 2. **Exports** - Reutilizar funciones de otros scripts

```lua
-- Script A exporta una función
function getPlayerLevel(player)
    return getElementData(player, "level") or 1
end

-- Script B usa la función
local db = exports.databaseScript
local playerLevel = db:getPlayerLevel(player)
```

### 3. **Element Data** - Almacenar datos en elementos

```lua
-- Guardar datos
setElementData(player, "money", 5000)
setElementData(player, "job", "Police")

-- Recuperar datos
local money = getElementData(player, "money")
local job = getElementData(player, "job")

-- Escuchar cambios
function onDataChange(key, oldValue, newValue)
    if key == "money" then
        outputChatBox("Your money changed from " .. oldValue .. " to " .. newValue)
    end
end
addEventHandler("onElementDataChange", player, onDataChange)
```

### 4. **Timers** - Acciones periódicas

```lua
-- Ejecutar función cada 1000ms (1 segundo)
local myTimer = setTimer(function()
    print("1 segundo pasó")
end, 1000, 5)  -- 5 veces solamente

-- Infinitas veces
setTimer(function()
    -- Dar dinero a jugadores cada 10 segundos
    for _, player in ipairs(getElementsByType("player")) do
        addPlayerMoney(player, 10)
    end
end, 10000, 0)  -- 0 = infinito

-- Cancelar timer
killTimer(myTimer)
```

## Anti-Cheat en Scripts

### Validación del Servidor (CRÍTICO)

```lua
-- MALO - Confiar en datos del cliente
function onPlayerKill(killer, weapon)
    addPlayerMoney(killer, 500)  -- ¡INSEGURO! Killer es cliente
end

-- BUENO - Validar en servidor
function onPlayerKill(weapon)
    local server = source  -- source es SIEMPRE el jugador en servidor
    local killer = source
    
    -- Verificar validez
    if not killer or not isElement(killer) then
        return
    end
    
    addPlayerMoney(killer, 500)  -- SEGURO
end
```

### Detecciones Personalizadas

```lua
-- Detectar speed hack
local lastPos = {}
setTimer(function()
    for _, player in ipairs(getElementsByType("player")) do
        local x, y, z = getElementPosition(player)
        
        if lastPos[player] then
            local distance = getDistanceBetweenPoints3D(
                x, y, z,
                lastPos[player].x,
                lastPos[player].y,
                lastPos[player].z
            )
            
            -- Velocidad máxima: 250 km/h
            if distance > 7 then  -- Distancia en 100ms
                outputChatBox("Speed hack detected: " .. getPlayerName(player), root, 255, 0, 0)
            end
        end
        
        lastPos[player] = {x = x, y = y, z = z}
    end
end, 100, 0)
```

## Mejores Prácticas

### 1. Usar Variables Locales
```lua
-- MALO - Contamina namespace global
function = "value"

-- BUENO - Variables locales
local myVar = "value"
```

### 2. Validar Entrada del Cliente
```lua
function onMoneyCommand(amount)
    amount = tonumber(amount)
    
    if not amount or amount < 0 then
        outputChatBox("Invalid amount!", source)
        return
    end
    
    -- Ahora es seguro usar amount
end
```

### 3. Usar Try-Catch Equivalentes
```lua
local function safeCall(func, ...)
    local result = pcall(func, ...)
    if not result then
        print("Error: " .. tostring(result))
    end
end
```

### 4. Documentar Funciones
```lua
--- Obtiene el dinero de un jugador
-- @param player El elemento jugador
-- @return Cantidad de dinero (number)
-- @usage local money = getPlayerMoney(player)
function getPlayerMoney(player)
    return getElementData(player, "money") or 0
end
```

## Depuración

### Funciones de Debug
```lua
-- Imprimir en consola
print("Variable value: " .. myVar)

-- Imprimir tabla completa
function dumpTable(table)
    for key, value in pairs(table) do
        print(key .. " = " .. tostring(value))
    end
end

-- Imprimir en chat (visible a jugador)
outputChatBox("Debug: " .. message, player)

-- Imprimir en log del servidor
outputServerLog("Server log: " .. message)
```

### Validar Elementos
```lua
if not isElement(player) then
    print("Invalid player element")
    return false
end

if getElementType(player) ~= "player" then
    print("Not a player")
    return false
end
```

## Repositorio de Scripts

Los usuarios pueden:
1. **Crear scripts personalizados** 
2. **Compartir scripts en el repositorio**
3. **Descargar scripts de otros**
4. **Votarlos y comentar**

Ejemplo de instalación desde repositorio:
```
Launcher → Browse Scripts → "Economy System" → Install
```

## Recursos Adicionales

- **Lua Documentation**: https://www.lua.org/manual/5.1/
- **GTAS API Reference**: (En el launcher)
- **Script Templates**: (Incluidos en el launcher)
- **Community Forum**: (Comunidad)

## Conclusión

Con Lua y el sistema Manifest mejorado, **cualquiera puede crear scripts** poderosos para GTAS Multiplayer. 

El sistema es:
- **Fácil de aprender** - Lua es simple
- **Seguro** - Anti-cheat integrado
- **Flexible** - Infinitas posibilidades
- **Comunitario** - Compartir y descargar

---

**¡A programar!** 🚀

