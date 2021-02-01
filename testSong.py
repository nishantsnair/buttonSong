import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer
from mutagen.mp3 import MP3

from pynput import keyboard

global songs
songdir = "songs"
def stop_music():
    mixer.music.stop()

def start_count(t):
    global paused
    # global stop_threads 
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and mixer.music.get_busy():
        if paused:
            continue
        # elif stop_threads:
            # return
        else:
            mins, secs = divmod(current_time, 60)
            mins = round(mins)
            secs = round(secs)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            # currenttimelabel['text'] = "Current Time" + ' - ' + timeformat
            time.sleep(1)
            print(current_time)
            current_time += 1
paused = False
mixer.init()  
stop_music()
time.sleep(1)
playlist = os.listdir(songdir)
playlist = [os.path.abspath(songdir+"\\"+song) for song in playlist]
play_it = playlist[0]


mixer.music.load(play_it)
mixer.music.play()

def on_press(key):
    try:
        print('alphanumeric key {0} pressed'.format(
            key.char))
    except AttributeError:
        print('special key {0} pressed'.format(
            key))
            
def on_release(key):
    global paused
    print('{0} released'.format(
        key))
    if key == keyboard.Key.enter:
        if paused:
            print('resuming')
            mixer.music.unpause()
            paused = not paused
        else:
            print('pausing')
            mixer.music.pause()
            paused = not paused
    if key == keyboard.Key.esc:
        # Stop listener
        
        return False

paused = False
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
