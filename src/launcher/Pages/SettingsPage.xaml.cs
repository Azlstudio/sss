using System.Windows;
using System.Windows.Controls;

namespace GTASALauncher.Pages
{
    public partial class SettingsPage : Page
    {
        private UserSettings settings;

        public SettingsPage(UserSettings userSettings)
        {
            InitializeComponent();
            settings = userSettings;
        }

        private void BtnSaveSettings_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Configuración guardada", "Éxito");
        }
    }
}
