-- NGR Spawn - Server Side
-- Lightweight spawn point system

local spawns = {
    {name = "Downtown", x = 1958.3, y = -2407.9, z = 13.5},
    {name = "Beach", x = 390.7, y = -1823.7, z = 4.3},
    {name = "Airport", x = 1948.5, y = 1021.1, z = 10.8},
    {name = "Grove Street", x = 2536.7, y = -1671.3, z = 32.3},
}

local function getSpawns()
    return spawns
end

local function addSpawn(name, x, y, z)
    table.insert(spawns, {name = name, x = x, y = y, z = z})
    return true
end

local function spawnPlayer(player, spawnId)
    if spawns[spawnId] then
        local spawn = spawns[spawnId]
        setElementPosition(player, spawn.x, spawn.y, spawn.z)
        return true
    end
    return false
end

-- Event: Player selects spawn
addEventHandler("spawnSelected", root, function(spawnId)
    local player = source
    if spawnPlayer(player, spawnId) then
        outputChatBox("Spawned at " .. spawns[spawnId].name, player, 0, 255, 0)
    end
end)

-- Exports
exports("getSpawns", getSpawns)
exports("addSpawn", addSpawn)
exports("spawnPlayer", spawnPlayer)

print("[NGR Spawn] Loaded - " .. #spawns .. " spawn points")
