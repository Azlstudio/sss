using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace GTASALauncher.Pages
{
    public partial class ServersPage : Page
    {
        private List<ServerData> allServers;
        private UserSettings settings;

        public ServersPage(List<ServerData> servers, UserSettings userSettings)
        {
            InitializeComponent();
            allServers = servers;
            settings = userSettings;

            LoadServers();
        }

        private void LoadServers()
        {
            var filtered = allServers.Where(s => s.IsOnline).ToList();

            DataContext = new
            {
                Servers = filtered,
                ServerCount = filtered.Count
            };
        }

        private void OnServerDoubleClick(object sender, MouseButtonEventArgs e)
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
        }

        private void OnFavoriteClick(object sender, RoutedEventArgs e)
        {
            var button = sender as Button;
            var parent = FindParentByType<Border>(button);

            if (parent?.DataContext is ServerData server)
            {
                if (!settings.FavoriteServers.Contains(server.ServerId))
                {
                    settings.FavoriteServers.Add(server.ServerId);
                    button.Content = "⭐ (Guardado)";
                }
                else
                {
                    settings.FavoriteServers.Remove(server.ServerId);
                    button.Content = "⭐";
                }
            }
        }

        private void ConnectToServer(ServerData server)
        {
            if (server == null) return;

            // Add to recent
            if (!settings.RecentServers.Contains(server.ServerId))
                settings.RecentServers.Insert(0, server.ServerId);

            MessageBox.Show(
                $"Conectando a {server.Name}...\n\n" +
                $"IP: {server.IP}:{server.Port}\n" +
                $"Jugadores: {server.CurrentPlayers}/{server.MaxPlayers}",
                "Conectar"
            );
        }

        private void BtnRefresh_Click(object sender, RoutedEventArgs e)
        {
            LoadServers();
            MessageBox.Show("Lista de servidores actualizada", "Éxito");
        }

        private void BtnClearFilters_Click(object sender, RoutedEventArgs e)
        {
            LoadServers();
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
