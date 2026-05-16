-- NGR Spawn - Client Side
-- Spawn UI and selection

local spawns = {}
local selectedSpawn = 1

-- Get spawns from server
function loadSpawns()
    spawns = exports["ngr_spawn"]:getSpawns()
end

-- Select spawn
function selectSpawn(spawnId)
    selectedSpawn = spawnId
end

-- Confirm spawn
function confirmSpawn()
    triggerServerEvent("spawnSelected", root, selectedSpawn)
end

-- Setup
addEventHandler("onClientResourceStart", resourceRoot, function()
    loadSpawns()
    print("[NGR Spawn Client] Ready")
end)

-- Commands
addCommandHandler("spawn", function()
    local menu = {}
    for i, spawn in ipairs(spawns) do
        table.insert(menu, "[" .. i .. "] " .. spawn.name)
    end
    outputChatBox("Available spawns:", 0, 255, 0)
    for _, item in ipairs(menu) do
        outputChatBox(item)
    end
    outputChatBox("Use: /spawnselect [number]")
end)

addCommandHandler("spawnselect", function(cmd, spawnId)
    spawnId = tonumber(spawnId)
    if spawnId and spawns[spawnId] then
        selectSpawn(spawnId)
        confirmSpawn()
    else
        outputChatBox("Invalid spawn", 255, 0, 0)
    end
end)
