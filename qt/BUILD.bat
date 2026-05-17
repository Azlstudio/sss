@echo off
REM NextAI Qt Build Script for Windows

echo.
echo 🔨 Building NextAI Qt Desktop Application
echo =========================================
echo.

REM Check for CMake
where cmake >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo ❌ CMake not found. Please install CMake 3.21+
    echo    Download from: https://cmake.org/download/
    pause
    exit /b 1
)

REM Create build directory
if not exist "build" (
    echo 📁 Creating build directory...
    mkdir build
)

REM Build
echo 🏗️  Configuring with CMake...
cd build
cmake ..

if %ERRORLEVEL% NEQ 0 (
    echo ❌ CMake configuration failed
    pause
    exit /b 1
)

echo ⚙️  Building (Release)...
cmake --build . --config Release

if %ERRORLEVEL% NEQ 0 (
    echo ❌ Build failed
    pause
    exit /b 1
)

echo.
echo ✅ Build complete!
echo.
echo 🚀 To run the application:
echo    Release\NextAI.exe
echo.
echo 📝 Don't forget to set your Gemini API key when the app starts!
echo.
pause
