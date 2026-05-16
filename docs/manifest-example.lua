--[[
    GTAS Multiplayer - Manifest (Lua version)
    Superior to XML for flexibility and single-language approach
    Server loads this and extracts configuration table
]]

return {
    -- ============================================
    -- INFORMACIÓN DEL RECURSO
    -- ============================================
    info = {
        name = "Mi Primer Script",
        author = "MiNombre",
        version = "1.0.0",
        description = "Script de ejemplo para GTAS Multiplayer",
        type = "gamemode",  -- gamemode, script, tool, library
        category = "Gameplay",
        tags = {"RP", "Custom"},
    },

    -- ============================================
    -- CONFIGURACIÓN
    -- ============================================
    config = {
        max_players = 100,
        max_vehicles = 500,
        max_objects = 1000,

        update_rate = 100,        -- ms entre updates
        bandwidth_limit = 1024,   -- KB/s por jugador

        features = {
            voice_chat = true,
            vehicles = true,
            gangs = true,
            economy = true,
        }
    },

    -- ============================================
    -- SCRIPTS
    -- ============================================
    scripts = {
        -- Server-side scripts
        {
            file = "scripts/server/database.lua",
            type = "server",
            priority = 0,  -- Cargar primero (1 = highest)
            timeout = 5000,
        },
        {
            file = "scripts/server/main.lua",
            type = "server",
            priority = 1,
            timeout = 5000,
        },
        {
            file = "scripts/server/events.lua",
            type = "server",
            priority = 2,
        },

        -- Client-side scripts
        {
            file = "scripts/client/main.lua",
            type = "client",
            cache = true,
            priority = 1,
        },
        {
            file = "scripts/client/hud.lua",
            type = "client",
            cache = true,
            priority = 2,
        },
        {
            file = "scripts/client/render.lua",
            type = "client",
            cache = false,  -- No cachear, cargar cada vez
            priority = 3,
        },

        -- Shared scripts
        {
            file = "scripts/shared/constants.lua",
            type = "shared",
        },
        {
            file = "scripts/shared/utils.lua",
            type = "shared",
        },
    },

    -- ============================================
    -- DEPENDENCIAS
    -- ============================================
    dependencies = {
        {
            name = "database",
            version = "1.0.0",
            required = true,
        },
        {
            name = "accounts",
            version = "1.5.0",
            required = true,
        },
        {
            name = "utils",
            version = "2.0.0",
            required = false,
        },
    },

    -- ============================================
    -- FUNCIONES EXPORTADAS
    -- ============================================
    exports = {
        {
            name = "getPlayerMoney",
            parameters = "player",
            returns = "number",
            type = "server",
        },
        {
            name = "setPlayerMoney",
            parameters = "player, amount",
            type = "server",
        },
        {
            name = "addPlayerMoney",
            parameters = "player, amount",
            type = "server",
        },
        {
            name = "getPlayerJobs",
            parameters = "player",
            returns = "table",
            type = "server",
        },
    },

    -- ============================================
    -- EVENTOS PERSONALIZADOS
    -- ============================================
    events = {
        -- Server events
        {
            name = "onPlayerMoneyChange",
            type = "server",
            parameters = "player, oldAmount, newAmount",
            can_trigger_from_client = false,
        },
        {
            name = "onPlayerJobChange",
            type = "server",
            parameters = "player, oldJob, newJob",
            can_trigger_from_client = false,
        },
        {
            name = "onPlayerLogin",
            type = "server",
            parameters = "player, username",
            can_trigger_from_client = true,
        },

        -- Client events
        {
            name = "onHUDUpdate",
            type = "client",
            parameters = "data",
            can_trigger_from_server = true,
        },
        {
            name = "onPlayerSpotted",
            type = "client",
            parameters = "player, distance",
        },
    },

    -- ============================================
    -- RECURSOS (MODELOS, SONIDOS, IMÁGENES)
    -- ============================================
    resources = {
        models = {
            {
                file = "models/car.dff",
                id = 490,  -- Reemplaza el modelo 490
                texture = "models/car.txd",
            },
        },
        sounds = {
            {
                file = "sounds/notification.mp3",
                id = "notification_sound",
            },
        },
        images = {
            {
                file = "images/logo.png",
                id = "logo",
            },
        },
        data = {
            {
                file = "data/config.json",
                access = "server",
            },
        },
    },

    -- ============================================
    -- CONFIGURACIÓN DE ACL (PERMISOS)
    -- ============================================
    acl = {
        groups = {
            {
                name = "admin",
                permissions = {
                    "script.start",
                    "script.stop",
                    "kick.player",
                    "ban.player",
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
                },
            },
        },
    },

    -- ============================================
    -- ANTI-CHEAT Y SEGURIDAD
    -- ============================================
    security = {
        anti_cheat = {
            enabled = true,
            level = 2,  -- 0=None, 1=Basic, 2=Advanced, 3=Strict

            detections = {
                {
                    name = "speed_hack",
                    enabled = true,
                    threshold = 250,  -- km/h máximo
                },
                {
                    name = "teleport_hack",
                    enabled = true,
                    threshold = 100,  -- distancia máxima en 1 frame
                },
                {
                    name = "health_hack",
                    enabled = true,
                },
                {
                    name = "weapon_hack",
                    enabled = true,
                },
            },
        },

        validation = {
            client_prediction = true,
            server_override = true,
            timeout = 5000,
        },
    },

    -- ============================================
    -- BASE DE DATOS
    -- ============================================
    database = {
        type = "sqlite",  -- sqlite, mysql, postgresql
        host = "localhost",
        port = 3306,
        database = "gtas_db",
        username = "root",
        password = "password",
        pool_size = 10,
    },

    -- ============================================
    -- LOGGING
    -- ============================================
    logging = {
        level = "info",  -- debug, info, warning, error
        file = "logs/script.log",
        max_size = "10MB",
        backup_count = 5,
    },

    -- ============================================
    -- VALIDACIÓN
    -- ============================================
    validation = {
        check_syntax = true,
        check_performance = true,
        max_execution_time = 10000,  -- ms
    },
}
