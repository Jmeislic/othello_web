import numpy as np
from stable_baselines3 import PPO
import just_for_testing as main


class OthelloPolicy:
    """
    Wrapper around a trained PPO model that can play Othello.
    Can play as black or white. PPO is trained to play black,
    but we can switch perspectives for white by inverting the board.
    """

    def __init__(self, model_path: str):
        self.model = PPO.load(model_path)

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

    # ----------------------------
    # Predict move
    # ----------------------------
    def predict_move(self, dic, move_number, color: str):
        """
        Returns (row, col) for the move or None if no legal moves.
        Handles both black and white by adjusting the board perspective.
        """
        obs = self.dic_to_tensor(dic, color)
        mask = self.legal_mask(dic, move_number, color)

        if not mask.any():
            return None  # no legal moves

        # Predict action
        action, _ = self.model.predict(
            obs,
            deterministic=True
        )

        # Safety: force legality
        if not mask[action]:
            action = np.where(mask)[0][0]

        return divmod(action, 8)
