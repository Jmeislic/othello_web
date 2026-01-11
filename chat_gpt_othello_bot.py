import just_for_testing as main
import random

def playcom(movenumber, dic, color):
    possiblemoves = main.findpossiblemoves(movenumber, dic, color)

    corners = ['0,0','0,7','7,0','7,7']
    xsquares = ['1,1','1,6','6,1','6,6']

    scored = []

    for m in possiblemoves:
        x = int(m[0])
        y = int(m[2])
        score = 0

        # corners
        if m in corners:
            score += 1000

        # X-square suicide
        if m in xsquares:
            corner = str(0 if x < 4 else 7) + ',' + str(0 if y < 4 else 7)
            if corner not in dic:
                score -= 800

        # edge timing
        if x==0 or x==7 or y==0 or y==7:
            if movenumber < 30:
                score -= 50
            else:
                score += 40

        # mobility
        i, out = possiblemoves[m]
        if movenumber < 40:
            score += 4*i - 10*out
        else:
            score += 10*i

        scored.append((score, m))

    # sort by score
    scored.sort(reverse=True)

    # randomness: pick from top N
    if len(scored) >= 3:
        return random.choice(scored[:3])[1]
    else:
        return scored[0][1]
