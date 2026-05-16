--[[
    GTAS Multiplayer - Script de Cliente Ejemplo
    Corre en la máquina de cada jugador, maneja renderizado y UI
]]

-- ============================================
-- VARIABLES LOCALES
-- ============================================
local playerMoney = 0
local playerJob = 0
local showHUD = true
local screenWidth, screenHeight = guiGetScreenSize()

-- ============================================
-- FUNCIONES DE RENDERIZADO
-- ============================================

local function drawHUD()
    if not showHUD then return end

    -- Dinero en la pantalla
    dxDrawText("Money: $" .. playerMoney, 20, 20, 300, 60, tocolor(0, 255, 0, 255), 1.5)

    -- Coordenadas
    local x, y, z = getElementPosition(localPlayer)
    dxDrawText(string.format("Pos: %.0f, %.0f, %.0f", x, y, z), 20, 50, 300, 90, tocolor(255, 255, 0, 255), 1.0)

    -- Velocidad
    local vx, vy, vz = getElementVelocity(localPlayer)
    local speed = math.sqrt(vx^2 + vy^2 + vz^2) * 160  -- Convertir a km/h
    dxDrawText("Speed: " .. math.floor(speed) .. " km/h", 20, 80, 300, 120, tocolor(255, 100, 0, 255), 1.0)

    -- FPS
    local fps = round(1000 / getTickCount() * 1000)  -- Aproximado
    dxDrawText("FPS: " .. fps, 20, 110, 300, 150, tocolor(100, 200, 255, 255), 1.0)
end

local function round(num)
    return math.floor(num + 0.5)
end

-- ============================================
-- EVENTOS DEL SERVIDOR
-- ============================================

-- Evento personalizado: Actualizar dinero
function onMoneyUpdate(amount)
    playerMoney = amount
    outputChatBox("Money updated: $" .. amount, 0, 255, 0)
end
addEventHandler("onMoneyUpdate", localPlayer, onMoneyUpdate)

-- Evento: Notificación del servidor
function onNotification(title, message, r, g, b)
    -- Mostrar notificación
    outputChatBox("[" .. title .. "] " .. message, r, g, b)

    -- Aquí podrías hacer un overlay visual más bonito
    print("NOTIFICATION: " .. title .. " - " .. message)
end
addEventHandler("onNotification", localPlayer, onNotification)

-- Evento: Información del vehículo
function onVehicleInfo(vehicleData)
    outputChatBox("Entered vehicle at seat " .. vehicleData.seat, 0, 255, 0)

    if vehicleData.jacked then
        outputChatBox("WARNING: You jacked this vehicle!", 255, 0, 0)
    end
end
addEventHandler("onVehicleInfo", localPlayer, onVehicleInfo)

-- ============================================
-- EVENTOS INCORPORADOS DEL CLIENTE
-- ============================================

-- Renderizado en cada frame
function render()
    drawHUD()
end
addEventHandler("onClientRender", root, render)

-- Cuando el jugador se une al servidor
function onClientResourceStart()
    outputChatBox("Connected to GTAS Multiplayer!", 0, 255, 0)
    outputChatBox("Press H to toggle HUD", 255, 255, 0)
    outputChatBox("Available commands: /money, /job [1-4]", 255, 255, 0)
end
addEventHandler("onClientResourceStart", resourceRoot, onClientResourceStart)

-- ============================================
-- MANEJO DE INPUT (TECLADO/MOUSE)
-- ============================================

-- Presionar H para mostrar/ocultar HUD
function onKeyPress(button, press)
    if button == "h" and press then
        showHUD = not showHUD
        outputChatBox("HUD " .. (showHUD and "enabled" or "disabled"), 0, 255, 0)
    end
end
bindKey("h", "down", onKeyPress)

-- Presionar T para chat
bindKey("t", "down", function()
    outputChatBox("Type your message (available commands: /money, /job, /givemoney)", 255, 255, 0)
end)

-- ============================================
-- COMANDOS DEL CLIENTE
-- ============================================

-- Comando local /money (también puede ir al servidor)
function commandLocalMoney(command)
    outputChatBox("Your current money: $" .. playerMoney, 0, 255, 0)
end
addCommandHandler("money", commandLocalMoney)

-- Comando /job
function commandJob(command, jobId)
    -- Enviar al servidor
    triggerServerEvent("playerChangeJob", localPlayer, jobId or 1)
end
addCommandHandler("job", commandJob)

-- Comando /help
function commandHelp(command)
    outputChatBox("=== Available Commands ===", 255, 255, 0)
    outputChatBox("/money - Check your money", 255, 255, 0)
    outputChatBox("/job [1-4] - Change job", 255, 255, 0)
    outputChatBox("/help - Show this help", 255, 255, 0)
    outputChatBox("H - Toggle HUD", 255, 255, 0)
end
addCommandHandler("help", commandHelp)

-- ============================================
-- FUNCIONES DE UTILIDAD
-- ============================================

local function formatNumber(n)
    -- Formatear número con separadores de miles
    return tostring(n):reverse():gsub("(%d%d%d)", "%1,"):reverse()
end

local function drawBox(x, y, w, h, color, alpha)
    dxDrawRectangle(x, y, w, h, tocolor(color[1], color[2], color[3], alpha))
end

local function drawBorderedBox(x, y, w, h, borderColor, fillColor, borderSize)
    borderSize = borderSize or 2
    -- Border
    dxDrawRectangle(x, y, w, h, borderColor)
    -- Fill
    dxDrawRectangle(x + borderSize, y + borderSize, w - borderSize * 2, h - borderSize * 2, fillColor)
end

-- ============================================
-- ANTI-CHEAT BÁSICO (CLIENT-SIDE VALIDATION)
-- ============================================

-- Detectar cambios imposibles de velocidad
local lastPos = {x = 0, y = 0, z = 0}
local lastTime = getTickCount()

function validateMovement()
    local currentPos = {getElementPosition(localPlayer)}
    local currentTime = getTickCount()

    if lastTime == 0 then
        lastTime = currentTime
        lastPos = currentPos
        return
    end

    local timeDiff = (currentTime - lastTime) / 1000  -- En segundos
    if timeDiff == 0 then return end

    local distance = math.sqrt(
        (currentPos.x - lastPos.x)^2 +
        (currentPos.y - lastPos.y)^2 +
        (currentPos.z - lastPos.z)^2
    )

    local speed = distance / timeDiff

    -- Si la velocidad es imposible (>250 km/h sin vehículo)
    if speed > 250 and not getPedOccupiedVehicle(localPlayer) then
        outputChatBox("ANTI-CHEAT: Impossible speed detected!", 255, 0, 0)
        -- El servidor también valida esto
    end

    lastPos = currentPos
    lastTime = currentTime
end
setTimer(validateMovement, 1000, 0)  -- Cada segundo

-- ============================================
-- SINCRONIZACIÓN CON SERVIDOR
-- ============================================

-- Enviar datos al servidor cada 100ms
local function syncWithServer()
    local x, y, z = getElementPosition(localPlayer)
    local rx, ry, rz = getElementRotation(localPlayer)
    local vx, vy, vz = getElementVelocity(localPlayer)

    -- Enviar al servidor
    triggerServerEvent("onClientPositionSync", localPlayer, {
        x = x, y = y, z = z,
        rx = rx, ry = ry, rz = rz,
        vx = vx, vy = vy, vz = vz
    })
end
setTimer(syncWithServer, 100, 0)  -- Cada 100ms

-- ============================================
-- INICIALIZACIÓN
-- ============================================

print("=== Client Script Loaded ===")
print("Commands: /money, /job, /help")
print("Press H to toggle HUD")
print("Press T to chat")
