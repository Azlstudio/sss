# NextAI Setup Guide

## Quick Start (5 minutes)

### 1. Install Dependencies
All dependencies have already been installed via npm:
```bash
npm install  # Already completed ✓
```

### 2. Get Your Gemini API Key
1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click "Create API Key"
3. Copy your API key (keep it safe!)

### 3. Start the Development Server
```bash
npm start
```

You'll see:
```
> expo start
```

This starts the Expo development server and displays a QR code.

### 4. Open on iPhone
**Option A: Expo Go App (Recommended)**
- Install [Expo Go](https://apps.apple.com/app/expo-go/id982107779) from App Store
- Open Expo Go
- Scan the QR code from terminal
- App opens automatically

**Option B: Development Build**
```bash
npm run ios
```
(Requires Xcode)

### 5. Set up API Key in App
1. When app opens, you'll see "Welcome to Next AI"
2. Tap "Set up API Key"
3. Paste your Gemini API key
4. Start chatting!

## Project Structure

```
NextAI/
├── app/
│   ├── index.tsx           Main chat screen
│   └── _layout.tsx         Expo Router setup
├── components/
│   └── CodeBlock.tsx       Code display component
├── services/
│   └── aiService.ts        Gemini API service
├── utils/
│   └── codeExtractor.ts    Code detection utility
├── types.ts                TypeScript definitions
├── constants.ts            Colors & prompts
├── package.json            Dependencies
├── app.json                Expo configuration
├── babel.config.js         Babel setup
└── tsconfig.json           TypeScript config
```

## Available Commands

| Command | Purpose |
|---------|---------|
| `npm start` | Start development server |
| `npm run ios` | Build and run on iOS |
| `npm run android` | Build and run on Android |
| `npm run web` | Run on web (experimental) |
| `npm build` | Build for production |

## Features

### Chat
- Type messages and get AI responses
- Full conversation history is saved automatically
- Context from last 10 messages included in each response

### Code Handling
- AI automatically detects code blocks in responses
- Code displays with line numbers and syntax highlighting
- Copy button to copy code to clipboard
- Supports all programming languages

### Storage
- All messages stored locally on device via AsyncStorage
- Messages persist between app sessions
- Tap "Clear" button to delete all messages

## API Configuration

The app uses Google Generative AI with `gemini-2.5-flash` model:

- **Unrestricted**: No content filters
- **Spanish**: All responses in Spanish
- **Stateful**: Remembers conversation context
- **Fast**: Uses Flash model for speed

## Troubleshooting

### Blank Screen After Opening
- Check that you've set your API key
- Make sure API key is valid
- Try killing the app and restarting

### Network Errors
- Check internet connection
- Verify API key is correct
- Ensure Gemini API is enabled in Google Cloud

### App Crashes
- Try `npm start` and reload
- Clear app cache if needed
- Check console logs for errors

### Code Display Issues
- Ensure code is in triple backticks: ```language\ncode\n```
- Supported detection: JavaScript, Python, SQL, PHP, Rust

## Performance Tips

1. **Message Limit**: Keep app open for reasonable session length
2. **Storage**: App will use local storage for all messages
3. **Battery**: Long conversations may use more battery
4. **Network**: Requires active internet for AI responses

## Customization

### Colors
Edit `constants.ts`:
- `COLORS` object for UI colors
- `CODE_COLORS` for syntax highlighting

### System Prompt
Edit `SYSTEM_PROMPT` in `constants.ts` to change AI behavior

### Message Context
Change `MAX_CONTEXT_MESSAGES` in `services/aiService.ts` (default: 10)

## Support

For issues:
1. Check console logs: open Expo Go, shake phone, tap "View debug logs"
2. Verify API key is valid
3. Check network connection
4. Try force closing and reopening the app

## Next Steps

1. ✅ Dependencies installed
2. ✅ TypeScript configured
3. ✅ Project structure created
4. ⏭️ Get API key from Google AI Studio
5. ⏭️ Run `npm start`
6. ⏭️ Scan QR code with Expo Go
7. ⏭️ Set up API key in app
8. ⏭️ Start chatting!

---

**Happy chatting with NextAI! 🚀**
