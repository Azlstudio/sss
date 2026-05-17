import React, { useState, useEffect, useRef, useCallback } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TextInput,
  TouchableOpacity,
  SafeAreaView,
  ActivityIndicator,
  KeyboardAvoidingView,
  Platform,
  Alert,
} from 'react-native';
import { useSafeAreaInsets } from 'react-native-safe-area-context';
import { StatusBar } from 'expo-status-bar';
import { Message, CodeBlock } from '../types';
import { COLORS, CODE_COLORS } from '../constants';
import {
  setGeminiApiKey,
  sendMessage,
  saveConversationHistory,
  loadConversationHistory,
  clearConversationHistory,
} from '../services/aiService';
import { extractCodeBlocks } from '../utils/codeExtractor';
import CodeBlockComponent from '../components/CodeBlock';

const ChatScreen: React.FC = () => {
  const insets = useSafeAreaInsets();
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputText, setInputText] = useState('');
  const [loading, setLoading] = useState(false);
  const [apiKeySet, setApiKeySet] = useState(false);
  const [userId] = useState('user_' + Date.now());
  const scrollViewRef = useRef<ScrollView>(null);

  useEffect(() => {
    initializeApp();
  }, []);

  const initializeApp = async () => {
    try {
      const history = await loadConversationHistory(userId);
      setMessages(history);
    } catch (error) {
      console.error('Error initializing app:', error);
    }
  };

  const handleSendMessage = useCallback(async () => {
    if (!inputText.trim()) return;

    if (!apiKeySet) {
      Alert.alert('API Key Required', 'Please set your Gemini API key first');
      return;
    }

    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: inputText.trim(),
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setInputText('');
    setLoading(true);

    try {
      const response = await sendMessage(userMessage.text, [...messages, userMessage]);

      const { text, codeBlocks } = extractCodeBlocks(response);

      const aiMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'ai',
        text,
        timestamp: new Date(),
        codeBlocks,
      };

      setMessages(prev => {
        const updated = [...prev, aiMessage];
        saveConversationHistory(userId, updated);
        return updated;
      });
    } catch (error) {
      Alert.alert('Error', 'Failed to get response from AI');
      console.error('Error:', error);
    } finally {
      setLoading(false);
    }

    setTimeout(() => scrollViewRef.current?.scrollToEnd({ animated: true }), 100);
  }, [inputText, messages, apiKeySet, userId]);

  const handleClearHistory = () => {
    Alert.alert('Clear History', 'Are you sure you want to clear all messages?', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Clear',
        style: 'destructive',
        onPress: async () => {
          await clearConversationHistory(userId);
          setMessages([]);
        },
      },
    ]);
  };

  const handleSetApiKey = () => {
    Alert.prompt('Gemini API Key', 'Enter your Gemini API key:', [
      { text: 'Cancel', style: 'cancel' },
      {
        text: 'Save',
        onPress: (key) => {
          if (key?.trim()) {
            setGeminiApiKey(key.trim());
            setApiKeySet(true);
          }
        },
      },
    ]);
  };

  return (
    <SafeAreaView style={[styles.container, { paddingTop: insets.top, paddingBottom: insets.bottom }]}>
      <StatusBar hidden={false} />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Next AI</Text>
        <TouchableOpacity onPress={handleClearHistory} style={styles.clearButton}>
          <Text style={styles.clearButtonText}>Clear</Text>
        </TouchableOpacity>
      </View>

      {/* Messages */}
      {messages.length === 0 ? (
        <View style={styles.emptyState}>
          <Text style={styles.emptyStateTitle}>Welcome to Next AI</Text>
          <Text style={styles.emptyStateText}>
            Start a conversation with your unrestricted AI assistant. Your messages are saved automatically.
          </Text>
          {!apiKeySet && (
            <TouchableOpacity onPress={handleSetApiKey} style={styles.setupButton}>
              <Text style={styles.setupButtonText}>Set up API Key</Text>
            </TouchableOpacity>
          )}
        </View>
      ) : (
        <ScrollView
          ref={scrollViewRef}
          style={styles.messagesContainer}
          contentContainerStyle={styles.messagesContent}
          showsVerticalScrollIndicator={true}
          scrollEventThrottle={16}
        >
          {messages.map((message) => (
            <View
              key={message.id}
              style={[
                styles.messageWrapper,
                message.sender === 'user' ? styles.userMessageWrapper : styles.aiMessageWrapper,
              ]}
            >
              <View
                style={[
                  styles.messageBubble,
                  message.sender === 'user' ? styles.userBubble : styles.aiBubble,
                ]}
              >
                <Text style={styles.messageText}>{message.text}</Text>
                <Text style={styles.timestamp}>
                  {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                </Text>

                {message.codeBlocks && message.codeBlocks.length > 0 && (
                  <View style={styles.codeBlocksContainer}>
                    {message.codeBlocks.map((block, idx) => (
                      <CodeBlockComponent key={idx} code={block.code} language={block.language} />
                    ))}
                  </View>
                )}
              </View>
            </View>
          ))}

          {loading && (
            <View style={styles.loadingContainer}>
              <ActivityIndicator size="large" color={COLORS.accent} />
              <Text style={styles.loadingText}>Thinking...</Text>
            </View>
          )}
        </ScrollView>
      )}

      {/* Input Area */}
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        keyboardVerticalOffset={Platform.OS === 'ios' ? 90 : 0}
      >
        <View style={styles.inputContainer}>
          {!apiKeySet && (
            <TouchableOpacity onPress={handleSetApiKey} style={styles.setupApiKeyButton}>
              <Text style={styles.setupApiKeyText}>Tap to set API Key</Text>
            </TouchableOpacity>
          )}
          <View style={styles.inputRow}>
            <TextInput
              style={styles.input}
              placeholder="Type your message..."
              placeholderTextColor={COLORS.accent}
              value={inputText}
              onChangeText={setInputText}
              multiline
              maxLength={1000}
              editable={!loading && apiKeySet}
            />
            <TouchableOpacity
              style={[styles.sendButton, (!apiKeySet || loading) && styles.sendButtonDisabled]}
              onPress={handleSendMessage}
              disabled={loading || !apiKeySet}
            >
              <Text style={styles.sendButtonText}>Send</Text>
            </TouchableOpacity>
          </View>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    color: COLORS.text,
  },
  clearButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: COLORS.secondary,
    borderRadius: 8,
  },
  clearButtonText: {
    color: COLORS.text,
    fontSize: 12,
    fontWeight: '600',
  },
  emptyState: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 24,
  },
  emptyStateTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: COLORS.text,
    marginBottom: 12,
    textAlign: 'center',
  },
  emptyStateText: {
    fontSize: 16,
    color: COLORS.textSecondary,
    textAlign: 'center',
    marginBottom: 24,
    lineHeight: 24,
  },
  setupButton: {
    paddingHorizontal: 24,
    paddingVertical: 12,
    backgroundColor: COLORS.accent,
    borderRadius: 8,
    marginTop: 16,
  },
  setupButtonText: {
    color: COLORS.text,
    fontSize: 14,
    fontWeight: '600',
  },
  messagesContainer: {
    flex: 1,
  },
  messagesContent: {
    paddingVertical: 16,
  },
  messageWrapper: {
    paddingHorizontal: 16,
    marginVertical: 8,
    flexDirection: 'row',
  },
  userMessageWrapper: {
    justifyContent: 'flex-end',
  },
  aiMessageWrapper: {
    justifyContent: 'flex-start',
  },
  messageBubble: {
    maxWidth: '85%',
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 12,
  },
  userBubble: {
    backgroundColor: COLORS.secondary,
  },
  aiBubble: {
    backgroundColor: COLORS.tertiary,
  },
  messageText: {
    fontSize: 14,
    color: COLORS.text,
    lineHeight: 20,
  },
  timestamp: {
    fontSize: 10,
    color: COLORS.accent,
    marginTop: 6,
    alignSelf: 'flex-end',
  },
  codeBlocksContainer: {
    marginTop: 12,
  },
  loadingContainer: {
    alignItems: 'center',
    justifyContent: 'center',
    paddingVertical: 24,
  },
  loadingText: {
    color: COLORS.textSecondary,
    marginTop: 12,
    fontSize: 14,
  },
  inputContainer: {
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderTopWidth: 1,
    borderTopColor: COLORS.border,
    backgroundColor: COLORS.background,
  },
  setupApiKeyButton: {
    backgroundColor: COLORS.secondary,
    paddingVertical: 10,
    borderRadius: 8,
    marginBottom: 8,
  },
  setupApiKeyText: {
    color: COLORS.accent,
    textAlign: 'center',
    fontSize: 12,
    fontWeight: '600',
  },
  inputRow: {
    flexDirection: 'row',
    alignItems: 'flex-end',
    gap: 8,
  },
  input: {
    flex: 1,
    backgroundColor: COLORS.secondary,
    color: COLORS.text,
    paddingHorizontal: 12,
    paddingVertical: 10,
    borderRadius: 8,
    maxHeight: 100,
    fontSize: 14,
    borderWidth: 1,
    borderColor: COLORS.border,
  },
  sendButton: {
    paddingHorizontal: 16,
    paddingVertical: 10,
    backgroundColor: COLORS.accent,
    borderRadius: 8,
  },
  sendButtonDisabled: {
    opacity: 0.5,
  },
  sendButtonText: {
    color: COLORS.text,
    fontWeight: '600',
    fontSize: 14,
  },
});

export default ChatScreen;
