export interface Message {
  id: string;
  sender: 'user' | 'ai';
  text: string;
  timestamp: Date;
  codeBlocks?: CodeBlock[];
}

export interface CodeBlock {
  language: string;
  code: string;
  startIndex: number;
  endIndex: number;
}

export interface ConversationHistory {
  userId: string;
  messages: Message[];
  createdAt: Date;
  updatedAt: Date;
}
