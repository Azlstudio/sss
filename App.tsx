
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { GameStatus, Player, RoomState, ChaosTask, GameAction, ChaosMode } from './types';
import { AVATARS, COLORS } from './constants';
import { RoomConnector, generateRoomCode } from './services/roomService';
import { generateChaosTask, judgeWinner } from './services/geminiService';
import { 
  Users, Play, ShieldAlert, Timer, 
  Trophy, MessageSquare, Send, X, 
  Crown, Hash, Copy, Check, Palette, Zap, Ghost, Vote
} from 'lucide-react';

const PLAYER_COLORS = [
  '#f43f5e', '#8b5cf6', '#06b6d4', '#10b981', '#f59e0b', '#ec4899', '#6366f1', '#a855f7'
];

const App: React.FC = () => {
  const [view, setView] = useState<'LANDING' | 'ROOM'>('LANDING');
  const [player, setPlayer] = useState<Player & { color?: string } | null>(null);
  const [room, setRoom] = useState<RoomState | null>(null);
  const [chat, setChat] = useState<{ sender: string, text: string }[]>([]);
  const [answer, setAnswer] = useState('');
  const [hasVoted, setHasVoted] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const [winnerInfo, setWinnerInfo] = useState<{ winner: string, reason: string } | null>(null);
  const [timer, setTimer] = useState(0);
  const [submissions, setSubmissions] = useState<{ player: string, text?: string, drawingBase64?: string }[]>([]);

  const connectorRef = useRef<RoomConnector | null>(null);
  const canvasRef = useRef<HTMLCanvasElement | null>(null);
  const isDrawing = useRef(false);

  const clearCanvas = useCallback(() => {
    if (canvasRef.current) {
      const ctx = canvasRef.current.getContext('2d');
      if (ctx) ctx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
    }
  }, []);

  const handleAction = useCallback((action: GameAction) => {
    setRoom(prev => {
      if (!prev) return null;
      if (action.payload.roomCode && action.payload.roomCode !== prev.code) return prev;

      switch (action.type) {
        case 'PLAYER_JOINED':
          if (prev.players.find(p => p.id === action.payload.player.id)) return prev;
          return { ...prev, players: [...prev.players, action.payload.player] };
        
        case 'READY_TOGGLE':
          return {
            ...prev,
            players: prev.players.map(p => 
              p.id === action.senderId ? { ...p, isReady: !p.isReady } : p
            )
          };
          
        case 'START_GAME':
          setTimer(action.payload.task.timer);
          setSubmissions([]);
          setAnswer('');
          setHasVoted(false);
          setShowResults(false);
          if (action.payload.task.type === 'DRAWING') setTimeout(clearCanvas, 50);
          return { 
            ...prev, 
            status: GameStatus.PLAYING, 
            currentTask: action.payload.task,
            round: action.payload.round
          };

        case 'SUBMIT_ANSWER':
          setSubmissions(s => [...s, { player: action.payload.playerName, text: action.payload.text, drawingBase64: action.payload.drawingBase64 }]);
          return prev;

        case 'DRAW_STROKE':
          if (canvasRef.current && action.senderId !== player?.id) {
            const ctx = canvasRef.current.getContext('2d');
            if (ctx) {
              const { x, y, prevX, prevY, color } = action.payload;
              ctx.strokeStyle = color;
              ctx.lineWidth = 5;
              ctx.lineCap = 'round';
              ctx.lineJoin = 'round';
              ctx.beginPath();
              ctx.moveTo(prevX, prevY);
              ctx.lineTo(x, y);
              ctx.stroke();
            }
          }
          return prev;

        case 'FINISH_ROUND':
          setWinnerInfo(action.payload.winnerInfo);
          setShowResults(true);
          return {
            ...prev,
            players: prev.players.map(p => 
              p.name === action.payload.winnerInfo.winner ? { ...p, score: p.score + 10 } : p
            )
          };

        case 'CHAT_MESSAGE':
          setChat(c => [...c, { sender: action.payload.senderName, text: action.payload.text }]);
          return prev;

        default:
          return prev;
      }
    });
  }, [player?.id, clearCanvas]);

  useEffect(() => {
    connectorRef.current = new RoomConnector(handleAction);
    return () => connectorRef.current?.close();
  }, [handleAction]);

  useEffect(() => {
    if (room?.status === GameStatus.PLAYING && timer > 0) {
      const interval = setInterval(() => setTimer(t => t - 1), 1000);
      return () => clearInterval(interval);
    } else if (room?.status === GameStatus.PLAYING && timer === 0 && player?.isHost) {
      handleRoundEnd();
    }
  }, [timer, room?.status, player?.isHost]);

  const handleRoundEnd = async () => {
    if (!room?.currentTask || !player?.isHost) return;
    
    let currentSubmissions = [...submissions];
    if (room.currentTask.type === 'DRAWING' && canvasRef.current) {
      const drawingBase64 = canvasRef.current.toDataURL('image/png');
      currentSubmissions.push({ player: 'Collaborative', drawingBase64 });
    }

    const info = await judgeWinner(room.currentTask, currentSubmissions);
    connectorRef.current?.send({
      type: 'FINISH_ROUND',
      senderId: player.id,
      payload: { winnerInfo: info, roomCode: room.code }
    });
  };

  const createRoom = () => {
    const code = generateRoomCode();
    const newPlayer: Player & { color: string } = {
      id: Math.random().toString(36).substring(7),
      name: `Host_${Math.floor(Math.random() * 99)}`,
      avatar: AVATARS[Math.floor(Math.random() * AVATARS.length)],
      score: 0,
      isHost: true,
      isReady: true,
      color: PLAYER_COLORS[0]
    };
    setPlayer(newPlayer);
    setRoom({
      code,
      players: [newPlayer],
      status: GameStatus.LOBBY,
      round: 0,
      maxRounds: 5,
      history: []
    });
    setView('ROOM');
  };

  const joinRoom = (code: string) => {
    const newPlayer: Player & { color: string } = {
      id: Math.random().toString(36).substring(7),
      name: `Chaos_${Math.floor(Math.random() * 99)}`,
      avatar: AVATARS[Math.floor(Math.random() * AVATARS.length)],
      score: 0,
      isHost: false,
      isReady: false,
      color: PLAYER_COLORS[Math.floor(Math.random() * PLAYER_COLORS.length)]
    };
    setPlayer(newPlayer);
    setRoom({ code, players: [newPlayer], status: GameStatus.LOBBY, round: 0, maxRounds: 5, history: [] });
    connectorRef.current?.send({ type: 'PLAYER_JOINED', senderId: newPlayer.id, payload: { player: newPlayer, roomCode: code } });
    setView('ROOM');
  };

  const startGame = async () => {
    if (!room || !player?.isHost) return;
    const task = await generateChaosTask(room.round + 1, room.players.map(p => p.name));
    connectorRef.current?.send({ type: 'START_GAME', senderId: player.id, payload: { task, round: room.round + 1, roomCode: room.code } });
  };

  const submitAnswer = (text?: string) => {
    if (!player || !room) return;
    connectorRef.current?.send({
      type: 'SUBMIT_ANSWER',
      senderId: player.id,
      payload: { playerName: player.name, text: text || answer, roomCode: room.code }
    });
    setAnswer('');
    if (room.currentTask?.type === 'VOTE') setHasVoted(true);
  };

  const drawOnCanvas = (e: React.MouseEvent | React.TouchEvent, isStart: boolean) => {
    if (room?.currentTask?.type !== 'DRAWING' || !canvasRef.current) return;
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const rect = canvas.getBoundingClientRect();
    const x = ('touches' in e) ? e.touches[0].clientX - rect.left : (e as React.MouseEvent).clientX - rect.left;
    const y = ('touches' in e) ? e.touches[0].clientY - rect.top : (e as React.MouseEvent).clientY - rect.top;

    if (isStart) {
      isDrawing.current = true;
      (canvas as any).lastPos = { x, y };
      return;
    }

    if (!isDrawing.current) return;

    const lastPos = (canvas as any).lastPos;
    const color = player?.color || '#ffffff';

    ctx.strokeStyle = color;
    ctx.lineWidth = 5;
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.beginPath();
    ctx.moveTo(lastPos.x, lastPos.y);
    ctx.lineTo(x, y);
    ctx.stroke();

    connectorRef.current?.send({
      type: 'DRAW_STROKE',
      senderId: player?.id || '',
      payload: { x, y, prevX: lastPos.x, prevY: lastPos.y, color, roomCode: room.code }
    });

    (canvas as any).lastPos = { x, y };
  };

  const stopDrawing = () => { isDrawing.current = false; };

  // --- UI Components ---

  const DrawingBoard = () => (
    <div className="w-full flex flex-col items-center">
      <div className="flex items-center gap-2 text-violet-400 mb-6 font-bungee">
        <Palette size={20} className="animate-bounce" /> DRAW TOGETHER: <span className="text-white ml-2">"{room?.currentTask?.description}"</span>
      </div>
      <div className="relative p-1 rounded-3xl bg-gradient-to-br from-violet-500 via-slate-800 to-pink-500 shadow-2xl">
        <canvas 
          ref={canvasRef}
          width={640}
          height={400}
          onMouseDown={(e) => drawOnCanvas(e, true)}
          onMouseMove={(e) => drawOnCanvas(e, false)}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          onTouchStart={(e) => drawOnCanvas(e, true)}
          onTouchMove={(e) => drawOnCanvas(e, false)}
          onTouchEnd={stopDrawing}
          className="bg-slate-900 rounded-[1.4rem] cursor-crosshair max-w-full touch-none"
        />
        <div className="absolute top-4 right-4 flex gap-2">
           <div className="px-3 py-1 rounded-full bg-slate-950/80 border border-white/10 text-[10px] font-bold flex items-center gap-2">
             <div className="w-2 h-2 rounded-full" style={{ backgroundColor: player?.color }} /> YOUR COLOR
           </div>
        </div>
      </div>
    </div>
  );

  const FastestFinger = () => (
    <div className="w-full text-center space-y-8 animate-in zoom-in-95">
      <Zap className="w-20 h-20 text-amber-400 mx-auto animate-pulse" />
      <div className="text-4xl font-bungee text-white bg-slate-800/80 p-10 rounded-[3rem] border-4 border-slate-700 shadow-inner">
        {room?.currentTask?.description}
      </div>
      <div className="flex flex-col gap-4 max-w-md mx-auto">
        <input 
          autoFocus
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && submitAnswer()}
          placeholder="TYPE HERE FAST!"
          className="w-full bg-slate-950 border-4 border-violet-500/50 p-6 rounded-2xl text-3xl text-center focus:border-violet-500 outline-none transition-all uppercase font-bungee tracking-tighter"
        />
        <button onClick={() => submitAnswer()} className="bg-violet-600 hover:bg-violet-500 py-6 rounded-2xl font-bungee text-2xl shadow-lg transition-transform active:scale-95">SUBMIT ANSWER</button>
      </div>
    </div>
  );

  const LieDetector = () => (
    <div className="w-full text-center space-y-8">
      <Ghost className="w-20 h-20 text-pink-400 mx-auto" />
      <div>
        <h3 className="text-2xl font-bungee text-slate-500 mb-2 uppercase tracking-widest">Lie Category</h3>
        <div className="text-4xl font-bungee text-white">{room?.currentTask?.description}</div>
      </div>
      <div className="max-w-xl mx-auto space-y-4">
        <textarea 
          autoFocus
          value={answer}
          onChange={(e) => setAnswer(e.target.value)}
          placeholder="Tell a convincing, weird lie..."
          className="w-full bg-slate-800/50 border-2 border-slate-700 p-6 rounded-3xl text-xl focus:border-pink-500 outline-none transition-all h-40 resize-none font-medium"
        />
        <button onClick={() => submitAnswer()} className="w-full bg-pink-600 hover:bg-pink-500 py-6 rounded-2xl font-bungee text-2xl shadow-lg active:scale-95 transition-all">DECEIVE THEM</button>
      </div>
    </div>
  );

  const VotingMode = () => (
    <div className="w-full text-center space-y-8 animate-in slide-in-from-bottom-8">
      <Vote className="w-20 h-20 text-emerald-400 mx-auto" />
      <div>
        <h3 className="text-2xl font-bungee text-slate-500 mb-2 uppercase tracking-widest">WHO AMONG YOU...</h3>
        <div className="text-4xl font-bungee text-white px-4">{room?.currentTask?.description}</div>
      </div>
      
      {hasVoted ? (
        <div className="bg-slate-800/40 p-12 rounded-[3rem] border-2 border-slate-700/50 animate-pulse">
          <p className="text-3xl font-bungee text-emerald-400">VOTE CAST!</p>
          <p className="text-slate-500 uppercase tracking-widest font-bold mt-2">Waiting for others to decide your fate...</p>
        </div>
      ) : (
        <div className="grid grid-cols-2 md:grid-cols-3 gap-6 max-w-4xl mx-auto">
          {room?.players.map((p) => (
            <button 
              key={p.id}
              onClick={() => submitAnswer(p.name)}
              className="group relative bg-slate-800/50 border-2 border-slate-700 p-6 rounded-[2rem] hover:border-emerald-500 hover:bg-emerald-500/10 transition-all flex flex-col items-center gap-4"
            >
              <div className="text-5xl group-hover:scale-125 transition-transform duration-300">{p.avatar}</div>
              <span className="font-bungee text-xl truncate w-full text-white">{p.name}</span>
            </button>
          ))}
        </div>
      )}
    </div>
  );

  // --- Views ---

  const LandingView = () => (
    <div className="min-h-screen flex flex-col items-center justify-center p-6 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-violet-900 via-slate-950 to-black overflow-hidden">
      <div className="text-center mb-16 animate-float relative">
        <div className="absolute -top-32 -left-32 w-80 h-80 bg-violet-600/20 blur-[120px] rounded-full" />
        <div className="absolute -bottom-32 -right-32 w-80 h-80 bg-pink-600/20 blur-[120px] rounded-full" />
        <h1 className="text-7xl md:text-[10rem] font-bungee mb-4 text-transparent bg-clip-text bg-gradient-to-br from-white via-violet-200 to-violet-700 drop-shadow-[0_10px_30px_rgba(139,92,246,0.3)]">
          CHAOS ROOM
        </h1>
        <p className="text-2xl text-slate-400 max-w-xl mx-auto font-bold tracking-tight opacity-80 uppercase">
          Collaborative Art. Competitive Speed. <br/>
          Infinite Weirdness.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-10 w-full max-w-4xl z-10">
        <button onClick={createRoom} className="group relative p-[2px] rounded-[3rem] bg-gradient-to-tr from-violet-600 via-fuchsia-500 to-pink-500 hover:scale-[1.02] transition-transform duration-300">
          <div className="bg-[#0b1120] rounded-[2.9rem] p-12 flex flex-col items-center border border-white/5 h-full">
            <div className="bg-violet-600/20 p-6 rounded-3xl mb-8 group-hover:rotate-12 transition-transform">
              <Users className="w-16 h-16 text-violet-400" />
            </div>
            <h2 className="text-4xl font-bungee text-white">HOST LOBBY</h2>
            <p className="text-slate-500 text-center font-bold uppercase text-xs tracking-widest mt-4">For you and up to 7 friends</p>
          </div>
        </button>

        <div className="group relative p-[2px] rounded-[3rem] bg-gradient-to-tr from-emerald-500 via-teal-400 to-cyan-500">
          <div className="bg-[#0b1120] rounded-[2.9rem] p-12 flex flex-col items-center border border-white/5">
            <div className="bg-emerald-600/20 p-6 rounded-3xl mb-8">
              <Hash className="w-16 h-16 text-emerald-400" />
            </div>
            <h2 className="text-4xl font-bungee text-white mb-8 tracking-tighter">JOIN PARTY</h2>
            <div className="flex w-full gap-4">
              <input id="jcode" placeholder="CODE" className="w-full bg-slate-900 border-2 border-slate-800 rounded-2xl px-6 py-5 font-bungee text-2xl tracking-[0.3em] focus:border-emerald-500 outline-none transition-all placeholder:opacity-30" />
              <button onClick={() => joinRoom((document.getElementById('jcode') as HTMLInputElement).value.toUpperCase())} className="bg-emerald-500 px-8 rounded-2xl font-black text-slate-950 hover:bg-emerald-400 transition-colors shadow-2xl">GO</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const RoomView = () => (
    <div className="min-h-screen grid grid-cols-1 lg:grid-cols-12 bg-[#020617] text-white">
      {/* Sidebar: Players */}
      <div className="lg:col-span-3 border-r border-white/5 p-8 flex flex-col bg-slate-950/40 backdrop-blur-3xl">
        <div className="flex items-center justify-between mb-12">
          <div>
            <h2 className="text-4xl font-bungee text-white">SQUAD</h2>
            <div className="flex items-center gap-2 mt-2">
              <span className="text-[10px] text-slate-500 font-black uppercase tracking-[0.3em]">Room: {room?.code}</span>
              <button onClick={() => {
                navigator.clipboard.writeText(room?.code || '');
              }} className="text-slate-600 hover:text-violet-400"><Copy size={12} /></button>
            </div>
          </div>
          <div className="bg-white/5 border border-white/10 px-5 py-3 rounded-2xl text-sm font-black text-slate-400">
            {room?.players.length}/8
          </div>
        </div>
        
        <div className="space-y-4 flex-grow overflow-y-auto pr-2 custom-scrollbar">
          {room?.players.map((p) => (
            <div key={p.id} className={`flex items-center gap-5 p-5 rounded-[2rem] border transition-all ${p.id === player?.id ? 'bg-violet-600/10 border-violet-500/50' : 'bg-slate-900/40 border-slate-800/50 hover:border-slate-700'}`}>
              <div className="text-4xl bg-slate-800 w-16 h-16 flex items-center justify-center rounded-[1.4rem] shadow-xl relative overflow-hidden">
                {p.avatar}
                <div className="absolute bottom-0 left-0 w-full h-1" style={{ backgroundColor: (p as any).color }} />
              </div>
              <div className="flex-grow">
                <div className="flex items-center gap-2">
                  <span className="font-extrabold text-xl truncate max-w-[120px]">{p.name}</span>
                  {p.isHost && <Crown className="w-4 h-4 text-amber-400 fill-amber-400" />}
                </div>
                <div className="text-[10px] font-black uppercase tracking-widest flex items-center gap-2 mt-1">
                  {p.isReady ? <span className="text-emerald-400 flex items-center gap-1"><Check size={10} /> READY</span> : <span className="text-slate-600 animate-pulse">WAITING</span>}
                </div>
              </div>
              <div className="text-3xl font-bungee text-white/20">{p.score}</div>
            </div>
          ))}
        </div>

        <button onClick={() => setView('LANDING')} className="mt-8 flex items-center justify-center gap-3 text-slate-600 hover:text-red-500 font-black uppercase text-xs tracking-[0.2em] transition-all py-6 border-t border-white/5">
          <ShieldAlert size={16} /> Abandon Chaos
        </button>
      </div>

      {/* Main Arena */}
      <div className="lg:col-span-6 p-10 flex flex-col relative">
        {room?.status === GameStatus.LOBBY ? (
          <div className="flex-grow flex flex-col items-center justify-center text-center">
            <div className="relative mb-12">
               <div className="absolute inset-0 bg-violet-600 blur-[80px] opacity-20 animate-pulse" />
               <div className="relative bg-slate-900 border border-white/10 p-20 rounded-[5rem] shadow-2xl">
                 <Play className="w-28 h-28 text-violet-500 fill-violet-500" />
               </div>
            </div>
            <h3 className="text-6xl font-bungee mb-4">THE VOID</h3>
            <p className="text-slate-500 text-xl mb-14 max-w-sm font-bold uppercase tracking-tighter opacity-70">Waiting for all conscious entities to synchronize.</p>
            
            <div className="flex flex-col sm:flex-row gap-6 w-full max-w-lg">
              <button onClick={() => {
                connectorRef.current?.send({ type: 'READY_TOGGLE', senderId: player?.id || '', payload: { roomCode: room.code } });
              }} className={`flex-grow py-6 rounded-3xl font-bungee text-3xl transition-all shadow-2xl ${player?.isReady ? 'bg-slate-800 text-slate-600' : 'bg-emerald-500 text-slate-950 hover:scale-105 active:scale-95'}`}>
                {player?.isReady ? 'READY!' : 'PREPARE'}
              </button>
              {player?.isHost && (
                <button onClick={startGame} className="flex-grow py-6 bg-violet-600 text-white rounded-3xl font-bungee text-3xl shadow-2xl hover:bg-violet-500 transition-all hover:scale-105 active:scale-95">
                  UNLEASH
                </button>
              )}
            </div>
          </div>
        ) : (
          <div className="flex-grow flex flex-col h-full z-10">
            <div className="flex items-center justify-between mb-10 bg-slate-900/80 backdrop-blur-xl p-6 rounded-[3rem] border border-white/5 shadow-2xl">
              <div className="flex items-center gap-6">
                <div className="w-16 h-16 rounded-[1.4rem] bg-violet-600 flex items-center justify-center font-bungee text-2xl shadow-lg">
                  {room?.round}
                </div>
                <div>
                   <h4 className="font-bungee text-2xl text-white tracking-tighter">{room?.currentTask?.title}</h4>
                   <p className="text-[10px] font-black text-violet-400 tracking-[0.4em] uppercase opacity-60">{room?.currentTask?.type} MODE</p>
                </div>
              </div>
              <div className={`flex items-center gap-4 text-5xl font-bungee ${timer < 5 ? 'text-red-500 animate-ping' : 'text-amber-500'}`}>
                <Timer size={40} /> {timer}s
              </div>
            </div>

            <div className="flex-grow bg-slate-900/30 backdrop-blur-sm border-2 border-white/5 rounded-[4rem] p-12 flex items-center justify-center relative shadow-inner overflow-hidden">
              <div className="w-full h-full flex flex-col items-center justify-center">
                {room?.currentTask?.type === 'DRAWING' && <DrawingBoard />}
                {room?.currentTask?.type === 'FASTEST_FINGER' && <FastestFinger />}
                {room?.currentTask?.type === 'LIE_DETECTOR' && <LieDetector />}
                {room?.currentTask?.type === 'VOTE' && <VotingMode />}
              </div>

              {showResults && (
                <div className="absolute inset-0 bg-[#020617]/98 backdrop-blur-2xl flex flex-col items-center justify-center p-12 z-50 text-center animate-in zoom-in-95 duration-700 rounded-[4rem]">
                  <div className="relative group">
                    <Trophy className="w-48 h-48 text-yellow-400 mb-10 drop-shadow-[0_0_60px_rgba(250,204,21,0.4)] group-hover:scale-110 transition-transform duration-500" />
                    <div className="absolute -top-4 -right-4 bg-gradient-to-r from-red-500 to-pink-500 text-white px-6 py-2 rounded-full font-bungee text-2xl rotate-12 shadow-xl">+10 PTS</div>
                  </div>
                  <h3 className="text-8xl font-bungee text-white mb-4 tracking-tighter uppercase">{winnerInfo?.winner}</h3>
                  <div className="h-1 w-20 bg-violet-600 mb-8 rounded-full" />
                  <p className="text-3xl text-slate-400 font-bold mb-16 max-w-2xl italic leading-relaxed">"{winnerInfo?.reason}"</p>
                  <button onClick={() => {
                    setShowResults(false);
                    if (player?.isHost) startGame();
                  }} className="px-20 py-8 bg-gradient-to-r from-violet-600 via-fuchsia-600 to-pink-600 rounded-[2.5rem] font-bungee text-4xl shadow-2xl hover:scale-105 transition-transform active:scale-95 text-white">
                    {player?.isHost ? 'NEXT ROUND' : 'WAITING...'}
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Chat Sidebar */}
      <div className="lg:col-span-3 border-l border-white/5 flex flex-col h-full bg-slate-950/20">
        <div className="p-10 border-b border-white/5 flex items-center gap-4">
          <MessageSquare className="text-violet-500 w-6 h-6" />
          <h3 className="font-bungee text-lg tracking-widest text-slate-500 uppercase">Trash Talk</h3>
        </div>
        
        <div className="flex-grow p-8 space-y-6 overflow-y-auto custom-scrollbar">
          {chat.map((msg, i) => (
            <div key={i} className={`flex flex-col ${msg.sender === player?.name ? 'items-end' : 'items-start'} animate-in slide-in-from-bottom-4 duration-300`}>
              <span className="text-[10px] font-black text-slate-600 mb-2 uppercase tracking-[0.2em]">{msg.sender}</span>
              <div className={`px-6 py-4 rounded-[1.8rem] text-sm font-bold leading-relaxed max-w-[95%] shadow-2xl border ${
                msg.sender === player?.name 
                  ? 'bg-violet-600 text-white rounded-tr-none border-white/10' 
                  : 'bg-slate-900 text-slate-200 rounded-tl-none border-white/5'
              }`}>
                {msg.text}
              </div>
            </div>
          ))}
        </div>

        <form onSubmit={(e) => {
          e.preventDefault();
          const input = e.currentTarget.elements.namedItem('chat') as HTMLInputElement;
          if (input.value.trim()) {
            connectorRef.current?.send({ type: 'CHAT_MESSAGE', senderId: player?.id || '', payload: { senderName: player?.name, text: input.value, roomCode: room?.code } });
            input.value = '';
          }
        }} className="p-10 border-t border-white/5 bg-slate-950/50">
          <div className="relative group">
            <input name="chat" autoComplete="off" placeholder="Roast them..." className="w-full bg-slate-900/80 border-2 border-slate-800 rounded-2xl px-8 py-5 pr-16 text-sm font-bold focus:outline-none focus:border-violet-500 transition-all placeholder:text-slate-700" />
            <button type="submit" className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-500 group-focus-within:text-violet-400 p-3 hover:bg-violet-500/10 rounded-xl transition-all">
              <Send size={24} />
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  return (
    <div className="selection:bg-violet-500 selection:text-white">
      {view === 'LANDING' ? <LandingView /> : <RoomView />}
    </div>
  );
};

export default App;
