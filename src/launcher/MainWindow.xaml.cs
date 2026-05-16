using System;
using System.Collections.Generic;
using System.Windows;

namespace GTASALauncher
{
    public partial class MainWindow : Window
    {
        private UserSettings currentSettings;
        private List<ServerData> allServers;

        public MainWindow()
        {
            InitializeComponent();
            InitializeApp();
        }

        private void InitializeApp()
        {
            // Load user settings
            currentSettings = new UserSettings { Username = "Player1", AccountId = "123456" };

            // Load servers from database/API
            LoadServersFromAPI();

            // Load home page
            ShowHomePage();
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
                    IP = "192.168.1.100",
                    Port = 8888,
                    Owner = "AdminUser",
                    MaxPlayers = 100,
                    CurrentPlayers = 78,
                    Tags = new[] { "RP", "Economia", "Familias" },
                    GameMode = "Role Play",
                    BannerUrl = "server1_banner.png",
                    LogoUrl = "server1_logo.png",
                    PingMs = 45,
                    Rating = 4.8,
                    RatingCount = 1250,
                    IsOnline = true
                },
                new ServerData
                {
                    ServerId = 2,
                    Name = "TDM Insano",
                    Description = "Team Deathmatch hardcore sin reglas",
                    IP = "192.168.1.101",
                    Port = 8889,
                    Owner = "GamerKing",
                    MaxPlayers = 32,
                    CurrentPlayers = 31,
                    Tags = new[] { "TDM", "PvP", "Hardcore" },
                    GameMode = "Team Deathmatch",
                    PingMs = 32,
                    Rating = 4.2,
                    RatingCount = 856,
                    IsOnline = true
                },
                new ServerData
                {
                    ServerId = 3,
                    Name = "Sandbox Mode",
                    Description = "Modo sandbox con todos los vehiculos",
                    IP = "192.168.1.102",
                    Port = 8890,
                    Owner = "CreativeAdmin",
                    MaxPlayers = 50,
                    CurrentPlayers = 25,
                    Tags = new[] { "Sandbox", "Creative", "Vehiculos" },
                    GameMode = "Sandbox",
                    PingMs = 85,
                    Rating = 4.5,
                    RatingCount = 432,
                    IsOnline = true
                }
            };
        }

        private void ShowHomePage()
        {
            TxtPageTitle.Text = "Home";
            var homePage = new Pages.HomePage(allServers, currentSettings);
            ContentFrame.Navigate(homePage);
        }

        private void ShowServersPage()
        {
            TxtPageTitle.Text = "Buscar Servidores";
            var serversPage = new Pages.ServersPage(allServers, currentSettings);
            ContentFrame.Navigate(serversPage);
        }

        private void ShowFavoritesPage()
        {
            TxtPageTitle.Text = "Servidores Favoritos";
            var favoritesPage = new Pages.FavoritesPage(allServers, currentSettings);
            ContentFrame.Navigate(favoritesPage);
        }

        private void ShowRecentPage()
        {
            TxtPageTitle.Text = "Recientes";
            var recentPage = new Pages.RecentPage(allServers, currentSettings);
            ContentFrame.Navigate(recentPage);
        }

        private void ShowSettingsPage()
        {
            TxtPageTitle.Text = "Configuración";
            var settingsPage = new Pages.SettingsPage(currentSettings);
            ContentFrame.Navigate(settingsPage);
        }

        private void ShowAdminPanel()
        {
            TxtPageTitle.Text = "Panel de Administrador";
            var adminPage = new Pages.AdminPanel(currentSettings);
            ContentFrame.Navigate(adminPage);
        }

        // Button Click Events
        private void BtnHome_Click(object sender, RoutedEventArgs e) => ShowHomePage();
        private void BtnServers_Click(object sender, RoutedEventArgs e) => ShowServersPage();
        private void BtnFavorites_Click(object sender, RoutedEventArgs e) => ShowFavoritesPage();
        private void BtnRecent_Click(object sender, RoutedEventArgs e) => ShowRecentPage();
        private void BtnSettings_Click(object sender, RoutedEventArgs e) => ShowSettingsPage();
        private void BtnAdminPanel_Click(object sender, RoutedEventArgs e) => ShowAdminPanel();

        private void BtnCreateServer_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Crear servidor - Próximamente");
        }

        private void BtnSearch_Click(object sender, RoutedEventArgs e)
        {
            // Filter and search servers
            string searchText = TxtSearch.Text;
            ShowServersPage();
        }

        private void TxtSearch_TextChanged(object sender, System.Windows.Controls.TextChangedEventArgs e)
        {
            // Real-time search
        }
    }
}
