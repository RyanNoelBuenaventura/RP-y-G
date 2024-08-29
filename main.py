#Ryan Noel Buenaventura

import keyboard

import program_loop
from character import *
import design

def main(stdscr):
    stdscr = curses.initscr()
    design.AttributeManager.initialize_attribute
    game = program_loop.Game()
    game.generate_world()
    game.start_game(stdscr)
    game.menu(stdscr)
    
if __name__ == "__main__":
    keyboard.press_and_release('f11')
    curses.wrapper(main)