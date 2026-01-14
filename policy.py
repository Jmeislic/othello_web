import numpy as np
from stable_baselines3 import PPO
import just_for_testing as main


import numpy as np
import pickle

def relu(x):
    return np.maximum(0, x)

class OthelloPolicy:
    def __init__(self, path):
        with open(path, "rb") as f:
            self.w = pickle.load(f)

    def predict_move(self, board, player_index, color):
        obs = self.board_to_obs(board, color)

        x = obs
        x = relu(
            x @ self.w["mlp_extractor.policy_net.0.weight"].T +
            self.w["mlp_extractor.policy_net.0.bias"]
        )
        x = x @ self.w["action_net.weight"].T + self.w["action_net.bias"]

        action = int(np.argmax(x))
        return divmod(action, 8)

    def board_to_obs(self, board, color):
        obs = np.zeros((64,), dtype=np.float32)
        for key, v in board.items():
            r, c = map(int, key.split(","))
            idx = r * 8 + c
            if v == color:
                obs[idx] = 1
            elif v is not None:
                obs[idx] = -1
        return obs

    # ----------------------------
    # Board conversion
    # ----------------------------
    def dic_to_tensor(self, dic, color: str):
        """
        Convert board dict to (8,8) tensor.
        Positive = current player's pieces, negative = opponent.
        """
        board = np.zeros((8, 8), dtype=np.int8)

        for k, v in dic.items():
            r, c = map(int, k.split(","))
            if v == color:
                board[r, c] = 1
            else:
                board[r, c] = -1

        return board

    # ----------------------------
    # Legal move mask
    # ----------------------------
    def legal_mask(self, dic, move_number, color: str):
        """
        Returns boolean mask of size 64. True = legal move for `color`.
        """
        mask = np.zeros(64, dtype=bool)

        for r in range(8):
            for c in range(8):
                coord = f"{r},{c}"
                if main.checkpiecenosorry(coord, move_number, dic, color):
                    mask[r * 8 + c] = True

        return mask

