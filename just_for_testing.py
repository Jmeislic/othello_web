import string
import human
import computer
import randombot
import chat_gpt_othello_bot as chatgpt
import aimodelclass

# helper for circles





def checkenddown(dic,move,x,y):
    #check if there is a piece directly under it
    
    try:
        dic[str(x)+","+str(y+1)]
    except:
        return False
    #is the piece right under it the same color
    if dic[str(x)+","+str(y+1)]==move:
        return False
    #try to see 
    out = 0
    for i in range(2,8):
        if str(x)+","+str(y+i) in dic:
            if isoutside(x,y+i,move,dic):
                out +=1
            if dic[str(x)+","+str(y+i)]==move:
                return (i,out)
          
        else:
            return False
    return False
    
def checkendup(dic,move,x,y):
    #check if there is a piece directly over it     
    try:
        dic[str(x)+","+str(y-1)]
    except:
        return False
    out = 0
    #is the piece right under it the same color
    if dic[str(x)+","+str(y-1)]==move:
        return False
    #try to see 
    for i in range(2,8):
        if str(x)+","+str(y-i) in dic:
            if isoutside(x,y-i,move,dic):
                out +=1
            if dic[str(x)+","+str(y-i)]==move:
                return (i,out)
        else:
            return False
    return False
        
        
def checkendleft(dic,move,x,y):
   
        #check if there is a piece directly left it
    
    try:
        dic[str(x-1)+","+str(y)]
        
        
    except:
        return False
    out = 0
    #is the piece right under it the same color
    if dic[str(x-1)+","+str(y)]==move:
        return False
    #try to see 
    for i in range(2,8):
        if str(x-i)+","+str(y) in dic:
            if isoutside(x-i,y,move,dic):
                out +=1
            if dic[str(x-i)+","+str(y)]==move:
                return (i,out) 

        else:
            return False
    return False
        
def checkendright(dic,move,x,y):
        #check if there is a piece directly right it
    
    try:
        dic[str(x+1)+","+str(y)]
        
        
    except:
        return False

    out = 0
    #is the piece right of it the same color
    if dic[str(x+1)+","+str(y)]==move:
        return False
    #try to see 
    for i in range(2,8):
        if str(x+i)+","+str(y) in dic:
            if isoutside(x+i,y,move,dic):
                out +=1
            if dic[str(x+i)+","+str(y)]==move:
                return (i,out)
        
        else:
            return False
    return False

def checkendupdiag(dic,move,x,y):
    #check if there is a piece directly up diagonal it
    try:
        dic[str(x+1)+","+str(y-1)]
    except:
        return False

    out = 0
    #is the piece right under it the same color
    if dic[str(x+1)+","+str(y-1)]==move:
        return False
    #try to see 
    for i in range(2,8):
        if str(x+i)+","+str(y-i) in dic:
            if isoutside(x+i,y-i,move,dic):
                out +=1
            if dic[str(x+i)+","+str(y-i)]==move:
                return (i,out)

        else:
            return False
    return False
    
   
        
def checkenddowndia(dic,move,x,y):
            #check if there is a piece directly up diagonal it
    
    try:
        dic[str(x+1)+","+str(y+1)]
        
        
    except:
        return False
    out = 0
    #is the piece right under it the same color
    if dic[str(x+1)+","+str(y+1)]==move:
        return False
    #try to see 
    for i in range(2,8):
        if str(x+i)+","+str(y+i) in dic:
            if isoutside(x+i,y+i,move,dic):
                out +=1
            if dic[str(x+i)+","+str(y+i)]==move:
                return (i,out)
        
        else:
            return False
    return False

  
        
def checkendotherdia(dic,move,x,y):
            #check if there is a piece directly down diagonal it
    
    try:
        dic[str(x-1)+","+str(y-1)]
        
        
    except:
        return False
    out = 0
    #is the piece right under it the same color
    if dic[str(x-1)+","+str(y-1)]==move:
        return False
    #try to see 
    for i in range(2,8):
        if str(x-i)+","+str(y-i) in dic:
            if isoutside(x-i,y-i,move,dic):
                out +=1
            if dic[str(x-i)+","+str(y-i)]==move:
                return (i,out)

        else:
            return False
    return False
        
def checkendolastdia(dic,move,x,y):
    #check if there is a piece directly down diagonal it
    
    try:
        dic[str(x-1)+","+str(y+1)]
    except:
        return False
    out = 0
    #is the piece right under it the same color
    if dic[str(x-1)+","+str(y+1)]==move:
        return False
    #try to see 
    for i in range(2,8):
        if str(x-i)+","+str(y+i) in dic:
            if isoutside(x-i,y+i,move,dic):
                out +=1
            if dic[str(x-i)+","+str(y+i)]==move:

                return (i,out)
        
        else:
            return False
    return False





def flippieces1(dic,move,x,y):


    #flip pieces down
    #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    
    dic[str(x)+","+str(y)]=move
    return flippieces1(dic,move,x,y+1)          



             
def flippieces2(dic,move,x,y):

    #flip pieces up
    #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    dic[str(x)+","+str(y)]=move
    return flippieces2(dic,move,x,y-1)
             
                    

def flippieces3(dic,move,x,y):
    #flip pieces left
   #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    dic[str(x)+","+str(y)]=move
    return flippieces3(dic,move,x-1,y)
                 
                    
def flippieces4(dic,move,x,y):
    #flip pieces right
    #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    dic[str(x)+","+str(y)]=move
    return flippieces4(dic,move,x+1,y)                          

def flippieces5(dic,move,x,y):
    
    #flip pieces diagonal down
    #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    dic[str(x)+","+str(y)]=move
    return flippieces5(dic,move,x+1,y+1)                        
                
def flippieces6(dic,move,x,y):
    #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    dic[str(x)+","+str(y)]=move
    return flippieces6(dic,move,x-1,y-1)

def flippieces7(dic,move,x,y):
    #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    dic[str(x)+","+str(y)]=move
    return flippieces7(dic,move,x-1,y+1)

def flippieces8(dic,move,x,y):
    #condition the reursive thing will stop when it gets to the a piece that it 
    if dic[str(x)+","+str(y)]==move:
        return dic
    
    dic[str(x)+","+str(y)]=move
    return flippieces8(dic,move,x+1,y-1)

     
def isoutside(x,y,move,dic):
    if x ==0 or x==7 or y==0 or y==7:
        return False
    elif str(x+1)+","+str(y) not in dic:
        return True
    elif str(x)+","+str(y+1) not in dic:
        return True
    elif str(x+1)+","+str(y+1) not in dic:
        return True
    elif str(x-1)+","+str(y+1) not in dic:
        return True
    elif str(x-1)+","+str(y) not in dic:
        return True
    elif str(x-1)+","+str(y-1) not in dic:
        return True
    elif str(x+1)+","+str(y) not in dic:
        return True
    elif str(x)+","+str(y-1) not in dic:
        return True
    else:
        return False


def checkpiece(coordinates,movenumber,dic,move):
    try:
      x=int(coordinates[0])
      y=int(coordinates[2])
    except:
        print("sorry your input was bad")
        return False
    if len(coordinates)>3:
            print("sorry your input should be three characters like '0,4' and no more")
            return False
    if x<0 or x>7:
        print("sorry your x coordinate should greater than or equal to 0 and be less than or equal to 7")
        return False
    if 0>y or y>7:
        print("sorry your y coordinate should greater than or equal to 0 and be less than or equal to 7")
        return False
    if coordinates[1]!=',':
        print("sorry your input should be three characters like '0,4' and no more")
        return False
   
    for i in dic.keys():
        if int(i[0])==x and int(i[2])==y:
            print("sorry there is already a piece there")
            return False
  
    
    #make sure that the piecce bing placed will flip other pieces on the board
    if checkenddown(dic,move,x,y)==False and checkendup(dic,move,x,y)==False and checkendleft(dic,move,x,y)==False and checkendright(dic,move,x,y)==False and checkendupdiag(dic,move,x,y)==False and checkenddowndia(dic,move,x,y)==False and checkendotherdia(dic,move,x,y)==False and checkendolastdia(dic,move,x,y)==False:
        print("sorry you cannot put a piece there")
        return False
        #if one of those returns true then the piece will flip something

    return True

def checkpiecenosorry(coordinates,movenumber,dic,move):
    #this is a check with no print statments so that the computer can check pieces anywhere on the board without unnecesary print statements
    try:
      x=int(coordinates[0])
      y=int(coordinates[2])
    except:
        return False
    if len(coordinates)>3:
        return False
    
    if x<0 or x>7:
        return False
    if 0>y or y>7:
       
        return False
    if coordinates in dic:
        return False
    
    #make sure that the piecce bing placed will flip other pieces on the board
    if checkenddown(dic,move,x,y)==False and checkendup(dic,move,x,y)==False and checkendleft(dic,move,x,y)==False and checkendright(dic,move,x,y)==False and checkendupdiag(dic,move,x,y)==False and checkenddowndia(dic,move,x,y)==False and checkendotherdia(dic,move,x,y)==False and checkendolastdia(dic,move,x,y)==False:
     
        return False
    
    
    
    return True

def flip(coordinates,movenumber,dic,move):
    x=int(coordinates[0])
    y=int(coordinates[2])
    dic1 = dic.copy()
    dic1[coordinates]= move
    if checkenddown(dic1,move,x,y)!=False:
        #flip those pieces
        dic1=flippieces1(dic1,move,x,y+1)
        
    if checkendup(dic1,move,x,y)!=False:
     
        dic1=flippieces2(dic1,move,x,y-1) 
    if checkendleft(dic1,move,x,y)!=False:
       

        dic1=flippieces3(dic1,move,x-1,y)
    if checkendright(dic1,move,x,y)!=False:
      

        dic1=flippieces4(dic1,move,x+1,y)
    if checkendupdiag(dic1,move,x,y)!=False:
 
        dic1=flippieces8(dic1,move,x+1,y-1)
        
    if checkenddowndia(dic1,move,x,y)!=False:
 
        dic1=flippieces5(dic1,move,x+1,y+1)
        
    if checkendotherdia(dic1,move,x,y)!=False:


        dic1=flippieces6(dic1,move,x-1,y-1)

    if checkendolastdia(dic1,move,x,y)!=False:
     
        dic1=flippieces7(dic1,move,x-1,y+1)
    return dic1

def donecount(dic):
    black=0
    white=0
    for i in dic.values():
        if i=='black':
            black+=1
        else:
            white+=1
    if black>white:
     
        return 0, black, white
    if black<white:
       
        return 1, black, white
    if black==white:
        return 2, black, white
    


def findpossiblemoves(movenumber,dic, color):
    if not checkthatthereisamove(movenumber,dic,color):
        return None
    possiblemoves={}
    move=color
    k=0
    #starts by seeing if there are any good places near the center
    
    #this cycles through all the possible moves to find the amount of pieces each move flips and saves it to a dictionary
    for x in range(8):
        for y in range(8):
            if checkpiecenosorry(str(x)+","+str(y),movenumber,dic,color):
                out = 0
                k = 0
                if checkenddown(dic,color,x,y)!=False:
                    (k1,out1)=checkenddown(dic,color,x,y)
                    k+=k1
                    out+=out1
                if checkendup(dic,color,x,y)!=False:
                    (k1,out1)=checkendup(dic,color,x,y)
                    k+=k1
                    out+=out1
                if checkendleft(dic,color,x,y)!=False:
                    (k1, out1)=checkendleft(dic,color,x,y)
                    k+=k1
                    out+=out1
                if checkendright(dic,color,x,y)!=False:
                    (k1, out1)=checkendright(dic,color,x,y)
                    k+=k1
                    out+=out1
                if checkendupdiag(dic,color,x,y)!=False:
                    (k1, out1)=checkendupdiag(dic,color,x,y)
                    k+=k1
                    out+=out1
                if checkenddowndia(dic,color,x,y)!=False: 
                    (k1,out1)=checkenddowndia(dic,color,x,y)
                    k+=k1
                    out+=out1
                if checkendotherdia(dic,color,x,y)!=False:
                    (k1,out1)=checkendotherdia(dic,color,x,y)
                    k+=k1
                    out+=out1
                if checkendolastdia(dic,color,x,y)!=False:
                    (k1,out1)=checkendolastdia(dic,color,x,y)
                    k+=k1
                    out+=out1
           
                if k>0:
                
                    possiblemoves[str(x)+","+str(y)]=(int(k), out)

    return possiblemoves
       
def checkthatthereisamove(movenumber,dic,move):
    
    for x in range(8):
        for y in range(8):

            if checkpiecenosorry(str(x)+","+str(y),movenumber,dic,move):
            
                return True
    return False
    

def init_board():
    """
    Returns a fresh Othello board as a dict:
    key   = "row,col"
    value = "black" or "white"
    """
    return {
        "3,3": "white",
        "3,4": "black",
        "4,3": "black",
        "4,4": "white"
    }


def main_test(computerblack,computerwhite,randomblack,randomwhite, chat_gpt_black, chat_gpt_white, aimodel_black,aimodel_white, weights,):
  
    done1=False
    move='black'
    movenumber=1
    dic={}
    #there are four pieces already on the board
    dic['3,3']='white'
    dic['4,4']='white'
    dic['4,3']='black'
    dic['3,4']='black'
    aimodel= aimodel.model()
    while not done1:
        done = False
        #need to make sure there is a place to put the piece
        if checkthatthereisamove(movenumber,dic,'black'):
          
            if computerblack:
                coordinates=  computer.playcom(movenumber,dic,'black', weights)
            elif randomblack:
                coordinates= randombot.randomplaycom(movenumber,dic,'black')
            elif chat_gpt_black:
                coordinates= chatgpt.playcom(movenumber,dic,'black')
            elif aimodel_black:
                coordinates= aimodel.playcom(movenumber,dic,'black', weights)
            x=int(coordinates[0])
            y=int(coordinates[2])
        
            flip(coordinates,movenumber,dic,'black')
            dic[coordinates] = move
       
       

            "it is whites turn "
        else:
            done = True
        if checkthatthereisamove(movenumber,dic,'white'):
            
            if computerwhite:
                o= computer.playcom(movenumber,dic,'white', weights)
            elif randomwhite:
                o= randombot.randomplaycom(movenumber,dic,'white')
            elif chat_gpt_white:
                o= chatgpt.playcom(movenumber,dic,'white')
            elif aimodel_white:
                o= aimodel.playcom(movenumber,dic,'white', weights)
            x=int(o[0])
            y=int(o[2])
         
            flip(o,movenumber,dic,'white')
            dic[o] = 'white'
           

        elif done:
          
            return donecount(dic)
            done1=True
        movenumber+=2