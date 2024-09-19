#© 2024 Ryan Noel Buenaventura.

import keyboard
import program_loop
from character import *
import design

class RestartException(Exception):
    pass

# NORMAL MAIN
# comment out main below for normal use
# this main does not display traceback error information
def main(stdscr):
    #stdscr = curses.initscr()
    design.AttributeManager.initialize_attribute
    while True:
        try:
            game = program_loop.Game()
            game.generate_world()
            game.start_game(stdscr)
            game.menu(stdscr)
        except Exception as e:
            continue

# DEBUGGING MAIN
# comment out above main for debugging
# this main does display traceback error information
# def main(stdscr):
#     design.AttributeManager.initialize_attribute
#     while True:
#             game = program_loop.Game()
#             game.generate_world()
#             game.start_game(stdscr)
#             game.menu(stdscr)

if __name__ == "__main__":
    keyboard.press_and_release('f11')
    curses.wrapper(main)