
export enum GameStatus {
  LOBBY = 'LOBBY',
  PLAYING = 'PLAYING',
  RESULTS = 'RESULTS'
}

export type ChaosMode = 'DRAWING' | 'FASTEST_FINGER' | 'LIE_DETECTOR' | 'VOTE';

export interface Player {
  id: string;
  name: string;
  avatar: string;
  score: number;
  isHost: boolean;
  isReady: boolean;
}

export interface ChaosTask {
  id: string;
  type: ChaosMode;
  title: string;
  description: string;
  timer: number;
  correctAnswer?: string;
  options?: string[];
}

export interface RoomState {
  code: string;
  players: Player[];
  status: GameStatus;
  currentTask?: ChaosTask;
  round: number;
  maxRounds: number;
  history: string[];
}

export interface GameAction {
  type: 'PLAYER_JOINED' | 'PLAYER_LEFT' | 'READY_TOGGLE' | 'START_GAME' | 'SUBMIT_ANSWER' | 'CHAT_MESSAGE' | 'DRAW_STROKE' | 'FINISH_ROUND';
  payload: any;
  senderId: string;
}
