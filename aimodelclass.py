from policy import OthelloPolicy
import numpy as np

class ModelWrapper:
    """
    Wrapper around the trained PPO model for playing Othello.
    Can play as black or white.
    """

    def __init__(self, model_path="othello_ppo_model.zip"):
        self.policy = OthelloPolicy(model_path)


    def playcom(self, movenumber, dic, color, weights=None):
        """
        Decide the move using the PPO model.

        Parameters:
            movenumber: int - current move number
            dic: dict - current board state
            color: str - "black" or "white"
            weights: dict - unused (only for compatibility with computer player)
        
        Returns:
            tuple (row, col) or None if no legal move
        """
        # Copy dic to avoid mutating the original
        board_copy = dic.copy()

        # If model plays white, invert the board for PPO
        if color == "white":
            inverted_board = {}
            for k, v in board_copy.items():
                inverted_board[k] = "black" if v == "white" else "white"
            board_copy = inverted_board

        # Ask PPO for move
        move = self.policy.predict_move(board_copy, movenumber)

        # If playing white, flip move coordinates back (board orientation stays the same)
        return move
