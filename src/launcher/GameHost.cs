using System;
using System.Diagnostics;
using System.Runtime.InteropServices;
using System.Threading;
using System.Threading.Tasks;

namespace GTASALauncher
{
    public class GameHost
    {
        private Process gameProcess;
        private IntPtr gameWindowHandle;
        private bool isRunning;

        [DllImport("user32.dll", SetLastError = true)]
        private static extern bool SetParent(IntPtr hWndChild, IntPtr hWndNewParent);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern bool ShowWindow(IntPtr hWnd, int nCmdShow);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern int SetWindowLong(IntPtr hWnd, int nIndex, int dwNewLong);

        [DllImport("user32.dll", SetLastError = true)]
        private static extern bool MoveWindow(IntPtr hWnd, int X, int Y, int nWidth, int nHeight, bool bRepaint);

        [DllImport("user32.dll")]
        private static extern IntPtr FindWindow(string className, string windowName);

        [DllImport("user32.dll")]
        private static extern bool IsWindow(IntPtr hWnd);

        private const int GWL_STYLE = -16;
        private const int WS_CHILD = 0x40000000;
        private const int WS_POPUP = unchecked((int)0x80000000);
        private const int SW_HIDE = 0;
        private const int SW_SHOW = 5;

        public event Action<string> OnStatusChanged;
        public event Action<Exception> OnError;

        public bool IsRunning => isRunning && gameProcess != null && !gameProcess.HasExited;

        public GameHost()
        {
            isRunning = false;
        }

        /// <summary>
        /// Inicia GTA San Andreas en background
        /// </summary>
        public bool StartGameInBackground(string gtaSAPath = "C:\\Program Files (x86)\\Rockstar Games\\GTA San Andreas\\gta_sa.exe")
        {
            try
            {
                OnStatusChanged?.Invoke("Iniciando GTA San Andreas en background...");

                // Kill existing GTA process if any
                KillExistingProcess();

                // Start GTA SA
                ProcessStartInfo psi = new ProcessStartInfo
                {
                    FileName = gtaSAPath,
                    UseShellExecute = true,
                    CreateNoWindow = false,
                    WindowStyle = ProcessWindowStyle.Hidden
                };

                gameProcess = Process.Start(psi);
                if (gameProcess == null)
                {
                    OnError?.Invoke(new Exception("No se pudo iniciar GTA SA"));
                    return false;
                }

                // Wait for window to appear
                gameWindowHandle = IntPtr.Zero;
                int attempts = 0;
                while (gameWindowHandle == IntPtr.Zero && attempts < 30)
                {
                    Thread.Sleep(100);
                    gameWindowHandle = FindWindow(null, "GTA: San Andreas");
                    attempts++;
                }

                if (gameWindowHandle == IntPtr.Zero)
                {
                    OnError?.Invoke(new Exception("No se pudo encontrar ventana de GTA SA"));
                    return false;
                }

                isRunning = true;
                OnStatusChanged?.Invoke("GTA San Andreas iniciado en background");
                return true;
            }
            catch (Exception ex)
            {
                OnError?.Invoke(ex);
                return false;
            }
        }

        /// <summary>
        /// Embeds la ventana de GTA en un control WPF
        /// </summary>
        public bool EmbedGameWindow(IntPtr parentWindowHandle, int x, int y, int width, int height)
        {
            try
            {
                if (!IsWindow(gameWindowHandle))
                {
                    OnError?.Invoke(new Exception("Ventana de GTA no válida"));
                    return false;
                }

                OnStatusChanged?.Invoke("Incrustando GTA en el launcher...");

                // Hide the window first
                ShowWindow(gameWindowHandle, SW_HIDE);
                Thread.Sleep(200);

                // Set as child of parent window
                SetParent(gameWindowHandle, parentWindowHandle);

                // Change window style
                int style = SetWindowLong(gameWindowHandle, GWL_STYLE, WS_CHILD);

                // Resize and position
                MoveWindow(gameWindowHandle, x, y, width, height, true);

                // Show the window
                ShowWindow(gameWindowHandle, SW_SHOW);

                OnStatusChanged?.Invoke("GTA San Andreas incrustado");
                return true;
            }
            catch (Exception ex)
            {
                OnError?.Invoke(ex);
                return false;
            }
        }

        /// <summary>
        /// Maximiza la ventana de GTA (rellenar el espacio disponible)
        /// </summary>
        public void MaximizeGameWindow(int x, int y, int width, int height)
        {
            try
            {
                if (IsWindow(gameWindowHandle))
                {
                    MoveWindow(gameWindowHandle, x, y, width, height, true);
                }
            }
            catch (Exception ex)
            {
                OnError?.Invoke(ex);
            }
        }

        /// <summary>
        /// Inyecta la DLL del multiplayer en GTA
        /// </summary>
        public bool InjectMultiplayerDLL(string dllPath)
        {
            try
            {
                OnStatusChanged?.Invoke("Inyectando módulo multijugador...");

                if (gameProcess == null || gameProcess.HasExited)
                {
                    OnError?.Invoke(new Exception("GTA SA no está ejecutándose"));
                    return false;
                }

                // Get process handle
                IntPtr hProcess = gameProcess.Handle;

                // Allocate memory in GTA process for DLL path
                IntPtr allocMemAddress = VirtualAllocEx(hProcess, IntPtr.Zero,
                    (uint)(dllPath.Length + 1), 0x1000, 0x04);

                if (allocMemAddress == IntPtr.Zero)
                {
                    OnError?.Invoke(new Exception("No se pudo asignar memoria"));
                    return false;
                }

                // Write DLL path to memory
                if (!WriteProcessMemory(hProcess, allocMemAddress, dllPath, (uint)dllPath.Length, out IntPtr bytesWritten))
                {
                    OnError?.Invoke(new Exception("No se pudo escribir en memoria"));
                    return false;
                }

                // Get LoadLibraryA address
                IntPtr loadLibAddr = GetProcAddress(GetModuleHandle("kernel32.dll"), "LoadLibraryA");

                // Create remote thread
                IntPtr hThread = CreateRemoteThread(hProcess, IntPtr.Zero, 0, loadLibAddr, allocMemAddress, 0, IntPtr.Zero);

                if (hThread == IntPtr.Zero)
                {
                    OnError?.Invoke(new Exception("No se pudo crear thread remoto"));
                    return false;
                }

                // Wait for thread
                WaitForSingleObject(hThread, 5000);

                // Clean up
                VirtualFreeEx(hProcess, allocMemAddress, 0, 0x8000);
                CloseHandle(hThread);

                OnStatusChanged?.Invoke("DLL inyectada exitosamente");
                return true;
            }
            catch (Exception ex)
            {
                OnError?.Invoke(ex);
                return false;
            }
        }

        /// <summary>
        /// Conecta a un servidor
        /// </summary>
        public bool ConnectToServer(string serverIP, ushort port, string dllPath)
        {
            try
            {
                OnStatusChanged?.Invoke($"Conectando a {serverIP}:{port}...");

                // Make sure game window is visible
                if (IsWindow(gameWindowHandle))
                {
                    ShowWindow(gameWindowHandle, SW_SHOW);
                }

                // Inject DLL
                if (!InjectMultiplayerDLL(dllPath))
                {
                    return false;
                }

                // TODO: Send server address to DLL via IPC
                OnStatusChanged?.Invoke($"Conectado a {serverIP}:{port}");
                return true;
            }
            catch (Exception ex)
            {
                OnError?.Invoke(ex);
                return false;
            }
        }

        /// <summary>
        /// Cierra GTA de forma segura
        /// </summary>
        public void StopGame()
        {
            try
            {
                if (gameProcess != null && !gameProcess.HasExited)
                {
                    gameProcess.Kill();
                    gameProcess.WaitForExit(5000);
                }
            }
            catch { }

            isRunning = false;
            gameWindowHandle = IntPtr.Zero;
        }

        private void KillExistingProcess()
        {
            try
            {
                foreach (Process p in Process.GetProcessesByName("gta_sa"))
                {
                    p.Kill();
                    p.WaitForExit(1000);
                }
            }
            catch { }
        }

        // Windows API declarations
        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern IntPtr VirtualAllocEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint flAllocationType, uint flProtect);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern bool VirtualFreeEx(IntPtr hProcess, IntPtr lpAddress, uint dwSize, uint dwFreeType);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern bool WriteProcessMemory(IntPtr hProcess, IntPtr lpBaseAddress, string lpBuffer, uint nSize, out IntPtr lpNumberOfBytesWritten);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern IntPtr CreateRemoteThread(IntPtr hProcess, IntPtr lpThreadAttributes, uint dwStackSize, IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern uint WaitForSingleObject(IntPtr hHandle, uint dwMilliseconds);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern bool CloseHandle(IntPtr hObject);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern IntPtr GetModuleHandle(string lpModuleName);

        [DllImport("kernel32.dll", SetLastError = true)]
        private static extern IntPtr GetProcAddress(IntPtr hModule, string lpProcName);
    }
}
