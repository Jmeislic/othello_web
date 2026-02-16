import gymnasium as gym
from gymnasium import spaces
import numpy as np
import random
import just_for_testing as main
from computer import playcom
from chat_gpt_othello_bot import playcom2
from sb3_contrib.ppo_mask.policies import MaskableActorCriticPolicy
CORNERS = {(0,0), (0,7), (7,0), (7,7)}

class OthelloTrainEnvBot(gym.Env):
    def __init__(self, opponent_policy=None):
        super().__init__()
        self.action_space = spaces.Discrete(64)
        self.observation_space = spaces.Box(
            low=-1.0, high=1.0, shape=(8, 8), dtype=np.float32
        )
        self.opponent_policy = opponent_policy
        self.reset()

    # Required for self-play training loop
    def set_opponent(self, policy):
        self.opponent_policy = policy

    # --------------------
    # Helpers
    # --------------------
    def _legal_moves(self, color):
        moves_dict = main.findpossiblemoves(self.move_number, self.board, color)
        # FIX: Handle None return from game logic
        return list(moves_dict.keys()) if moves_dict else []

    def action_masks(self):
        mask = np.zeros(64, dtype=bool)
        moves = self._legal_moves(self.player)
        for (r, c) in moves:
            mask[r * 8 + c] = True
        return mask

    def _obs(self):
        obs = np.zeros((8, 8), dtype=np.float32)
        for k, v in self.board.items():
            # Handle both string "r,c" and tuple (r,c) keys
            if isinstance(k, str):
                try:
                    r, c = map(int, k.split(","))
                except ValueError:
                    continue
            else:
                r, c = k
            # Perspective encoding: 1.0 for current player, -1.0 for opponent
            obs[r, c] = 1.0 if v == self.player else -1.0
        return obs

    def _final_reward(self):
        black = sum(1 for v in self.board.values() if v == "black")
        white = len(self.board) - black
        if black == white: return 0
        
        winner = "black" if black > white else "white"
        return 10.0 if self.agent_color == winner else -10.0

    def _check_game_over(self):
        # Game ends if neither player can move
        if not self._legal_moves("black") and not self._legal_moves("white"):
            self.done = True
            return True
        return False

    # --------------------
    # Opponent Logic
    # --------------------
    def _opponent_turn(self):
        # Continue playing as opponent as long as it's their turn 
        # AND they have moves AND the game isn't over.
        while self.player != self.agent_color and not self.done:
            opp_moves = self._legal_moves(self.player)
            
            if not opp_moves:
                # Opponent has no moves, they must pass
                if not self._legal_moves(self.agent_color):
                    # NEITHER player has moves, game is over
                    self.done = True
                    break
                # Switch back to agent turn
                self.player = self.agent_color
                break

            # Pick move based on opponent type
            o_coord = None
            if self.opponent_type == "random":
                o_coord = random.choice(opp_moves)
            elif self.opponent_type == "heuristic":
                # Assuming playcom returns a single coord (r, c)
                o_coord = playcom(self.move_number, self.board, self.player)
            elif self.opponent_type == "selfplay" and self.opponent_policy:
                obs = self._obs()
                mask = self.action_masks()
                action_p, _ = self.opponent_policy.predict(obs, action_masks=mask, deterministic=False)
                o_coord = divmod(action_p, 8)
            
            # --- CRITICAL SAFETY CHECK ---
            if o_coord is not None:
                self.board = main.flip(o_coord, self.move_number, self.board, self.player)
                self.move_number += 1
            
            # Check if turn swaps back to agent or continues (if agent must pass)
            if self._legal_moves(self.agent_color):
                self.player = self.agent_color

    # --------------------
    # Gym API
    # --------------------
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        self.board = main.init_board()
        self.move_number = 0
        self.done = False
        self.agent_color = random.choice(["black", "white"])
        self.player = "black"

        self.opponent_type = random.choice([
            "random", "heuristic", "chat", 
            "selfplay" if self.opponent_policy else "random"
        ])

        # If Agent is White, Opponent (Black) must move first
        if self.agent_color == "white":
            self._opponent_turn()

        return self._obs(), {}

    def step(self, action):
        if self.done:
            return self._obs(), 0, True, False, {}

        reward = 0.0
        r, c = divmod(action, 8)
        coord = (r, c)

        # 1. Agent Logic
        legal_dict = main.findpossiblemoves(self.move_number, self.board, self.player)
        
        # --- CRITICAL FIX: Handle NoneType if findpossiblemoves returns None ---
        if legal_dict is None:
            legal_dict = {}

        if coord not in legal_dict:
            # Illegal move penalty
            return self._obs(), -100.0, True, False, {"illegal_move": True}
        # -----------------------------------------------------------------------

        if coord in CORNERS:
            reward += 5.0

        self.board = main.flip(coord, self.move_number, self.board, self.player)
        self.move_number += 1

        if self._check_game_over():
            return self._obs(), reward + self._final_reward(), True, False, {}

        # Switch to Opponent
        self.player = "white" if self.player == "black" else "black"

        # 2. Opponent Logic (Simulate until it's agent's turn again)
        self._opponent_turn()

        if self.done:
            reward += self._final_reward()

        return self._obs(), reward, self.done, False, {}
        if self.done:
            return self._obs(), 0, True, False, {}

        reward = 0.0
        r, c = divmod(action, 8)
        coord = (r, c)

        # 1. Agent Logic
        legal_dict = main.findpossiblemoves(self.move_number, self.board, self.player)
        
        # FIX: Handle NoneType if findpossiblemoves returns None
        if legal_dict is None:
            legal_dict = {}

        if coord not in legal_dict:
            # Illegal move penalty
            return self._obs(), -100.0, True, False, {"illegal_move": True}

        if coord in CORNERS:
            reward += 5.0

        self.board = main.flip(coord, self.move_number, self.board, self.player)
        self.move_number += 1

        if self._check_game_over():
            return self._obs(), reward + self._final_reward(), True, False, {}

        # Switch to Opponent
        self.player = "white" if self.player == "black" else "black"

        # 2. Opponent Logic (Simulate until it's agent's turn again)
        self._opponent_turn()

        if self.done:
            reward += self._final_reward()

        return self._obs(), reward, self.done, False, {}