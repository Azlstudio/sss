-- NGR Admin - Small Resource Example
-- Lightweight admin commands system

-- manifest.lua
local manifest = {
    info = {
        name = "NGR Admin",
        author = "NGR Team",
        version = "1.0.0",
        description = "Admin commands and utilities",
    },

    dependencies = {
        {name = "ngr_core", version = "1.0.0", required = true},
    },

    scripts = {
        {file = "server/main.lua", type = "server", priority = 1},
    },
}

-- server/main.lua
local adminLevel = {
    ["player1"] = 0,      -- Regular player
    ["admin1"] = 3,       -- Admin
    ["moderator1"] = 2,   -- Moderator
}

local function getPlayerLevel(player)
    local name = getPlayerName(player)
    return adminLevel[name] or 0
end

local function isAdmin(player, level)
    return getPlayerLevel(player) >= (level or 3)
end

-- Admin commands

-- /kick command
addCommandHandler("kick", function(player, cmd, targetName, reason)
    if not isAdmin(player, 2) then
        outputChatBox("You don't have permission", player, 255, 0, 0)
        return
    end

    local target = nil
    for _, p in ipairs(getElementsByType("player")) do
        if string.find(getPlayerName(p), targetName) then
            target = p
            break
        end
    end

    if target then
        reason = reason or "No reason given"
        outputChatBox(getPlayerName(player) .. " kicked " .. getPlayerName(target) .. ": " .. reason, root, 255, 0, 0)
        kickPlayer(target, reason)
    else
        outputChatBox("Player not found", player, 255, 0, 0)
    end
end)

-- /mute command
addCommandHandler("mute", function(player, cmd, targetName, duration)
    if not isAdmin(player, 2) then
        outputChatBox("You don't have permission", player, 255, 0, 0)
        return
    end

    local target = nil
    for _, p in ipairs(getElementsByType("player")) do
        if string.find(getPlayerName(p), targetName) then
            target = p
            break
        end
    end

    if target then
        duration = tonumber(duration) or 60
        outputChatBox(getPlayerName(player) .. " muted " .. getPlayerName(target) .. " for " .. duration .. "s", root, 255, 165, 0)
        -- Implement mute logic
    else
        outputChatBox("Player not found", player, 255, 0, 0)
    end
end)

-- /getpos command (Get player position)
addCommandHandler("getpos", function(player)
    local x, y, z = getElementPosition(player)
    outputChatBox(string.format("Position: %.2f, %.2f, %.2f", x, y, z), player, 0, 255, 0)
end)

-- /teleport command
addCommandHandler("teleport", function(player, cmd, x, y, z)
    if not isAdmin(player, 3) then
        outputChatBox("You don't have permission", player, 255, 0, 0)
        return
    end

    x = tonumber(x)
    y = tonumber(y)
    z = tonumber(z)

    if x and y and z then
        setElementPosition(player, x, y, z)
        outputChatBox("Teleported", player, 0, 255, 0)
    else
        outputChatBox("Usage: /teleport x y z", player, 255, 0, 0)
    end
end)

-- /freeze command
addCommandHandler("freeze", function(player, cmd, targetName)
    if not isAdmin(player, 3) then
        outputChatBox("You don't have permission", player, 255, 0, 0)
        return
    end

    local target = nil
    for _, p in ipairs(getElementsByType("player")) do
        if string.find(getPlayerName(p), targetName) then
            target = p
            break
        end
    end

    if target then
        toggleAllControls(target, false)
        outputChatBox(getPlayerName(target) .. " is now frozen", root, 0, 255, 0)
    else
        outputChatBox("Player not found", player, 255, 0, 0)
    end
end)

-- /unfreeze command
addCommandHandler("unfreeze", function(player, cmd, targetName)
    if not isAdmin(player, 3) then
        outputChatBox("You don't have permission", player, 255, 0, 0)
        return
    end

    local target = nil
    for _, p in ipairs(getElementsByType("player")) do
        if string.find(getPlayerName(p), targetName) then
            target = p
            break
        end
    end

    if target then
        toggleAllControls(target, true)
        outputChatBox(getPlayerName(target) .. " is now unfrozen", root, 0, 255, 0)
    else
        outputChatBox("Player not found", player, 255, 0, 0)
    end
end)

-- /help command
addCommandHandler("help", function(player)
    outputChatBox("=== NGR Admin Commands ===", player, 0, 255, 0)
    outputChatBox("/getpos - Get your position", player)

    if isAdmin(player, 2) then
        outputChatBox("/kick [player] [reason] - Kick a player", player)
        outputChatBox("/mute [player] [duration] - Mute a player", player)
    end

    if isAdmin(player, 3) then
        outputChatBox("/teleport [x] [y] [z] - Teleport", player)
        outputChatBox("/freeze [player] - Freeze player", player)
        outputChatBox("/unfreeze [player] - Unfreeze player", player)
    end
end)

print("[NGR Admin] Loaded")

return manifest
