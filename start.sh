#!/bin/bash

echo "🚀 NextAI - Expo Development Server"
echo "===================================="
echo ""
echo "Starting Expo development server..."
echo "Port: 8081"
echo ""

# Kill any existing processes
pkill -f "expo start" 2>/dev/null || true
sleep 1

# Clear Metro bundler cache
rm -rf /tmp/metro-cache 2>/dev/null || true

# Start Expo with explicit configuration
cd "$(dirname "$0")"

export EXPO_NO_TYPESCRIPT_SETUP=false
npx expo start \
  --localhost \
  --clear \
  --dev-client \
  --web=false \
  --max-workers=4

