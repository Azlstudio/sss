using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace GTASALauncher.Pages
{
    public partial class RecentPage : Page
    {
        private List<ServerData> allServers;
        private UserSettings settings;

        public RecentPage(List<ServerData> servers, UserSettings userSettings)
        {
            InitializeComponent();
            allServers = servers;
            settings = userSettings;

            LoadRecent();
        }

        private void LoadRecent()
        {
            var recentServers = allServers
                .Where(s => settings.RecentServers.Contains(s.ServerId))
                .OrderBy(s => settings.RecentServers.IndexOf(s.ServerId))
                .ToList();

            DataContext = new
            {
                Servers = recentServers,
                ServerCount = recentServers.Count
            };
        }

        private void OnServerDoubleClick(object sender, MouseButtonEventArgs e)
        {
            MessageBox.Show("Conectando al servidor...", "Conectar");
        }

        private void OnConnectClick(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Conectando al servidor...", "Conectar");
        }

        private void OnFavoriteClick(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Agregado a favoritos", "Favoritos");
        }
    }
}
