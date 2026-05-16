using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace GTASALauncher.Pages
{
    public partial class HomePage : Page
    {
        private List<ServerData> allServers;
        private UserSettings settings;

        public HomePage(List<ServerData> servers, UserSettings userSettings)
        {
            InitializeComponent();
            allServers = servers;
            settings = userSettings;

            LoadData();
        }

        private void LoadData()
        {
            // Set featured server (highest rated or random)
            var featured = allServers.OrderByDescending(s => s.Rating).FirstOrDefault();
            DataContext = new
            {
                FeaturedServer = featured,
                RecommendedServers = allServers.Take(3).ToList()
            };
        }

        private void OnFeaturedServerDoubleClick(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            var featured = allServers.OrderByDescending(s => s.Rating).FirstOrDefault();
            ConnectToServer(featured);
        }

        private void OnServerDoubleClick(object sender, System.Windows.Input.MouseButtonEventArgs e)
        {
            var border = sender as Border;
            if (border?.DataContext is ServerData server)
            {
                ConnectToServer(server);
            }
        }

        private void OnConnectClick(object sender, RoutedEventArgs e)
        {
            var button = sender as Button;
            var parent = FindParentByType<Border>(button);

            if (parent?.DataContext is ServerData server)
            {
                ConnectToServer(server);
            }
            else
            {
                // It's the featured server
                var featured = allServers.OrderByDescending(s => s.Rating).FirstOrDefault();
                ConnectToServer(featured);
            }
        }

        private void ConnectToServer(ServerData server)
        {
            if (server == null) return;

            // Add to recent servers
            if (!settings.RecentServers.Contains(server.ServerId))
            {
                settings.RecentServers.Insert(0, server.ServerId);
                if (settings.RecentServers.Count > 10)
                    settings.RecentServers.RemoveAt(settings.RecentServers.Count - 1);
            }

            MessageBox.Show(
                $"Conectando a {server.Name}...\n\n" +
                $"IP: {server.IP}:{server.Port}\n" +
                $"Ping: {server.PingMs}ms\n" +
                $"Jugadores: {server.CurrentPlayers}/{server.MaxPlayers}",
                "Conectar al Servidor"
            );

            // TODO: Launch actual game with server parameters
            // System.Diagnostics.Process.Start("sa_launcher.exe", $"{server.IP} {server.Port}");
        }

        private T FindParentByType<T>(DependencyObject element) where T : DependencyObject
        {
            var parent = element;
            while (parent != null)
            {
                if (parent is T typed)
                    return typed;
                parent = LogicalTreeHelper.GetParent(parent);
            }
            return null;
        }
    }
}
