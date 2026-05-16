using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;

namespace GTASALauncher.Pages
{
    public partial class SettingsPage : Page
    {
        private const string SettingsFile = "gta_settings.ini";
        private GraphicsSettings currentSettings;

        public SettingsPage()
        {
            InitializeComponent();
            LoadSettings();
            AttachEventHandlers();
        }

        private void AttachEventHandlers()
        {
            // Update labels when sliders change
            DrawDistanceSlider.ValueChanged += (s, e) =>
            {
                DrawDistanceLabel.Text = (int)DrawDistanceSlider.Value + " meters";
            };

            LODSlider.ValueChanged += (s, e) =>
            {
                LODLabel.Text = (int)LODSlider.Value + " units";
            };
        }

        private void LoadSettings()
        {
            try
            {
                if (File.Exists(SettingsFile))
                {
                    currentSettings = GraphicsSettings.LoadFromFile(SettingsFile);
                }
                else
                {
                    currentSettings = GraphicsSettings.CreateDefault();
                }

                ApplySettingsToUI();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error loading settings: " + ex.Message, "Error");
                currentSettings = GraphicsSettings.CreateDefault();
                ApplySettingsToUI();
            }
        }

        private void ApplySettingsToUI()
        {
            // Display
            ResolutionCombo.SelectedIndex = currentSettings.ResolutionIndex;
            FullscreenCheck.IsChecked = currentSettings.Fullscreen;
            VSyncCheck.IsChecked = currentSettings.VSync;

            // Quality
            BlurCheck.IsChecked = currentSettings.MotionBlur;
            ShadowsCheck.IsChecked = currentSettings.DynamicShadows;
            ReflectionsCheck.IsChecked = currentSettings.Reflections;
            ParticlesCheck.IsChecked = currentSettings.Particles;
            FogCheck.IsChecked = currentSettings.DistanceFog;

            // Performance
            DrawDistanceSlider.Value = currentSettings.ViewDistance;
            LODSlider.Value = currentSettings.LODDistance;

            // Advanced
            AACombo.SelectedIndex = currentSettings.AntiAliasingIndex;
            TextureCombo.SelectedIndex = currentSettings.TextureQualityIndex;
            AFCheck.IsChecked = currentSettings.AnisotropicFiltering;
            HDRCheck.IsChecked = currentSettings.HDR;
        }

        private void ApplySettings(object sender, RoutedEventArgs e)
        {
            try
            {
                // Save settings to file
                SaveSettingsFromUI();
                currentSettings.SaveToFile(SettingsFile);

                // Apply graphics changes
                ApplyGraphicsChanges();

                StatusMessage.Text = "Settings applied successfully!";
                StatusMessage.Foreground = System.Windows.Media.Brushes.LimeGreen;

                // Reset message after 3 seconds
                System.Windows.Threading.DispatcherTimer timer = new System.Windows.Threading.DispatcherTimer();
                timer.Interval = TimeSpan.FromSeconds(3);
                timer.Tick += (s, args) =>
                {
                    StatusMessage.Text = "Settings will be applied next time you join a server";
                    StatusMessage.Foreground = System.Windows.Media.Brushes.LimeGreen;
                    timer.Stop();
                };
                timer.Start();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Error applying settings: " + ex.Message, "Error");
            }
        }

        private void ResetSettings(object sender, RoutedEventArgs e)
        {
            var result = MessageBox.Show(
                "Reset all settings to default?",
                "Reset Settings",
                MessageBoxButton.YesNo,
                MessageBoxImage.Question);

            if (result == MessageBoxResult.Yes)
            {
                currentSettings = GraphicsSettings.CreateDefault();
                ApplySettingsToUI();
                SaveSettingsFromUI();

                StatusMessage.Text = "Settings reset to default!";
                StatusMessage.Foreground = System.Windows.Media.Brushes.Yellow;
            }
        }

        private void SaveSettingsFromUI()
        {
            currentSettings.ResolutionIndex = ResolutionCombo.SelectedIndex;
            currentSettings.Fullscreen = FullscreenCheck.IsChecked ?? false;
            currentSettings.VSync = VSyncCheck.IsChecked ?? false;

            currentSettings.MotionBlur = BlurCheck.IsChecked ?? false;
            currentSettings.DynamicShadows = ShadowsCheck.IsChecked ?? false;
            currentSettings.Reflections = ReflectionsCheck.IsChecked ?? false;
            currentSettings.Particles = ParticlesCheck.IsChecked ?? false;
            currentSettings.DistanceFog = FogCheck.IsChecked ?? false;

            currentSettings.ViewDistance = (int)DrawDistanceSlider.Value;
            currentSettings.LODDistance = (int)LODSlider.Value;

            currentSettings.AntiAliasingIndex = AACombo.SelectedIndex;
            currentSettings.TextureQualityIndex = TextureCombo.SelectedIndex;
            currentSettings.AnisotropicFiltering = AFCheck.IsChecked ?? false;
            currentSettings.HDR = HDRCheck.IsChecked ?? false;
        }

        private void ApplyGraphicsChanges()
        {
            // This would communicate with GTA process to apply settings
            // For now, we just save to file

            // TODO: Use DLL injection to apply settings to running GTA process
            // ApplyResolution(currentSettings.GetResolution());
            // ApplyBlur(!currentSettings.MotionBlur);
            // ApplyShadows(currentSettings.DynamicShadows);
            // etc.
        }

        private void ApplyLowPreset(object sender, RoutedEventArgs e)
        {
            // Low performance preset
            BlurCheck.IsChecked = false;
            ShadowsCheck.IsChecked = false;
            ReflectionsCheck.IsChecked = false;
            ParticlesCheck.IsChecked = false;
            FogCheck.IsChecked = false;

            DrawDistanceSlider.Value = 800;
            LODSlider.Value = 100;

            AACombo.SelectedIndex = 0; // Disabled
            TextureCombo.SelectedIndex = 0; // Low
            AFCheck.IsChecked = false;
            HDRCheck.IsChecked = false;

            VSyncCheck.IsChecked = false;

            StatusMessage.Text = "Low performance preset applied";
        }

        private void ApplyMediumPreset(object sender, RoutedEventArgs e)
        {
            // Medium preset
            BlurCheck.IsChecked = true;
            ShadowsCheck.IsChecked = true;
            ReflectionsCheck.IsChecked = false;
            ParticlesCheck.IsChecked = true;
            FogCheck.IsChecked = true;

            DrawDistanceSlider.Value = 1500;
            LODSlider.Value = 250;

            AACombo.SelectedIndex = 2; // 4x MSAA
            TextureCombo.SelectedIndex = 1; // Medium
            AFCheck.IsChecked = true;
            HDRCheck.IsChecked = false;

            VSyncCheck.IsChecked = true;

            StatusMessage.Text = "Medium preset applied";
        }

        private void ApplyHighPreset(object sender, RoutedEventArgs e)
        {
            // Ultra high preset
            BlurCheck.IsChecked = true;
            ShadowsCheck.IsChecked = true;
            ReflectionsCheck.IsChecked = true;
            ParticlesCheck.IsChecked = true;
            FogCheck.IsChecked = true;

            DrawDistanceSlider.Value = 3000;
            LODSlider.Value = 500;

            AACombo.SelectedIndex = 3; // 8x MSAA
            TextureCombo.SelectedIndex = 3; // Ultra
            AFCheck.IsChecked = true;
            HDRCheck.IsChecked = true;

            VSyncCheck.IsChecked = true;

            StatusMessage.Text = "Ultra high preset applied";
        }
    }

    /// <summary>
    /// Graphics settings data class
    /// </summary>
    public class GraphicsSettings
    {
        // Display
        public int ResolutionIndex { get; set; } = 0;
        public bool Fullscreen { get; set; } = false;
        public bool VSync { get; set; } = true;

        // Quality
        public bool MotionBlur { get; set; } = true;
        public bool DynamicShadows { get; set; } = true;
        public bool Reflections { get; set; } = true;
        public bool Particles { get; set; } = true;
        public bool DistanceFog { get; set; } = true;

        // Performance
        public int ViewDistance { get; set; } = 2000;
        public int LODDistance { get; set; } = 300;

        // Advanced
        public int AntiAliasingIndex { get; set; } = 1;
        public int TextureQualityIndex { get; set; } = 2;
        public bool AnisotropicFiltering { get; set; } = true;
        public bool HDR { get; set; } = false;

        public string[] Resolutions = new[]
        {
            "1920x1080",
            "1680x1050",
            "1600x900",
            "1440x900",
            "1366x768",
            "1280x720",
            "1024x768"
        };

        public (int width, int height) GetResolution()
        {
            var res = Resolutions[ResolutionIndex].Split('x');
            return (int.Parse(res[0]), int.Parse(res[1]));
        }

        public static GraphicsSettings CreateDefault()
        {
            return new GraphicsSettings();
        }

        public void SaveToFile(string filename)
        {
            var lines = new List<string>
            {
                "[Display]",
                "resolution=" + ResolutionIndex,
                "fullscreen=" + Fullscreen,
                "vsync=" + VSync,
                "",
                "[Quality]",
                "motion_blur=" + MotionBlur,
                "dynamic_shadows=" + DynamicShadows,
                "reflections=" + Reflections,
                "particles=" + Particles,
                "distance_fog=" + DistanceFog,
                "",
                "[Performance]",
                "view_distance=" + ViewDistance,
                "lod_distance=" + LODDistance,
                "",
                "[Advanced]",
                "anti_aliasing=" + AntiAliasingIndex,
                "texture_quality=" + TextureQualityIndex,
                "anisotropic_filtering=" + AnisotropicFiltering,
                "hdr=" + HDR
            };

            File.WriteAllLines(filename, lines);
        }

        public static GraphicsSettings LoadFromFile(string filename)
        {
            var settings = new GraphicsSettings();
            var lines = File.ReadAllLines(filename);

            foreach (var line in lines)
            {
                if (string.IsNullOrWhiteSpace(line) || line.StartsWith("["))
                    continue;

                var parts = line.Split('=');
                if (parts.Length != 2)
                    continue;

                var key = parts[0].Trim();
                var value = parts[1].Trim();

                switch (key)
                {
                    case "resolution":
                        settings.ResolutionIndex = int.Parse(value);
                        break;
                    case "fullscreen":
                        settings.Fullscreen = bool.Parse(value);
                        break;
                    case "vsync":
                        settings.VSync = bool.Parse(value);
                        break;
                    case "motion_blur":
                        settings.MotionBlur = bool.Parse(value);
                        break;
                    case "dynamic_shadows":
                        settings.DynamicShadows = bool.Parse(value);
                        break;
                    case "reflections":
                        settings.Reflections = bool.Parse(value);
                        break;
                    case "particles":
                        settings.Particles = bool.Parse(value);
                        break;
                    case "distance_fog":
                        settings.DistanceFog = bool.Parse(value);
                        break;
                    case "view_distance":
                        settings.ViewDistance = int.Parse(value);
                        break;
                    case "lod_distance":
                        settings.LODDistance = int.Parse(value);
                        break;
                    case "anti_aliasing":
                        settings.AntiAliasingIndex = int.Parse(value);
                        break;
                    case "texture_quality":
                        settings.TextureQualityIndex = int.Parse(value);
                        break;
                    case "anisotropic_filtering":
                        settings.AnisotropicFiltering = bool.Parse(value);
                        break;
                    case "hdr":
                        settings.HDR = bool.Parse(value);
                        break;
                }
            }

            return settings;
        }
    }
}
