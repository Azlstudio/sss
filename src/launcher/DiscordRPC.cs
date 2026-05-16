using System;
using System.Diagnostics;
using System.Threading.Tasks;
using DiscordRPC;
using DiscordRPC.Logging;

namespace GTASALauncher
{
    /// <summary>
    /// Discord RPC Manager for NGR Launcher
    /// Shows "Playing on NGR Launcher" status in Discord
    /// </summary>
    public class DiscordRPCManager
    {
        private DiscordRpcClient client;
        private bool isInitialized = false;

        // Discord Application ID (you need to register on Discord Developer Portal)
        private const string ApplicationId = "YOUR_DISCORD_APP_ID";

        public DiscordRPCManager()
        {
            InitializeDiscordRPC();
        }

        /// <summary>
        /// Initialize Discord RPC connection
        /// </summary>
        private void InitializeDiscordRPC()
        {
            try
            {
                client = new DiscordRpcClient(ApplicationId)
                {
                    Logger = new ConsoleLogger() { Level = LogLevel.Warning }
                };

                client.OnReady += (sender) =>
                {
                    Console.WriteLine("[Discord RPC] Connected!");
                    isInitialized = true;
                };

                client.OnClose += (sender, args) =>
                {
                    Console.WriteLine("[Discord RPC] Disconnected!");
                    isInitialized = false;
                };

                client.OnError += (sender, args) =>
                {
                    Console.WriteLine($"[Discord RPC] Error: {args.Code} - {args.Message}");
                    isInitialized = false;
                };

                // Connect to Discord
                if (!client.Initialize())
                {
                    Console.WriteLine("[Discord RPC] Failed to initialize");
                    isInitialized = false;
                }
                else
                {
                    isInitialized = true;
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Exception: {ex.Message}");
                isInitialized = false;
            }
        }

        /// <summary>
        /// Update status: On Launcher (Main Menu)
        /// </summary>
        public void UpdateStatusOnLauncher()
        {
            if (!isInitialized || client == null)
                return;

            try
            {
                var presence = new RichPresence()
                {
                    Details = "Browsing Servers",
                    State = "On Launcher",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher",
                        SmallImageKey = "gta_sa",
                        SmallImageText = "GTA San Andreas"
                    },
                    Timestamps = Timestamps.Now,
                    Buttons = new Button[]
                    {
                        new Button() { Label = "Download NGR", Url = "https://ngr.launcher" }
                    }
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: On Launcher");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Error updating status: {ex.Message}");
            }
        }

        /// <summary>
        /// Update status: Loading Server
        /// </summary>
        public void UpdateStatusLoading(string serverName)
        {
            if (!isInitialized || client == null)
                return;

            try
            {
                var presence = new RichPresence()
                {
                    Details = $"Joining {serverName}",
                    State = "Loading...",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher",
                        SmallImageKey = "loading",
                        SmallImageText = "Connecting"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine($"[Discord RPC] Status: Loading {serverName}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Error updating status: {ex.Message}");
            }
        }

        /// <summary>
        /// Update status: Playing on Server
        /// </summary>
        public void UpdateStatusPlaying(string serverName, int playerCount, int maxPlayers, int ping)
        {
            if (!isInitialized || client == null)
                return;

            try
            {
                var presence = new RichPresence()
                {
                    Details = $"Playing on {serverName}",
                    State = $"Players: {playerCount}/{maxPlayers} | Ping: {ping}ms",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher - GTA San Andreas",
                        SmallImageKey = "gta_sa",
                        SmallImageText = "GTA San Andreas"
                    },
                    Timestamps = Timestamps.Now,
                    Buttons = new Button[]
                    {
                        new Button()
                        {
                            Label = $"Join {serverName}",
                            Url = $"ngr://join/{serverName.Replace(" ", "%20")}"
                        }
                    }
                };

                client.SetPresence(presence);
                Console.WriteLine($"[Discord RPC] Status: Playing on {serverName}");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Error updating status: {ex.Message}");
            }
        }

        /// <summary>
        /// Update status: In Settings
        /// </summary>
        public void UpdateStatusSettings()
        {
            if (!isInitialized || client == null)
                return;

            try
            {
                var presence = new RichPresence()
                {
                    Details = "Configuring Settings",
                    State = "Graphics Settings",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher",
                        SmallImageKey = "settings",
                        SmallImageText = "Settings"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: In Settings");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Error updating status: {ex.Message}");
            }
        }

        /// <summary>
        /// Update status: In Favorites
        /// </summary>
        public void UpdateStatusFavorites()
        {
            if (!isInitialized || client == null)
                return;

            try
            {
                var presence = new RichPresence()
                {
                    Details = "Viewing Favorites",
                    State = "Favorite Servers",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher",
                        SmallImageKey = "star",
                        SmallImageText = "Favorites"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: In Favorites");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Error updating status: {ex.Message}");
            }
        }

        /// <summary>
        /// Update status: Idle
        /// </summary>
        public void UpdateStatusIdle()
        {
            if (!isInitialized || client == null)
                return;

            try
            {
                var presence = new RichPresence()
                {
                    Details = "Idle",
                    State = "No server selected",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: Idle");
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Error updating status: {ex.Message}");
            }
        }

        /// <summary>
        /// Disconnect from Discord RPC
        /// </summary>
        public void Disconnect()
        {
            try
            {
                if (client != null && isInitialized)
                {
                    client.Dispose();
                    isInitialized = false;
                    Console.WriteLine("[Discord RPC] Disconnected");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"[Discord RPC] Error disconnecting: {ex.Message}");
            }
        }

        /// <summary>
        /// Check if Discord RPC is initialized
        /// </summary>
        public bool IsInitialized
        {
            get { return isInitialized; }
        }
    }
}
