class MTAKnowledge:
    """MTA: San Andreas scripting knowledge base."""

    SYSTEM_PROMPT = """You are an expert MTA: San Andreas scripting assistant specializing in:
- Lua scripting for MTA servers
- Multi Theft Auto framework
- Client-side and server-side resource management
- Vehicle systems and physics
- Weapon systems and combat
- Map system and marker management
- Database integration (SQLite, MySQL)
- GUI and interface design
- Custom gamemodes (DM, TDM, RPG)
- Anti-cheat and security systems

Focus on MTA-specific mechanics and best practices."""

    KNOWLEDGE_BASE = {
        'core_concepts': {
            'resources': """MTA resources are independent game packages containing:
- Lua scripts (client-side and server-side)
- Images, sounds, and media files
- Configuration files
- Can communicate with other resources
- Have their own namespace and environment""",

            'events': """Event system allows resources to communicate:
- triggerEvent: Trigger events locally
- triggerClientEvent: Server to client
- triggerServerEvent: Client to server
- addEventHandler: Register event listeners
- removeEventHandler: Unregister listeners""",

            'elements': """MTA elements (game objects):
- Players: Human players
- Vehicles: Cars, motorcycles, boats
- Objects: Static/dynamic world objects
- Markers: Invisible game zones
- Blips: Radar markers
- Peds: Non-player characters
- Pickups: Collectible items"""
        },

        'code_patterns': {
            'server_client_call': """
-- Server-side
function givePlayerWeapon(player, weaponId, ammo)
    giveWeapon(player, weaponId, ammo)
    triggerClientEvent(player, 'onWeaponGive', player, weaponId)
end

-- Client-side
addEventHandler('onWeaponGive', root, function(player, weaponId)
    outputChatBox('You received weapon ID: ' .. weaponId)
end)""",

            'database_sqlite': """
local db = dbConnect('sqlite', ':memory:')
dbExec(db, 'CREATE TABLE players (id INTEGER, name TEXT)')
dbExec(db, 'INSERT INTO players VALUES (1, "John")')
local result = dbQuery(db, 'SELECT * FROM players')
local row = dbPoll(result, -1)""",

            'vehicle_spawn': """
local x, y, z = 0, 0, 3
local rotation = 0
local vehID = 411  -- Infernus
local vehicle = createVehicle(vehID, x, y, z, 0, 0, rotation)
warpPlayerIntoVehicle(getLocalPlayer(), vehicle)""",

            'marker_system': """
local x, y, z = 0, 0, 0
local size = 2.0
local r, g, b, a = 255, 0, 0, 100
local marker = createMarker(x, y, z, 'cylinder', size, r, g, b, a)

addEventHandler('onMarkerHit', marker, function(element)
    if getElementType(element) == 'player' then
        outputChatBox('Entered marker!')
    end
end)"""
        },

        'optimization': [
            "Use getElementsByType instead of looping all elements",
            "Cache element references instead of calling functions repeatedly",
            "Use setTimer with appropriate intervals",
            "Avoid heavy operations on onRender event",
            "Use getDevelopmentMode() to debug",
            "Batch database queries when possible",
            "Use locals instead of globals where possible",
            "Profile with client metrics and server performance tools"
        ],

        'best_practices': [
            "Always validate player permissions before actions",
            "Use proper namespacing for variables",
            "Handle errors with pcall for robustness",
            "Document functions with clear comments",
            "Use consistent naming conventions",
            "Implement proper logging system",
            "Test with multiple clients",
            "Keep client-side code secure (assume compromised)"
        ]
    }

    @staticmethod
    def get_concept(concept: str) -> str:
        """Get explanation of MTA concept."""
        return MTAKnowledge.KNOWLEDGE_BASE['core_concepts'].get(
            concept.lower(),
            "Concept not found."
        )

    @staticmethod
    def get_pattern(pattern_name: str) -> str:
        """Get MTA code pattern."""
        return MTAKnowledge.KNOWLEDGE_BASE['code_patterns'].get(
            pattern_name.lower(),
            "Pattern not found."
        )

    @staticmethod
    def get_tips(category: str) -> list:
        """Get tips for a category."""
        if category.lower() == 'optimization':
            return MTAKnowledge.KNOWLEDGE_BASE['optimization']
        elif category.lower() == 'best_practices':
            return MTAKnowledge.KNOWLEDGE_BASE['best_practices']
        return []
