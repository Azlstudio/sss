import React, { useState } from 'react';
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  Alert,
  Clipboard,
  StyleSheet,
} from 'react-native';
import { COLORS, CODE_COLORS } from '../constants';

interface CodeBlockProps {
  code: string;
  language: string;
}

const CodeBlock: React.FC<CodeBlockProps> = ({ code, language }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await Clipboard.setString(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (error) {
      Alert.alert('Error', 'Failed to copy code');
    }
  };

  const highlightSyntax = (text: string) => {
    const keywords = /\b(function|const|let|var|return|if|else|for|while|class|import|export|async|await|interface|type|enum)\b/g;
    const strings = /(['"`])([^\\]|\\.|(?=\1))*?\1/g;
    const numbers = /\b\d+\b/g;
    const comments = /(\/\/.*$|\/\*[\s\S]*?\*\/)/g;
    const functions = /\b([a-zA-Z_]\w*)\s*(?=\()/g;

    let highlighted = text
      .replace(/&/g, '&amp;')
      .replace(/</g, '&lt;')
      .replace(/>/g, '&gt;');

    highlighted = highlighted.replace(keywords, (match) => `<keyword>${match}</keyword>`);
    highlighted = highlighted.replace(strings, (match) => `<string>${match}</string>`);
    highlighted = highlighted.replace(numbers, (match) => `<number>${match}</number>`);
    highlighted = highlighted.replace(comments, (match) => `<comment>${match}</comment>`);
    highlighted = highlighted.replace(functions, (match) => `<function>${match}</function>`);

    return highlighted;
  };

  const lines = code.split('\n');

  return (
    <View style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.language}>{language}</Text>
        <TouchableOpacity style={styles.copyButton} onPress={handleCopy}>
          <Text style={styles.copyButtonText}>{copied ? '✓ Copied' : 'Copy'}</Text>
        </TouchableOpacity>
      </View>

      <ScrollView
        style={styles.codeContainer}
        horizontal={true}
        scrollEventThrottle={16}
        showsHorizontalScrollIndicator={true}
      >
        <View style={styles.code}>
          {lines.map((line, index) => (
            <View key={index} style={styles.line}>
              <Text style={styles.lineNumber}>{String(index + 1).padStart(3, ' ')}</Text>
              <Text style={styles.lineContent}>{line || ' '}</Text>
            </View>
          ))}
        </View>
      </ScrollView>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    borderRadius: 12,
    overflow: 'hidden',
    marginVertical: 12,
    backgroundColor: CODE_COLORS.background,
    borderColor: COLORS.border,
    borderWidth: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 12,
    paddingVertical: 10,
    backgroundColor: COLORS.secondary,
    borderBottomColor: COLORS.border,
    borderBottomWidth: 1,
  },
  language: {
    color: COLORS.textSecondary,
    fontSize: 12,
    fontWeight: '600',
    textTransform: 'uppercase',
  },
  copyButton: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    backgroundColor: COLORS.accent,
    borderRadius: 6,
  },
  copyButtonText: {
    color: COLORS.text,
    fontSize: 12,
    fontWeight: '600',
  },
  codeContainer: {
    maxHeight: 400,
  },
  code: {
    backgroundColor: CODE_COLORS.background,
    paddingVertical: 12,
  },
  line: {
    flexDirection: 'row',
    minHeight: 20,
  },
  lineNumber: {
    color: COLORS.accent,
    fontSize: 12,
    fontFamily: 'Courier New',
    paddingLeft: 12,
    paddingRight: 12,
    fontWeight: '500',
    width: 50,
  },
  lineContent: {
    color: COLORS.text,
    fontSize: 12,
    fontFamily: 'Courier New',
    paddingRight: 12,
  },
});

export default CodeBlock;
