-- NGR Notifications - Small Resource Example
-- Lightweight notification system

-- manifest.lua
local manifest = {
    info = {
        name = "NGR Notifications",
        author = "NGR Team",
        version = "1.0.0",
        description = "Fast notification system",
    },

    dependencies = {
        {name = "ngr_core", version = "1.0.0", required = true},
    },

    scripts = {
        {file = "client/main.lua", type = "client", priority = 1},
    },

    exports = {
        {name = "notify", params = "title, message, type, duration"},
        {name = "notifyPlayer", params = "player, title, message, type, duration"},
    },
}

-- client/main.lua (Optimized)

local notifications = {}
local notificationId = 0

-- Notification colors (RGB)
local colors = {
    success = {r = 0, g = 255, b = 0},      -- Green
    error = {r = 255, g = 0, b = 0},       -- Red
    warning = {r = 255, g = 165, b = 0},   -- Orange
    info = {r = 0, g = 150, b = 255},      -- Blue
}

-- Show notification
local function notify(title, message, notifType, duration)
    notifType = notifType or "info"
    duration = duration or 5000

    notificationId = notificationId + 1
    local id = notificationId

    local color = colors[notifType] or colors.info

    notifications[id] = {
        title = title,
        message = message,
        type = notifType,
        color = color,
        duration = duration,
        startTime = getTickCount(),
        id = id,
    }

    return id
end

-- Show notification to player (server-side RPC)
local function notifyPlayer(player, title, message, notifType, duration)
    triggerClientEvent(player, "notificationShow", player, title, message, notifType, duration)
end

-- Listen for server notifications
addEventHandler("notificationShow", root, function(title, message, notifType, duration)
    notify(title, message, notifType, duration)
end)

-- Render notifications
addEventHandler("onClientRender", root, function()
    local screenWidth, screenHeight = guiGetScreenSize()
    local yOffset = 20

    for id, notif in pairs(notifications) do
        local elapsed = getTickCount() - notif.startTime
        local progress = elapsed / notif.duration

        -- Remove if expired
        if progress >= 1 then
            notifications[id] = nil
        else
            -- Calculate alpha (fade out)
            local alpha = 255 * (1 - math.max(0, progress - 0.8) * 5)

            -- Draw notification box
            dxDrawRectangle(
                screenWidth - 320, yOffset,
                300, 80,
                tocolor(30, 30, 30, alpha)
            )

            -- Draw border (color based on type)
            dxDrawRectangle(
                screenWidth - 320, yOffset,
                300, 3,
                tocolor(notif.color.r, notif.color.g, notif.color.b, alpha)
            )

            -- Draw title
            dxDrawText(
                notif.title,
                screenWidth - 315, yOffset + 8,
                screenWidth - 25, yOffset + 30,
                tocolor(255, 255, 255, alpha),
                1.2, "default", "left", "top"
            )

            -- Draw message
            dxDrawText(
                notif.message,
                screenWidth - 315, yOffset + 30,
                screenWidth - 25, yOffset + 75,
                tocolor(200, 200, 200, alpha),
                0.9, "default", "left", "top"
            )

            yOffset = yOffset + 90
        end
    end
end)

-- Exports
exports("notify", notify)
exports("notifyPlayer", notifyPlayer)

print("[NGR Notifications] Loaded")

return manifest
