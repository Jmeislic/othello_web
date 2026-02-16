import just_for_testing as main
import random

def playcom2(movenumber, dic, color):
    # Standardize dictionary to tuples if they come in as strings
    if dic and isinstance(next(iter(dic)), str):
        dic = {tuple(map(int, k.split(','))): v for k, v in dic.items()}

    opp = "white" if color == "black" else "black"
    pm = main.findpossiblemoves(movenumber, dic, color)
    
    if not pm:
        return None

    best = -10**18
    best_moves = []
    
    # Pre-calculate corners as tuples
    CORNERS = {(0, 0), (0, 7), (7, 0), (7, 7)}

    for move, (i, out) in pm.items():
        x, y = move
        s = 0

        # --------------------
        # SIMULATE MOVE (Fast Tuple Flip)
        # --------------------
        newdic = main.flip(move, movenumber, dic.copy(), color)
        opp_moves = main.findpossiblemoves(movenumber+1, newdic, opp)
        opp_mob = len(opp_moves) if opp_moves else 0

        # --------------------
        # CORNER LOGIC
        # --------------------
        if move in CORNERS:
            s += 100000

        # --------------------
        # X-SQUARE & C-SQUARE LOGIC (Using Math instead of Sets)
        # --------------------
        # X-Squares are (1,1), (1,6), (6,1), (6,6)
        if x in (1, 6) and y in (1, 6):
            cx, cy = (0 if x < 4 else 7, 0 if y < 4 else 7)
            if (cx, cy) not in dic:
                s -= 90000

        # C-Squares are squares adjacent to corners on the edges
        elif (x in (0, 7) and y in (1, 6)) or (y in (0, 7) and x in (1, 6)):
            # Find closest corner
            cx, cy = (0 if x <= 1 else 7 if x >= 6 else x, 
                      0 if y <= 1 else 7 if y >= 6 else y)
            # Only penalize if the actual corner is empty
            if (cx, cy) in CORNERS and (cx, cy) not in dic:
                s -= 25000

        # --------------------
        # CORNER GIVING / DENIAL
        # --------------------
        if opp_moves:
            for c in CORNERS:
                if c in opp_moves:
                    s -= 120000

        opp_before = main.findpossiblemoves(movenumber, dic, opp)
        if opp_before:
            # Denied: corners the opponent could move to before, but can't now
            denied = (set(opp_before.keys()) & CORNERS) - (set(opp_moves.keys()) if opp_moves else set())
            s += 60000 * len(denied)

        # --------------------
        # EDGE STABILITY
        # --------------------
        if x in (0, 7) or y in (0, 7):
            if move not in CORNERS:
                # Logic: Is a relevant corner owned by ANYONE? (Stability protection)
                corner_owned = False
                if x == 0: corner_owned = (0, 0) in dic or (0, 7) in dic
                elif x == 7: corner_owned = (7, 0) in dic or (7, 7) in dic
                elif y == 0: corner_owned = (0, 0) in dic or (7, 0) in dic
                elif y == 7: corner_owned = (0, 7) in dic or (7, 7) in dic
                
                s += 20000 if corner_owned else -12000

        # --------------------
        # MOBILITY & FRONTIER
        # --------------------
        if movenumber < 20:
            s += -40 * i + 80 * out
            s -= 3000 * opp_mob
        elif movenumber < 45:
            s += 30 * i - 20 * out
            s -= 2000 * opp_mob
        else:
            s += 500 * i  # Total Capture

        # Frontier Penalty: Checking for empty spaces around the move
        frontier = 0
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if (x + dx, y + dy) not in newdic:
                frontier += 1
        s -= frontier * 300

        # --------------------
        # LATE GAME BIASES
        # --------------------
        empties = 64 - len(newdic)
        if empties < 14:
            s += 5000 if empties % 2 == 1 else -5000  # Parity

        if movenumber > 50:
            # Efficient disc counting
            my_count = sum(1 for v in newdic.values() if v == color)
            opp_count = len(newdic) - my_count
            s += (my_count - opp_count) * 1000

        # --------------------
        # TRACK BEST
        # --------------------
        if s > best:
            best = s
            best_moves = [move]
        elif s == best:
            best_moves.append(move)

    return random.choice(best_moves)