
import string
import human
import computer
import randombot 
import chat_gpt_othello_bot as chatgpt
from policy import OthelloPolicy
# helper for circles
# Optimized Directional Check
def isoutside(x, y, move, dic):
    if x == 0 or x == 7 or y == 0 or y == 7:
        return False
    # Check all 8 neighbors for empty spaces
    for dx, dy in [(0,1),(0,-1),(1,0),(-1,0),(1,1),(1,-1),(-1,1),(-1,-1)]:
        if (x + dx, y + dy) not in dic:
            return True
    return False

def check_dir_base(dic, move, x, y, dx, dy):
    # This is the logic shared by all your checkend functions
    if dic.get((x + dx, y + dy)) is None or dic.get((x + dx, y + dy)) == move:
        return False
    out = 0
    for i in range(2, 8):
        nx, ny = x + (dx * i), y + (dy * i)
        piece = dic.get((nx, ny))
        if piece:
            if isoutside(nx, ny, move, dic):
                out += 1
            if piece == move:
                return (i, out)
        else:
            return False
    return False

# Individual functions so playcom doesn't crash
def checkenddown(dic, move, x, y): return check_dir_base(dic, move, x, y, 0, 1)
def checkendup(dic, move, x, y): return check_dir_base(dic, move, x, y, 0, -1)
def checkendleft(dic, move, x, y): return check_dir_base(dic, move, x, y, -1, 0)
def checkendright(dic, move, x, y): return check_dir_base(dic, move, x, y, 1, 0)
def checkendupdiag(dic, move, x, y): return check_dir_base(dic, move, x, y, 1, -1)
def checkenddowndia(dic, move, x, y): return check_dir_base(dic, move, x, y, 1, 1)
def checkendotherdia(dic, move, x, y): return check_dir_base(dic, move, x, y, -1, -1)
def checkendolastdia(dic, move, x, y): return check_dir_base(dic, move, x, y, -1, 1)

def flip(coordinates, movenumber, dic, move):
    if isinstance(coordinates, str):
        x, y = map(int, coordinates.split(','))
    else:
        x, y = coordinates
    
    newdic = dic.copy()
    newdic[(x, y)] = move
    
    # Map the directions to your specific checkend functions
    checkers = [
        (0, 1, checkenddown), (0, -1, checkendup), 
        (-1, 0, checkendleft), (1, 0, checkendright),
        (1, -1, checkendupdiag), (1, 1, checkenddowndia),
        (-1, -1, checkendotherdia), (-1, 1, checkendolastdia)
    ]
    
    for dx, dy, checker in checkers:
        res = checker(dic, move, x, y)
        if res:
            dist, _ = res
            for i in range(1, dist):
                newdic[(x + dx * i, y + dy * i)] = move
    return newdic
def check_direction(dic, move, x, y, dx, dy):
    opponent = 'white' if move == 'black' else 'black'
    nx, ny = x + dx, y + dy
    
    # Must have at least one opponent piece immediately adjacent
    if dic.get((nx, ny)) != opponent:
        return False
    
    out_count = 0
    # Search further in that direction
    for i in range(2, 8):
        nx, ny = x + dx * i, y + dy * i
        
        # Othello boards are 0-7
        if not (0 <= nx <= 7 and 0 <= ny <= 7):
            return False
            
        piece = dic.get((nx, ny))
        if piece is None:
            return False # Empty space, move invalid in this direction
    
            
        if piece == move:
            return i - 1 # Return pieces flipped and outside count
            
    return False

# Condensed directions list
DIRECTIONS = [
    (0, 1), (0, -1), (1, 0), (-1, 0),   # Down, Up, Right, Left
    (1, 1), (-1, -1), (1, -1), (-1, 1)  # Diagonals
]

def flip(coordinates, movenumber, dic, move):
    # Convert string key to tuple if necessary
    x, y = coordinates

    dic[(x, y)] = move
    
    for dx, dy in DIRECTIONS:
        dist = check_direction(dic, move, x, y, dx, dy)
        if dist:
            # Flip pieces in this direction
            for i in range(1, dist + 1):
                dic[(x + dx * i, y + dy * i)] = move
    return dic

def findpossiblemoves(movenumber, dic, color):
    possiblemoves = {}
    
    for x in range(8):
        for y in range(8):
            # 1. Skip if already occupied
            if (x, y) in dic:
                continue
                
            total_k = 0
            total_out = 0
            
            # 2. Check all directions
            for dx, dy in DIRECTIONS:
                res = check_direction(dic, color, x, y, dx, dy)
                if res:
    
                    total_k += res

            
            # 3. If it flips anything, it's a valid move
            if total_k > 0:
                possiblemoves[(x, y)] = (total_k, total_out)

    return possiblemoves if possiblemoves else None
    
def checkthatthereisamove(movenumber, dic, move):
    """
    Returns True as soon as one valid move is found.
    Extremely fast for checking if the game should continue.
    """
    # Directions: (dx, dy)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    
    for x in range(8):
        for y in range(8):
            # Skip occupied squares immediately
            if (x, y) in dic:
                continue
            
            # Check if this empty square flips anything in any direction
            for dx, dy in directions:
                if check_direction(dic, move, x, y, dx, dy):
                    return True # Stop and return immediately
                    
    return False

def donecount(dic):
    black_score = list(dic.values()).count('black')
    white_score = list(dic.values()).count('white')
    
    # Return 0 if black wins, 1 if white wins, 2 for draw
    if black_score > white_score:
        return 0, black_score, white_score
    elif white_score > black_score:
        return 1, black_score, white_score
    else:
        return 2, black_score, white_score
def init_board():
    """
    Returns a fresh Othello board as a dict:
    key   = "row,col"
    value = "black" or "white"
    """
    return {
        (3,3): "white",
        (3,4): "black",
        (4,3): "black",
        (4,4): "white"
    }

def main_test1(computerblack, computerwhite, randomblack, randomwhite, chat_gpt_black, chat_gpt_white, aimodel_black, aimodel_white, dic):
    # 1. Convert board to tuples once for high-speed access
    # Handles both "x,y" and (x,y) formats for safety
    fast_dic = {}
    for k, v in dic.items():
        if isinstance(k, str):
            fast_dic[tuple(map(int, k.split(',')))] = v
        else:
            fast_dic[k] = v

    movenumber = 1
    
    while True:
        black_moved = False
        white_moved = False

        # --- BLACK'S TURN ---
        if checkthatthereisamove(movenumber, fast_dic, 'black'):
            if computerblack:
                coords = computer.playcom(movenumber, fast_dic, 'black')
            elif randomblack:
                coords = randombot.randomplaycom(movenumber, fast_dic, 'black')
            elif chat_gpt_black:
                coords = chatgpt.playcom2(movenumber, fast_dic, 'black')
            elif aimodel_black:
                coords = OthelloPolicy("final").predict_move(fast_dic, movenumber, 'black')
            
            flip(coords, movenumber, fast_dic, 'black')
            black_moved = True

        # --- WHITE'S TURN ---
        if checkthatthereisamove(movenumber, fast_dic, 'white'):
            if computerwhite:
                o = computer.playcom(movenumber, fast_dic, 'white')
            elif randomwhite:
                o = randombot.randomplaycom(movenumber, fast_dic, 'white')
            elif chat_gpt_white:
                o = chatgpt.playcom2(movenumber, fast_dic, 'white')
            elif aimodel_white:
                o = OthelloPolicy("final").predict_move(fast_dic, movenumber, 'white')

            flip(o, movenumber, fast_dic, 'white')
            white_moved = True

        # --- END CONDITION ---
        if not black_moved and not white_moved:
            return donecount(fast_dic)

        movenumber += 2