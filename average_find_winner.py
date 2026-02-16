

import just_for_testing as main
import itertools
import random

def get_win_chance_percentage(current_board_dic):
    # Standardize tuples
    if current_board_dic and isinstance(next(iter(current_board_dic)), str):
        current_board_dic = {tuple(map(int, k.split(','))): v for k, v in current_board_dic.items()}

    # Adding variance by including 'random' and 'computer' (heuristic) 
    # but keeping the total game count manageable (8 games total)
    bots = ["computer", "aimodel"]
    total_games = 0
    total_black_wins = 0

    # 1. Precise Matchups (Determinstic baseline)
    for bot1, bot2 in [("computer", "aimodel"), ("aimodel", "computer")]:
        setup = {
                "computerblack": bot1 == "computer", "computerwhite": bot2 == "computer",
                "randomblack": bot1 == "random", "randomwhite": bot2 == "random",
                "chat_gpt_black": bot1 == "chat_gpt", "chat_gpt_white": bot2 == "chat_gpt",
                "aimodel_black": bot1 == "aimodel", "aimodel_white": bot2 == "aimodel",
                "dic": current_board_dic.copy()
        }
        result, _, _ = main.main_test1(**setup)
        if result == 0: total_black_wins += 1
        total_games += 1

    # 2. Stochastic Matchups (Adds the 'Gradient' / Percentage flavor)
    # We run 3 games where one side is 'random' to see how robust the board position is
    for _ in range(6):
        # Randomly choose if black or white is the 'unpredictable' player
        b_bot = random.choice(["computer", "aimodel", "random"])
        w_bot = random.choice(["computer", "aimodel", "random"])
        
        setup = {
                "computerblack": b_bot == "computer", "computerwhite": w_bot == "computer",
                "randomblack": b_bot == "random", "randomwhite": w_bot == "random",
                "chat_gpt_black": b_bot == "chat_gpt", "chat_gpt_white": w_bot == "chat_gpt",
                "aimodel_black": b_bot == "aimodel", "aimodel_white": w_bot == "aimodel",
                "dic": current_board_dic.copy()
        }
        result, _, _ = main.main_test1(**setup)
        if result == 0: total_black_wins += 1
        total_games += 1

    black_win_chance = (total_black_wins / total_games) * 100
    return black_win_chance