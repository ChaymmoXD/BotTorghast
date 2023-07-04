import numpy as np
import cv2

def image_to_string(photo_to_check):

    reference =[]
    for i in range(10):
        ref = cv2.imread('references/' + str(i) + '.png',cv2.COLOR_BGR2GRAY)
        reference.append([ref,i])

    result = []
    for ref,i in reference:
        res = cv2.matchTemplate(photo_to_check, ref, cv2.TM_CCOEFF_NORMED)
        result.append([res,i])

    threshold = 0.8
    locations = []

    for res,i in result:
        loc = np.where(res >= threshold)
        locations.append([loc,i])
    
    matches = []

    for loc,i in locations: 
        for pt in zip(*loc[::-1]):
            matches.append([pt,i])

    matches.sort(key=lambda x: x[0])

    #afisare fiecare element in parte cand e gasit intr un vector
    #for match,i in matches:
    #    print("{}: Match at (x={}, y={})".format(i,match[0], match[1]))

    text = ''
    count = 0
    for match,i in matches:
        if i == 1 :
            if count != 2 :
                count = count + 1
            else:
                text = text + str(i)
                count = 0
        else:
            text = text + str(i)

    
    if len(text) <= 3:
        text = int(text)
    else :
        text = [float(text[:2] + '.' + text[2:4]),float( text [4:6] + '.' + text[6:])]
        
    return text
