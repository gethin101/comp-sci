#!/usr/bin/env python3
"""
Fully Functional Multiplayer Blackjack Server
A complete multiplayer blackjack game server with WebSocket support
Run this file to start the server and connect via http://localhost:8000
"""

import asyncio
import json
import random
import secrets
from dataclasses import dataclass
from typing import Dict, Optional, List

try:
    from aiohttp import web
except ImportError:
    print("Installing aiohttp...")
    import subprocess
    subprocess.check_call(["pip", "install", "aiohttp"])
    from aiohttp import web


# ==================== Card Game Logic ====================

@dataclass
class Card:
    suit: str
    rank: str
    
    def value(self) -> int:
        if self.rank in ['J', 'Q', 'K']:
            return 10
        elif self.rank == 'A':
            return 11
        else:
            return int(self.rank)
    
    def to_dict(self):
        return {'suit': self.suit, 'rank': self.rank}


class Deck:
    def __init__(self):
        self.cards: List[Card] = []
        self.reset()
    
    def reset(self):
        suits = ['♠', '♥', '♦', '♣']
        ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
        self.cards = [Card(suit, rank) for suit in suits for rank in ranks]
        random.shuffle(self.cards)
    
    def draw(self) -> Card:
        if len(self.cards) < 10:
            self.reset()
        return self.cards.pop()
    
    def draw_multiple(self, count: int) -> List[Card]:
        return [self.draw() for _ in range(count)]


class Hand:
    def __init__(self, cards: List[Card] = None):
        self.cards = cards or []
    
    def add_card(self, card: Card):
        self.cards.append(card)
    
    def value(self) -> int:
        total = 0
        aces = 0
        for card in self.cards:
            if card.rank == 'A':
                aces += 1
                total += 11
            else:
                total += card.value()
        
        while total > 21 and aces > 0:
            total -= 10
            aces -= 1
        return total
    
    def is_blackjack(self) -> bool:
        return len(self.cards) == 2 and self.value() == 21
    
    def is_bust(self) -> bool:
        return self.value() > 21
    
    def to_dict(self, show_all: bool = True):
        if show_all:
            return {
                'cards': [card.to_dict() for card in self.cards],
                'value': self.value()
            }
        else:
            return {
                'cards': [self.cards[0].to_dict()] if self.cards else [],
                'value': self.cards[0].value() if self.cards else 0
            }


# ==================== Player Management ====================

@dataclass
class Player:
    player_id: str
    username: str
    websocket: web.WebSocketResponse
    hand: Hand
    bet: int = 0
    is_dealer: bool = False
    is_busted: bool = False
    is_standing: bool = False
    result: Optional[str] = None
    balance: int = 1000
    
    def to_dict(self, show_hand: bool = True):
        return {
            'player_id': self.player_id,
            'username': self.username,
            'hand': self.hand.to_dict(show_hand),
            'bet': self.bet,
            'is_dealer': self.is_dealer,
            'is_busted': self.is_busted,
            'is_standing': self.is_standing,
            'result': self.result,
            'balance': self.balance
        }


# ==================== Game Room ====================

class GameRoom:
    def __init__(self, room_id: str):
        self.room_id = room_id
        self.players: Dict[str, Player] = {}
        self.deck = Deck()
        self.game_phase = 'waiting'  # waiting, betting, playing, dealer_turn, results
        self.round_number = 0
        self.betting_timer = 0
        self.dealer_player: Optional[Player] = None
    
    def add_player(self, player: Player):
        self.players[player.player_id] = player
        if len(self.players) == 1:
            player.is_dealer = True
            self.dealer_player = player
    
    def remove_player(self, player_id: str):
        if player_id in self.players:
            del self.players[player_id]
    
    def reset_hands(self):
        for player in self.players.values():
            player.hand = Hand()
            player.is_busted = False
            player.is_standing = False
            player.result = None
            player.bet = 0
    
    def get_active_players(self) -> List[Player]:
        return [p for p in self.players.values() if not p.is_dealer]
    
    def get_all_players_ready(self) -> bool:
        for player in self.get_active_players():
            if player.bet == 0:
                return False
        return len(self.get_active_players()) > 0
    
    def get_all_players_done(self) -> bool:
        for player in self.get_active_players():
            if not player.is_busted and not player.is_standing:
                return False
        return True
    
    def to_dict(self, include_dealer_hand: bool = False):
        players_dict = []
        for player in self.players.values():
            if player.is_dealer:
                show_hand = include_dealer_hand
            else:
                show_hand = True
            players_dict.append(player.to_dict(show_hand))
        
        return {
            'room_id': self.room_id,
            'game_phase': self.game_phase,
            'round_number': self.round_number,
            'players': players_dict
        }


# ==================== Game Server ====================

class BlackjackServer:
    def __init__(self):
        self.rooms: Dict[str, GameRoom] = {}
        self.player_rooms: Dict[str, str] = {}
        self.player_sockets: Dict[str, web.WebSocketResponse] = {}
    
    async def register_player(self, websocket: web.WebSocketResponse, player_id: str, username: str, room_id: Optional[str] = None) -> str:
        """Register a player and assign them to a room"""
        if room_id is None:
            room_id = secrets.token_hex(4)
            self.rooms[room_id] = GameRoom(room_id)
        
        if room_id not in self.rooms:
            self.rooms[room_id] = GameRoom(room_id)
        
        room = self.rooms[room_id]
        player = Player(
            player_id=player_id,
            username=username,
            websocket=websocket,
            hand=Hand()
        )
        
        room.add_player(player)
        self.player_rooms[player_id] = room_id
        self.player_sockets[player_id] = websocket
        
        if room.game_phase == 'waiting':
            room.game_phase = 'betting'
            await self.start_new_round(room_id)
        
        await self.broadcast_to_room(room_id, {
            'type': 'player_joined',
            'message': f'{username} joined the game',
            'game_state': room.to_dict()
        })
        
        return room_id
    
    async def unregister_player(self, player_id: str):
        """Remove a player from the game"""
        if player_id in self.player_rooms:
            room_id = self.player_rooms[player_id]
            room = self.rooms[room_id]
            
            if player_id in room.players:
                username = room.players[player_id].username
                room.remove_player(player_id)
                
                await self.broadcast_to_room(room_id, {
                    'type': 'player_left',
                    'message': f'{username} left the game',
                    'game_state': room.to_dict()
                })
                
                if len(room.players) == 0:
                    del self.rooms[room_id]
            
            del self.player_rooms[player_id]
        
        if player_id in self.player_sockets:
            del self.player_sockets[player_id]
    
    async def broadcast_to_room(self, room_id: str, message: dict):
        """Send message to all players in a room"""
        if room_id not in self.rooms:
            return
        
        room = self.rooms[room_id]
        message_str = json.dumps(message)
        
        dead_sockets = []
        for player in room.players.values():
            try:
                await player.websocket.send_str(message_str)
            except:
                dead_sockets.append(player.player_id)
        
        for player_id in dead_sockets:
            await self.unregister_player(player_id)
    
    async def start_new_round(self, room_id: str):
        """Start a new round of blackjack"""
        room = self.rooms[room_id]
        room.reset_hands()
        room.round_number += 1
        room.game_phase = 'betting'
        
        await self.broadcast_to_room(room_id, {
            'type': 'round_started',
            'message': 'New round starting! Place your bets.',
            'game_state': room.to_dict()
        })
    
    async def place_bet(self, room_id: str, player_id: str, amount: int):
        """Place a bet for a player"""
        if room_id not in self.rooms or player_id not in self.rooms[room_id].players:
            return
        
        room = self.rooms[room_id]
        player = room.players[player_id]
        
        if player.balance >= amount and amount > 0:
            player.bet = amount
            player.balance -= amount
            
            await self.broadcast_to_room(room_id, {
                'type': 'bet_placed',
                'message': f'{player.username} bet ${amount}',
                'game_state': room.to_dict()
            })
            
            if room.get_all_players_ready():
                await self.deal_initial_hands(room_id)
    
    async def deal_initial_hands(self, room_id: str):
        """Deal initial hands to all players"""
        room = self.rooms[room_id]
        room.game_phase = 'playing'
        
        for player in room.players.values():
            for _ in range(2):
                player.hand.add_card(room.deck.draw())
        
        await self.broadcast_to_room(room_id, {
            'type': 'hands_dealt',
            'message': 'Cards dealt!',
            'game_state': room.to_dict()
        })
        
        for player in room.get_active_players():
            if player.hand.is_blackjack():
                player.is_standing = True
                await self.broadcast_to_room(room_id, {
                    'type': 'blackjack',
                    'message': f'{player.username} has blackjack!',
                    'player_id': player.player_id
                })
        
        if room.get_all_players_done():
            await self.dealer_turn(room_id)
    
    async def hit(self, room_id: str, player_id: str):
        """Player hits (draws another card)"""
        if room_id not in self.rooms or player_id not in self.rooms[room_id].players:
            return
        
        room = self.rooms[room_id]
        player = room.players[player_id]
        
        if room.game_phase != 'playing' or player.is_standing or player.is_busted:
            return
        
        player.hand.add_card(room.deck.draw())
        
        await self.broadcast_to_room(room_id, {
            'type': 'player_hit',
            'message': f'{player.username} hit',
            'player_id': player_id,
            'game_state': room.to_dict()
        })
        
        if player.hand.is_bust():
            player.is_busted = True
            await self.broadcast_to_room(room_id, {
                'type': 'player_bust',
                'message': f'{player.username} busted!',
                'player_id': player_id
            })
        
        if room.get_all_players_done():
            await self.dealer_turn(room_id)
    
    async def stand(self, room_id: str, player_id: str):
        """Player stands"""
        if room_id not in self.rooms or player_id not in self.rooms[room_id].players:
            return
        
        room = self.rooms[room_id]
        player = room.players[player_id]
        
        if room.game_phase != 'playing' or player.is_standing or player.is_busted:
            return
        
        player.is_standing = True
        
        await self.broadcast_to_room(room_id, {
            'type': 'player_stand',
            'message': f'{player.username} stands',
            'player_id': player_id,
            'game_state': room.to_dict()
        })
        
        if room.get_all_players_done():
            await self.dealer_turn(room_id)
    
    async def dealer_turn(self, room_id: str):
        """Dealer plays their hand"""
        room = self.rooms[room_id]
        room.game_phase = 'dealer_turn'
        
        await self.broadcast_to_room(room_id, {
            'type': 'dealer_turn',
            'message': "Dealer's turn...",
            'game_state': room.to_dict(include_dealer_hand=True)
        })
        
        await asyncio.sleep(1)
        
        dealer = room.dealer_player
        while dealer.hand.value() < 17:
            dealer.hand.add_card(room.deck.draw())
            await self.broadcast_to_room(room_id, {
                'type': 'dealer_hit',
                'message': f'Dealer hit (value: {dealer.hand.value()})',
                'game_state': room.to_dict(include_dealer_hand=True)
            })
            await asyncio.sleep(0.5)
        
        if dealer.hand.is_bust():
            await self.broadcast_to_room(room_id, {
                'type': 'dealer_bust',
                'message': 'Dealer busted!',
                'game_state': room.to_dict(include_dealer_hand=True)
            })
        
        await self.determine_results(room_id)
    
    async def determine_results(self, room_id: str):
        """Determine winner and update balances"""
        room = self.rooms[room_id]
        room.game_phase = 'results'
        
        dealer = room.dealer_player
        dealer_value = dealer.hand.value()
        dealer_bust = dealer.hand.is_bust()
        
        for player in room.get_active_players():
            if player.is_busted:
                player.result = 'lost'
            elif dealer_bust:
                player.result = 'won'
                winnings = int(player.bet * 2.5) if player.hand.is_blackjack() else int(player.bet * 2)
                player.balance += winnings
            elif player.hand.value() > dealer_value:
                player.result = 'won'
                winnings = int(player.bet * 2.5) if player.hand.is_blackjack() else int(player.bet * 2)
                player.balance += winnings
            elif player.hand.value() == dealer_value:
                player.result = 'push'
                player.balance += player.bet
            else:
                player.result = 'lost'
        
        await self.broadcast_to_room(room_id, {
            'type': 'round_results',
            'message': 'Round over!',
            'game_state': room.to_dict(include_dealer_hand=True)
        })
        
        await asyncio.sleep(3)
        await self.start_new_round(room_id)


# ==================== HTTP Server ====================

def get_html_client() -> str:
    """Return the complete HTML/JavaScript client"""
    return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Multiplayer Blackjack</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            padding: 20px;
        }
        
        .container {
            width: 100%;
            max-width: 1200px;
            background: rgba(0, 0, 0, 0.7);
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
            color: #fff;
        }
        
        .header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #4CAF50;
            padding-bottom: 20px;
        }
        
        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            background: linear-gradient(45deg, #4CAF50, #45a049);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        
        .join-section {
            display: none;
            text-align: center;
            padding: 30px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            margin-bottom: 20px;
        }
        
        .join-section.active {
            display: block;
        }
        
        .join-section input {
            padding: 12px;
            margin: 10px;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            width: 200px;
        }
        
        .join-section button {
            padding: 12px 30px;
            margin: 10px;
            background: #4CAF50;
            color: white;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            cursor: pointer;
            transition: background 0.3s;
        }
        
        .join-section button:hover {
            background: #45a049;
        }
        
        .game-section {
            display: none;
        }
        
        .game-section.active {
            display: block;
        }
        
        .info-bar {
            display: flex;
            justify-content: space-between;
            margin-bottom: 20px;
            padding: 15px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 5px;
        }
        
        .info-item {
            text-align: center;
        }
        
        .info-label {
            font-size: 0.8em;
            color: #aaa;
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.5em;
            color: #4CAF50;
            font-weight: bold;
        }
        
        .players-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .player-card {
            background: rgba(255, 255, 255, 0.1);
            border: 2px solid rgba(255, 255, 255, 0.2);
            border-radius: 10px;
            padding: 20px;
            transition: all 0.3s;
        }
        
        .player-card.dealer {
            border-color: #FFD700;
            background: rgba(255, 215, 0, 0.1);
        }
        
        .player-card.active {
            border-color: #4CAF50;
            background: rgba(76, 175, 80, 0.1);
        }
        
        .player-name {
            font-size: 1.2em;
            font-weight: bold;
            margin-bottom: 10px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .dealer-badge {
            background: #FFD700;
            color: #000;
            padding: 3px 8px;
            border-radius: 3px;
            font-size: 0.7em;
            font-weight: bold;
        }
        
        .hand {
            margin: 15px 0;
            padding: 15px;
            background: rgba(0, 0, 0, 0.3);
            border-radius: 8px;
        }
        
        .cards {
            display: flex;
            gap: 10px;
            flex-wrap: wrap;
            margin-bottom: 10px;
            justify-content: center;
        }
        
        .card {
            background: white;
            color: #000;
            width: 60px;
            height: 90px;
            border-radius: 5px;
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            font-weight: bold;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
            font-size: 1.2em;
            padding: 5px;
            text-align: center;
        }
        
        .card.red {
            color: #e74c3c;
        }
        
        .card.black {
            color: #000;
        }
        
        .hand-value {
            text-align: center;
            font-size: 1.1em;
            color: #4CAF50;
            font-weight: bold;
        }
        
        .player-status {
            text-align: center;
            margin-top: 10px;
            font-size: 0.9em;
        }
        
        .status-busted {
            color: #e74c3c;
        }
        
        .status-standing {
            color: #2196F3;
        }
        
        .status-won {
            color: #4CAF50;
        }
        
        .status-lost {
            color: #e74c3c;
        }
        
        .status-push {
            color: #FFC107;
        }
        
        .player-balance {
            margin-top: 10px;
            font-size: 0.9em;
            color: #FFD700;
        }
        
        .betting-section {
            display: none;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            text-align: center;
        }
        
        .betting-section.active {
            display: block;
        }
        
        .bet-input {
            width: 100px;
            padding: 10px;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            margin-right: 10px;
        }
        
        .btn-group {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .btn {
            padding: 12px 25px;
            border: none;
            border-radius: 5px;
            font-size: 1em;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .btn-primary {
            background: #4CAF50;
            color: white;
        }
        
        .btn-primary:hover {
            background: #45a049;
            transform: scale(1.05);
        }
        
        .btn-secondary {
            background: #2196F3;
            color: white;
        }
        
        .btn-secondary:hover {
            background: #0b7dda;
            transform: scale(1.05);
        }
        
        .btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        
        .message {
            background: rgba(255, 255, 255, 0.1);
            border-left: 4px solid #4CAF50;
            padding: 15px;
            margin-bottom: 20px;
            border-radius: 5px;
            text-align: center;
            font-size: 1.1em;
        }
        
        .quick-bet-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        
        .quick-bet {
            padding: 8px 15px;
            background: rgba(76, 175, 80, 0.3);
            color: #4CAF50;
            border: 2px solid #4CAF50;
            border-radius: 5px;
            cursor: pointer;
            transition: all 0.3s;
            font-weight: bold;
        }
        
        .quick-bet:hover {
            background: #4CAF50;
            color: white;
        }
        
        .action-buttons {
            display: none;
            justify-content: center;
            gap: 15px;
            margin-top: 20px;
        }
        
        .action-buttons.active {
            display: flex;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .header h1 {
                font-size: 1.8em;
            }
            
            .players-section {
                grid-template-columns: 1fr;
            }
            
            .card {
                width: 50px;
                height: 75px;
                font-size: 1em;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎰 Multiplayer Blackjack</h1>
            <p id="connection-status">Connecting...</p>
        </div>
        
        <div id="join-section" class="join-section active">
            <h2>Welcome to Blackjack</h2>
            <div style="margin: 20px 0;">
                <input type="text" id="username" placeholder="Enter your name" value="">
                <input type="text" id="room-id" placeholder="Room ID (optional)" value="">
            </div>
            <div class="btn-group">
                <button class="btn btn-primary" onclick="joinGame()">Join Game</button>
            </div>
            <p style="margin-top: 15px; color: #aaa; font-size: 0.9em;">Leave room ID empty to create a new room or enter one to join existing</p>
        </div>
        
        <div id="game-section" class="game-section">
            <div class="info-bar">
                <div class="info-item">
                    <div class="info-label">Round</div>
                    <div class="info-value" id="round-number">1</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Your Balance</div>
                    <div class="info-value" id="your-balance">1000</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Phase</div>
                    <div class="info-value" id="game-phase">Waiting</div>
                </div>
                <div class="info-item">
                    <div class="info-label">Room</div>
                    <div class="info-value" id="room-display">N/A</div>
                </div>
            </div>
            
            <div id="message" class="message" style="display: none;"></div>
            
            <div id="betting-section" class="betting-section">
                <h3>Place Your Bet</h3>
                <div style="margin: 20px 0;">
                    <input type="number" id="bet-amount" class="bet-input" placeholder="Bet amount" min="1" max="1000" value="10">
                    <button class="btn btn-primary" onclick="placeBet()">Place Bet</button>
                </div>
                <div class="quick-bet-buttons">
                    <button class="quick-bet" onclick="quickBet(10)">$10</button>
                    <button class="quick-bet" onclick="quickBet(25)">$25</button>
                    <button class="quick-bet" onclick="quickBet(50)">$50</button>
                    <button class="quick-bet" onclick="quickBet(100)">$100</button>
                </div>
            </div>
            
            <div class="players-section" id="players-section"></div>
            
            <div id="action-buttons" class="action-buttons">
                <button class="btn btn-secondary" onclick="hitAction()">Hit</button>
                <button class="btn btn-secondary" onclick="standAction()">Stand</button>
            </div>
        </div>
    </div>
    
    <script>
        let ws = null;
        let playerId = null;
        let roomId = null;
        let gameState = null;
        let currentPhase = 'waiting';
        let isDealer = false;
        
        function connect() {
            const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
            const wsUrl = `${protocol}//${window.location.host}/ws`;
            
            ws = new WebSocket(wsUrl);
            
            ws.onopen = function() {
                updateConnectionStatus('Connected');
                console.log('WebSocket connected');
            };
            
            ws.onmessage = function(event) {
                try {
                    const data = JSON.parse(event.data);
                    handleMessage(data);
                } catch (e) {
                    console.error('Failed to parse message:', e);
                }
            };
            
            ws.onclose = function() {
                updateConnectionStatus('Disconnected - Reconnecting...');
                setTimeout(connect, 3000);
            };
            
            ws.onerror = function(error) {
                updateConnectionStatus('Error: Connection failed');
                console.error('WebSocket error:', error);
            };
        }
        
        function updateConnectionStatus(status) {
            const element = document.getElementById('connection-status');
            element.textContent = '🔴 ' + status;
            if (status === 'Connected') {
                element.style.color = '#4CAF50';
                element.textContent = '🟢 Connected';
            }
        }
        
        function joinGame() {
            const username = document.getElementById('username').value || 'Player_' + Math.random().toString(36).substr(2, 4);
            const room = document.getElementById('room-id').value || null;
            
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    action: 'join',
                    username: username,
                    room_id: room
                }));
            } else {
                alert('Not connected to server');
            }
        }
        
        function placeBet() {
            const amount = parseInt(document.getElementById('bet-amount').value);
            if (amount > 0 && ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    action: 'bet',
                    amount: amount
                }));
            }
        }
        
        function quickBet(amount) {
            document.getElementById('bet-amount').value = amount;
            placeBet();
        }
        
        function hitAction() {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    action: 'hit'
                }));
            }
        }
        
        function standAction() {
            if (ws && ws.readyState === WebSocket.OPEN) {
                ws.send(JSON.stringify({
                    action: 'stand'
                }));
            }
        }
        
        function handleMessage(data) {
            if (data.type === 'joined') {
                playerId = data.player_id;
                roomId = data.room_id;
                document.getElementById('join-section').classList.remove('active');
                document.getElementById('game-section').classList.add('active');
                document.getElementById('room-display').textContent = roomId.substring(0, 8);
                updateGameState(data.game_state);
            } else if (data.game_state) {
                updateGameState(data.game_state);
            }
            
            if (data.type === 'player_joined' || data.type === 'player_left') {
                showMessage(data.message);
            } else if (data.type === 'bet_placed') {
                showMessage(data.message);
            } else if (data.type === 'hands_dealt') {
                showMessage(data.message);
            } else if (data.type === 'player_hit') {
                showMessage(data.message);
            } else if (data.type === 'player_stand') {
                showMessage(data.message);
            } else if (data.type === 'player_bust') {
                showMessage('🔥 ' + data.message);
            } else if (data.type === 'dealer_bust') {
                showMessage('💥 ' + data.message);
            } else if (data.type === 'dealer_turn') {
                showMessage(data.message);
            } else if (data.type === 'round_results') {
                showMessage(data.message);
            } else if (data.type === 'blackjack') {
                showMessage('✨ ' + data.message);
            }
        }
        
        function updateGameState(state) {
            gameState = state;
            currentPhase = state.game_phase;
            
            document.getElementById('round-number').textContent = state.round_number;
            document.getElementById('game-phase').textContent = capitalizeFirst(state.game_phase);
            
            updatePlayersDisplay(state.players);
            updateCurrentPlayer(state.players);
            updateBettingSection(state.game_phase);
            updateActionButtons(state.players);
        }
        
        function updatePlayersDisplay(players) {
            const container = document.getElementById('players-section');
            container.innerHTML = '';
            
            for (const player of players) {
                const card = createPlayerCard(player);
                container.appendChild(card);
            }
        }
        
        function createPlayerCard(player) {
            const card = document.createElement('div');
            card.className = 'player-card';
            
            if (player.is_dealer) {
                card.classList.add('dealer');
            } else if (player.player_id === playerId) {
                card.classList.add('active');
            }
            
            let html = '<div class="player-name">';
            html += player.username;
            if (player.is_dealer) {
                html += '<span class="dealer-badge">DEALER</span>';
            }
            html += '</div>';
            
            if (!player.is_dealer || currentPhase === 'results' || currentPhase === 'dealer_turn') {
                html += '<div class="hand">';
                html += '<div class="cards">';
                for (const card of player.hand.cards) {
                    const color = (card.suit === '♥' || card.suit === '♦') ? 'red' : 'black';
                    html += `<div class="card ${color}">${card.rank}<br>${card.suit}</div>`;
                }
                html += '</div>';
                html += `<div class="hand-value">Value: ${player.hand.value()}</div>`;
                html += '</div>';
            }
            
            if (player.bet > 0) {
                html += `<div style="text-align: center; color: #FFD700; margin: 10px 0;">Bet: $${player.bet}</div>`;
            }
            
            if (player.is_busted) {
                html += '<div class="player-status status-busted">BUSTED</div>';
            } else if (player.is_standing && player.player_id !== playerId) {
                html += '<div class="player-status status-standing">STANDING</div>';
            }
            
            if (player.result) {
                html += `<div class="player-status status-${player.result}">${player.result.toUpperCase()}</div>`;
            }
            
            if (!player.is_dealer) {
                html += `<div class="player-balance">Balance: $${player.balance}</div>`;
            }
            
            card.innerHTML = html;
            return card;
        }
        
        function updateCurrentPlayer(players) {
            for (const player of players) {
                if (player.player_id === playerId) {
                    document.getElementById('your-balance').textContent = player.balance;
                    isDealer = player.is_dealer;
                    break;
                }
            }
        }
        
        function updateBettingSection(phase) {
            const section = document.getElementById('betting-section');
            if (phase === 'betting' && !isDealer) {
                section.classList.add('active');
            } else {
                section.classList.remove('active');
            }
        }
        
        function updateActionButtons(players) {
            const buttons = document.getElementById('action-buttons');
            for (const player of players) {
                if (player.player_id === playerId && !player.is_dealer && currentPhase === 'playing' && !player.is_busted && !player.is_standing) {
                    buttons.classList.add('active');
                    return;
                }
            }
            buttons.classList.remove('active');
        }
        
        function showMessage(message) {
            const msgDiv = document.getElementById('message');
            msgDiv.textContent = message;
            msgDiv.style.display = 'block';
            setTimeout(() => {
                msgDiv.style.display = 'none';
            }, 5000);
        }
        
        function capitalizeFirst(str) {
            return str.charAt(0).toUpperCase() + str.slice(1);
        }
        
        connect();
    </script>
</body>
</html>"""


async def websocket_handler(request):
    """Handle WebSocket connections"""
    server = request.app['server']
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    player_id = secrets.token_hex(8)
    room_id = None
    
    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    action = data.get('action')
                    
                    if action == 'join':
                        username = data.get('username', f'Player_{player_id[:4]}')
                        room_id = data.get('room_id')
                        room_id = await server.register_player(ws, player_id, username, room_id)
                        
                        await ws.send_str(json.dumps({
                            'type': 'joined',
                            'player_id': player_id,
                            'room_id': room_id,
                            'game_state': server.rooms[room_id].to_dict()
                        }))
                    
                    elif action == 'bet' and room_id:
                        amount = data.get('amount', 0)
                        await server.place_bet(room_id, player_id, amount)
                    
                    elif action == 'hit' and room_id:
                        await server.hit(room_id, player_id)
                    
                    elif action == 'stand' and room_id:
                        await server.stand(room_id, player_id)
                
                except json.JSONDecodeError:
                    pass
            elif msg.type == web.WSMsgType.ERROR:
                break
    
    finally:
        if room_id:
            await server.unregister_player(player_id)
    
    return ws


async def index_handler(request):
    """Serve the HTML client"""
    return web.Response(text=get_html_client(), content_type='text/html')


async def main():
    """Main entry point"""
    server = BlackjackServer()
    
    app = web.Application()
    app['server'] = server
    app.router.add_get('/', index_handler)
    app.router.add_get('/ws', websocket_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, 'localhost', 8000)
    await site.start()
    
    print("""
    ╔═══════════════════════════════════════════════════════╗
    ║     MULTIPLAYER BLACKJACK SERVER STARTED!             ║
    ║                                                       ║
    ║  🎰 Open your browser: http://localhost:8000        ║
    ║                                                       ║
    ║  Share the room ID with other players to join!      ║
    ║                                                       ║
    ║  Press Ctrl+C to stop the server                     ║
    ║                                                       ║
    ╚═══════════════════════════════════════════════════════╝
    """)
    
    await asyncio.Future()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nServer shutted down")
