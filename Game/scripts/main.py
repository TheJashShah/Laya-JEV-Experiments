from laya_inference import ask_laya_prompt
from image_to_text import read_board, annotate, board_to_text
from illegal_moves import legal_moves
from collections import Counter
import itertools

import os
import pyautogui
import time


'''
main flow (as of now):

run code -> wait for 2s -> press enter key -> first ss -> laya -> all other ss -> regular flow.
'''

from pynput.keyboard import Listener as KeyboardListener, Key
import pyscreenshot
import os

import laya
agent = laya.load("convaiinnovations/laya")

root = os.getcwd()
game_folder = os.path.join(root, "Game", "Sample_Game")
os.makedirs(game_folder, exist_ok=True)

img_folder = os.path.join(game_folder, "images")
annot_folder = os.path.join(game_folder, "annot_images")

os.makedirs(img_folder, exist_ok=True)
os.makedirs(annot_folder, exist_ok=True)

log_file = os.path.join(game_folder, "log.txt")

top_left = (638, 317)
bottom_right = (1263, 937)
moves = 0
current_move = None

def count_zeros(board):
    totals = Counter(i for i in list(itertools.chain.from_iterable(board)))
    return totals[0]

def on_press(key):
    
    global moves
    
    keys = {Key.left, Key.right, Key.up, Key.down}
    
    if key == Key.esc:
        keyboard_listener.stop()
    
    if moves == 0:
        if key == Key.enter:
            image = pyscreenshot.grab(bbox=(top_left[0], top_left[1],bottom_right[0], bottom_right[1]))
            image.save(os.path.join(img_folder, f"Image_first.png"))
            
            img, board = read_board(image)
            legal_move_list = legal_moves(board)
            board_text = board_to_text(board)
            _ = annotate(img, board, os.path.join(annot_folder, f"Annot_Image_first.png"))

            current_move = ask_laya_prompt(agent=agent, board=board_text, legal_moves=legal_move_list)
            
            with open(log_file, "a") as f:
                f.write("Current Board: \n")
                f.write(board_text)
                f.write("\n")
                f.write(f"Move Played: {current_move}\n")
                f.write("======\n")
            
            moves += 1
            pyautogui.press(current_move)
            
    elif moves > 0:
        
        if key in keys:
            
            image = pyscreenshot.grab(bbox=(top_left[0], top_left[1],bottom_right[0], bottom_right[1]))
            image.save(os.path.join(img_folder, f"Image_{moves}.png"))
            
            img, board = read_board(image)
            
            if count_zeros(board) == 0:
                with open(log_file, "a") as f:
                    f.write("Game has ended.")
                    f.write("=====\n")
                    
                keyboard_listener.stop()
            
            legal_move_list = legal_moves(board)
            board_text = board_to_text(board)
            _ = annotate(img, board, os.path.join(annot_folder, f"Annot_Image_{moves}.png"))

            current_move = ask_laya_prompt(agent=agent, board=board_text, legal_moves=legal_move_list)
            
            with open(log_file, "a") as f:
                f.write("Current Board: \n")
                f.write(board_text)
                f.write("\n")
                f.write(f"Move Played: {current_move}\n")
                f.write("======\n")
    
            moves += 1
            pyautogui.press(current_move)
            
keyboard_listener = KeyboardListener(on_press=on_press)
keyboard_listener.start()
keyboard_listener.join()