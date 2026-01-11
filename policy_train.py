import gymnasium as gym
from gymnasium import spaces
import numpy as np
import just_for_testing as main
import computer

CORNERS = {"0,0", "0,7", "7,0", "7,7"}


class OthelloTrainEnvBot(gym.Env):
    metadata = {"render_modes": ["human"]}

    def __init__(self, verbose=False):
        super().__init__()

        self.action_space = spaces.Discrete(64)
        self.observation_space = spaces.Box(
            low=-1, high=1, shape=(8, 8), dtype=np.int8
        )

        # Keep track of who starts first
        self.starting_player = "black"
        self.verbose = verbose

        # Initialize game state
        self.reset()

    # ------------------
    # Helpers
    # ------------------
    def _has_move(self, color):
        for r in range(8):
            for c in range(8):
                if main.checkpiecenosorry(f"{r},{c}", self.move_number, self.dic, color):
                    return True
        return False

    def _final_reward(self):
        black = sum(v == "black" for v in self.dic.values())
        white = sum(v == "white" for v in self.dic.values())
        if black > white:
            return 1.0 if self.player == "black" else -1.0
        elif white > black:
            return 1.0 if self.player == "white" else -1.0
        return 0.0

    def _switch_player(self):
        self.player = "white" if self.player == "black" else "black"

    def _obs(self):
        """
        Returns board from current player's perspective
        """
        board = np.zeros((8, 8), dtype=np.int8)
        for k, v in self.dic.items():
            r, c = map(int, k.split(","))
            board[r, c] = 1 if v == self.player else -1
        return board

    # ------------------
    # Gym API
    # ------------------
    def reset(self, seed=None, options=None):
        # Alternate starting player
        self.starting_player = "white" if self.starting_player == "black" else "black"
        self.player = self.starting_player

        self.dic = main.init_board()
        self.move_number = 0
        self.done = False

        if self.verbose:
            print(f"--- NEW GAME --- Starting player: {self.player}")
            print("Initial board:", self.dic)

        return self._obs(), {}

    def step(self, action):
        if self.done:
            raise RuntimeError("Step called on finished game")

        reward = 0.0

        if self.verbose:
            print(f"--- STEP {self.move_number + 1} ---")
            print(f"Current player: {self.player}")
            print(f"Current board: {self.dic}")
            print(f"Received action: {action}")

        # --- AGENT MOVE ---
        if self._has_move(self.player):
            r, c = divmod(action, 8)
            coord = f"{r},{c}"

            # If illegal, pick first legal
            if not main.checkpiecenosorry(coord, self.move_number, self.dic, self.player):
                found = False
                for rr in range(8):
                    for cc in range(8):
                        if main.checkpiecenosorry(f"{rr},{cc}", self.move_number, self.dic, self.player):
                            coord = f"{rr},{cc}"
                            found = True
                            break
                    if found:
                        break

            if coord in CORNERS:
                reward += 0.5

            self.dic = main.flip(coord, self.move_number, self.dic, self.player)
            self.move_number += 1

            if self.verbose:
                print(f"{self.player.upper()} played: {coord}")
                print("Board after move:", self.dic)

        # --- BOT MOVE (opponent) ---
        self._switch_player()
        if self._has_move(self.player):
            weights = {
                'corner': 968, 'x_square': 445, 'c_square': 31, 'edge_safe': 39,
                'edge_bad': 111, 'edge_very_good': 122, 'mobility_i_early': 5,
                'mobility_out_early': -2, 'mobility_i_mid': 34, 'mobility_out_mid': 28,
                'mobility_i_late': 53, 'opp_mobility': 200, 'stable_edge': 75,
                'unstable_edge': -80, "edge_retake": 200, "corner_give": 250,
                'edge_annoying': 150, 'edge_less_annoying': 50, "corner_deny": 300
            }
            bot_move = computer.playcom(self.move_number, self.dic, self.player, weights)

            if bot_move:
                self.dic = main.flip(bot_move, self.move_number, self.dic, self.player)
                self.move_number += 1

                if self.verbose:
                    print(f"{self.player.upper()} (BOT) played: {bot_move}")
                    print("Board after bot move:", self.dic)

        self._switch_player()

        # --- GAME OVER CHECK ---
        if not self._has_move("black") and not self._has_move("white"):
            self.done = True
            final_reward = self._final_reward()
            reward += final_reward
            if self.verbose:
                print("Game over!")
                print(f"Final reward: {final_reward}")
                print("Final board:", self.dic)

        return self._obs(), reward, self.done, False, {}
