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
                    Details = "Buscando Servidores",
                    State = "En Inicio",
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
                        new Button() { Label = "Descargar NGR", Url = "https://ngr.launcher" }
                    }
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: En Inicio");
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
                    Details = $"Uniéndose a {serverName}",
                    State = "Entrando A Servidor",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher",
                        SmallImageKey = "loading",
                        SmallImageText = "Conectando"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine($"[Discord RPC] Status: Entrando A Servidor {serverName}");
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
                var playingMessages = new[] { "Roliando En", "Jugando En", "Conectado A", "En Vivo En" };
                var random = new Random();
                var playingMessage = playingMessages[random.Next(playingMessages.Length)];

                var presence = new RichPresence()
                {
                    Details = $"{playingMessage} {serverName}",
                    State = $"Jugadores: {playerCount}/{maxPlayers} | Ping: {ping}ms",
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
                            Label = $"Unirse A {serverName}",
                            Url = $"ngr://join/{serverName.Replace(" ", "%20")}"
                        }
                    }
                };

                client.SetPresence(presence);
                Console.WriteLine($"[Discord RPC] Status: {playingMessage} {serverName}");
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
                    Details = "Configurando Gráficos",
                    State = "En Configuración",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher",
                        SmallImageKey = "settings",
                        SmallImageText = "Configuración"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: En Configuración");
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
                    Details = "Viendo Favoritos",
                    State = "En Favoritos",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher",
                        SmallImageKey = "star",
                        SmallImageText = "Favoritos"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: En Favoritos");
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
                    Details = "En Pausa",
                    State = "Sin Servidor Seleccionado",
                    Assets = new Assets()
                    {
                        LargeImageKey = "ngr_launcher",
                        LargeImageText = "NGR Launcher"
                    },
                    Timestamps = Timestamps.Now
                };

                client.SetPresence(presence);
                Console.WriteLine("[Discord RPC] Status: En Pausa");
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
