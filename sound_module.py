# ----- Imports ----- #
import random
from pygame import mixer
import time
import pygame
import pickle
import os
global set_rumble

file = "set_rumble_file.pkl"
if os.path.exists(file):
    with open(file, "rb") as f:
        set_rumble = pickle.load(f)
if os.path.exists(file):
    os.remove(file)
# ----- Initialize Mixer ----- #
mixer.init()
mixer.set_num_channels(25)


# ----- Initialize Joystick ----- #
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()
if joystick_count > 0:
    joystick = pygame.joystick.Joystick(0)

# ----- Variables ----- #
Jump_count = False
global player_sprite
global run_sprite_right
global run_sprite_left

# ------------------------------------------ P L A Y   S O U N D   E F F E C T S ------------------------------------------ #

# Stamina = Zero
def stamina_zero_sound():
    sta1 = mixer.Sound('stamina_zero.wav')
    sta1.set_volume(0.5)
    sta2 = mixer.find_channel()
    sta2.play(sta1)

# Jump Sound
def jump_sound():
    Jump_count = True
    random_jump_number = random.randint(1, 3)

    if random_jump_number == 1:
        jump1_1 = mixer.Sound('jump1.wav')
        jump1_2 = mixer.find_channel()
        jump1_1.set_volume(0.2)
        jump1_2.play(jump1_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.rumble(0, 0.4, 400)

    elif random_jump_number == 2:
        jump2_1 = mixer.Sound('jump2.wav')
        jump2_2 = mixer.find_channel()
        jump2_1.set_volume(0.2)
        jump2_2.play(jump2_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.rumble(0, 0.4, 400)

    elif random_jump_number == 3:
        jump3_1 = mixer.Sound('jump3.wav')
        jump3_2 = mixer.find_channel()
        jump3_1.set_volume(0.2)
        jump3_2.play(jump3_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.rumble(0, 0.4, 400)



# Land Sound
def land_sound():
    global joystick
    random_land_number = random.randint(1, 3)

    if random_land_number == 1:
        land1_1 = mixer.Sound('land1.wav')
        land1_2 = mixer.find_channel()
        land1_1.set_volume(0.6)
        land1_2.play(land1_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.rumble(1, 1, 100)

    elif random_land_number == 2:
        land2_1 = mixer.Sound('land2.wav')
        land2_2 = mixer.find_channel()
        land2_1.set_volume(0.6)
        land2_2.play(land2_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.rumble(1, 1, 100)

    elif random_land_number == 3:
        land3_1 = mixer.Sound('land3.wav')
        land3_2 = mixer.find_channel()
        land3_1.set_volume(0.6)
        land3_2.play(land3_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.rumble(1, 1, 100)

# Death Sound
def death_sound():
    random_death_number = random.randint(1, 3)

    if random_death_number == 1:
        die1_1 = mixer.Sound('die1.wav')
        die1_2 = mixer.find_channel()
        die1_1.set_volume(0.55)
        die1_2.play(die1_1)
    elif random_death_number == 2:
        die2_1 = mixer.Sound('die2.wav')
        die2_2 = mixer.find_channel()
        die2_1.set_volume(0.75)
        die2_2.play(die2_1)
    elif random_death_number == 3:
        die3_1 = mixer.Sound('die3.wav')
        die3_2 = mixer.find_channel()
        die3_1.set_volume(0.8)
        die3_2.play(die3_1)

# Win Sound
def win_sound():
    random_win_number = random.randint(1, 2)

    if random_win_number == 1:
        win1_1 = mixer.Sound('win1.wav')
        win1_2 = mixer.find_channel()
        win1_1.set_volume(0.40)
        win1_2.play(win1_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.stop_rumble()
                joystick.rumble(3, 10, 400)

    elif random_win_number == 2:
        win2_1 = mixer.Sound('win2.wav')
        win2_2 = mixer.find_channel()
        win2_1.set_volume(0.40)
        win2_2.play(win2_1)
        if joystick_count > 0:
            if set_rumble == True:
                joystick.stop_rumble()
                joystick.rumble(3, 10, 400)


def win_sound10():
    win10_1 = mixer.Sound("win10.wav")
    win10_2 = mixer.find_channel()
    win10_1.set_volume(0.40)
    win10_2.play(win10_1)
    if joystick_count > 0:
        if set_rumble == True:
            joystick.stop_rumble()
            joystick.rumble(3, 10, 4000)




# Hit Left Wall Sound
def hit_left_wall():
    hit_wall1 = mixer.Sound('hit_left_wall.wav')
    hit_wall1.set_volume(1)
    hit_wall2 = mixer.find_channel()
    hit_wall2.play(hit_wall1)
    if Jump_count == True:
        if joystick_count > 0:
            if set_rumble == True:
                joystick.stop_rumble()
                joystick.rumble(0.6, 10, 190)
                jump_count == False
    elif Jump_count == False:
        if joystick_count > 0:
            if set_rumble == True:
                joystick.rumble(0.6, 10, 190)


# ------------------------------------------ P L A Y   M U S I C ------------------------------------------ #
# Background Sound
first = 0
NEXT = pygame.USEREVENT + 1


def background_sound():
    NEXT = pygame.USEREVENT + 1
    global first
    if first == 0:
        mixer.music.load('song1.mp3')
        mixer.music.set_volume(0.5)
        first += 1
        mixer.music.play()
    elif first == 1:
        pass

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song2.wav')
            mixer.music.play()

    mixer.music.set_endevent(NEXT)

    for event in pygame.event.get():
        if event.type == NEXT:
            mixer.music.queue('song1.mp3')
            mixer.music.play()

        mixer.music.set_endevent(NEXT)

# Pause Music
def music_pause():
    mixer.music.pause()

# Play Music
def music_play():
    mixer.music.unpause()


# Restart Sound
restart1 = mixer.Sound('Restart.wav')
restart2 = mixer.find_channel()


def restart_sound():
    restart2.play(restart1)
    if joystick_count > 0:
        if set_rumble == True:
            joystick.stop_rumble()
            joystick.rumble(1, 10, 1)
    Jump_count == False

# Controller Connected Sound
def controller_connected_sound():
    connected1 = mixer.Sound("controller_connected.mp3")
    connected2 = mixer.find_channel()
    connected2.play(connected1)

# Controller Disconnected Sound
def controller_disconnected_sound():
    disconnected1 = mixer.Sound("controller_disconnect.mp3")
    disconnected2 = mixer.find_channel()
    disconnected2.play(disconnected1)

# Stop Sound
def stop_sound_all():
    mixer.music.stop()

# Rumble Connected
def rumble_connected():
    joystick.stop_rumble()
    joystick.rumble(1, 1, 100)

# Rumble Stop
def rumble_stop():
    joystick.stop_rumble()


