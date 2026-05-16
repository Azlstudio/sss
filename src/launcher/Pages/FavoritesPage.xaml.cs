using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Input;

namespace GTASALauncher.Pages
{
    public partial class FavoritesPage : Page
    {
        private List<ServerData> allServers;
        private UserSettings settings;

        public FavoritesPage(List<ServerData> servers, UserSettings userSettings)
        {
            InitializeComponent();
            allServers = servers;
            settings = userSettings;

            LoadFavorites();
        }

        private void LoadFavorites()
        {
            var favoriteServers = allServers
                .Where(s => settings.FavoriteServers.Contains(s.ServerId))
                .ToList();

            DataContext = new
            {
                Servers = favoriteServers,
                ServerCount = favoriteServers.Count
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
            MessageBox.Show("Servidor removido de favoritos", "Favoritos");
            LoadFavorites();
        }
    }
}
