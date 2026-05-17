# NextAI Qt - Quick Start Guide

Build and run NextAI desktop application in minutes!

## Installation (Choose Your Platform)

### 🐧 Ubuntu/Debian

```bash
# Install dependencies
sudo apt-get update
sudo apt-get install -y build-essential cmake qt6-base-dev qt6-qml-module-quick

# Navigate to qt directory
cd qt

# Build
bash BUILD.sh

# Run
cd build
./NextAI
```

### 🍎 macOS

```bash
# Install dependencies with Homebrew
brew install cmake qt6

# Navigate to qt directory
cd qt

# Build
bash BUILD.sh

# Run
cd build
./NextAI
```

### 🪟 Windows

```bash
# 1. Install CMake from https://cmake.org/download/
# 2. Install Qt6 from https://www.qt.io/download/
# 3. Open Command Prompt or PowerShell
# 4. Navigate to qt directory

cd qt

# Build
BUILD.bat

# Run
cd build\Release
NextAI.exe
```

## After Installation

1. **Launch the app** - Double-click the executable or run from terminal
2. **Click "API Key"** - Enter your Gemini API key
3. **Get API Key** - Visit https://aistudio.google.com/app/apikey
4. **Start Chatting!** - Type messages and get instant AI responses

## Features Working

✅ Chat with Gemini AI  
✅ Message persistence (SQLite)  
✅ Code block display  
✅ Dark theme UI  
✅ Copy to clipboard  
✅ Clear history  

## Troubleshooting

### Build fails with "CMake not found"
- **Linux**: `sudo apt-get install cmake`
- **macOS**: `brew install cmake`
- **Windows**: Download from https://cmake.org/download/

### Build fails with "Qt6 not found"
- **Linux**: `sudo apt-get install qt6-base-dev`
- **macOS**: `brew install qt6`
- **Windows**: Download from https://www.qt.io/download/

### "API Key" button does nothing
- Make sure you have internet connection
- Check API key is valid
- Try clicking again

### App crashes on startup
- Check error messages in terminal
- Verify Qt6 is properly installed
- Try rebuilding: `rm -rf build && bash BUILD.sh`

## File Structure

```
qt/
├── src/                  # Source code
│   ├── main.cpp         # Entry point
│   ├── mainwindow.*     # Main UI
│   ├── aiservice.*      # Gemini API
│   ├── storageservice.* # Database
│   └── codeblock.*      # Code display
├── CMakeLists.txt       # CMake config
├── NextAI.pro           # QMake config (alternative)
├── BUILD.sh             # Linux/macOS build script
├── BUILD.bat            # Windows build script
└── README.md            # Full documentation
```

## Building with Qt Creator (Alternative)

1. **Install Qt Creator** - From https://www.qt.io/download/
2. **Open project** - File → Open → select `NextAI.pro`
3. **Configure** - Select Qt 6.x kit
4. **Build** - Press Ctrl+B (or Cmd+B on macOS)
5. **Run** - Press Ctrl+R (or Cmd+R on macOS)

## Next Steps

- Customize colors in `mainwindow.cpp`
- Modify system prompt in `aiservice.cpp`
- Add new features and UI elements
- Build distributable packages

## Support

For issues:
1. Check terminal output for error messages
2. Verify Qt6 installation: `qmake --version`
3. Check CMake version: `cmake --version`
4. Review README.md for more info

---

**Happy building! 🚀**
