import numpy as np
from sb3_contrib import MaskablePPO
import just_for_testing as main


class OthelloPolicy:
    """
    Wrapper around a trained MaskablePPO model.
    Guaranteed to return only legal moves.
    """

    def __init__(self, model_path: str):
        self.model = MaskablePPO.load(model_path)

    # ----------------------------
    # Board encoding
    # ----------------------------
    def dic_to_tensor(self, board, color: str):
        """
        +1 = current player
        -1 = opponent
        """
        obs = np.zeros((8, 8), dtype=np.float32)
        for k, v in board.items():
            r, c = map(int, k.split(","))
            obs[r, c] = 1.0 if v == color else -1.0
        return obs

    # ----------------------------
    # Legal action mask
    # ----------------------------
    def legal_mask(self, board, move_number, color: str):
        mask = np.zeros(64, dtype=bool)
        for r in range(8):
            for c in range(8):
                if main.checkpiecenosorry(f"{r},{c}", move_number, board, color):
                    mask[r * 8 + c] = True
        return mask

    # ----------------------------
    # Predict move
    # ----------------------------
    def predict_move(self, board, move_number, color: str):
        mask = self.legal_mask(board, move_number, color)
        if not mask.any():
            return None  # pass

        obs = self.dic_to_tensor(board, color)

        action, _ = self.model.predict(
            obs,
            action_masks=mask,
            deterministic=True
        )

        return divmod(action, 8)
