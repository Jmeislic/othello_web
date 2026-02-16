import just_for_testing as main

def count_stable_edge(dic, color, x, y):
    if x not in (0, 7) and y not in (0, 7):
        return 0

    if x == 0:    corner, step = ((0, 0), (0, 1)) if y < 4 else ((0, 7), (0, -1))
    elif x == 7:  corner, step = ((7, 0), (0, 1)) if y < 4 else ((7, 7), (0, -1))
    elif y == 0:  corner, step = ((0, 0), (1, 0)) if x < 4 else ((7, 0), (-1, 0))
    else:         corner, step = ((0, 7), (1, 0)) if x < 4 else ((7, 7), (-1, 0))

    if dic.get(corner) != color:
        return -1  

    cx, cy = corner
    dx, dy = step
    while (cx, cy) != (x, y):
        if dic.get((cx, cy)) != color:
            return -1
        cx += dx
        cy += dy
    return 1

def owns_relevant_corner(dic, x, y, color):
    if x == 0 and 0 < y < 7:
        return dic.get((0, 0)) == color or dic.get((0, 7)) == color
    if x == 7 and 0 < y < 7:
        return dic.get((7, 0)) == color or dic.get((7, 7)) == color
    if y == 0 and 0 < x < 7:
        return dic.get((0, 0)) == color or dic.get((7, 0)) == color
    if y == 7 and 0 < x < 7:
        return dic.get((0, 7)) == color or dic.get((7, 7)) == color
    return False

def opens_corner(dic, x, y, color, movenumber):
    opponent = "white" if color == "black" else "black"
    corners = {(0, 0), (0, 7), (7, 0), (7, 7)}
    before = main.findpossiblemoves(movenumber, dic, opponent)
    before_corners = set(before.keys()) & corners if before else set()

    # Use main.flip instead of flip.py
    newdic = main.flip((x, y), movenumber, dic.copy(), color)
    after = main.findpossiblemoves(movenumber + 1, newdic, opponent)
    after_corners = set(after.keys()) & corners if after else set()
    return len(after_corners - before_corners) > 0

def denies_corner(dic, x, y, color, movenumber):
    opponent = "white" if color == "black" else "black"
    corners = {(0, 0), (0, 7), (7, 0), (7, 7)}
    before = main.findpossiblemoves(movenumber, dic, opponent)
    before_corners = set(before.keys()) & corners if before else set()
    if not before_corners:
        return False

    newdic = main.flip((x, y), movenumber, dic.copy(), color)
    after = main.findpossiblemoves(movenumber + 1, newdic, opponent)
    after_corners = set(after.keys()) & corners if after else set()
    return len(before_corners - after_corners) > 0

def flips_along_edge(dic, color, x, y):
    # This calls the functions we just added to main
    if y in (0, 7):
        return (main.checkendright(dic, color, x, y) is not False or 
                main.checkendleft(dic, color, x, y) is not False)
    if x in (0, 7):
        return (main.checkendup(dic, color, x, y) is not False or 
                main.checkenddown(dic, color, x, y) is not False)
    return False

def edge_moves(dic, color):
    moves = main.findpossiblemoves(0, dic, color)
    if not moves: return set()
    return {m for m in moves.keys() if m[0] in (0, 7) or m[1] in (0, 7)}

def creates_edge_snapback(dic, new_dic, color):
    opp = "white" if color == "black" else "black"
    before = edge_moves(dic, opp)
    after = edge_moves(new_dic, opp)
    return len(after - before) > 0

def playcom(movenumber, dic, color):
    if dic and isinstance(next(iter(dic)), str):
        dic = {tuple(map(int, k.split(','))): v for k, v in dic.items()}

    if main.checkthatthereisamove(movenumber, dic, color):
        WEIGHTS = {
            'corner': 968, 'x_square': 445, 'c_square': -49, 'edge_safe': 39, 
            'edge_bad': 111, 'edge_very_good': 122, 'mobility_i_early': 5, 
            'mobility_out_early': -2, 'mobility_i_mid': 44, 'mobility_out_mid': 28, 
            'mobility_i_late': 53, 'opp_mobility': 200, 'stable_edge': 75, 
            'unstable_edge': -80, 'edge_retake': 280, 'corner_give': 240, 
            'edge_annoying': 150, 'edge_less_annoying': 50, 'corner_deny': 260
        }

        possiblemoves = main.findpossiblemoves(movenumber, dic, color)
        score = {i: 0 for i in possiblemoves.keys()}
        opponent_color = 'white' if color == 'black' else 'black'

        for c_sq in [(2,2), (5,2), (5,5), (2,5)]:
            if c_sq in possiblemoves:
                score[c_sq] += WEIGHTS['c_square'] * (1/movenumber)

        for pop in possiblemoves.keys():
            x, y = pop
            
            if opens_corner(dic, x, y, color, movenumber):
                score[pop] -= WEIGHTS["corner"]
            if denies_corner(dic, x, y, color, movenumber):
                score[pop] += WEIGHTS["corner_deny"]
            
            is_corner = pop in [(0,0), (0,7), (7,0), (7,7)]
            if is_corner: score[pop] += WEIGHTS['corner']

            stable = count_stable_edge(dic, color, x, y)
            if stable > 0: score[pop] += WEIGHTS["stable_edge"]
            elif stable < 0: score[pop] += WEIGHTS["unstable_edge"]

            # Simulation using main.flip
            new_dic = main.flip(pop, movenumber, dic.copy(), color)
            opp_moves = main.findpossiblemoves(movenumber+1, new_dic, opponent_color)
            opp_mobility = len(opp_moves) if opp_moves else 0
            i_flipped, out_frontier = possiblemoves[pop]

            if movenumber <= 20:
                score[pop] += -WEIGHTS['mobility_i_early']*i_flipped + WEIGHTS['mobility_out_early']*out_frontier - opp_mobility*WEIGHTS['opp_mobility']
            elif movenumber <= 45:
                score[pop] += WEIGHTS['mobility_i_mid']*i_flipped + WEIGHTS['mobility_out_mid']*out_frontier - opp_mobility*WEIGHTS['opp_mobility']
            else:
                score[pop] += WEIGHTS['mobility_i_late']*i_flipped

            if x == 0 and (0, y+1) not in dic and (0, y-1) not in dic: score[pop] += WEIGHTS['edge_safe']
            elif x == 7 and (7, y+1) not in dic and (7, y-1) not in dic: score[pop] += WEIGHTS['edge_safe']
            if y == 0 and (x+1, 0) not in dic and (x-1, 0) not in dic: score[pop] += WEIGHTS['edge_safe']
            elif y == 7 and (x+1, 7) not in dic and (x-1, 7) not in dic: score[pop] += WEIGHTS['edge_safe']

            if pop == (1,1) and (0,0) not in dic: score[pop] -= WEIGHTS['x_square']
            if pop == (1,6) and (0,7) not in dic: score[pop] -= WEIGHTS['x_square']
            if pop == (6,1) and (7,0) not in dic: score[pop] -= WEIGHTS['x_square']
            if pop == (6,6) and (7,7) not in dic: score[pop] -= WEIGHTS['x_square']

            corx = False
            if opens_corner(dic, x, y, color, movenumber):
                score[pop] -= WEIGHTS['corner_give']
                corx = True

            if x in (0,7) or y in (0,7):
                if not is_corner and flips_along_edge(dic, color, x, y):
                    snapback = creates_edge_snapback(dic, new_dic, color)
                    has_corner = owns_relevant_corner(dic, x, y, color)
                    if snapback and not has_corner: score[pop] -= WEIGHTS["edge_retake"]
                    elif corx and not has_corner: score[pop] -= WEIGHTS["corner_give"]
                    else: score[pop] += WEIGHTS["edge_very_good"]

                if y == 0 or y == 7:
                    if (x+1, y) in dic and (x-1, y) in dic:
                        if dic[(x-1, y)] == color and dic[(x+1, y)] == color: score[pop] += WEIGHTS['edge_very_good']
                        if dic[(x+1, y)] != color and dic[(x-1, y)] != color: score[pop] += WEIGHTS['edge_very_good']
                    elif (x-1, y) not in dic:
                        if (x-2, y) not in dic: score[pop] += WEIGHTS['edge_safe']
                        elif dic.get((x-2, y)) == color: score[pop] -= WEIGHTS['edge_annoying']*2
                        else: score[pop] += WEIGHTS['edge_less_annoying']

                if x == 0 or x == 7:
                    if (x, y+1) in dic and (x, y-1) in dic:
                        if dic[(x, y+1)] == color and dic[(x, y-1)] == color: score[pop] += WEIGHTS['edge_very_good']
                        if dic[(x, y+1)] != color and dic[(x, y-1)] != color: score[pop] += WEIGHTS['edge_very_good']
                    elif (x, y-1) not in dic:
                        if (x, y-2) not in dic: score[pop] += WEIGHTS['edge_safe']
                        elif dic.get((x, y-2)) == color: score[pop] -= WEIGHTS['edge_annoying']*2
                        else: score[pop] += WEIGHTS['edge_less_annoying']

        return max(score, key=score.get)
    return None