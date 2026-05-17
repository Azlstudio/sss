import { GoogleGenerativeAI } from '@google/generative-ai';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Message, ConversationHistory } from '../types';
import { SYSTEM_PROMPT } from '../constants';

const GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY_HERE';
const HISTORY_STORAGE_KEY = 'conversation_history';
const MAX_CONTEXT_MESSAGES = 10;

let client: GoogleGenerativeAI;
let model: any;

const initializeClient = () => {
  if (!client) {
    client = new GoogleGenerativeAI(GEMINI_API_KEY);
    model = client.getGenerativeModel({ model: 'gemini-2.5-flash' });
  }
};

export const setGeminiApiKey = (apiKey: string) => {
  client = new GoogleGenerativeAI(apiKey);
  model = client.getGenerativeModel({ model: 'gemini-2.5-flash' });
};

export const saveConversationHistory = async (userId: string, messages: Message[]): Promise<void> => {
  try {
    const history: ConversationHistory = {
      userId,
      messages,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
    await AsyncStorage.setItem(`${HISTORY_STORAGE_KEY}_${userId}`, JSON.stringify(history));
  } catch (error) {
    console.error('Error saving conversation history:', error);
  }
};

export const loadConversationHistory = async (userId: string): Promise<Message[]> => {
  try {
    const data = await AsyncStorage.getItem(`${HISTORY_STORAGE_KEY}_${userId}`);
    if (data) {
      const history: ConversationHistory = JSON.parse(data);
      return history.messages.map(msg => ({
        ...msg,
        timestamp: new Date(msg.timestamp),
      }));
    }
    return [];
  } catch (error) {
    console.error('Error loading conversation history:', error);
    return [];
  }
};

export const clearConversationHistory = async (userId: string): Promise<void> => {
  try {
    await AsyncStorage.removeItem(`${HISTORY_STORAGE_KEY}_${userId}`);
  } catch (error) {
    console.error('Error clearing conversation history:', error);
  }
};

export const sendMessage = async (userMessage: string, messages: Message[]): Promise<string> => {
  initializeClient();

  try {
    const recentMessages = messages.slice(-MAX_CONTEXT_MESSAGES);

    const conversationContext = recentMessages
      .map(msg => `${msg.sender === 'user' ? 'User' : 'Assistant'}: ${msg.text}`)
      .join('\n');

    const fullPrompt = `${SYSTEM_PROMPT}\n\nConversation context:\n${conversationContext}\n\nUser: ${userMessage}`;

    const result = await model.generateContent(fullPrompt);
    const response = await result.response;
    return response.text();
  } catch (error) {
    console.error('Error sending message to Gemini:', error);
    throw new Error('Failed to get response from AI');
  }
};
