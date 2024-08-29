import curses
from curses.textpad import rectangle

class CursesFunctions:
    def curses_input(self, stdscr, r, c, prompt):
        curses.echo()
        stdscr.addstr(r,c,prompt)
        input = stdscr.getstr().decode("utf-8")
        return input
    
    def curses_center(stdscr, text, y_offset, x_offset):
        y, x = stdscr.getmaxyx()
        #create array of items if string uses newline
        lines = text.split('\n')
        h = (y // 2) - (len(lines) // 2)
        for line in lines:
            w = (x - max(len(line) for line in lines)) // 2 + x_offset
            try:
                stdscr.addstr(h - y_offset, w + x_offset, line)
            except curses.error:
                pass
            h += 1

    def curses_box(stdscr, height, width, y_offset, x_offset):
        y, x = stdscr.getmaxyx()
        uly = (y - height) // 2 - y_offset
        ulx = (x - width) // 2 + x_offset
        lry = uly + height
        lrx = ulx + width
        if lry > uly and lrx > ulx:
            try:
                rectangle(stdscr, uly, ulx, lry, lrx)
            except curses.error:
                pass
    
    def curses_center_insertion_point(stdscr, y_offset, x_offset):
        """
        \n@purpose\n
        returns y_cursor, x_cursor points that are offset from the center by y_offset, x_offset
        \n@param\n
        y_offset - int to offset insertion point\n
        x_offset - int to offset insertion point\n
        \n@return\n
        y_cursor - new insertion y coordinate\n
        x_cursor - new insertion y coordinate\n
        \n@notes\n
        none\n
        """
        y, x = stdscr.getmaxyx()
        y_cursor = y // 2 - y_offset
        x_cursor = x // 2 + x_offset
        return y_cursor, x_cursor
    
    def curses_getch_to_str(stdscr, ch):
        """
        converts the input of getch into a string
        """
        if 32 <= ch <= 126:
            ch_str = chr(ch)
        else:
            ch_str = ''
        return ch_str
    
    def curses_clear_to_row(stdscr, row_stop):
        """
        clear rows until specified row
        """
        for i in range(row_stop):
            stdscr.move(i, 0)
            stdscr.clrtoeol()