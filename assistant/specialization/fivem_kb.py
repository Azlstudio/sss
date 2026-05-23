class FiveMLLMKnowledge:
    """FiveM and GTA V scripting knowledge base."""

    SYSTEM_PROMPT = """You are an expert FiveM scripting assistant specializing in:
- Lua scripting for FiveM servers
- RedM (Red Dead Redemption 2) framework
- QBCore and ESX framework implementation
- Database management (MySQL, MongoDB)
- Client-side and server-side mechanics
- Vehicle handling, weapon systems, NPC behavior
- Custom jobs, heists, and game modes
- Performance optimization
- Security best practices

Always provide code examples and reference the FiveM documentation when applicable.
Focus on best practices and secure, efficient implementations."""

    KNOWLEDGE_BASE = {
        'frameworks': {
            'qbcore': """QBCore is a comprehensive FiveM framework featuring:
- Player management and character system
- Jobs and employment system
- Inventory and item management
- Property ownership
- Gang system
- Database integration with MySQL
- Server callbacks and client-server communication""",

            'esx': """ESX (Extended Server X) framework includes:
- Job and grading system
- Bank and money management
- Inventory system
- Character data persistence
- Native ESX exports
- Job-specific equipment and vehicles""",

            'redm': """RedM framework for Red Dead Redemption 2:
- Character creation and management
- Job system unique to RDR2
- Camp management
- Hunting and fishing mechanics
- Gang wars
- Custom missions and storylines"""
        },

        'common_patterns': {
            'client_server_sync': """
-- Server-side
exports['qbcore']:TriggerClientCallback('GetPlayerData', function(source)
    local Player = QBCore.Functions.GetPlayer(source)
    return Player.PlayerData
end)

-- Client-side
QBCore.Functions.TriggerCallback('GetPlayerData', function(data)
    print("Got player data:", json.encode(data))
end)""",

            'database_query': """
-- Query the database
exports.oxmysql:execute('SELECT * FROM `users` WHERE `citizenid` = ?', {citizenid}, function(result)
    if result[1] then
        print("User found: " .. result[1].name)
    end
end)""",

            'command_handler': """
-- Register a command
RegisterCommand('test', function(source, args, rawCommand)
    if source == 0 then return end
    local Player = QBCore.Functions.GetPlayer(source)
    TriggerClientEvent('chat:addMessage', source, {
        args = {'System'},
        msg = 'Hello ' .. Player.PlayerData.charinfo.firstname
    })
end, false)""",

            'marker_blip': """
-- Create a blip
local blip = AddBlipForCoord(coords)
SetBlipAsNoLongerNeeded(blip)
SetBlipSprite(blip, 227)
SetBlipColour(blip, 0)
AddTextComponentString(label)
AddBlipTextComponentSubstring_2N(0x9B292A1C)"""
        },

        'optimization_tips': [
            "Use server callbacks only when necessary to minimize network traffic",
            "Batch database queries and use caching where possible",
            "Avoid using TriggerClientEvent in loops",
            "Use exports for cross-resource communication",
            "Always validate input on server-side",
            "Use proper error handling with try-catch blocks",
            "Profile your code with lua timer and optimize hot paths",
            "Use timers instead of while loops with sleeps"
        ],

        'security': [
            "Never trust client-side data",
            "Validate all server-side calls",
            "Use token/session validation for sensitive operations",
            "Encrypt sensitive database fields",
            "Implement rate limiting for API calls",
            "Sanitize all user input",
            "Use server-side permissions checking",
            "Log all sensitive operations for audit trails"
        ]
    }

    @staticmethod
    def get_framework_info(framework: str) -> str:
        """Get information about a specific framework."""
        return FiveMLLMKnowledge.KNOWLEDGE_BASE['frameworks'].get(
            framework.lower(),
            "Framework not found in knowledge base."
        )

    @staticmethod
    def get_pattern(pattern_name: str) -> str:
        """Get a code pattern."""
        return FiveMLLMKnowledge.KNOWLEDGE_BASE['common_patterns'].get(
            pattern_name.lower(),
            "Pattern not found."
        )

    @staticmethod
    def get_tips(category: str) -> list:
        """Get tips for a specific category."""
        if category.lower() == 'optimization':
            return FiveMLLMKnowledge.KNOWLEDGE_BASE['optimization_tips']
        elif category.lower() == 'security':
            return FiveMLLMKnowledge.KNOWLEDGE_BASE['security']
        return []
