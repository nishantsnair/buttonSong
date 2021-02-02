import os # for reading files in directories
import threading    # for starting a thread with button inputs, currently does nothing
import time # with time we sleep
import random # to choose a ranom funny sound

# for playing pausing stopping queuing music
import pygame 
from pygame import mixer, display, USEREVENT, event

# for input from keyboard
from pynput import keyboard

# define directory names
song_dir = "songs"
funny_dir = "funny"


def stop_music():
    """All channels are stopped"""
    song_channel.stop()
    funny_channel.stop()

def makeplaylist(songdir):
    """Given a directory makes a sound object list for all songs in directory"""
    playlist = os.listdir(songdir)
    playlist = [os.path.abspath(songdir+"\\"+song) for song in playlist]
    playlist = [mixer.Sound(song) for song in playlist]
    return playlist
    
def on_press(key):
    """Let's do nothing for now"""
    pass
    
def on_release(key):
    """On releasing key"""
    global stop
    # if spacebar pressed
    if key == keyboard.Key.space:
        print('pausing')
        # pause the current song playing
        song_channel.pause()
        print('playing randome sound')
        # get a random sound from all funny sounds
        play_funny = random.choice(funny_list)
        # play the random sound
        funny_channel.play(play_funny)
        print('resuming')
        # sleep for duration of funny sounds
        time.sleep(play_funny.get_length())
        # resume the songs
        song_channel.unpause()
    if key == keyboard.Key.esc:
        # Stop listener
        stop = True
        stop_music()
        return False
        
# start the mixer for playing sounds
mixer.init()
# display needed to get a event when one song ends
display.init()

# create a song channel
song_channel = mixer.Channel(0)
# create a funny sound channel
funny_channel = mixer.Channel(1)

# make sure everything is stopped  
stop_music()
time.sleep(1)

# get list of sounds
song_list = makeplaylist(song_dir)
# get list of funny sounds
funny_list = makeplaylist(funny_dir)

# get first song from song list
play_song_1 = song_list[0]

# play first song
song_channel.play(play_song_1)

# queue the next song
song_channel.queue(song_list.pop())
# set an endevent to mark end of current song
song_channel.set_endevent(USEREVENT)

stop = False

# start a listener for keyboard keys
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()


while True:
    for event in pygame.event.get():
        # if one song has ended
        if event.type == USEREVENT:
            print("Playing Next")
            # if more songs are left
            if len ( song_list ) > 0:
                # queue the next song
                song_channel.queue ( song_list.pop() ) # Q
            else:
                listener.stop()
                break
    if stop:
        break