#!/bin/bash

# NextAI Qt Build Script

set -e

echo "🔨 Building NextAI Qt Desktop Application"
echo "========================================"

# Check for CMake
if ! command -v cmake &> /dev/null; then
    echo "❌ CMake not found. Please install CMake 3.21+"
    echo "   Ubuntu: sudo apt-get install cmake"
    echo "   macOS: brew install cmake"
    echo "   Windows: https://cmake.org/download/"
    exit 1
fi

# Check for Qt6
if ! pkg-config --exists Qt6Core 2>/dev/null; then
    echo "⚠️  Qt6 not found. Please install Qt6"
    echo "   Ubuntu: sudo apt-get install qt6-base-dev"
    echo "   macOS: brew install qt6"
    echo "   Windows: https://www.qt.io/download"
fi

# Create build directory
if [ ! -d "build" ]; then
    echo "📁 Creating build directory..."
    mkdir build
fi

# Build
echo "🏗️  Configuring with CMake..."
cd build
cmake ..

echo "⚙️  Building..."
cmake --build . --config Release

echo ""
echo "✅ Build complete!"
echo ""
echo "🚀 To run the application:"
echo "   ./NextAI"
echo ""
echo "📝 Don't forget to set your Gemini API key when the app starts!"
