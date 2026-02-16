import just_for_testing as main
class computer():
    # WEIGHTS = {
    #     "corner": 1000,
    #     "x_square": -75,
    #     "c_square": -15,
    #     "edge_safe": 40,
    #     "edge_bad": -50,
    #     "edge_very_good": 100,
    #     "mobility_i_early": 2,
    #     "mobility_out_early": -25,
    #     "mobility_i_mid": 4,
    #     "mobility_out_mid": -12,
    #     "mobility_i_late": 12

    # }
    @staticmethod
    def count_stable_edge(dic, color, x, y):
        """
        Returns +1 if move creates a stable edge disc,
        -1 if it creates an unstable edge disc,
        0 otherwise.
        """

        # Not on edge → not stable
        if x not in (0, 7) and y not in (0, 7):
            return 0

        # Check which corner this edge belongs to
        if x == 0:  # left edge
            corner = (0, 0) if y < 4 else (0, 7)
            step = (0, 1) if y < 4 else (0, -1)
        elif x == 7:  # right edge
            corner = (7, 0) if y < 4 else (7, 7)
            step = (0, 1) if y < 4 else (0, -1)
        elif y == 0:  # top edge
            corner = (0, 0) if x < 4 else (7, 0)
            step = (1, 0) if x < 4 else (-1, 0)
        else:  # bottom edge
            corner = (0, 7) if x < 4 else (7, 7)
            step = (1, 0) if x < 4 else (-1, 0)

        corner_key = f"{corner[0]},{corner[1]}"
        if corner_key not in dic or dic[corner_key] != color:
            return -1  # edge without corner support → unstable

        # Walk from corner to move; must be continuous
        cx, cy = corner
        dx, dy = step

        while (cx, cy) != (x, y):
            if f"{cx},{cy}" not in dic or dic[f"{cx},{cy}"] != color:
                return -1
            cx += dx
            cy += dy

        return 1

    @staticmethod
    def findpossiblemoves(movenumber,dic, color):
        if not main.checkthatthereisamove(movenumber,dic,color):
            return None
        possiblemoves={}
        move=color
        k=0
        

        #starts by seeing if there are any good places near the center
        
        #this cycles through all the possible moves to find the amount of pieces each move flips and saves it to a dictionary
        for x in range(8):
            for y in range(8):
                if main.checkpiecenosorry(str(x)+","+str(y),movenumber,dic,color):
                    out = 0
                    k = 0
                    if main.checkenddown(dic,color,x,y)!=False:
                        (k1,out1)=main.checkenddown(dic,color,x,y)
                        k+=k1
                        out+=out1
                    if main.checkendup(dic,color,x,y)!=False:
                        (k1,out1)=main.checkendup(dic,color,x,y)
                        k+=k1
                        out+=out1
                    if main.checkendleft(dic,color,x,y)!=False:
                        (k1, out1)=main.checkendleft(dic,color,x,y)
                        k+=k1
                        out+=out1
                    if main.checkendright(dic,color,x,y)!=False:
                        (k1, out1)=main.checkendright(dic,color,x,y)
                        k+=k1
                        out+=out1
                    if main.checkendupdiag(dic,color,x,y)!=False:
                        (k1, out1)=main.checkendupdiag(dic,color,x,y)
                        k+=k1
                        out+=out1
                    if main.checkenddowndia(dic,color,x,y)!=False: 
                        (k1,out1)=main.checkenddowndia(dic,color,x,y)
                        k+=k1
                        out+=out1
                    if main.checkendotherdia(dic,color,x,y)!=False:
                        (k1,out1)=main.checkendotherdia(dic,color,x,y)
                        k+=k1
                        out+=out1
                    if main.checkendolastdia(dic,color,x,y)!=False:
                        (k1,out1)=main.checkendolastdia(dic,color,x,y)
                        k+=k1
                        out+=out1

                    if k>0:
            
                        possiblemoves[str(x)+","+str(y)]=(int(k), out)

        return possiblemoves
    @staticmethod
    def opponent_can_retake_edge(dic, x, y, color):
        if color=='black':
            opp='white'
        else:
            opp='black'
        if x==0 or x==7:
            if main.checkendright(dic, opp, x, y) != False:
                if str(x-1)+','+str(y) in dic:
                    if dic[str(x-1)+','+str(y)]==opp:
                        return True
            if main.checkendleft(dic, opp, x, y) != False:
                if str(x+1)+','+str(y) in dic:
                    if dic[str(x+1)+','+str(y)]==opp:
                        return True
        elif y==7 or y==0:
            if main.checkendup(dic, opp, x, y) != False:
                if str(x)+','+str(y+1) in dic:
                    if dic[str(x)+','+str(y+1)]==opp:
                        return True
            if main.checkenddown(dic, opp, x, y) != False:
                if str(x)+','+str(y-1) in dic:
                    if dic[str(x)+','+str(y-1)]==opp:
                        return True
        return False
    @staticmethod
    def owns_relevant_corner(dic, x, y, color):
        if x == 0 and y > 0 and y < 7:
            return dic.get("0,0") == color or dic.get("0,7") == color
        if x == 7 and y > 0 and y < 7:
            return dic.get("7,0") == color or dic.get("7,7") == color
        if y == 0 and x > 0 and x < 7:
            return dic.get("0,0") == color or dic.get("7,0") == color
        if y == 7 and x > 0 and x < 7:
            return dic.get("0,7") == color or dic.get("7,7") == color
        return False
    @staticmethod
    def opens_corner(dic, x, y, color, movenumber):
        opponent = "white" if color == "black" else "black"
        move = f"{x},{y}"

        corners = {"0,0", "0,7", "7,0", "7,7"}

        
        before = main.findpossiblemoves(movenumber, dic, opponent)
        before_corners = set(before.keys()) & corners if before else set()

    
        newdic = main.flip(move, movenumber, dic, color)


        after = main.findpossiblemoves(movenumber + 1, newdic, opponent)
        after_corners = set(after.keys()) & corners if after else set()

    
        return len(after_corners - before_corners) > 0
    @staticmethod
    def corner_risk(dic, x, y, color, movenumber):
        """
        Returns True if playing at (x,y) allows the opponent
        to take a corner in their next move.
        """
        opponent = "white" if color == "black" else "black"
        move = f"{x},{y}"


        newdic = main.flip(move, movenumber, dic, color)

        opp_moves = main.findpossiblemoves(movenumber + 1, newdic, opponent)
        if not opp_moves:
            return False
        corners = {"0,0", "0,7", "7,0", "7,7"}
        return any(pos in corners for pos in opp_moves.keys())
    @staticmethod
    def denies_corner(dic, x, y, color, movenumber):
        opponent = "white" if color == "black" else "black"
        move = f"{x},{y}"

        corners = {"0,0", "0,7", "7,0", "7,7"}

        before = main.findpossiblemoves(movenumber, dic, opponent)
        before_corners = set(before.keys()) & corners if before else set()

        if not before_corners:
            return False  # nothing to deny

        newdic = main.flip(move, movenumber, dic, color)

        after = main.findpossiblemoves(movenumber + 1, newdic, opponent)
        after_corners = set(after.keys()) & corners if after else set()

        return len(before_corners - after_corners) > 0

    @staticmethod
    def flips_along_edge(dic, color, x, y):

        if y == 0 or y == 7:
            return (
                main.checkendright(dic, color, x, y) != False or
                main.checkendleft(dic, color, x, y) != False
            )

    
        if x == 0 or x == 7:
            return (
                main.checkendup(dic, color, x, y) != False or
                main.checkenddown(dic, color, x, y) != False
            )

        return False

    @staticmethod
    def edge_moves(dic, color):
        moves = main.findpossiblemoves(0, dic, color)
        if not moves:
            return set()
        edges = set()
        for m in moves:
            x,y = map(int, m.split(","))
            if x in (0,7) or y in (0,7):
                edges.add(m)
        return edges

    @staticmethod
    def creates_edge_snapback(dic, new_dic, color):
        opp = "white" if color == "black" else "black"

        before = computer.edge_moves(dic, opp)
        after  = computer.edge_moves(new_dic, opp)
        # new dangerous edge moves created
        created = after - before

        return len(created) > 0

    def playcom(self, movenumber,dic, color, weights):
        if main.checkthatthereisamove(movenumber,dic,color):
            WEIGHTS = weights
            # addplaces(possiblemoves)
            possiblemoves=main.findpossiblemoves(movenumber,dic,color)
            score={}
            for i in possiblemoves.keys():
                score[i]=0
            if color=='black':
                opponent_color='white'
            else:
                opponent_color='black'
            


            if '2,2' in possiblemoves:
                score['2,2']+=WEIGHTS['c_square']*(1/movenumber)
            if '5,2' in possiblemoves:
                score['5,2']+=WEIGHTS['c_square']*(1/movenumber)
            if '5,5' in possiblemoves:
                score['5,5']+=WEIGHTS['c_square']*(1/movenumber)
            if '2,5' in possiblemoves:
                score['2,5']+=WEIGHTS['c_square']*(1/movenumber)
            
            #the computer takes the corners if possible
            
            #check for places to play around the edges
            for pop in possiblemoves.keys():
                x = int(pop[0])
                y = int(pop[2])
                if computer.corner_risk(dic, x, y, color, movenumber):
                    score[pop] -= WEIGHTS["corner"]
                if computer.denies_corner(dic, x, y, color, movenumber):
                    score[pop] += WEIGHTS["corner_deny"]
                is_corner = False
                if '0,0' ==pop or '0,7'==pop or '7,0'==pop or '7,7'==pop:
                    score[pop]+=WEIGHTS['corner']
                    is_corner = True
            
                stable = computer.count_stable_edge(dic, color, x, y)
                if stable > 0:
                    score[pop] += WEIGHTS["stable_edge"]
                elif stable < 0:
                    score[pop] += WEIGHTS["unstable_edge"]
                
                new_dic = main.flip(pop, movenumber, dic.copy(), color) 
                opp_moves = main.findpossiblemoves(movenumber+1, new_dic, opponent_color)
                opp_mobility = 0 if not opp_moves else len(opp_moves)
                i, out = possiblemoves[pop]
                if movenumber <= 20:
                    score[pop] += -WEIGHTS['mobility_i_early']*i + WEIGHTS['mobility_out_early']*out -opp_mobility*WEIGHTS['opp_mobility']      # early: mobility matters
                elif movenumber > 20 and movenumber <= 45:
                    score[pop] += WEIGHTS['mobility_i_mid']*i + WEIGHTS['mobility_out_mid']*out - opp_mobility*WEIGHTS['opp_mobility']   # midgame: balance
                else:
                    score[pop] += WEIGHTS['mobility_i_late']*i               # endgame: GRAB PIECES
                if x==0 and '0,'+str(int(y)+1) not in dic and '0,'+str(int(y)-1) not in dic:
                    score[pop]+=WEIGHTS['edge_safe']
                elif x==7 and '7,'+str(int(y)+1) not in dic and '7,'+str(int(y)-1) not in dic:
                    score[pop]+=WEIGHTS['edge_safe']
                if y==0 and str(int(x)+1)+','+str(y) not in dic and str(int(x)+1)+','+str(y) not in dic:
                    score[pop]+=WEIGHTS['edge_safe']
                elif y==7 and str(int(x)+1)+','+str(y) not in dic and str(int(x)+1)+','+str(y) not in dic:
                    score[pop]+=WEIGHTS['edge_safe']
                if x==1 and y==1 and '0,0' not in dic:
                    score[pop]-=WEIGHTS['x_square']
                if x==1 and y==6 and '0,7' not in dic:
                    score[pop]-=WEIGHTS['x_square']
                if x==6 and y==1 and '7,0' not in dic:
                    score[pop]-=WEIGHTS['x_square']
                if x==6 and y==6 and '7,7' not in dic:
                    score[pop]-=WEIGHTS['x_square']
                corx = False
                if computer.opens_corner(dic, x, y, color, movenumber):
                    score[pop]-=WEIGHTS['corner_give']
                    corx =True
                if x==0 or x==7 or y==0 or y==7:

                    if not is_corner and computer.flips_along_edge(dic, color, x, y):
                        snapback = computer.creates_edge_snapback(dic, new_dic, color)
                        owns_corner = computer.owns_relevant_corner(dic, x, y, color)

                        if snapback and not owns_corner:
                            score[pop] -= WEIGHTS["edge_retake"]
                        elif corx and not owns_corner:
                            score[pop] -= WEIGHTS["corner_give"]
                        else:
                            score[pop] += WEIGHTS["edge_very_good"]



                    if y==0 or y==7:
                        if str(x+1)+','+str(y) in dic:
                            if str(x-1)+','+str(y) in dic:
                                if dic[str(x-1)+','+str(y)]==color:
                                    if str(x+1)+','+str(y) in dic:
                                        if dic[str(x+1)+','+str(y)]==color:
                                            score[pop]+=WEIGHTS['edge_very_good']

                                if dic[str(x+1)+','+str(y)]!=color and dic[str(x-1)+','+str(y)]!=color:
                                    score[pop]+=WEIGHTS['edge_very_good']
                        elif str(x-1)+','+str(y) not in dic:
                            if str(x-2)+','+str(y) not in dic:
                                score[pop]+=WEIGHTS['edge_safe']
                            elif dic[str(x-2)+','+str(y)]==color:
                                score[pop]-=WEIGHTS['edge_annoying']*2
                            else:
                                score[pop]+=WEIGHTS['edge_less_annoying']
                        

                        

                    if x==0 or x==7:
                        if str(x)+','+str(y+1) in dic:
                            if str(x)+','+str(y-1) in dic:
                                
                                if dic[str(x)+','+str(y+1)]==color and dic[str(x)+','+str(y-1)]==color:
                                    score[pop]+=WEIGHTS['edge_very_good']
                                if dic[str(x)+','+str(y+1)]!=color and dic[str(x)+','+str(y-1)]!=color:
                                    score[pop]+=WEIGHTS['edge_very_good']
                            else:
                                score[pop]+=WEIGHTS['edge_safe']
                        elif str(x)+','+str(y-1) not in dic:
                            # is there a piece two spaces away?
                            if str(x)+','+str(y-2) not in dic:
                                score[pop]+=WEIGHTS['edge_safe']
                            # is the piece two spaces away mine of the same color
                            elif dic[str(x)+','+str(y-2)]==color:
                                score[pop]-=WEIGHTS['edge_annoying']*2
                            else:
                                score[pop]+=WEIGHTS['edge_less_annoying']

                
                
            thing = -10**10                  
            for i in score.keys():
                if score[i]>thing:
                    thing=score[i]
                    ans=i
            
        return ans
