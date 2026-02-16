import numpy as np
from sb3_contrib import MaskablePPO
import just_for_testing as main
from sb3_contrib.ppo_mask.policies import MaskableActorCriticPolicy # Add this import
class OthelloPolicy:
    def __init__(self, model_path: str):
        self.model = MaskablePPO.load(
            model_path, 
            policy=MaskableActorCriticPolicy
        )

    def dic_to_tensor(self, board, color: str):
        obs = np.zeros((8, 8), dtype=np.float32)
        for k, v in board.items():
            # Fix: Handle both tuple (r, c) and old string "r,c"
            if isinstance(k, str):
                r, c = map(int, k.split(","))
            else:
                r, c = k
            obs[r, c] = 1.0 if v == color else -1.0
        return obs

    def legal_mask(self, board, move_number, color: str):
        mask = np.zeros(64, dtype=bool)
        
        # Ensure we are working with tuple keys for the game logic
        clean_board = {}
        for k, v in board.items():
            if isinstance(k, str):
                r, c = map(int, k.split(','))
                clean_board[(r, c)] = v
            else:
                clean_board[k] = v

        # Use the cleaned board with the game logic
        legal_moves = main.findpossiblemoves(move_number, clean_board, color)
        
        if legal_moves:
            for (r, c) in legal_moves.keys():
                mask[r * 8 + c] = True
        
        return mask

    def predict_move(self, board, move_number, color: str):
        # 1. Generate mask (now uses tuples)
        mask = self.legal_mask(board, move_number, color)
        
        if not mask.any():
            return None

        # 2. Convert board to tensor (now handles tuples)
        obs = self.dic_to_tensor(board, color)

        action, _ = self.model.predict(
            obs,
            action_masks=mask,
            deterministic=True
        )

        # Returns (row, col) as a tuple
        return divmod(action, 8)