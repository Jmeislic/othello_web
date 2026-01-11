import random
import just_for_testing as  main

def randomplaycom(movenumber,dic,color):
    possiblemoves=main.findpossiblemoves(movenumber,dic,color)
    arr = []
    for i in possiblemoves.keys():
        arr.append(i)
    

    return arr[random.randint(0,len(arr)-1)]
