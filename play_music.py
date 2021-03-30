from pynput import keyboard
import time
import threading
import re

kb = keyboard.Controller()
slot_time_raw = 0.6

def play_notes():
    #str = "12311231345_345_56543_1_56543_1_2_5-_1_0_2_5-_1_0_"#two tigers
    fo = open('wind.txt', 'r')
    slot_time = 0.18
    str = fo.read()
    str = re.sub(r'^//.*\n?', '', str, flags=re.MULTILINE)
    fo.close()
    str = str.replace('\n', '').replace(' ', '').replace('|', '')
    for i in range(0,len(str)):
        print('{0}'.format(str[i]))
        if(str[i]<='7' and str[i]>='1'):
            index_val = int(str[i])+7-1
            if(i<len(str)-1):#check for + and -
                if(str[i+1]=='+'):
                    index_val-=7
                elif(str[i+1]=='-'):
                    index_val+=7
            play_note(index_val)
            time.sleep(slot_time)
        elif(str[i]=='_'):#skip space
            time.sleep(slot_time)
        elif(str[i]=='m'):
            slot_time = 0.2
        elif(str[i]=='h'):
            slot_time = 0.18

def play_notes_raw():
    str = open('fish.txt', 'r').read()
    str = str.lower().replace('\n', '')
    tag = False;
    for i in range(0,len(str)):
        if(str[i]=='('):
            tag = True;
        elif(str[i]==')'):
            tag = False;
            time.sleep(slot_time_raw)
        elif(str[i]==' '):
            time.sleep(slot_time_raw)
        else:
            play_note_raw(str[i],0 if tag else slot_time_raw)
        
def play_note_raw(note, delay_time):
    kb.tap(note)
    time.sleep(delay_time)

def play_note(note_index):
    keys = "qwertyu"+"asdfghj"+"zxcvbnm"
    kb.press(keys[note_index])
    kb.release(keys[note_index])#index start from 0

def on_press(key):
    '''
    try:
        print('alphanumeric key {0} pressed'.format(key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
    '''

def on_release(key):

    if(key == keyboard.Key.space):
        th = threading.Timer(2.0, play_notes)
        th.start()
    if(key == keyboard.Key.alt_l):
        th_raw = threading.Timer(2.0, play_notes_raw)
        th_raw.start()
    if key == keyboard.Key.alt_gr:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()
