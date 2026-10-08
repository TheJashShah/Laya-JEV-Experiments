# from pynput.mouse import Listener, Button
# from pynput.keyboard import Listener as KeyBoardListener, Key

# clicks = 0

# def on_press(key):
#     if key == Key.esc:
#         listener.stop()
#         keyboard_listener.stop()

# def on_click(x, y, button, pressed):
    
#     global clicks
    
#     if pressed and button == Button.left:
#         clicks += 1
#         print(f"x = {x} and y = {y} | clicks = {clicks}")

# listener = Listener(on_click=on_click)  
# keyboard_listener = KeyBoardListener(on_press=on_press)

# listener.start()
# keyboard_listener.start()
# keyboard_listener.join()

# SIMPLE CODE TO CAPTURE MOUSE CO-ORDINATES ON LEFT CLICK.

'''
x = 1441 and y = 1067 | clicks = 1
x = 638 and y = 317 | clicks = 2
x = 1262 and y = 318 | clicks = 3
x = 1263 and y = 937 | clicks = 4
x = 637 and y = 937 | clicks = 5
x = 1766 and y = 26 | clicks = 6

clicks 1 and 6 are noise. From 2 to 5 are the co-ordinates of the 2048 game on my screen.
From top-left, clockwise.
'''

# import pyscreenshot
# image = pyscreenshot.grab()

# image.show()

# image_second = pyscreenshot.grab(bbox=(100, 200, 200, 700)) # x1, y1, x2, y2 | top_left, bottom_right
# image_second.show()

# PYSCREENSHOT CODE TO CAPTURE SCREENSHOT. NOW WE HAVE TO CONNECT KEY CAPTURE AND SCREENSHOT USING THE COORDINATES.

from pynput.keyboard import Listener as KeyboardListener, Key
import pyscreenshot
import os

root = os.getcwd()
sample_folder = os.path.join(root, "Game", "sample_images")

top_left = (638, 317)
bottom_right = (1263, 937)

images = 0

def on_press(key):
    
    global images
    
    keys = {Key.left, Key.right, Key.up, Key.down}
    
    if key in keys:
        images += 1
        image = pyscreenshot.grab(bbox=(top_left[0], top_left[1],bottom_right[0], bottom_right[1]))
        image.save(os.path.join(sample_folder, f"image_{images}.png"))
        
    if key == Key.esc:
        keyboard_listener.stop()
        
keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()
keyboard_listener.join()