#© 2024 Ryan Noel Buenaventura.

import keyboard
import program_loop
from character import *
import design

class RestartException(Exception):
    pass

def main(stdscr):
    #stdscr = curses.initscr()
    design.AttributeManager.initialize_attribute
    #game_state = 'running'
    while True:
        game_state = 'running'
        try:
            game = program_loop.Game()
            game.generate_world()
            game.start_game(stdscr)
            game.menu(stdscr, game_state)
        except Exception as e:
            #stdscr.clear()
            continue
    
if __name__ == "__main__":
    keyboard.press_and_release('f11')
    curses.wrapper(main)