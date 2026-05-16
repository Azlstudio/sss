using System;
using System.Windows;
using System.Collections.Generic;
using System.Linq;

namespace GTASALauncher
{
    public partial class MainWindowIntegrated : Window
    {
        private GameHost gameHost;
        private UserSettings currentSettings;
        private List<ServerData> allServers;
        private ServerData connectedServer;
        private DiscordRPCManager discordRPC;

        public MainWindowIntegrated()
        {
            InitializeComponent();
            InitializeApp();
        }

        private void InitializeApp()
        {
            currentSettings = new UserSettings { Username = "Player1", AccountId = "123456" };
            LoadServersFromAPI();

            // Initialize Discord RPC
            discordRPC = new DiscordRPCManager();
            discordRPC.UpdateStatusOnLauncher();

            // Initialize GameHost
            gameHost = new GameHost();
            gameHost.OnStatusChanged += GameHost_OnStatusChanged;
            gameHost.OnError += GameHost_OnError;

            // Start GTA in background
            Task.Run(() =>
            {
                bool success = gameHost.StartGameInBackground();
                if (!success)
                {
                    Dispatcher.Invoke(() =>
                    {
                        MessageBox.Show("Error: No se pudo iniciar GTA San Andreas. " +
                            "Verifica que esté instalado en la ruta por defecto.",
                            "Error", MessageBoxButton.OK, MessageBoxImage.Error);
                    });
                }
            });
        }

        private void LoadServersFromAPI()
        {
            allServers = new List<ServerData>
            {
                new ServerData
                {
                    ServerId = 1,
                    Name = "SA-RP Server",
                    Description = "Servidor RP con economia y familias",
                    IP = "127.0.0.1",
                    Port = 8888,
                    Owner = "AdminUser",
                    MaxPlayers = 100,
                    CurrentPlayers = 78,
                    Tags = new[] { "RP", "Economia", "Familias" },
                    GameMode = "Role Play",
                    PingMs = 45,
                    Rating = 4.8,
                    RatingCount = 1250,
                    IsOnline = true
                }
            };
        }

        private void GameHost_OnStatusChanged(string status)
        {
            Dispatcher.Invoke(() =>
            {
                TxtGameStatus.Text = status;
            });
        }

        private void GameHost_OnError(Exception ex)
        {
            Dispatcher.Invoke(() =>
            {
                TxtGameStatus.Foreground = System.Windows.Media.Brushes.Red;
                TxtGameStatus.Text = "Error: " + ex.Message;
            });
        }

        private void BtnHome_Click(object sender, RoutedEventArgs e)
        {
            TxtGameInfo.Text = "Vuelve a Home - Selecciona un servidor";
            connectedServer = null;
            NoServerOverlay.Visibility = Visibility.Visible;
            discordRPC?.UpdateStatusOnLauncher();
        }

        private void BtnServers_Click(object sender, RoutedEventArgs e)
        {
            // Show servers dialog or navigate to servers
            var result = MessageBox.Show(
                "Selecciona un servidor:\n\n" +
                string.Join("\n", allServers.Select(s => $"[{s.ServerId}] {s.Name} ({s.CurrentPlayers}/{s.MaxPlayers})")),
                "Buscar Servidores", MessageBoxButton.YesNo);

            if (result == MessageBoxResult.Yes)
            {
                ConnectToServer(allServers[0]);
            }
            else
            {
                discordRPC?.UpdateStatusOnLauncher();
            }
        }

        private void BtnFavorites_Click(object sender, RoutedEventArgs e)
        {
            discordRPC?.UpdateStatusFavorites();
            MessageBox.Show("Favoritos - Próximamente", "Favoritos");
        }

        private void BtnSettings_Click(object sender, RoutedEventArgs e)
        {
            discordRPC?.UpdateStatusSettings();
            MessageBox.Show("Configuración - Próximamente", "Configuración");
        }

        private void BtnExitGame_Click(object sender, RoutedEventArgs e)
        {
            if (MessageBox.Show("¿Salir del juego?", "Salir", MessageBoxButton.YesNo) == MessageBoxResult.Yes)
            {
                connectedServer = null;
                NoServerOverlay.Visibility = Visibility.Visible;
                TxtServerInfo.Text = "No conectado";
                discordRPC?.UpdateStatusOnLauncher();
            }
        }

        private void BtnReport_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Reportar - Próximamente", "Reportar");
        }

        private void BtnSendChat_Click(object sender, RoutedEventArgs e)
        {
            if (!string.IsNullOrEmpty(TxtChatInput.Text))
            {
                ChatBox.Items.Add($"[Tú] {TxtChatInput.Text}");
                TxtChatInput.Clear();
            }
        }

        private void TxtChatInput_KeyDown(object sender, System.Windows.Input.KeyEventArgs e)
        {
            if (e.Key == System.Windows.Input.Key.Return)
            {
                BtnSendChat_Click(null, null);
            }
        }

        private void ConnectToServer(ServerData server)
        {
            if (server == null) return;

            try
            {
                discordRPC?.UpdateStatusLoading(server.Name);

                connectedServer = server;
                TxtServerInfo.Text = $"Conectado a {server.Name}";
                TxtServerName.Text = server.Name;
                TxtPlayerCount.Text = $"{server.CurrentPlayers}/{server.MaxPlayers}";
                TxtPing.Text = $"{server.PingMs}ms";
                TxtGameInfo.Text = $"Conectado a {server.Name} | Ping: {server.PingMs}ms";

                NoServerOverlay.Visibility = Visibility.Hidden;
                discordRPC?.UpdateStatusPlaying(server.Name, server.CurrentPlayers, server.MaxPlayers, server.PingMs);

                // Add to recent
                if (!currentSettings.RecentServers.Contains(server.ServerId))
                    currentSettings.RecentServers.Insert(0, server.ServerId);

                // Embed game window
                if (gameHost.IsRunning)
                {
                    // Get container size
                    var containerWidth = (int)GameContainer.ActualWidth;
                    var containerHeight = (int)GameContainer.ActualHeight;

                    if (containerWidth > 0 && containerHeight > 0)
                    {
                        var containerHandle = new System.Windows.Forms.Control();
                        gameHost.EmbedGameWindow(
                            gameHost.GetType().BaseType?.Name ?? "",
                            0, 0, containerWidth, containerHeight);
                    }
                }

                // Inject DLL
                string dllPath = System.IO.Path.Combine(
                    System.IO.Directory.GetCurrentDirectory(),
                    "sa_inject.dll");

                gameHost.ConnectToServer(server.IP, server.Port, dllPath);

                // Add chat message
                ChatBox.Items.Add($"[SYSTEM] Conectado a {server.Name}");
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error al conectar: {ex.Message}", "Error", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private void Window_Closing(object sender, System.ComponentModel.CancelEventArgs e)
        {
            discordRPC?.Disconnect();
            gameHost?.StopGame();
        }
    }
}
