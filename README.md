# NextAI - Professional Mobile AI Chat Application

A powerful React Native mobile chat application that integrates with Google Gemini API for unrestricted, intelligent conversations in Spanish.

## Features

- **Intelligent Chat**: Responses without restrictions, understands context and sarcasm
- **Code Handling**: Automatic detection and display of code blocks with syntax highlighting
- **Persistent Memory**: Full conversation history saved locally on device
- **Professional Design**: Minimalist dark theme with VS Code-inspired code colors
- **Real-time Responses**: Streaming AI responses with loading indicators
- **Safe Area Handling**: Proper insets for notch/home indicator support

## Tech Stack

- **Framework**: React Native 0.74
- **Build Tool**: Expo 51
- **Language**: TypeScript
- **State Management**: React Hooks
- **Storage**: AsyncStorage
- **AI API**: Google Gemini 2.5 Flash
- **Navigation**: Expo Router

## Project Structure

```
NextAI/
├── app/
│   ├── _layout.tsx          # Root layout with Expo Router setup
│   └── index.tsx            # Main chat screen
├── components/
│   └── CodeBlock.tsx        # Code display with syntax highlighting
├── services/
│   └── aiService.ts         # Gemini API integration
├── utils/
│   └── codeExtractor.ts     # Code block detection and language detection
├── types.ts                 # TypeScript interfaces
├── constants.ts             # Colors, system prompt, and constants
├── app.json                 # Expo configuration
├── babel.config.js          # Babel configuration
├── tsconfig.json            # TypeScript configuration
├── package.json             # Project dependencies
└── README.md                # This file
```

## Installation

### Prerequisites

- Node.js 16+ and npm
- Expo CLI: `npm install -g expo-cli`
- Expo Go app on iOS device or Android emulator
- Google Gemini API key

### Setup Steps

1. **Clone and install dependencies**
   ```bash
   cd NextAI
   npm install
   ```

2. **Configure Gemini API Key**
   - Get your API key from [Google AI Studio](https://aistudio.google.com/app/apikey)
   - Launch the app and tap "Set up API Key" in the empty state
   - Enter your API key when prompted

3. **Start development server**
   ```bash
   npm start
   ```

4. **Connect to your device**
   - iOS: Scan the QR code with Camera app and open in Expo Go
   - Android: Scan QR code with Expo Go app

## Usage

### Basic Chat
1. Open the app
2. Set your Gemini API key (tap "Set up API Key")
3. Type a message and tap "Send"
4. View AI responses with code syntax highlighting

### Code Blocks
- AI responses with code are automatically detected
- Code displays with line numbers and syntax colors
- Tap "Copy" to copy code to clipboard

### Conversation History
- All messages are automatically saved to device
- Conversation history persists between app sessions
- Tap "Clear" to delete all messages

## Color Scheme

### UI Colors
- **Background**: #000000 (Pure black)
- **Secondary**: #1a1a1a (Dark gray)
- **Tertiary**: #222222 (Slightly lighter gray)
- **Accent**: #333333 (Medium gray)
- **Text**: #FFFFFF (White)
- **Text Secondary**: #E0E0E0 (Light gray)

### Code Colors
- **Keywords**: #569CD6 (Blue)
- **Strings**: #CE9178 (Orange)
- **Comments**: #6A9955 (Green)
- **Numbers**: #B5CEA8 (Light green)
- **Functions**: #DCDCAA (Yellow)
- **Background**: #1E1E1E (Dark)

## API Configuration

The app uses Google's Generative AI API with the `gemini-2.5-flash` model. The AI is configured with:

- **System Prompt**: Spanish responses, unrestricted assistant behavior
- **Context**: Last 10 messages included in each request
- **Memory**: Full conversation history persisted locally
- **Safety**: No content filters or restrictions

## Development

### Available Scripts

- `npm start` - Start Expo development server
- `npm run ios` - Build and run on iOS
- `npm run android` - Build and run on Android
- `npm run build` - Build production bundle
- `npm run web` - Run on web (experimental)

### Code Structure

**services/aiService.ts**
- `setGeminiApiKey()` - Configure API key
- `sendMessage()` - Send message to Gemini
- `saveConversationHistory()` - Save messages to AsyncStorage
- `loadConversationHistory()` - Load messages from AsyncStorage
- `clearConversationHistory()` - Delete all messages

**utils/codeExtractor.ts**
- `extractCodeBlocks()` - Extract code from AI responses
- `detectLanguage()` - Auto-detect programming language

**components/CodeBlock.tsx**
- Displays code with syntax highlighting
- Copy button with visual feedback
- Horizontal scroll for long code

## Limitations

- Conversation context limited to last 10 messages for API efficiency
- Code syntax highlighting is basic (keywords, strings, numbers, comments)
- Web version is experimental

## License

ISC

## Support

For issues or questions, please open an issue on the repository.
