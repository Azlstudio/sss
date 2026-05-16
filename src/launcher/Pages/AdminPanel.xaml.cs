using System.Windows;
using System.Windows.Controls;

namespace GTASALauncher.Pages
{
    public partial class AdminPanel : Page
    {
        private UserSettings settings;

        public AdminPanel(UserSettings userSettings)
        {
            InitializeComponent();
            settings = userSettings;
        }

        private void BtnSaveChanges_Click(object sender, RoutedEventArgs e)
        {
            MessageBox.Show("Cambios guardados exitosamente", "Éxito");
        }
    }
}
