--[[
    GTAS Multiplayer - Script de Servidor Ejemplo
    Demuestra cómo crear scripts en Lua para nuestro launcher
]]

-- ============================================
-- VARIABLES GLOBALES
-- ============================================
local playerData = {}  -- Almacenar datos de jugadores
local jobNames = {
    [1] = "Police",
    [2] = "Taxi Driver",
    [3] = "Trucker",
    [4] = "Bus Driver"
}

-- ============================================
-- FUNCIONES LOCALES (privadas)
-- ============================================
local function logAction(action, player)
    local timestamp = os.date("%Y-%m-%d %H:%M:%S")
    print("[" .. timestamp .. "] " .. action .. ": " .. getPlayerName(player))
end

local function sendToPlayer(player, title, message, r, g, b)
    triggerClientEvent(player, "onNotification", player, title, message, r, g, b)
end

-- ============================================
-- FUNCIONES EXPORTADAS (públicas - para otros scripts)
-- ============================================
function getPlayerMoney(player)
    if not playerData[player] then
        return 0
    end
    return playerData[player].money or 0
end

function setPlayerMoney(player, amount)
    if not playerData[player] then
        playerData[player] = {}
    end

    local oldMoney = playerData[player].money or 0
    playerData[player].money = amount

    -- Disparar evento personalizado
    triggerEvent("onPlayerMoneyChange", player, oldMoney, amount)

    -- Actualizar cliente
    triggerClientEvent(player, "onMoneyUpdate", player, amount)

    return true
end

function addPlayerMoney(player, amount)
    local currentMoney = getPlayerMoney(player)
    setPlayerMoney(player, currentMoney + amount)
end

function getPlayerJobs(player)
    if not playerData[player] then
        return {}
    end
    return playerData[player].jobs or {}
end

function setPlayerJob(player, jobId)
    if not playerData[player] then
        playerData[player] = {}
    end

    local oldJob = playerData[player].job
    playerData[player].job = jobId

    -- Disparar evento
    triggerEvent("onPlayerJobChange", player, oldJob, jobId)

    -- Notificar al cliente
    sendToPlayer(player, "Job Changed", "You are now a " .. (jobNames[jobId] or "Unknown"), 0, 255, 0)

    return true
end

-- ============================================
-- EVENT HANDLERS - EVENTOS INCORPORADOS
-- ============================================

-- Cuando un jugador se conecta
function onPlayerJoin(player)
    logAction("Player joined", player)

    -- Inicializar datos del jugador
    playerData[player] = {
        money = 5000,  -- Dinero inicial
        job = 0,
        level = 1,
        jobs = {},
        playtime = 0
    }

    -- Notificar a todos
    local playerName = getPlayerName(player)
    outputChatBox(playerName .. " has joined the server!", root, 0, 255, 0)
end
addEventHandler("onPlayerJoin", root, onPlayerJoin)

-- Cuando un jugador se desconecta
function onPlayerQuit(player, quitType, reason)
    logAction("Player quit", player)

    -- Guardar datos (en una base de datos real)
    -- database:savePlayerData(player, playerData[player])

    -- Limpiar datos
    playerData[player] = nil

    outputChatBox(getPlayerName(player) .. " has left the server", root, 255, 0, 0)
end
addEventHandler("onPlayerQuit", root, onPlayerQuit)

-- Cuando un jugador muere
function onPlayerDeath(ammo, killer, weapon, bodypart)
    logAction("Player died", source)

    -- Perder dinero al morir
    local moneyLost = 1000
    local currentMoney = getPlayerMoney(source)

    if currentMoney >= moneyLost then
        addPlayerMoney(source, -moneyLost)
        sendToPlayer(source, "Death Penalty", "You lost $" .. moneyLost, 255, 0, 0)
    end

    -- Si hay killer, dar dinero
    if killer and killer ~= source then
        addPlayerMoney(killer, 500)
        sendToPlayer(killer, "Kill Reward", "You earned $500", 0, 255, 0)
    end
end
addEventHandler("onPlayerDeath", root, onPlayerDeath)

-- Cuando un jugador entra en un vehículo
function onVehicleEnter(player, seat, jacked)
    logAction("Vehicle enter", player)

    -- Enviar mensaje personalizado
    triggerClientEvent(player, "onVehicleInfo", player, {
        seat = seat,
        jacked = jacked
    })
end
addEventHandler("onVehicleEnter", root, onVehicleEnter)

-- ============================================
-- EVENTOS PERSONALIZADOS
-- ============================================

-- Crear eventos personalizados
addEvent("onPlayerMoneyChange", true)  -- true = se puede disparar desde cliente
addEvent("onPlayerJobChange", true)
addEvent("playerLogin", true)
addEvent("playerLogout", true)

-- Handler para login
function onPlayerLogin(username, password)
    -- Validar en servidor (CRÍTICO: nunca confiar en datos del cliente)
    local client = source  -- source es SIEMPRE confiable

    if not client then
        return
    end

    -- Verificar credenciales (en base de datos)
    -- local validUser = database:validateUser(username, password)

    -- Por ahora, aceptar
    playerData[client].username = username
    playerData[client].money = 5000

    outputChatBox(username .. " logged in!", root, 0, 255, 0)
    sendToPlayer(client, "Welcome", "Welcome to GTAS Multiplayer!", 0, 255, 0)

    -- Disparar evento de login
    triggerEvent("onPlayerLogin", client, username)
end
addEventHandler("playerLogin", root, onPlayerLogin)

-- ============================================
-- TIMERS - ACCIONES PERIÓDICAS
-- ============================================

-- Timer que actualiza datos cada 10 segundos
local updateTimer = setTimer(function()
    -- Aumentar tiempo de juego
    for player, data in pairs(playerData) do
        if data then
            data.playtime = (data.playtime or 0) + 10
        end
    end

    -- Dar dinero cada 10 segundos (por jugar)
    for player, data in pairs(playerData) do
        if data then
            addPlayerMoney(player, 10)
        end
    end
end, 10000, 0)  -- 10000ms, infinitas ejecuciones

-- ============================================
-- COMANDOS
-- ============================================

-- Comando /money para ver dinero
function commandMoney(player, command)
    local money = getPlayerMoney(player)
    outputChatBox("Your money: $" .. money, player, 0, 255, 0)
end
addCommandHandler("money", commandMoney)

-- Comando /job para cambiar trabajo
function commandJob(player, command, jobId)
    jobId = tonumber(jobId) or 1

    if jobId < 1 or jobId > 4 then
        outputChatBox("Invalid job ID (1-4)", player, 255, 0, 0)
        return
    end

    setPlayerJob(player, jobId)
    outputChatBox("Job changed to: " .. jobNames[jobId], player, 0, 255, 0)
end
addCommandHandler("job", commandJob)

-- Comando /givemoney (solo admin)
function commandGiveMoney(player, command, targetName, amount)
    amount = tonumber(amount) or 0

    if amount <= 0 then
        outputChatBox("Invalid amount", player, 255, 0, 0)
        return
    end

    -- Buscar jugador (en servidor real, usar ACL para permisos)
    local target = nil
    for _, p in ipairs(getElementsByType("player")) do
        if string.find(getPlayerName(p), targetName) then
            target = p
            break
        end
    end

    if not target then
        outputChatBox("Player not found", player, 255, 0, 0)
        return
    end

    addPlayerMoney(target, amount)
    outputChatBox(getPlayerName(player) .. " gave you $" .. amount, target, 0, 255, 0)
    outputChatBox("Gave $" .. amount .. " to " .. getPlayerName(target), player, 0, 255, 0)
end
addCommandHandler("givemoney", commandGiveMoney)

-- ============================================
-- INICIALIZACIÓN
-- ============================================

print("=== Server Script Loaded ===")
print("Available commands: /money, /job [1-4], /givemoney [player] [amount]")
print("Available exports: getPlayerMoney, setPlayerMoney, addPlayerMoney, getPlayerJobs, setPlayerJob")

-- Event que se dispara cuando el script inicia
triggerEvent("onResourceStart", resourceRoot)
