import pyautogui
import time
import pytesseract

time.sleep(2)

def rectify_str(text):
    text = str.replace(text,'A','4')
    text = str.replace(text,'T','7')
    if text == '' or text == None:
        #print(1)
        src_1 = pyautogui.locateOnScreen('1_angle.png')
        if src_1 != None:
            text = '1'
    return text
def read_from_screen(need):
    angle_box = [941, 0, 982, 23]
    coord_box = [1025, 812, 1131, 833]
    if need == 'angle':
        needed_box = angle_box
    if need == 'coord':
        needed_box = coord_box
    sc = pyautogui.screenshot()
    photo_box = sc.crop(needed_box)
    if need == 'angle':
        photo_box.save('cropped.png')
    text = pytesseract.image_to_string(photo_box)
    text = rectify_str(text)
    try :
        text = int(text)
    except :
        pass
    return text
def read_folder(coord_file_name):
    with open(coord_file_name, "r") as file:
        vector = [line.strip() for line in file]
    return vector
def remake_vector(vector):
    vector2 = []
    for element in vector:
        coords = []
        i=0
        while i < len(element):
            coords.append([float(element[i:i+5]),float(element[i+6:i+11])])
            i = i + 14
        vector2.append(coords)
    return vector2

vector = read_folder('coords_torghast.txt')
vector = remake_vector(vector)
for el in vector:
    print(el)