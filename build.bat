@echo off
echo Building GTA San Andreas Multiplayer...

if not exist build mkdir build
cd build

cmake -G "Visual Studio 17 2022" ..
cmake --build . --config Release

echo.
echo Build complete!
echo.
echo Server: build\Release\sa_server.exe
echo Client: build\Release\sa_client.exe
pause
