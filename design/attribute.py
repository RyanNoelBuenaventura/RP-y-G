from program_loop.curses_functions import *

class AttributeManager:
    def __init__(self):
        self.grey_on_black = None
        self.bold_attr = None

    def initialize_attribute(self):
    #initialize colors and pairs
        if curses.has_colors():
            if curses.can_change_color():
                curses.init_color(1, 500, 500, 500) #grey

            curses.init_pair(1, 1, curses.COLOR_BLACK)

        self.grey_on_black = curses.color_pair(1)
        self.bold_attr = curses.A_BOLD