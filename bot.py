import pyautogui
import time
import math
import keyboard
import random
import cv2
from modules import pathfinder as pf
from modules import image_to_string_module as tess

def read_from_screen(need: str):
    '''
    'angle' or 'coord'
    '''
    coord_box = [1022, 811, 1135-1022, 834-811]
    angle_box = [941, 0, 982-941, 23]
    box = angle_box
    if need == 'coord':
        box = coord_box
    if need == 'angle':
        box = angle_box
        
    sc = pyautogui.screenshot(region = box)
    sc.save('photo3.png')    
    photo_to_check = cv2.imread('photo3.png',cv2.COLOR_BGR2GRAY)
        
    text = tess.image_to_string(photo_to_check)
    print(text)
    return text
def read_folder(coord_file_name):
    with open(coord_file_name, "r") as file:
        vector = [line.strip() for line in file]
    vector = remake_vector(vector)
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
def calculate_angle(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1

    angle = math.degrees(math.atan2(dy, dx))
    angle = (angle + 360 + 90) % 360

    return angle
def nice_print(vector:list):
    for el in vector:
        print(el)
def enemy(need_to_check:bool = False):
    if need_to_check == False:
        return False
    enemy = pyautogui.locateOnScreen('check_health_bar.png',region=[1188, 662, 1443-1188, 747-662],confidence=0.9)
    if enemy:
        return True
    return False
def calculate_rotation_direction(current_angle, target_angle):
    if current_angle < target_angle:
        dif = target_angle - current_angle
        if dif <= 180:
            return "d",dif #right
        else:
            return "a",dif #left
    else:
        dif = current_angle - target_angle
        if dif <= 180:
            return "a",dif #left
        else:
            return "d",dif #right
def check_space():
    lc = []
    for i in range(1,5):
        ph = pyautogui.locateOnScreen('floors/floor_' + str(i) + '.png',region=[1475, 393, 1767, 477],confidence=0.9)
        lc.append(ph)
    for el in lc:
        if el != None:
            return lc.index(el)+1
    return 0
def check_map(space):
    if space == 0:
        return 0
    mp = []
def set_destination(space,mp):
    
    if space == 0 and mp == 0:
        destination = [50.0,27.0] 
        
    if space == 0:
        need_to_check = False
    else:
        need_to_check = True
    
    return destination,need_to_check
def menu_interaction(space,mp,destination):
    if space == 0 and mp == 0:
        lc = pyautogui.locateOnScreen('left_arrow.png',grayscale=True,region = [1121, 658, 1164-1121, 699-658])
        pyautogui.moveTo(pyautogui.center(lc))
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.2)
        
        lc = pyautogui.locateOnScreen('floor_1_icon.png',grayscale=True)
        pyautogui.moveTo(pyautogui.center(lc))
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.2)
        
        lc = pyautogui.locateOnScreen('climb_button.png',grayscale=True)
        pyautogui.moveTo(pyautogui.center(lc))
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(5)
        
        lc = pyautogui.locateOnScreen('accept_button.png',grayscale=True)
        pyautogui.moveTo(pyautogui.center(lc))
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.2)
time.sleep(2)

while keyboard.is_pressed('`') == False:
    #awareness
    space = check_space()
    mp = check_map(space=space)
    
    #locations
    nodes = read_folder('coords_torghast.txt')
    location = read_from_screen('coord')
    
    #set goals
    destination,need_to_check  = set_destination(space,mp)
    path = pf.pathfinding(nodes=nodes,location=location,destination=destination)
    step = 0
    
    #movement
    while enemy(need_to_check) == False and keyboard.is_pressed('`') == False:
        print('\n')
        angle = read_from_screen('angle')
        target_angle = calculate_angle(location[0],location[1],path[step][0],path[step][1],)
        print('target_angle: '+str(target_angle))
        print('path[step]: ' + str(path[step]))
        
        direction,dif_angle = calculate_rotation_direction(angle,target_angle)
        #if angle dif > 90 stop w
        if dif_angle > 90:
            keyboard.release('w')
        
        #if angle dif > 20 start rotating
        #if angle dif < 20 stop rotating
        if dif_angle > 20:
            keyboard.press(direction)
            time.sleep(dif_angle/180)
            keyboard.release(direction)
        
        #check location
        location = read_from_screen('coord')
        
        #if point reach the point go to next point
        if pf.calculate_distance(location,path[step]) < 2:
            if(step < len(path)-1):
                step=step+1
        else:
            keyboard.press('w')
        
        #if destination reach interact
        if pf.calculate_distance(location,destination) < 0.4:
            keyboard.release('w')
            time.sleep(2)
            menu_interaction(space,mp,destination)
            break
        #break
        
    keyboard.release('w')
    
    #fighting
    while enemy(need_to_check) == True and keyboard.is_pressed('`') == False:
        #verifica de vaza, daca e, click 4, daca nu, dai tare
        pass
        
    

