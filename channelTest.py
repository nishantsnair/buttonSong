import os
import threading
import time
import tkinter.messagebox
from tkinter import *
from tkinter import filedialog

from tkinter import ttk
from ttkthemes import themed_tk as tk

from mutagen.mp3 import MP3
from pygame import mixer, display, USEREVENT, event
from mutagen.mp3 import MP3

from pynput import keyboard

global songs


song_dir = "songs"
funny_dir = "funny"
def stop_music():
    channel1.stop()

def start_count(t):
    global paused
    # global stop_threads 
    # mixer.music.get_busy(): - Returns FALSE when we press the stop button (music stop playing)
    # Continue - Ignores all of the statements below it. We check if music is paused or not.
    current_time = 0
    while current_time <= t and channel1.music.get_busy():
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
display.init()
channel1 = mixer.Channel(0)
channel2 = mixer.Channel(1)
  
stop_music()
time.sleep(1)

def makeplaylist(songdir):
    playlist = os.listdir(songdir)
    playlist = [os.path.abspath(songdir+"\\"+song) for song in playlist]
    playlist = [mixer.Sound(song) for song in playlist]
    return playlist
    
playlist1 = makeplaylist(song_dir)
playlist2 = makeplaylist(funny_dir)
play_it = playlist1[0]


# channel1.load(playlist1.pop())
channel1.queue(playlist1.pop())
channel1.set_endevent(USEREVENT)
channel1.play(play_it)

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
    if key == keyboard.Key.space:
        if paused:
            print('resuming')
            channel1.unpause()
            paused = not paused
        else:
            print('pausing')
            channel1.pause()
            paused = not paused
    if key == keyboard.Key.esc:
        # Stop listener
        
        return False

paused = False
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
    while True:
        for event in event.get():
            if event.type == USEREVENT:    # A track has ended
                print("Playing Next")
                if len ( playlist1 ) > 0:       # If there are more tracks in the queue...
                    channel1.queue ( playlist1.pop() ) # Q
