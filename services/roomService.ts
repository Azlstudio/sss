
import { GameAction, RoomState, GameStatus } from '../types';

/**
 * Since we don't have a real socket backend, 
 * we use the BroadcastChannel API to simulate local multiplayer 
 * between different tabs on the same browser.
 */

const CHANNEL_NAME = 'chaos_room_sync';

export class RoomConnector {
  private channel: BroadcastChannel;
  private onAction: (action: GameAction) => void;

  constructor(onAction: (action: GameAction) => void) {
    this.channel = new BroadcastChannel(CHANNEL_NAME);
    this.onAction = onAction;
    this.channel.onmessage = (event) => {
      this.onAction(event.data);
    };
  }

  send(action: GameAction) {
    this.channel.postMessage(action);
  }

  close() {
    this.channel.close();
  }
}

export const generateRoomCode = () => {
  return Math.random().toString(36).substring(2, 7).toUpperCase();
};
