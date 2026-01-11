import just_for_testing as main

def human(movenumber,dic):
    possiblemoves=main.findpossiblemoves(movenumber,dic,'black')
    main.addplaces(possiblemoves)
    coordinates=str(input("what is the x and y cooridnates? (EX:'3,4') :"))
    return coordinates
