import time
from pynput import keyboard
import threading
import os
import random

def clear():
    # for windows
    if os.name == 'nt':
        os.system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        os.system('clear')

def on_press(key):
    global jmp
    jmp = True

inf = {
    "enemies":[],
    "me":[1,0],
    "base-rows":50,
    "base-columns":24,
    "base-size":1250,
    "base":""
}
def calc(coord):
    return (coord[0])+(coord[1]*inf["base-rows"])

def generic():
    global inf, alive
    if inf["me"] in inf["enemies"]:
        alive = False
        return
    inf["base"] = ""
    enemies = []
    i = 0
    while i < len(inf["enemies"]):
        inf["enemies"][i][0] -= 1
        if inf["enemies"][i][0] == -1:
            del inf["enemies"][i]
        i+=1
    for a in inf["enemies"]:
        enemies.append(calc(a))
    i = 1
    for a in range(inf["base-size"]):
        if a in enemies:
            inf["base"] += "-"
        if a == calc(inf["me"]):
            inf["base"] += "█"
        else:
            inf["base"] += " "
        if i == inf["base-rows"]:
            i = 0
            inf["base"] += '\n'
        i += 1

def jump():
    global inf
    if inf["me"][1] != 0:
        inf["me"][1] -= 1
    generic()

def fall():
    global inf
    if inf["me"][1] != inf["base-columns"]:
        inf["me"][1] += 1
    generic()
jmp = False
alive = True
def threaded():
    global jmp
    while alive:
        # Collect events until released
        if jmp:
            jump()
        else:
            fall()
        clear()
        print("\n"+inf["base"])
        jmp = False
        time.sleep(0.5)
        if random.randint(0,100) < 75:
            inf["enemies"].append([random.randint(10, inf["base-columns"]), random.randint(0, inf["base-rows"])])
    while True:
        clear()
        print("""
        
        
                                               GAME OVER!!!
        
        
        """)
        time.sleep(1.5)
        clear()
        print("\n" + inf["base"])
        time.sleep(1.5)

threading.Thread(args=(), target=threaded).start()
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()