# GTAS Framework Architecture - FiveM Style

## Overview

GTAS Framework is a comprehensive system inspired by FiveM (ESX, vRP, QBCore) that provides:

- Built-in job system
- Character management
- Economy system
- Permission system
- Database integration
- Event broadcasting
- Common APIs
- Resource management

## Framework Structure

```
Framework (fxframework)
├── Core
│   ├── Players API
│   ├── Jobs API
│   ├── Characters API
│   ├── Economy API
│   └── Database API
├── Utilities
│   ├── Events
│   ├── Exports
│   ├── Timers
│   └── Logging
├── Built-in Resources
│   ├── spawn-select
│   ├── character-creator
│   ├── job-system
│   ├── economy-system
│   └── permissions
└── Extensions
    └── Custom resources built on framework
```

## Framework APIs

### 1. Players API

```lua
-- Server side
local Players = Framework:GetModule("Players")

-- Get player by ID
local player = Players:GetPlayer(playerId)

-- Get all players
local allPlayers = Players:GetAllPlayers()

-- Get player data
local playerData = player:GetData()
local money = player:GetMoney()
local job = player:GetJob()

-- Set player data
player:SetMoney(5000)
player:SetJob("police")
player:AddMoney(100)

-- Events
Players:OnPlayerJoin(function(player)
    print("Player joined: " .. player:GetName())
end)

Players:OnPlayerQuit(function(player)
    print("Player quit: " .. player:GetName())
end)
```

### 2. Jobs API

```lua
-- Server side
local Jobs = Framework:GetModule("Jobs")

-- Define job
Jobs:RegisterJob({
    id = "police",
    label = "Police Officer",
    defaultGrade = 0,
    grades = {
        {id = 0, label = "Cadet", salary = 1000},
        {id = 1, label = "Officer", salary = 1500},
        {id = 2, label = "Sergeant", salary = 2000},
        {id = 3, label = "Captain", salary = 3000},
    }
})

-- Check if player has job
if Jobs:PlayerHasJob(player, "police") then
    print("Player is a cop")
end

-- Get player job
local playerJob = Jobs:GetPlayerJob(player)
print("Job: " .. playerJob.label .. " (Grade: " .. playerJob.grade.label .. ")")

-- Set player job
Jobs:SetPlayerJob(player, "police", 1)

-- Get salary
local salary = Jobs:GetPlayerSalary(player)

-- Pay players
setTimer(function()
    for _, player in ipairs(Players:GetAllPlayers()) do
        local salary = Jobs:GetPlayerSalary(player)
        if salary > 0 then
            player:AddMoney(salary)
        end
    end
end, 600000, 0)  -- Every 10 minutes
```

### 3. Economy API

```lua
-- Server side
local Economy = Framework:GetModule("Economy")

-- Setup economy
Economy:SetConfig({
    startMoney = 5000,
    bankEnabled = true,
    maxMoney = 999999999,
})

-- Bank system
local bankBalance = Economy:GetBankBalance(player)
Economy:SetBankBalance(player, 50000)
Economy:AddToBank(player, 1000)
Economy:RemoveFromBank(player, 500)

-- Money system
local cash = Economy:GetCash(player)
Economy:SetCash(player, 10000)
Economy:AddCash(player, 100)
Economy:RemoveCash(player, 50)

-- Transactions
Economy:Transaction({
    from = player1,
    to = player2,
    amount = 500,
    reason = "Item sale"
})

-- Business system
local business = Economy:CreateBusiness({
    id = "24-7",
    label = "24/7 Store",
    owner = player,
    funds = 50000,
    employees = {},
})

business:WithdrawFunds(1000)
business:AddEmployee(player2, "manager")
```

### 4. Character API

```lua
-- Server side
local Characters = Framework:GetModule("Characters")

-- Create character
local character = Characters:CreateCharacter(player, {
    firstName = "John",
    lastName = "Doe",
    dateOfBirth = "1990-01-15",
    gender = "M",
    skinHash = 0x94a5a5f,
})

-- Get character
local char = Characters:GetCharacter(player)
print("Character: " .. char:GetFullName())

-- Character customization
char:SetClothes(3, 0, 0, 0)  -- Head, drawable, texture, palette
char:SetClothes(8, 15, 0, 0)  -- Torso
char:SetModel("a_m_m_business_1")  -- Model

-- Character data
char:SetData("tattoos", tattoosTable)
char:SetData("scars", scarsTable)
char:SetMetadata("playtime", 1200)

-- Events
Characters:OnCharacterCreated(function(character)
    print("Character created: " .. character:GetFullName())
end)
```

### 5. Database API

```lua
-- Server side
local Database = Framework:GetDatabase()

-- Query
local results = Database:Query("SELECT * FROM players WHERE job = ?", {"police"})
for _, row in ipairs(results) do
    print(row.name)
end

-- Insert
Database:Insert("players", {
    name = "John Doe",
    job = "police",
    salary = 1500,
})

-- Update
Database:Update("players", {
    job = "doctor",
    salary = 2000,
}, "WHERE id = ?", {123})

-- Delete
Database:Delete("players", "WHERE id = ?", {123})

-- Raw query with caching
local cached = Database:Query(
    "SELECT * FROM players WHERE job = ?",
    {"police"},
    {cache = 300}  -- Cache 5 minutes
)

-- Transactions
Database:Transaction(function(tx)
    tx:Insert("transactions", {...})
    tx:Update("players", {...})
    -- Commits on success, rollbacks on error
end)
```

### 6. Event System

```lua
-- Server side
local Events = Framework:GetModule("Events")

-- Register event
Events:Register("playerJobChange", function(player, oldJob, newJob)
    print(player:GetName() .. " changed job from " .. oldJob .. " to " .. newJob)
    -- Broadcast to clients
    Events:Trigger("playerJobChangeClient", player, oldJob, newJob)
end)

-- Trigger event
Events:Trigger("playerJobChange", player, "police", "doctor")

-- Client side
Events:Register("playerJobChangeClient", function(player, oldJob, newJob)
    if player == localPlayer then
        print("Your job changed to: " .. newJob)
    end
end)

-- Wait for event (async)
local result = Events:Wait("playerMoneyChange", 5000)  -- 5 second timeout
```

### 7. Export System

```lua
-- Resource: job-dispatcher
local Jobs = Framework:GetModule("Jobs")

-- Export function
exports("getPlayerJob", function(player)
    return Jobs:GetPlayerJob(player)
end)

exports("setPlayerJob", function(player, jobId, grade)
    Jobs:SetPlayerJob(player, jobId, grade)
end)

-- Use from another resource
local job = exports["job-dispatcher"]:getPlayerJob(player)
```

## Framework Implementation

### Server Initialization

```lua
-- server/framework.lua

class "Framework"

Framework.modules = {}
Framework.config = {}
Framework.data = {}

function Framework:Initialize()
    print("[Framework] Initializing...")
    
    -- Load core modules
    self:LoadModule("Database", "framework/db")
    self:LoadModule("Players", "framework/players")
    self:LoadModule("Jobs", "framework/jobs")
    self:LoadModule("Characters", "framework/characters")
    self:LoadModule("Economy", "framework/economy")
    self:LoadModule("Events", "framework/events")
    
    -- Load configuration
    self:LoadConfig()
    
    -- Initialize modules
    for name, module in pairs(self.modules) do
        if module.Initialize then
            module:Initialize()
            print("[Framework] Initialized: " .. name)
        end
    end
    
    print("[Framework] Ready")
end

function Framework:LoadModule(name, path)
    local module = dofile(path .. ".lua")
    self.modules[name] = module
    return module
end

function Framework:GetModule(name)
    return self.modules[name]
end

function Framework:LoadConfig()
    local config = dofile("framework/config.lua")
    self.config = config
end
```

## Manifest for Framework

```lua
-- manifest.lua

return {
    info = {
        name = "GTAS Framework",
        author = "GTAS Dev",
        version = "1.0.0",
        description = "Core framework system like FiveM",
        type = "framework",
    },
    
    scripts = {
        -- Core
        {file = "server/framework.lua", type = "server", priority = 0},
        {file = "server/database.lua", type = "server", priority = 1},
        {file = "server/players.lua", type = "server", priority = 2},
        {file = "server/jobs.lua", type = "server", priority = 3},
        {file = "server/characters.lua", type = "server", priority = 4},
        {file = "server/economy.lua", type = "server", priority = 5},
        {file = "server/events.lua", type = "server", priority = 6},
        
        -- Client
        {file = "client/framework.lua", type = "client", priority = 1},
        {file = "client/ui.lua", type = "client", priority = 2},
    },
    
    exports = {
        {name = "getFramework", params = "", returns = "Framework"},
        {name = "getModule", params = "name", returns = "Module"},
        {name = "getPlayer", params = "playerId", returns = "Player"},
    },
    
    events = {
        {name = "onFrameworkReady", type = "server", params = "framework"},
        {name = "onPlayerJoin", type = "server", params = "player"},
        {name = "onPlayerQuit", type = "server", params = "player"},
        {name = "onJobChange", type = "server", params = "player, oldJob, newJob"},
        {name = "onMoneyChange", type = "server", params = "player, oldAmount, newAmount"},
    },
}
```

## Building on Framework

### Example: Custom Job Resource

```lua
-- resources/job-taxi/manifest.lua

return {
    info = {
        name = "Taxi Job",
        author = "Developer",
        type = "job",
    },
    
    dependencies = {
        {name = "fxframework", version = "1.0.0", required = true},
    },
    
    scripts = {
        {file = "server/taxi.lua", type = "server", priority = 1},
        {file = "client/taxi.lua", type = "client", priority = 1},
    },
}
```

```lua
-- resources/job-taxi/server/taxi.lua

local Framework = exports["fxframework"]:getFramework()
local Jobs = Framework:GetModule("Jobs")

-- Register taxi job
Jobs:RegisterJob({
    id = "taxi",
    label = "Taxi Driver",
    defaultGrade = 0,
    grades = {
        {id = 0, label = "Driver", salary = 500},
        {id = 1, label = "Senior Driver", salary = 750},
    }
})

-- Taxi specific events
Framework:GetModule("Events"):Register("taxiJobAccepted", function(player, destination)
    local job = Jobs:GetPlayerJob(player)
    if job.id == "taxi" then
        print("Taxi job accepted: " .. destination)
    end
end)
```

## Optimization Strategies

### 1. Memory Pooling

```lua
class "ObjectPool"

function ObjectPool:new(objectType, poolSize)
    self.objects = {}
    self.available = {}
    self.objectType = objectType
    
    -- Pre-allocate objects
    for i = 1, poolSize do
        table.insert(self.available, objectType())
    end
end

function ObjectPool:acquire()
    if #self.available > 0 then
        return table.remove(self.available)
    else
        return self.objectType()
    end
end

function ObjectPool:release(object)
    table.insert(self.available, object)
end
```

### 2. Event Debouncing

```lua
local function debounce(func, delay)
    local lastCall = 0
    return function(...)
        local now = getTickCount()
        if now - lastCall >= delay then
            lastCall = now
            return func(...)
        end
    end
end

-- Usage
addEventHandler("onPlayerMove", root, debounce(function(player)
    syncPlayerPosition(player)
end, 100))  -- Only sync every 100ms
```

### 3. Lazy Loading

```lua
local Framework = setmetatable({}, {
    __index = function(self, key)
        if key == "Players" then
            return dofile("server/players.lua")
        elseif key == "Jobs" then
            return dofile("server/jobs.lua")
        end
        return rawget(self, key)
    end
})
```

### 4. Network Optimization

```lua
-- Batch updates instead of individual packets
local pendingUpdates = {}

addEventHandler("playerMove", root, function(player, x, y, z)
    pendingUpdates[player] = {x=x, y=y, z=z}
end)

-- Send all updates in one packet every 100ms
setTimer(function()
    if next(pendingUpdates) then
        triggerClientEvent("batchPositionUpdate", root, pendingUpdates)
        pendingUpdates = {}
    end
end, 100, 0)
```

### 5. Database Connection Pooling

```lua
class "DatabasePool"

function DatabasePool:new(config, poolSize)
    self.connections = {}
    self.available = {}
    
    for i = 1, poolSize do
        table.insert(self.available, self:createConnection(config))
    end
end

function DatabasePool:acquire()
    if #self.available > 0 then
        return table.remove(self.available)
    else
        return self:createConnection(self.config)
    end
end

function DatabasePool:release(conn)
    table.insert(self.available, conn)
end
```

## Performance Tips

1. **Use Events over Direct Calls** - Events are asynchronous and non-blocking
2. **Cache Database Queries** - Use query caching for frequently accessed data
3. **Batch Network Updates** - Send multiple updates in one packet
4. **Use Object Pools** - Reuse objects instead of creating new ones
5. **Debounce High-Frequency Events** - Throttle position updates, input events
6. **Lazy Load Resources** - Load resources on demand, not all at startup
7. **Monitor Performance** - Use built-in profilers to find bottlenecks

## Framework Flow

```
Server Startup
    |
    |- Load Framework
    |- Initialize Core Modules
    |- Load Configuration
    |- Load Resources
    |- Register Exports
    |- Trigger onFrameworkReady
    |
    |- Wait for Clients
    |
Client Connects
    |
    |- Load Client Framework
    |- Sync Framework State
    |- Create Character Select UI
    |
Player Selects Character
    |
    |- Load Character Data
    |- Initialize Player Systems
    |- Load Job Data
    |- Load Economy Data
    |
Player In-Game
    |
    |- Sync Position/Rotation
    |- Listen for Job Events
    |- Update HUD
    |- Handle Input
    |
Player Quits
    |
    |- Save Character Data
    |- Save Job Progress
    |- Save Economy Data
    |- Cleanup Memory
    |- Trigger onPlayerQuit
```

## Comparison: Framework vs Raw Scripting

### Without Framework

```lua
-- server/main.lua
playerData = {}
jobNames = {[1] = "Police", [2] = "Doctor"}

function onPlayerJoin(player)
    playerData[player] = {money = 5000, job = 0}
    triggerClientEvent(player, "syncMoney", player, 5000)
end

function commandGiveMoney(player, amount)
    amount = tonumber(amount) or 0
    playerData[player].money = playerData[player].money + amount
    triggerClientEvent(player, "syncMoney", player, playerData[player].money)
end

addEventHandler("playerJoin", root, onPlayerJoin)
addCommandHandler("givemoney", commandGiveMoney)
```

### With Framework

```lua
-- resources/my-gamemode/server/main.lua
local Framework = exports["fxframework"]:getFramework()
local Players = Framework:GetModule("Players")
local Economy = Framework:GetModule("Economy")

Economy:SetConfig({startMoney = 5000})

Players:OnPlayerJoin(function(player)
    player:SetMoney(5000)
end)

addCommandHandler("givemoney", function(player, amount)
    Economy:AddCash(player, tonumber(amount) or 0)
end)
```

**Framework version is:**
- More readable
- Better organized
- Easier to maintain
- Comes with built-in systems
- Provides common APIs
- Better performance
