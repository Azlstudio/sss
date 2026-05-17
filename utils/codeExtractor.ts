import { CodeBlock } from '../types';

export const extractCodeBlocks = (text: string): { text: string; codeBlocks: CodeBlock[] } => {
  const codeBlocks: CodeBlock[] = [];
  let processedText = text;
  let offset = 0;

  const codeBlockRegex = /```(\w*)\n([\s\S]*?)```/g;
  let match;

  while ((match = codeBlockRegex.exec(text)) !== null) {
    const language = match[1] || 'text';
    const code = match[2];
    const fullMatch = match[0];
    const startIndex = match.index - offset;
    const endIndex = startIndex + fullMatch.length;

    codeBlocks.push({
      language,
      code,
      startIndex,
      endIndex,
    });
  }

  processedText = text.replace(codeBlockRegex, '');

  return {
    text: processedText.trim(),
    codeBlocks,
  };
};

export const detectLanguage = (code: string): string => {
  if (code.includes('import ') || code.includes('export ') || code.includes('const ') || code.includes('function ')) {
    return 'javascript';
  }
  if (code.includes('def ') || code.includes('import ')) {
    return 'python';
  }
  if (code.includes('SELECT ') || code.includes('INSERT ') || code.includes('UPDATE ')) {
    return 'sql';
  }
  if (code.includes('<?php') || code.includes('echo ')) {
    return 'php';
  }
  if (code.includes('fn main()') || code.includes('impl ')) {
    return 'rust';
  }
  return 'text';
};
