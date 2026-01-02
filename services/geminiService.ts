
import { GoogleGenAI, Type } from "@google/genai";

const ai = new GoogleGenAI({ apiKey: process.env.API_KEY });

export const generateChaosTask = async (roundNumber: number, playerNames: string[]) => {
  const modes: string[] = ['DRAWING', 'FASTEST_FINGER', 'LIE_DETECTOR', 'VOTE'];
  const selectedMode = modes[Math.floor(Math.random() * modes.length)];

  try {
    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: `Generate a task for a chaotic party game.
      Round: ${roundNumber}. 
      Players: ${playerNames.join(", ")}.
      Target Mode: ${selectedMode}.

      Specific Mode Requirements:
      - DRAWING: A weird, specific prompt (e.g., "A duck wearing a tuxedo at a disco").
      - FASTEST_FINGER: A difficult phrase to type or a math problem. Include 'correctAnswer'.
      - LIE_DETECTOR: Ask players to provide a convincing lie about a specific weird topic.
      - VOTE: A spicy or funny "Most Likely To..." or "Who among you..." question. (e.g., "Who is most likely to accidentally join a cult?").

      Ensure the JSON fits the schema exactly.`,
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            id: { type: Type.STRING },
            type: { type: Type.STRING },
            title: { type: Type.STRING },
            description: { type: Type.STRING },
            timer: { type: Type.NUMBER },
            correctAnswer: { type: Type.STRING },
            options: { type: Type.ARRAY, items: { type: Type.STRING } }
          },
          required: ["id", "type", "title", "description", "timer"]
        }
      }
    });

    return JSON.parse(response.text);
  } catch (error) {
    console.error("Gemini Error:", error);
    return {
      id: "fallback",
      type: "VOTE",
      title: "DEMOCRACY!",
      description: "Who is the most suspicious person in this room?",
      timer: 15
    };
  }
};

export const judgeWinner = async (task: any, submissions: { player: string, text?: string, drawingBase64?: string }[]) => {
  try {
    const parts: any[] = [
      { text: `Game Task: "${task.description}" (Mode: ${task.type}).` }
    ];

    if (task.type === 'DRAWING') {
      const drawingPart = submissions.find(s => s.drawingBase64);
      if (drawingPart?.drawingBase64) {
        parts.push({
          inlineData: {
            mimeType: 'image/png',
            data: drawingPart.drawingBase64.split(',')[1],
          },
        });
        parts.push({ text: "Above is the collaborative drawing. Judge the collective effort or pick one player who stood out." });
      }
    } else if (task.type === 'VOTE') {
      parts.push({ text: `Votes received: ${JSON.stringify(submissions.map(s => ({ voter: s.player, votedFor: s.text })))}.` });
      parts.push({ text: "Count the votes. Determine who got the most votes. If it's a tie, pick one and explain why in a funny way." });
    } else {
      parts.push({ text: `Submissions: ${JSON.stringify(submissions)}.` });
    }

    parts.push({ text: "Evaluate the outcome. Return JSON with winner name and a funny reason for their win (or why they were voted for)." });

    const response = await ai.models.generateContent({
      model: "gemini-3-flash-preview",
      contents: { parts },
      config: {
        responseMimeType: "application/json",
        responseSchema: {
          type: Type.OBJECT,
          properties: {
            winner: { type: Type.STRING },
            reason: { type: Type.STRING }
          },
          required: ["winner", "reason"]
        }
      }
    });
    return JSON.parse(response.text);
  } catch (error) {
    console.error("Judging Error:", error);
    return { winner: "The Void", reason: "Democracy has failed us. The AI has taken over." };
  }
};
