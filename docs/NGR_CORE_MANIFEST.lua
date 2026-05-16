-- NGR Core Framework - manifest.lua
-- Complete core framework for NGR Multiplayer

return {
    info = {
        name = "NGR Core Framework",
        author = "NGR Development Team",
        version = "1.0.0",
        description = "Core framework system for NGR Multiplayer - Fast, optimized, FiveM-style",
        type = "framework",
    },

    config = {
        max_players = 100,
        max_vehicles = 500,
        max_objects = 1000,

        update_rate = 100,        -- ms between updates
        bandwidth_limit = 1024,   -- KB/s per player

        features = {
            voice_chat = false,
            vehicles = true,
            gangs = true,
            economy = true,
        }
    },

    scripts = {
        -- Core framework (load first)
        {file = "server/framework.lua", type = "server", priority = 0, timeout = 5000},

        -- Database module
        {file = "server/database.lua", type = "server", priority = 1, timeout = 5000},

        -- Event system
        {file = "server/events.lua", type = "server", priority = 2, timeout = 5000},

        -- Players module
        {file = "server/players.lua", type = "server", priority = 3, timeout = 5000},

        -- Jobs module
        {file = "server/jobs.lua", type = "server", priority = 4, timeout = 5000},

        -- Characters module
        {file = "server/characters.lua", type = "server", priority = 5, timeout = 5000},

        -- Economy module
        {file = "server/economy.lua", type = "server", priority = 6, timeout = 5000},

        -- Client framework
        {file = "client/framework.lua", type = "client", priority = 1, cache = true},
    },

    dependencies = {},

    exports = {
        {name = "getFramework", params = "", returns = "Framework"},
        {name = "getModule", params = "name", returns = "Module"},
        {name = "getPlayer", params = "player", returns = "PlayerObject"},
    },

    events = {
        {name = "frameworkReady", type = "server", params = "framework"},
        {name = "playerJoin", type = "server", params = "player, playerData"},
        {name = "playerQuit", type = "server", params = "player"},
        {name = "jobChange", type = "server", params = "player, oldJob, newJob"},
        {name = "moneyChange", type = "server", params = "player, oldAmount, newAmount"},
        {name = "characterCreated", type = "server", params = "player, character"},
    },

    database = {
        type = "sqlite",
        file = "ngr_database.db",
        auto_create = true,
    },

    logging = {
        level = "info",
        file = "logs/ngr_core.log",
        max_size = "10MB",
        backup_count = 5,
    },

    security = {
        anti_cheat = {
            enabled = true,
            level = 2,  -- 0=None, 1=Basic, 2=Advanced, 3=Strict
            detections = {
                {name = "speed_hack", enabled = true, threshold = 250},
                {name = "teleport_hack", enabled = true, threshold = 100},
                {name = "health_hack", enabled = true},
                {name = "weapon_hack", enabled = true},
            },
        },
        validation = {
            client_prediction = true,
            server_override = true,
            timeout = 5000,
        },
    },

    acl = {
        groups = {
            {
                name = "admin",
                permissions = {
                    "script.start",
                    "script.stop",
                    "kick.player",
                    "ban.player",
                    "command.admin",
                },
            },
            {
                name = "moderator",
                permissions = {
                    "kick.player",
                    "mute.player",
                    "warn.player",
                },
            },
            {
                name = "player",
                permissions = {
                    "chat.send",
                    "move",
                    "attack",
                },
            },
        },
    },
}
