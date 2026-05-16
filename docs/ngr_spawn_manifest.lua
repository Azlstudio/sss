-- NGR Spawn - Small Resource Example
-- Lightweight spawn selector

return {
    info = {
        name = "NGR Spawn",
        author = "NGR Team",
        version = "1.0.0",
        description = "Simple spawn point selector",
    },

    dependencies = {
        {name = "ngr_core", version = "1.0.0", required = true},
    },

    scripts = {
        {file = "server/main.lua", type = "server", priority = 1},
        {file = "client/main.lua", type = "client", priority = 1},
        {file = "client/ui.lua", type = "client", priority = 2},
    },

    exports = {
        {name = "getSpawns", params = "", returns = "table"},
        {name = "addSpawn", params = "name, x, y, z", returns = "boolean"},
    },
}
