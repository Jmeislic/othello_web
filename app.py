from flask import Flask, render_template, request, jsonify
import just_for_testing as main
import random
import time
from computer import playcom
from policy import OthelloPolicy
import os


import copy
app = Flask(__name__)
class GameManager:
    def __init__(self):

        self.ai_model = OthelloPolicy("ppo_25000000")  # Model
        self.board = main.init_board()
        self.turn = "black"
        self.player_types = {"black": "human", "white": "human"}
        self.history = [self.board.copy()]
        self.current_index = 0
        self.game_over = False

    def reset(self, black="human", white="human"):
        self.board = main.init_board()
        self.turn = "black"
        self.player_types = {"black": black, "white": white}
        self.history = [copy.deepcopy(self.board)]
        self.current_index = 0
        self.game_over = False

    def legal_moves(self, color):
        moves = []
        for r in range(8):
            for c in range(8):
                if main.checkpiecenosorry(f"{r},{c}", 0, self.board, color):
                    moves.append((r, c))
        return moves

    def make_move(self, row=None, col=None):
        
       
        if self.game_over:
            return False
        if  not main.checkthatthereisamove(self.current_index,self.board,self.turn):
            self.turn = "white" if self.turn == "black" else "black"
            print(f" i do not believe that {self.turn} has a move {self.board}")
        color = self.turn
        move_made = False
        if self.player_types[color] == "human":
            if row is None or col is None:
                return False
            if main.checkpiecenosorry(f"{row},{col}", 0, self.board, color):
                self.board = main.flip(f"{row},{col}", 0, self.board, color)
                move_made = True

        elif self.player_types[color] == "random":
            moves = self.legal_moves(color)
            if moves:
                r, c = random.choice(moves)
                self.board = main.flip(f"{r},{c}", 0, self.board, color)
                move_made = True
        elif self.player_types[color] == "computer":
            weights = {'corner': 968, 'x_square': 445, 'c_square': -49, 'edge_safe': 39, 'edge_bad': 111, 'edge_very_good': 122, 'mobility_i_early': 5, 'mobility_out_early': -2, 'mobility_i_mid': 44, 'mobility_out_mid': 28, 'mobility_i_late': 53, 'opp_mobility': 200, 'stable_edge': 75, 'unstable_edge': -80, 'edge_retake': 280, 'corner_give': 240, 'edge_annoying': 150, 'edge_less_annoying': 50, 'corner_deny': 260}

            move = playcom(self.current_index, self.board, color, weights)

            if move is not None:
                r, c = move
                self.board = main.flip(f"{r},{c}", 0, self.board, color)
                move_made = True


        elif self.player_types[color] == "ai":
            move = self.ai_model.predict_move(self.board, 0, color)
            if move:
                r, c = move
                self.board = main.flip(f"{r},{c}", 0, self.board, color)
                move_made = True

        if move_made:
            self.history = self.history[:self.current_index+1]
            self.history.append(copy.deepcopy(self.board))
            self.current_index += 1

            # Switch turn
            self.turn = "white" if self.turn == "black" else "black"

            # Check game over
            if len(self.board) >= 64 or (not self.legal_moves("black") and not self.legal_moves("white")):
                self.game_over = True

        return move_made

    def go_back(self):
        if self.current_index > 0:
            self.current_index -= 1
            self.board = self.history[self.current_index].copy()
        return self.board

    def go_forward(self):
        if self.current_index < len(self.history)-1:
            self.current_index += 1
            self.board = self.history[self.current_index].copy()
        return self.board


    
game_manager = GameManager()

# ------------------------------
# Flask routes
# ------------------------------

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/start_game", methods=["POST"])
def start_game():
    data = request.get_json()
    black = data.get("blackPlayer", "human")
    white = data.get("whitePlayer", "human")

    game_manager.reset(black, white)

    return jsonify({
        "board": game_manager.board,
        "turn": game_manager.turn,
        "nextPlayerType": game_manager.player_types[game_manager.turn],
        "end": False
        
    })


@app.route("/reset_game", methods=["POST"])
def reset_game():
    game_manager.reset(game_manager.player_types["black"], game_manager.player_types["white"])
    return jsonify({"board": game_manager.board})




@app.route("/human_move", methods=["POST"])
def human_move():
    data = request.get_json()
    row = data["row"]
    col = data["col"]
    move_ok = game_manager.make_move(row, col)

    return jsonify({"board": game_manager.board, "ok": move_ok, "end": game_manager.game_over})

@app.route("/navigate", methods=["POST"])
def navigate():
    data = request.get_json()
    if data["direction"] == "back":
        board = game_manager.go_back()
    else:
        board = game_manager.go_forward()
    return jsonify({"board": board})

@app.route("/step", methods=["POST"])
def step():
    skip_human = False
    gm = game_manager
    post = ""

    def game_over_payload():
        black = sum(v == "black" for v in gm.board.values())
        white = sum(v == "white" for v in gm.board.values())
        diff = black - white

        if diff > 0:
            msg = f"Black wins by {diff} tiles"
        elif diff < 0:
            msg = f"White wins by {-diff} tiles"
        else:
            msg = "It was a tie — that's a bummer"

        return jsonify({
            "post": msg,
            "board": gm.board,
            "end": True,
            "turn": gm.turn,
            "nextPlayerType": None,
            "skip": skip_human
        })

    # ---------- GAME ALREADY OVER ----------
    if gm.game_over:
        return game_over_payload()

    color = gm.turn
    player_type = gm.player_types[color]

    # ---------- HUMAN TURN ----------
    if player_type == "human":
        if not gm.legal_moves(color):  # Check if the human has no valid move
            # Skip the human's turn
            gm.turn = "white" if gm.turn == "black" else "black"
            skip_human = True
        return jsonify({
            "post": "",
            "board": gm.board,
            "end": False,
            "turn": gm.turn,
            "nextPlayerType": player_type,
            "skip": skip_human
        })

    # ---------- COMPUTER MOVE ----------
    moved = gm.make_move(None, None)

    oppcolor = "white" if gm.turn == "black" else "black"
    if gm.legal_moves(oppcolor):
        skip_human = True  # The human doesn't have a valid move, computer will play again

    # ---------- SKIP TURN IF NO MOVE ----------
    if not moved:
        gm.turn = oppcolor

    # ---------- FINAL GAME CHECK ----------
    if not gm.legal_moves("black") and not gm.legal_moves("white"):
        gm.game_over = True
        return game_over_payload()

    # ---------- CONTINUE GAME ----------
    return jsonify({
        "post": "",
        "board": gm.board,
        "end": False,
        "turn": gm.turn,
        "nextPlayerType": gm.player_types[gm.turn],
        "skip": skip_human
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)