# GTAS Framework - Implementation Guide

## Quick Start: Building Your First Framework Resource

### Step 1: Create Framework Folder Structure

```
resources/
├── fxframework/                    # Core framework
│   ├── manifest.lua
│   ├── server/
│   │   ├── framework.lua          # Main framework class
│   │   ├── database.lua           # Database module
│   │   ├── players.lua            # Players module
│   │   ├── jobs.lua               # Jobs module
│   │   ├── characters.lua         # Characters module
│   │   ├── economy.lua            # Economy module
│   │   └── events.lua             # Events module
│   └── client/
│       ├── framework.lua
│       └── ui.lua
│
└── gamemode-sa-rp/                 # Your gamemode
    ├── manifest.lua
    ├── server/
    │   ├── main.lua
    │   ├── jobs.lua
    │   └── commands.lua
    └── client/
        ├── main.lua
        └── hud.lua
```

### Step 2: Core Framework Implementation

#### `fxframework/manifest.lua`

```lua
return {
    info = {
        name = "GTAS Framework",
        author = "GTAS Dev Team",
        version = "1.0.0",
        description = "Core framework system for GTAS",
        type = "framework",
    },
    
    scripts = {
        {file = "server/framework.lua", type = "server", priority = 0},
        {file = "server/database.lua", type = "server", priority = 1},
        {file = "server/players.lua", type = "server", priority = 2},
        {file = "server/jobs.lua", type = "server", priority = 3},
        {file = "server/characters.lua", type = "server", priority = 4},
        {file = "server/economy.lua", type = "server", priority = 5},
        {file = "server/events.lua", type = "server", priority = 6},
        {file = "client/framework.lua", type = "client", priority = 1},
    },
    
    exports = {
        {name = "getFramework", params = "", returns = "Framework"},
        {name = "getModule", params = "name", returns = "Module"},
    },
    
    events = {
        {name = "frameworkReady", type = "server"},
        {name = "playerJoin", type = "server"},
        {name = "playerQuit", type = "server"},
    },
}
```

#### `fxframework/server/framework.lua`

```lua
class "Framework"

Framework.modules = {}
Framework.config = {}
Framework.data = {}

-- Initialize framework
function Framework:Initialize()
    print("[Framework] Starting initialization...")
    
    -- Load all modules in order
    self:LoadModule("Database")
    self:LoadModule("Events")
    self:LoadModule("Players")
    self:LoadModule("Jobs")
    self:LoadModule("Characters")
    self:LoadModule("Economy")
    
    -- Initialize each module
    for name, module in pairs(self.modules) do
        if module.Initialize then
            module:Initialize()
            print("[Framework] Loaded: " .. name)
        end
    end
    
    -- Trigger ready event
    triggerEvent("frameworkReady", root, self)
    print("[Framework] Ready!")
end

function Framework:LoadModule(name)
    local path = getResourcePath(getThisResource()) .. "/server/"
    local filename = path .. string.lower(name) .. ".lua"
    local chunk = loadstring(love.filesystem.read(filename), filename)
    local module = chunk()
    
    self.modules[name] = module
    return module
end

function Framework:GetModule(name)
    return self.modules[name]
end

function Framework:SetConfig(config)
    self.config = config
end

function Framework:GetConfig()
    return self.config
end

-- Export framework
exports("getFramework", function()
    return Framework
end)

exports("getModule", function(name)
    return Framework:GetModule(name)
end)

-- Initialize on startup
setTimer(function()
    Framework:Initialize()
end, 100, 1)
```

#### `fxframework/server/players.lua`

```lua
class "PlayersModule"

PlayersModule.players = {}
PlayersModule.callbacks = {
    join = {},
    quit = {},
    dataChange = {},
}

function PlayersModule:Initialize()
    addEventHandler("playerJoin", root, function(player)
        self:OnPlayerJoin(player)
    end)
    
    addEventHandler("playerQuit", root, function(player)
        self:OnPlayerQuit(player)
    end)
end

function PlayersModule:OnPlayerJoin(player)
    -- Create player object
    local playerObj = {
        player = player,
        id = player.id or 0,
        name = getPlayerName(player),
        data = {
            money = 5000,
            job = "unemployed",
            grade = 0,
            health = 100,
        }
    }
    
    self.players[player] = playerObj
    
    -- Trigger callbacks
    for _, callback in ipairs(self.callbacks.join) do
        callback(playerObj)
    end
    
    triggerEvent("playerJoin", root, playerObj)
end

function PlayersModule:OnPlayerQuit(player)
    if self.players[player] then
        local playerObj = self.players[player]
        
        -- Trigger callbacks
        for _, callback in ipairs(self.callbacks.quit) do
            callback(playerObj)
        end
        
        self.players[player] = nil
    end
    
    triggerEvent("playerQuit", root, player)
end

function PlayersModule:GetPlayer(player)
    return self.players[player]
end

function PlayersModule:GetAllPlayers()
    local result = {}
    for _, playerObj in pairs(self.players) do
        table.insert(result, playerObj)
    end
    return result
end

function PlayersModule:OnPlayerJoin(callback)
    table.insert(self.callbacks.join, callback)
end

function PlayersModule:OnPlayerQuit(callback)
    table.insert(self.callbacks.quit, callback)
end

function PlayersModule:GetPlayerData(player, key)
    local playerObj = self.players[player]
    if playerObj then
        return playerObj.data[key]
    end
    return nil
end

function PlayersModule:SetPlayerData(player, key, value)
    local playerObj = self.players[player]
    if playerObj then
        local oldValue = playerObj.data[key]
        playerObj.data[key] = value
        
        triggerEvent("playerDataChange", root, player, key, oldValue, value)
    end
end

return PlayersModule
```

#### `fxframework/server/jobs.lua`

```lua
class "JobsModule"

JobsModule.jobs = {}
JobsModule.playerJobs = {}

function JobsModule:RegisterJob(jobData)
    self.jobs[jobData.id] = jobData
    print("[Jobs] Registered: " .. jobData.label)
end

function JobsModule:GetJob(jobId)
    return self.jobs[jobId]
end

function JobsModule:GetPlayerJob(player)
    return self.playerJobs[player]
end

function JobsModule:SetPlayerJob(player, jobId, grade)
    local job = self.jobs[jobId]
    if not job then
        print("[Jobs] ERROR: Job not found: " .. jobId)
        return false
    end
    
    local oldJob = self.playerJobs[player]
    
    self.playerJobs[player] = {
        id = jobId,
        label = job.label,
        grade = grade or 0,
        salary = job.grades[grade + 1].salary or 0,
    }
    
    triggerEvent("jobChange", root, player, oldJob, self.playerJobs[player])
    
    -- Sync to client
    local framework = exports["fxframework"]:getFramework()
    triggerClientEvent(player, "jobSync", player, self.playerJobs[player])
    
    return true
end

function JobsModule:PlayerHasJob(player, jobId)
    local playerJob = self.playerJobs[player]
    return playerJob and playerJob.id == jobId
end

function JobsModule:GetPlayerSalary(player)
    local playerJob = self.playerJobs[player]
    return playerJob and playerJob.salary or 0
end

return JobsModule
```

#### `fxframework/server/economy.lua`

```lua
class "EconomyModule"

EconomyModule.config = {
    startMoney = 5000,
    bankEnabled = true,
    maxMoney = 999999999,
}

EconomyModule.playerMoney = {}
EconomyModule.playerBank = {}

function EconomyModule:SetConfig(config)
    for k, v in pairs(config) do
        self.config[k] = v
    end
end

function EconomyModule:GetCash(player)
    return self.playerMoney[player] or 0
end

function EconomyModule:SetCash(player, amount)
    local oldAmount = self:GetCash(player)
    self.playerMoney[player] = math.min(amount, self.config.maxMoney)
    triggerEvent("moneyChange", root, player, oldAmount, self.playerMoney[player])
    triggerClientEvent(player, "cashSync", player, self.playerMoney[player])
end

function EconomyModule:AddCash(player, amount)
    self:SetCash(player, self:GetCash(player) + amount)
end

function EconomyModule:RemoveCash(player, amount)
    local newAmount = math.max(0, self:GetCash(player) - amount)
    self:SetCash(player, newAmount)
    return self:GetCash(player)
end

function EconomyModule:GetBankBalance(player)
    return self.playerBank[player] or 0
end

function EconomyModule:SetBankBalance(player, amount)
    self.playerBank[player] = math.min(amount, self.config.maxMoney)
    triggerClientEvent(player, "bankSync", player, self.playerBank[player])
end

function EconomyModule:AddToBank(player, amount)
    self:SetBankBalance(player, self:GetBankBalance(player) + amount)
end

function EconomyModule:RemoveFromBank(player, amount)
    self:SetBankBalance(player, math.max(0, self:GetBankBalance(player) - amount))
end

return EconomyModule
```

### Step 3: Create Your Gamemode Using Framework

#### `gamemode-sa-rp/manifest.lua`

```lua
return {
    info = {
        name = "SA-RP Gamemode",
        author = "Your Name",
        version = "1.0.0",
        type = "gamemode",
    },
    
    dependencies = {
        {name = "fxframework", version = "1.0.0", required = true},
    },
    
    scripts = {
        {file = "server/main.lua", type = "server", priority = 1},
        {file = "server/jobs.lua", type = "server", priority = 2},
        {file = "server/commands.lua", type = "server", priority = 3},
        {file = "client/main.lua", type = "client", priority = 1},
        {file = "client/hud.lua", type = "client", priority = 2},
    },
}
```

#### `gamemode-sa-rp/server/main.lua`

```lua
-- Get framework
local Framework = exports["fxframework"]:getFramework()
local Players = Framework:GetModule("Players")
local Jobs = Framework:GetModule("Jobs")
local Economy = Framework:GetModule("Economy")

-- Setup
Economy:SetConfig({
    startMoney = 5000,
    bankEnabled = true,
})

-- Register jobs
Jobs:RegisterJob({
    id = "police",
    label = "Police Officer",
    defaultGrade = 0,
    grades = {
        {id = 0, label = "Cadet", salary = 1000},
        {id = 1, label = "Officer", salary = 1500},
        {id = 2, label = "Sergeant", salary = 2000},
    }
})

Jobs:RegisterJob({
    id = "doctor",
    label = "Doctor",
    defaultGrade = 0,
    grades = {
        {id = 0, label = "Intern", salary = 800},
        {id = 1, label = "Doctor", salary = 1200},
    }
})

-- Player join event
Players:OnPlayerJoin(function(player)
    print("[Gamemode] Player joined: " .. player.name)
    Economy:SetCash(player.player, 5000)
    Jobs:SetPlayerJob(player.player, "unemployed", 0)
end)

-- Salary system (every 10 minutes)
setTimer(function()
    for _, playerObj in ipairs(Players:GetAllPlayers()) do
        local player = playerObj.player
        local salary = Jobs:GetPlayerSalary(player)
        if salary > 0 then
            Economy:AddCash(player, salary)
            outputChatBox("[Salary] You earned $" .. salary, player, 0, 255, 0)
        end
    end
end, 600000, 0)

print("[Gamemode] SA-RP initialized!")
```

#### `gamemode-sa-rp/server/jobs.lua`

```lua
local Framework = exports["fxframework"]:getFramework()
local Jobs = Framework:GetModule("Jobs")

-- Job commands
addCommandHandler("job", function(player, command, jobId, grade)
    jobId = jobId or "police"
    grade = tonumber(grade) or 0
    
    if Jobs:SetPlayerJob(player, jobId, grade) then
        outputChatBox("Job changed to: " .. jobId, player, 0, 255, 0)
    else
        outputChatBox("Job not found", player, 255, 0, 0)
    end
end)

addCommandHandler("myjob", function(player)
    local job = Jobs:GetPlayerJob(player)
    if job then
        outputChatBox("Your job: " .. job.label .. " (Grade: " .. job.grade .. ")", player, 0, 255, 0)
    else
        outputChatBox("You have no job", player, 255, 0, 0)
    end
end)
```

#### `gamemode-sa-rp/server/commands.lua`

```lua
local Framework = exports["fxframework"]:getFramework()
local Players = Framework:GetModule("Players")
local Economy = Framework:GetModule("Economy")

addCommandHandler("money", function(player)
    local cash = Economy:GetCash(player)
    local bank = Economy:GetBankBalance(player)
    outputChatBox("Cash: $" .. cash .. " | Bank: $" .. bank, player, 0, 255, 0)
end)

addCommandHandler("give", function(player, amount)
    amount = tonumber(amount) or 0
    if amount > 0 then
        Economy:AddCash(player, amount)
        outputChatBox("Given $" .. amount, player, 0, 255, 0)
    end
end)

addCommandHandler("players", function(player)
    local allPlayers = Players:GetAllPlayers()
    outputChatBox("Online players: " .. #allPlayers, player, 0, 255, 0)
    for _, playerObj in ipairs(allPlayers) do
        outputChatBox("- " .. playerObj.name, player)
    end
end)
```

#### `gamemode-sa-rp/client/main.lua`

```lua
-- Client framework
local playerData = {
    money = 0,
    job = "unemployed",
    health = 100,
}

-- Listen for sync events
addEventHandler("cashSync", root, function(amount)
    playerData.money = amount
end)

addEventHandler("jobSync", root, function(jobData)
    playerData.job = jobData.label
    outputChatBox("Your job: " .. jobData.label, 0, 255, 0)
end)

-- Commands
addCommandHandler("money", function()
    outputChatBox("Your money: $" .. playerData.money, 0, 255, 0)
end)
```

#### `gamemode-sa-rp/client/hud.lua`

```lua
local playerMoney = 0

addEventHandler("cashSync", root, function(amount)
    playerMoney = amount
end)

addEventHandler("onClientRender", root, function()
    -- Draw HUD
    dxDrawText("Money: $" .. playerMoney, 20, 20, 300, 60, tocolor(0, 255, 0, 255), 1.5)
end)
```

## Usage Examples

### Example 1: Adding a New Job Type

```lua
-- In your gamemode
local Jobs = Framework:GetModule("Jobs")

Jobs:RegisterJob({
    id = "taxi",
    label = "Taxi Driver",
    grades = {
        {id = 0, label = "Driver", salary = 400},
        {id = 1, label = "Senior Driver", salary = 600},
    }
})
```

### Example 2: Custom Event Handler

```lua
local Framework = exports["fxframework"]:getFramework()
local Events = Framework:GetModule("Events")

Events:Register("customEvent", function(player, data)
    print("Custom event fired: " .. player:GetName())
end)

-- Trigger it
Events:Trigger("customEvent", player, {some = "data"})
```

### Example 3: Database Integration

```lua
local Framework = exports["fxframework"]:getFramework()
local Database = Framework:GetDatabase()

-- Query
local players = Database:Query("SELECT * FROM players WHERE job = ?", {"police"})
for _, row in ipairs(players) do
    print(row.name)
end

-- Insert
Database:Insert("players", {
    name = "John Doe",
    job = "police",
})

-- Update
Database:Update("players", {job = "doctor"}, "WHERE name = ?", {"John Doe"})
```

## Best Practices

1. **Always check if framework is ready** before using modules
2. **Use local variables** for modules to improve performance
3. **Cache frequently accessed data**
4. **Use events instead of direct function calls** when possible
5. **Handle errors gracefully** with try-catch patterns
6. **Document your APIs** with examples
7. **Test with multiple players** to find performance issues

## Troubleshooting

### Framework not initializing

```lua
-- Add delay
setTimer(function()
    local Framework = exports["fxframework"]:getFramework()
    if Framework then
        print("Framework ready")
    end
end, 1000, 1)
```

### Module not found

```lua
-- Check if resource is running
if getResourceFromName("fxframework") then
    local Framework = exports["fxframework"]:getFramework()
    local Module = Framework:GetModule("Players")
end
```

### Performance issues

```lua
-- Check memory usage
print("Memory: " .. collectgarbage("count") / 1024 .. "MB")

-- Profile events
local startTime = getTickCount()
-- Do something
print("Time: " .. (getTickCount() - startTime) .. "ms")
```

## Next Steps

1. Create your own gamemode using the framework
2. Add custom jobs and events
3. Implement database persistence
4. Create NUI-based UI
5. Add voice communication
6. Implement anti-cheat

The framework provides the foundation - you build on it!
