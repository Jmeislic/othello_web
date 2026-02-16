from flask import Flask, render_template, request, jsonify
import just_for_testing as main
import random
import time
from computer import playcom
from policy import OthelloPolicy
from average_find_winner import get_win_chance_percentage
import os
import copy

app = Flask(__name__)

class GameManager:
    def __init__(self):
        self.ai_model = OthelloPolicy("final")
        self.board = main.init_board()
        self.turn = "black"
        self.player_types = {"black": "human", "white": "human"}
        # History stores (board, win_pct)
        initial_win_pct = get_win_chance_percentage(self.board)
        self.history = [(copy.deepcopy(self.board), initial_win_pct)]
        self.current_index = 0
        self.game_over = False

    def reset(self, black="human", white="human"):
        self.board = main.init_board()
        self.turn = "black"
        self.player_types = {"black": black, "white": white}
        initial_win_pct = get_win_chance_percentage(self.board)
        print(f"initial win {initial_win_pct}")
        self.history = [(copy.deepcopy(self.board), initial_win_pct)]
        self.current_index = 0
        self.game_over = False

    def legal_moves(self, color):
        moves_dict = main.findpossiblemoves(self.current_index, self.board, color)
        return list(moves_dict.keys()) if moves_dict else []

    def make_move(self, row=None, col=None):
        if self.game_over:
            return False
        
        color = self.turn
        move_made = False
        moves = self.legal_moves(color)

        if self.player_types[color] == "human":
            if row is not None and col is not None and (row, col) in moves:
                self.board = main.flip((row, col), 0, self.board, color)
                move_made = True
        elif self.player_types[color] == "random" and moves:
            c = random.choice(moves)
            self.board = main.flip(c, 0, self.board, color)
            move_made = True
        elif self.player_types[color] == "computer":
            move = playcom(self.current_index, self.board, color)
            if move:
                self.board = main.flip(move, self.current_index, self.board, color)
                move_made = True
        elif self.player_types[color] == "ai":
            move = self.ai_model.predict_move(self.board, 0, color)
            if move:
                self.board = main.flip(move, 0, self.board, color)
                move_made = True

        if move_made:
            win_pct = get_win_chance_percentage(self.board)
            self.history = self.history[:self.current_index + 1]
            self.history.append((copy.deepcopy(self.board), win_pct))
            self.current_index += 1
            self.turn = "white" if self.turn == "black" else "black"
            
            # Check if next player has moves
            if not self.legal_moves(self.turn):
                self.turn = "white" if self.turn == "black" else "black"
                if not self.legal_moves(self.turn):
                    self.game_over = True
        return move_made

    def get_current_state(self):
        board, win_pct = self.history[self.current_index]
        return board, win_pct

    def navigate(self, direction):
        if direction == "back" and self.current_index > 0:
            self.current_index -= 1
        elif direction == "forward" and self.current_index < len(self.history) - 1:
            self.current_index += 1
        board, win_pct = self.history[self.current_index]
        self.board = copy.deepcopy(board)
        return board, win_pct

game_manager = GameManager()

def get_json_board(board_dict):
    return {f"{k[0]},{k[1]}": v for k, v in board_dict.items()}

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()
    game_manager.reset(data.get("blackPlayer", "human"), data.get("whitePlayer", "human"))
    board, win_pct = game_manager.get_current_state()
    return jsonify({
        "board": get_json_board(board),
        "win_pct": win_pct,
        "turn": game_manager.turn,
        "nextPlayerType": game_manager.player_types[game_manager.turn],
        "end": False
    })

@app.route("/human_move", methods=["POST"])
def human_move():
    data = request.get_json()
    move_ok = game_manager.make_move(data["row"], data["col"])
    board, win_pct = game_manager.get_current_state()
    return jsonify({
        "board": get_json_board(board),
        "win_pct": win_pct,
        "ok": move_ok,
        "end": game_manager.game_over,
        "turn": game_manager.turn,
        "nextPlayerType": game_manager.player_types[game_manager.turn]
    })

@app.route("/navigate", methods=["POST"])
def navigate():
    data = request.get_json()
    board, win_pct = game_manager.navigate(data["direction"])
    return jsonify({
        "board": get_json_board(board),
        "win_pct": win_pct,
        "turn": game_manager.turn
    })

@app.route("/step", methods=["POST"])
def step():
    gm = game_manager
    if not gm.game_over:
        color = gm.turn
        if gm.player_types[color] != "human":
            gm.make_move()
        elif not gm.legal_moves(color):
            gm.turn = "white" if gm.turn == "black" else "black"
    
    board, win_pct = gm.get_current_state()
    return jsonify({
        "board": get_json_board(board),
        "win_pct": win_pct,
        "end": gm.game_over,
        "turn": gm.turn,
        "nextPlayerType": gm.player_types[gm.turn]
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)