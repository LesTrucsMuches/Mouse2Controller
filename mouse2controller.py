# --------------------------
# --  mouse to controller --
# --------------------------
# Le mouvement de la souris va déclencher les flèches (haut,droit,bas,gauche)
# le clique gauche active la barre d'espace
# le clique droit active le ctrl de gauche
# le clique du centre active le ctrl de droite
# pour quitter le script appuyer sur echap et attendre environ 1 seconde
# les boutons peuvent être modifié plus bas
# ---------------------------
# installer la libray pynput (pip install pynput)
#

from pynput import mouse, keyboard
import time
import threading
from math import atan2, degrees


#Mouse Sensibility
thresholdX = 5
thresholdY = 5
#time in seconde before release direction
run_time_threshold = 0.6
walk_time_threshold = 0.1
#clock in second
clock = 0.03
#buttons
left_click = keyboard.Key.space
right_click = keyboard.Key.ctrl_l
middle_click = keyboard.Key.ctrl_r
up = keyboard.Key.up
down = keyboard.Key.down
right = keyboard.Key.right
left = keyboard.Key.left
escape = keyboard.Key.esc

#Ne pas toucher à partir d'ici
exit_flag = False
lastX = 0
lastY = 0
GlobalX = 0
GlobalY = 0
run = False
last_wrapscreen_time = time.time()
last_movement_time_X = time.time()
last_movement_time_Y = time.time()

def calculate_angle(x, y):
    angle_rad = atan2(y, x)
    angle_deg = degrees(angle_rad)
    if angle_deg < 0:
        angle_deg += 360.0
    return angle_deg

def main():
    global last_movement_time_X, last_movement_time_Y,GlobalX,GlobalY
    global run_time_threshold
    global up, left,right, down
    mymouse = mouse.Controller()
    while True:

        current_time = time.time()
        if run:
            if current_time - last_movement_time_X >= run_time_threshold:
                GlobalX = 0
            if current_time - last_movement_time_Y >= run_time_threshold:
                GlobalY = 0
        else:
            if current_time - last_movement_time_X >= walk_time_threshold:
                GlobalX = 0
            if current_time - last_movement_time_Y >= walk_time_threshold:
                GlobalY = 0
        
        if GlobalX  == 1 :
            keyboard.Controller().release(left)
            keyboard.Controller().press(right)
        if GlobalX == -1:
            keyboard.Controller().release(right)
            keyboard.Controller().press(left)
        if GlobalX == 0:
            keyboard.Controller().release(right)
            keyboard.Controller().release(left)
        if GlobalY == 1:
            keyboard.Controller().release(up)
            keyboard.Controller().press(down)
        if GlobalY == -1:
            keyboard.Controller().release(down)
            keyboard.Controller().press(up)
        if GlobalY == 0:
            keyboard. Controller().release(up)
            keyboard.Controller().release(down)
        
        #screenwrap
        if mymouse.position[0] > 1910 :
            mymouse.position = (12,mymouse.position[1])
        elif mymouse.position[0] < 10: 
            mymouse.position = (1908 ,mymouse.position[1])
        if mymouse.position[1] > 1070:
            mymouse.position = (mymouse.position[0],12)
        elif mymouse.position[1] < 10: 
            mymouse.position = (mymouse.position[0],1068)
        #check if mouse move
        on_move(mymouse.position[0],mymouse.position[1])
        #clock
        time.sleep(clock)


def on_click(x, y, button, pressed):
    global run, exit_flag
    global left_click, right_click, middle_click
    if exit_flag == True:
        return False
    if button == mouse.Button.left and pressed:
        keyboard.Controller().press(left_click)
        print("left click")
    elif button == mouse.Button.left and not pressed:
        keyboard.Controller().release(left_click)
        print("left click release")
    if button == mouse.Button.right and pressed:
        keyboard.Controller().press(right_click)
        run = True
        print("right click")
    elif button == mouse.Button.right and not pressed:
        keyboard.Controller().release(right_click)
        run = False
        print("right click release")
    if button == mouse.Button.middle and pressed:
        keyboard.Controller().press(middle_click)
        print("middle click")
    elif button == mouse.Button.middle and not pressed:
        keyboard.Controller().release(middle_click)
        print("middle click release")

def on_move(x, y):
    global lastX, lastY, GlobalX, GlobalY, last_movement_time_X, last_movement_time_Y,exit_flag
    global thresholdX, thresholdY
    # 0 to 60 & 300 to 360 = right
    # 50 to 130 = down
    # 120 to 240 = left
    # 210 to 330 = top
    angle = calculate_angle(x - lastX,y - lastY)
    #print( angle)
    
    if ((angle >= 0 and angle <= 60) or (angle >= 300 and angle <= 360)) and (abs(x-lastX) > thresholdX) and (abs(x-lastX) < 500):
        print("move right : " + str(x))
        last_movement_time_X = time.time()
        GlobalX = 1
        #print(abs(x-lastX))
    if (angle >= 50 and angle <= 130) and (abs(y-lastY) > thresholdY) and (abs(y-lastY) < 500):
        print("move down : " + str(y))
        last_movement_time_Y = time.time()
        GlobalY = 1
    if (angle >= 120 and angle <= 240) and (abs(x-lastX) > thresholdX) and (abs(x-lastX) < 500):
        print("move left : " + str(x))
        last_movement_time_X = time.time()
        GlobalX = -1
 
    if (angle >= 210 and angle <= 330)and (abs(y-lastY) > thresholdY) and (abs(y-lastY) < 500):
        print("move  up : " + str(y))
        last_movement_time_Y = time.time()
        GlobalY = -1
    lastX = x 
    lastY = y
    if exit_flag == True:
        return False
def on_key_press(key):
    global exit_flag, escape
    if key == escape:  # Vérifiez si la touche "Esc" est pressée
        print("Le script se termine.")
        exit_flag = True  # Définissez le drapeau pour terminer le script
        mouse.Controller().click(mouse.Button.right,1)
        return False  # Retournez False pour arrêter l'écoute du clavier

 
    
inactivity_thread = threading.Thread(target=main)
inactivity_thread.daemon = True  # Terminer le thread lorsque le programme principal se termine
inactivity_thread.start()

# Créez des écouteurs de clavier et de souris
keyboard_listener = keyboard.Listener(on_press=on_key_press)
mouse_listener = mouse.Listener(on_click=on_click)

# Démarrer les écouteurs de clavier et de souris
keyboard_listener.start()
mouse_listener.start()

# Attendre la terminaison du script
keyboard_listener.join()
mouse_listener.join()
