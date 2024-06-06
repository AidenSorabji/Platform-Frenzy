import customtkinter
from PIL import Image
import sound_module
import pygame
import os
import subprocess
import sys
import pickle

# ----- Initialize Joystick ----- #
pygame.joystick.init()
joystick_count = pygame.joystick.get_count()

rumble_switch = False
play_controller_sound_once = False
disconnected_controller_sound = False
controller_connected = False
test_rumble = False
set_rumble = False

def rumble_settings():
    return set_rumble

controller_window = customtkinter.CTk()
controller_window.overrideredirect(True)

# Get screen width and height
w = 397
h = 130

# Get screen width and height
ws = controller_window.winfo_screenwidth()
hs = controller_window.winfo_screenheight()

# Calculate x and y coordinates for the Tk root window
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)

# Set the dimensions of the screen
controller_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
controller_window._set_appearance_mode("light")
controller_window.title("")
controller_window.resizable(False, False)
controller_window._disable_macos_dark_title_bar()

# Cooler border
cooler_border = customtkinter.CTkFrame(controller_window,
                                       width=397,
                                       height=130,
                                       fg_color="#eaeaeb",
                                       bg_color="#eaeaeb",
                                       border_color="#d9dbdb",
                                       border_width=5,
                                       corner_radius=0)
cooler_border.place(x=0, y=0)

def main_screen():
    global controls_callback
    # ------------------------------ Image ------------------------------ #
    controller_playstation = customtkinter.CTkImage(light_image=Image.open("ps5_controller.png"),
                                                    size=(172, 109))
    controller_label = customtkinter.CTkLabel(controller_window,
                                              image=controller_playstation,
                                              text="",
                                              bg_color="#eaeaeb")
    controller_label.place(x=12, y=11)
    # ------------------------ Frame For Buttons ------------------------ #
    frame_buttons = customtkinter.CTkFrame(cooler_border,
                                           width=196,
                                           height=110,
                                           corner_radius=5,
                                           fg_color="#e1e3e3",
                                           bg_color="#eaeaeb",
                                           border_width=2,
                                           border_color="#dedede")
    frame_buttons.place(x=190, y=10)
    # ---------------------------- Da Buttons --------------------------- #
    def connected_change():
        controller_detect_button.configure(
            text="Connected", fg_color="#229442", border_color="#1e823a", border_width=3, font=customtkinter.CTkFont(size=13, weight="bold"))

    def not_connected_change():
        not_connected_text = """Not
Connected"""
        controller_detect_button.configure(
            text=not_connected_text, fg_color="#942222", border_color="#821e20", border_width=3, font=customtkinter.CTkFont(size=13, weight="bold"))

    controller_detect_button = customtkinter.CTkButton(controller_window,
                                                       width=90,
                                                       height=49,
                                                       text="--",
                                                       font=customtkinter.CTkFont(
                                                           size=15, weight="bold"),
                                                       text_color="black",
                                                       corner_radius=5,
                                                       border_color="#d7d9d8",
                                                       border_width=1,
                                                       bg_color="#e1e3e3",
                                                       hover=False,
                                                       fg_color="#dee0df")
    controller_detect_button.place(x=195, y=15)

    def check_controller_connect():
        global play_controller_sound_once, joystick_count, disconnected_controller_sound

        # Update joystick count
        pygame.joystick.init()
        joystick_count = pygame.joystick.get_count()

        if joystick_count > 0:
            try:
                controller_connected = True
                disconnected_controller_sound = False
                joystick = pygame.joystick.Joystick(0)
                joystick.init()
                connected_change()
                if controller_connected == True:
                    if play_controller_sound_once == True:
                        pass
                    elif play_controller_sound_once == False:
                        play_controller_sound_once = True
                        sound_module.controller_connected_sound()
                elif controller_connected == False:
                    pass
                pass
            except:
                pass
        elif joystick_count <= 0:
            controller_connected = False
            play_controller_sound_once = False
            if disconnected_controller_sound == False:
                disconnected_controller_sound = True
                sound_module.controller_disconnected_sound()
            elif disconnected_controller_sound == True:
                pass
            not_connected_change()
        pass
        controller_detect_button.after(100, check_controller_connect)

    def play_game(): # here
        print("hehe")
        current_dir = os.path.dirname(os.path.realpath(__file__))
        os.system(f"python3 {current_dir}/test.py")
        sys.exit()

    play_button = customtkinter.CTkButton(controller_window,
                                          width=90,
                                          height=49,
                                          text="Play!",
                                          font=customtkinter.CTkFont(
                                              size=15, weight="bold"),
                                          text_color="black",
                                          corner_radius=5,
                                          border_color="#d7d9d8",
                                          border_width=1,
                                          bg_color="#e1e3e3",
                                          hover_color="#d7d9d8",
                                          fg_color="#dee0df",
                                          command=play_game)
    play_button.place(x=195, y=67)

    def rumble_change():
        global rumble_switch, test_rumble
        if rumble_switch == True:
            rumble_switch = False
            test_rumble = False
            rumble_button.configure(text="Rumble: Off")
            set_rumble = False
            if joystick_count > 0:
                sound_module.rumble_stop()

        elif rumble_switch == False:
            rumble_switch = True
            rumble_button.configure(text="Rumble: On")
            set_rumble = True
            if test_rumble == False:
                test_rumble = True
                if joystick_count > 0:
                    sound_module.rumble_connected()

    rumble_button = customtkinter.CTkButton(controller_window,
                                            width=91,
                                            height=49,
                                            text="Rumble: Off",
                                            font=customtkinter.CTkFont(
                                                size=13, weight="bold"),
                                            text_color="black",
                                            corner_radius=5,
                                            border_color="#d7d9d8",
                                            border_width=1,
                                            bg_color="#e1e3e3",
                                            hover_color="#d7d9d8",
                                            fg_color="#dee0df",
                                            command=rumble_change)
    rumble_button.place(x=290, y=15)

    def controls_callback_():
        controls_callback(controller_label, frame_buttons,
                          controller_detect_button, play_button, rumble_button, controls_button)

    controls_button = customtkinter.CTkButton(controller_window,
                                              width=91,
                                              height=49,
                                              text="Controls",
                                              font=customtkinter.CTkFont(
                                                  size=15, weight="bold"),
                                              text_color="black",
                                              corner_radius=5,
                                              border_color="#d7d9d8",
                                              border_width=1,
                                              bg_color="#e1e3e3",
                                              hover_color="#d7d9d8",
                                              fg_color="#dee0df",
                                              command=controls_callback_)
    controls_button.place(x=290, y=67)
    check_controller_connect()

def controls_callback(controller_label, frame_buttons, controller_detect_button, play_button, rumble_button, controls_button):
    controller_label.place_forget()
    frame_buttons.place_forget()
    controller_detect_button.place_forget()
    play_button.place_forget()
    rumble_button.place_forget()
    controls_button.place_forget()
    w = 600
    h = 440
    ws = controller_window.winfo_screenwidth()
    hs = controller_window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    controller_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    cooler_border.configure(width=600, height=440)

    # Image Labels
    controller_outline = customtkinter.CTkImage(light_image=Image.open("controller_outline.png"),
                                                size=(250, 160))
    keyboard_outline = customtkinter.CTkImage(light_image=Image.open("keyboard_layout.png"),
                                              size=(304, 150))

    controller_outline_label = customtkinter.CTkLabel(controller_window,
                                                      image=controller_outline,
                                                      text="",
                                                      width=300,
                                                      height=150,
                                                      bg_color="#eaeaeb")
    controller_outline_label.place(x=6, y=20)

    keyboard_outline_label = customtkinter.CTkLabel(controller_window,
                                                    image=keyboard_outline,
                                                    text="",
                                                    bg_color="#eaeaeb")
    keyboard_outline_label.place(x=18, y=240)

    # Control Frames
    controller_button_frames = customtkinter.CTkFrame(controller_window,
                                                      width=289,
                                                      height=162,
                                                      fg_color="#e1e3e3",
                                                      bg_color="#eaeaeb",
                                                      border_width=4,
                                                      border_color="#dedede")
    controller_button_frames.place(x=294, y=20)

    keyboard_button_frames = customtkinter.CTkFrame(controller_window,
                                                    width=251,
                                                    height=150,
                                                    fg_color="#e1e3e3",
                                                    bg_color="#eaeaeb",
                                                    border_width=4,
                                                    border_color="#dedede")
    keyboard_button_frames.place(x=334, y=240)

    # Importing and Placing Icons + Write-Up
    x_button = customtkinter.CTkImage(light_image=Image.open("x_button_icon.png"),
                                      size=(30, 30))
    dpad_left = customtkinter.CTkImage(light_image=Image.open("dpad_left_icon.png"),
                                       size=(30, 30))
    dpad_right = customtkinter.CTkImage(light_image=Image.open("dpad_right_icon.png"),
                                        size=(30, 30))
    joystick_left = customtkinter.CTkImage(light_image=Image.open("joystick_left_icon.png"),
                                           size=(30, 30))
    trigger_right = customtkinter.CTkImage(light_image=Image.open("trigger_right_icon.png"),
                                           size=(30, 30))
    options_button = customtkinter.CTkImage(light_image=Image.open("options_icon.png"),
                                            size=(20, 30))
    share_button = customtkinter.CTkImage(light_image=Image.open("share_icon.png"),
                                          size=(15, 30))
    # Left Column
    dpad_left1 = customtkinter.CTkLabel(controller_window,
                                        image=dpad_left,
                                        text="",
                                        bg_color="#e1e3e3")
    dpad_left1.place(x=302, y=27)

    dpad_left_label = customtkinter.CTkLabel(controller_window,
                                             text=""" Move 
Left""",
                                             font=customtkinter.CTkFont(
                                                 size=11, weight="bold"),
                                             text_color="black",
                                             bg_color="#e1e3e3")
    dpad_left_label.place(x=340, y=27)

    joystick_left1 = customtkinter.CTkLabel(controller_window,
                                            image=joystick_left,
                                            text="",
                                            bg_color="#e1e3e3")
    joystick_left1.place(x=302, y=86)

    joystick_left_label = customtkinter.CTkLabel(controller_window,
                                                 text="Move",
                                                 font=customtkinter.CTkFont(
                                                     size=11, weight="bold"),
                                                 text_color="black",
                                                 bg_color="#e1e3e3")
    joystick_left_label.place(x=342, y=84)

    dpad_right1 = customtkinter.CTkLabel(controller_window,
                                         image=dpad_right,
                                         text="",
                                         bg_color="#e1e3e3")
    dpad_right1.place(x=302, y=145)

    dpad_right_label = customtkinter.CTkLabel(controller_window,
                                              text=""" Move 
Right""",
                                              font=customtkinter.CTkFont(
                                                  size=11, weight="bold"),
                                              text_color="black",
                                              bg_color="#e1e3e3")
    dpad_right_label.place(x=340, y=144)

    x_button1 = customtkinter.CTkLabel(controller_window,
                                       image=x_button,
                                       text="",
                                       bg_color="#e1e3e3")
    x_button1.place(x=403, y=56)

    x_button_label = customtkinter.CTkLabel(controller_window,
                                            text="Jump",
                                            font=customtkinter.CTkFont(
                                                size=11, weight="bold"),
                                            text_color="black",
                                            bg_color="#e1e3e3")
    x_button_label.place(x=441, y=56)

    trigger_right1 = customtkinter.CTkLabel(controller_window,
                                            image=trigger_right,
                                            text="",
                                            bg_color="#e1e3e3")
    trigger_right1.place(x=404, y=110)

    trigger_right_label = customtkinter.CTkLabel(controller_window,
                                                 text="Sprint",
                                                 font=customtkinter.CTkFont(
                                                     size=11, weight="bold"),
                                                 text_color="black",
                                                 bg_color="#e1e3e3")
    trigger_right_label.place(x=441, y=110)

    options_button1 = customtkinter.CTkLabel(controller_window,
                                             image=options_button,
                                             text="",
                                             bg_color="#e1e3e3")
    options_button1.place(x=505, y=56)

    options_button_label = customtkinter.CTkLabel(controller_window,
                                                  text="Restart",
                                                  font=customtkinter.CTkFont(
                                                      size=11, weight="bold"),
                                                  text_color="black",
                                                  bg_color="#e1e3e3")
    options_button_label.place(x=530, y=56)

    share_button1 = customtkinter.CTkLabel(controller_window,
                                           image=share_button,
                                           text="",
                                           bg_color="#e1e3e3")
    share_button1.place(x=508, y=110)

    share_button_label = customtkinter.CTkLabel(controller_window,
                                                text="Quit",
                                                font=customtkinter.CTkFont(
                                                    size=11, weight="bold"),
                                                text_color="black",
                                                bg_color="#e1e3e3")
    share_button_label.place(x=530, y=110)
    # ---------------------------------------------------------------------- #
    a_key_label = customtkinter.CTkLabel(controller_window,
                                         text="[A] - Move Left",
                                         font=customtkinter.CTkFont(
                                             size=13, weight="bold"),
                                         text_color="black",
                                         bg_color="#e1e3e3",
                                         height=8)
    a_key_label.place(x=340, y=245)

    transition1 = customtkinter.CTkLabel(controller_window,
                                         text="|",
                                         font=customtkinter.CTkFont(
                                             size=15, weight="bold"),
                                         text_color="black",
                                         bg_color="#e1e3e3",
                                         height=20)
    transition1.place(x=452, y=243)

    d_key_label = customtkinter.CTkLabel(controller_window,
                                         text="[D] - Move Right",
                                         font=customtkinter.CTkFont(
                                             size=13, weight="bold"),
                                         text_color="black",
                                         bg_color="#e1e3e3",
                                         height=8)
    d_key_label.place(x=470, y=245)

    space_key_label = customtkinter.CTkLabel(controller_window,
                                             text="[Space] - Jump",
                                             font=customtkinter.CTkFont(
                                                 size=13, weight="bold"),
                                             text_color="black",
                                             bg_color="#e1e3e3",
                                             height=8)
    space_key_label.place(x=340, y=307)

    transition3 = customtkinter.CTkLabel(controller_window,
                                         text="|",
                                         font=customtkinter.CTkFont(
                                             size=15, weight="bold"),
                                         text_color="black",
                                         bg_color="#e1e3e3",
                                         height=20)
    transition3.place(x=465, y=305)

    shift_key_label = customtkinter.CTkLabel(controller_window,
                                             text="[Shift] - Run",
                                             font=customtkinter.CTkFont(
                                                 size=13, weight="bold"),
                                             text_color="black",
                                             bg_color="#e1e3e3",
                                             height=8)
    shift_key_label.place(x=495, y=307)

    r_key_label = customtkinter.CTkLabel(controller_window,
                                         text="[R] - Restart",
                                         font=customtkinter.CTkFont(
                                             size=13, weight="bold"),
                                         text_color="black",
                                         bg_color="#e1e3e3",
                                         height=8)
    r_key_label.place(x=340, y=367)

    transition2 = customtkinter.CTkLabel(controller_window,
                                         text="|",
                                         font=customtkinter.CTkFont(
                                             size=15, weight="bold"),
                                         text_color="black",
                                         bg_color="#e1e3e3",
                                         height=20)
    transition2.place(x=464, y=365)

    zero_key_label = customtkinter.CTkLabel(controller_window,
                                            text="[0] - Quit",
                                            font=customtkinter.CTkFont(
                                                size=13, weight="bold"),
                                            text_color="black",
                                            bg_color="#e1e3e3",
                                            height=8)
    zero_key_label.place(x=516, y=367)

    def back_callback():
        set_rumble_file = 'set_rumble_file.plk'
        with open(set_rumble_file, "wb") as f:
            pickle.dump(set_rumble_file, f)


        controller_outline_label.place_forget()
        keyboard_outline_label.place_forget()
        controller_button_frames.destroy()
        keyboard_button_frames.destroy()
        dpad_right1.place_forget()
        dpad_left1.place_forget()
        dpad_left_label.destroy()
        dpad_right_label.destroy()
        joystick_left1.place_forget()
        joystick_left_label.destroy()
        x_button1.place_forget()
        x_button_label.destroy()
        trigger_right1.place_forget()
        trigger_right_label.destroy()
        options_button1.place_forget()
        options_button_label.destroy()
        share_button1.place_forget()
        share_button_label.destroy()
        a_key_label.destroy()
        d_key_label.destroy()
        shift_key_label.destroy()
        space_key_label.destroy()
        zero_key_label.destroy()
        r_key_label.destroy()
        transition1.destroy()
        transition2.destroy()
        transition3.destroy()
        # Get screen width and height
        w = 397
        h = 130

        # Get screen width and height
        ws = controller_window.winfo_screenwidth()
        hs = controller_window.winfo_screenheight()

        # Calculate x and y coordinates for the Tk root window
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)

        # Set the dimensions of the screen
        controller_window.geometry('%dx%d+%d+%d' % (w, h, x, y))
        controller_window._set_appearance_mode("light")
        controller_window.title("")
        controller_window.resizable(False, False)
        controller_window._disable_macos_dark_title_bar()
        cooler_border.configure(width=600, height=440)
        main_screen()

    back_button = customtkinter.CTkButton(controller_window,
                                          text="Back",
                                          font=customtkinter.CTkFont(
                                              size=15, weight="bold"),
                                          text_color="black",
                                          corner_radius=5,
                                          border_color="#d7d9d8",
                                          border_width=3,
                                          bg_color="#e1e3e3",
                                          hover_color="#d7d9d8",
                                          fg_color="#dee0df",
                                          width=567,
                                          height=30,
                                          command=back_callback)
    back_button.place(x=17, y=398)

main_screen()
controller_window.mainloop()
