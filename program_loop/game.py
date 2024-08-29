from main import *
from character import *
from program_loop import *

class Game:
    def __init__(self):
        self.head, self.tail = self.generate_world()
        self.player_position = self.head
        self.world = Character(None, None, None, 1000, None, None)
        self.loot = Inventory(self.world)
        self.max_health = 100
        self.max_stamina = 75
        self.max_mana = 50
        self.player = Character(self.max_health, self.max_stamina, self.max_mana, 1, 1, 3)
        self.player_inventory = Inventory(self.player)
        self.menu_choice = ''
        self.player_name = ''

    def generate_world(self):
        self.head = self.tail = program_loop.MapDoublyNode(1, program_loop.Event.random_event())
        for i in range (2, 11):
            self.head, self.tail = program_loop.MapDoublyLinkedList.insert_at_end(self.head, self.tail, i, program_loop.Event.random_event())
        return self.head, self.tail

    def start_game(self, stdscr):
        curses.curs_set(0)
        curses.echo(0)
        attribute_manager = design.AttributeManager()
        attribute_manager.initialize_attribute()
        stdscr.clear()
        while True:
            curses.curs_set(0)
            stdscr.clear()
            stdscr.attron(attribute_manager.bold_attr)
            CursesFunctions.curses_center(stdscr, design.title_ascii, 0, 0)
            stdscr.attroff(attribute_manager.bold_attr)
            stdscr.attron(attribute_manager.grey_on_black)
            CursesFunctions.curses_center(stdscr, "Enter Any Key to Start", -6, 0)
            stdscr.attroff(attribute_manager.grey_on_black)
            start_input = stdscr.getch()
            if start_input == curses.KEY_RESIZE or start_input == curses.KEY_F11:
                continue
            else:
                break
        stdscr.clear()
        curses.curs_set(1)
        while True:
            y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, -3, -9)
            CursesFunctions.curses_center(stdscr, "Enter Name", 0, 0)
            CursesFunctions.curses_box(stdscr, 2, 21, -3, 0)
            self.player_name = CursesFunctions.curses_input(self, stdscr, y_cursor, x_cursor, '')
            if len(self.player_name) > 20 or len(self.player_name) <= 0:
                stdscr.clear()
                stdscr.attron(attribute_manager.grey_on_black)
                CursesFunctions.curses_center(stdscr, "Invalid Input", -5, 0)
                stdscr.attroff(attribute_manager.grey_on_black)
                continue
            else:
                break
        self.player_inventory.add_item("unarmed", "Unarmed", [0, float('inf'), float('inf')], stdscr, self)
        stdscr.clear()

        # trigger event in first node
        # Event.trigger_event(self.player_position, self, stdscr)
        # if self.player_position.flee_occur:
        #     self.player_position = Game.move(self.player_position, self.player_position.flee_direction, stdscr)

    def menu(self, stdscr):
        curses.curs_set(0)
        curses.echo(0)
        stdscr.clear()
        Game.menu_hud(stdscr)
        self.stat_hud(stdscr)
        self.inventory_hud(stdscr)
        Game.event_hud(stdscr)
        y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, -11, 0)
        stdscr.move(y_cursor, x_cursor)
        # convert integer from getch into a string
        menu_input = stdscr.getch()
        self.menu_choice = CursesFunctions.curses_getch_to_str(stdscr, menu_input)

        if self.menu_choice == '1':
            #stdscr.addstr(str(self.player_position))
            program_loop.Event.display_node_event(self.player_position, self, stdscr)
            self.menu(stdscr)
        elif self.menu_choice == '2':
            while True:
                CursesFunctions.curses_center(stdscr, "Forward/Backward (f/b) Or Return (r)", 10, 0)
                y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 8, 0)
                stdscr.move(y_cursor, x_cursor)
                direction_input = stdscr.getch()
                direction_choice = CursesFunctions.curses_getch_to_str(stdscr, direction_input)
                if direction_choice not in ['f', 'b', 'r', 'F', 'B', 'R']:
                    continue
                Game.redraw_event_hud(stdscr)
                Game.redraw_ui(self, stdscr)
                self.player_position = Game.move(self.player_position, direction_choice, stdscr)
                if direction_choice not in ['r', 'R']:
                    program_loop.Event.trigger_event(self.player_position, self, stdscr)
                while self.player_position.flee_occur:
                    self.player_position = Game.move(self.player_position, self.player_position.flee_direction, stdscr)
                    program_loop.Event.trigger_event(self.player_position, self, stdscr)
                self.menu(stdscr)
        elif self.menu_choice == '3':
            stdscr.addstr(self.player_name)
            stdscr.getch()
            self.player.health -= 10
            self.menu(stdscr)
        elif self.menu_choice == '4':
            Game.inventory_interact(self, self.player_position, stdscr)
            self.menu(stdscr)
        elif self.menu_choice == '5':
            while True:
                Game.redraw_ui(self, stdscr)
                CursesFunctions.curses_center(stdscr, "Confirm Exit (y/n)", 10, 0)
                y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 8, 0)
                stdscr.move(y_cursor, x_cursor)
                exit_input = stdscr.getch()
                exit_choice = CursesFunctions.curses_getch_to_str(stdscr, exit_input)
                if exit_choice == 'y' or exit_choice == 'Y':
                    keyboard.press_and_release('f11')
                    curses.endwin()
                    exit()
                    break
                elif exit_choice == 'n' or exit_choice == 'N':
                    self.menu(stdscr)
                    break
                else:
                    Game.redraw_event_hud(stdscr)
                    Game.redraw_ui(self, stdscr)
                    CursesFunctions.curses_center(stdscr, "Invalid Input", 8, 0)
                    continue
        else:
            self.menu(stdscr)

    def menu_hud(stdscr):
        menu_string = "1 - Area\n2 - Move\n3 - Rest\n4 - Gear\n5 - Exit"
        hud_height = -8
        CursesFunctions.curses_center(stdscr, menu_string, hud_height, 0)
        CursesFunctions.curses_box(stdscr, 8, 21, hud_height, 0)

    def stat_hud(self, stdscr):
        CursesFunctions.curses_center(stdscr, design.character_ascii, -15, -15)
        CursesFunctions.curses_center(stdscr, f" {self.player_name}", -15, 0)
        CursesFunctions.curses_box(stdscr, 2, len(self.player_name) + 1, -15, 0) #name box
        CursesFunctions.curses_center(stdscr, f"Health - {self.player.health} / {self.max_health}", -17, 0)
        CursesFunctions.curses_center(stdscr, f"Stamina - {self.player.stamina} / {self.max_stamina}", -18, 0)
        CursesFunctions.curses_center(stdscr, f"Mana - {self.player.mana} / {self.max_mana}", -19, 0)
        CursesFunctions.curses_center(stdscr, f"Strength - {self.player.strength}", -21, 0)
        CursesFunctions.curses_center(stdscr, f"Agility - {self.player.agility}", -22, 0)
        CursesFunctions.curses_center(stdscr, f"Intelligence - {self.player.intelligence}", -23, 0)
        CursesFunctions.curses_box(stdscr, 13, 21, -20, 0) #stat box

    def inventory_hud(self, stdscr):
        if len(self.player_inventory.item_array) != 0:
            self.player_inventory.display_hud_inventory(stdscr)
            stdscr.refresh()
        CursesFunctions.curses_center(stdscr, "Item | Damage | Durability", -5, 16)
        CursesFunctions.curses_box(stdscr, 22, 35, -15, 30)

    def redraw_inventory_hud(stdscr):
        try:
            stdscr.move(-15, 10)
            stdscr.clrtoeol()
            CursesFunctions.curses_box(stdscr, 22, 35, -15, 30)
        except curses.error:
            pass

    def inventory_interact(self, node, stdscr):
        if len(self.player_inventory.item_array) != 0:
            CursesFunctions.curses_center(stdscr, f"Select Item To Drop (1-{len(self.player_inventory.item_array)}) Or Return (r)", 10, 0)
            y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 8, 0)
            drop_select = CursesFunctions.curses_input(self, stdscr, y_cursor, x_cursor, '')
            drop_select = Game.input_validation(self.player_inventory.item_array, drop_select, stdscr)
            if drop_select == 'r' or drop_select == 'R':
                return
            dropped_item = self.player_inventory.drop_item(int(drop_select))
            program_loop.Event.add_to_loot_event(dropped_item, node, stdscr, self)
            Game.redraw_event_hud(stdscr)
        else:
            CursesFunctions.curses_center(stdscr, "Inventory Empty", 9, 0)
            stdscr.getch()

    def event_hud(stdscr):
        CursesFunctions.curses_box(stdscr, 30, 100, 12, 0) #name box

    def redraw_event_hud(stdscr):
        CursesFunctions.curses_clear_to_row(stdscr, 48) # clears screen until top of hud
        Game.event_hud(stdscr)

    def redraw_orc_ui(self, stdscr):
        attribute_manager = design.AttributeManager()
        attribute_manager.initialize_attribute()
        CursesFunctions.curses_clear_to_row(stdscr, 60) # clears screen until top of hud
        CursesFunctions.curses_box(stdscr, 38, 100, 16, 0) #name box
        Game.inventory_hud(self, stdscr)
        stdscr.attron(attribute_manager.grey_on_black)
        Game.menu_hud(stdscr)
        stdscr.attroff(attribute_manager.grey_on_black)
        Game.stat_hud(self, stdscr)

    def redraw_ui(self, stdscr):
        attribute_manager = design.AttributeManager()
        attribute_manager.initialize_attribute()
        Game.inventory_hud(self, stdscr)
        stdscr.attron(attribute_manager.grey_on_black)
        Game.menu_hud(stdscr)
        stdscr.attroff(attribute_manager.grey_on_black)
        Game.stat_hud(self, stdscr)
        Game.event_hud(stdscr)
        
    def move(player_node, direction, stdscr):
        while True:
            if direction == 'f' or direction == 'F':
                if player_node.next:
                    return player_node.next
                else:
                    CursesFunctions.curses_center(stdscr, "No Space In Front", 8, 0)
                    stdscr.getch()
                    return player_node
            elif direction == 'b' or direction == 'B':
                if player_node.prev:
                    return player_node.prev
                else:
                    CursesFunctions.curses_center(stdscr, "No Space Behind", 8, 0)
                    stdscr.getch()
                    return player_node
            elif direction == 'r' or direction == 'R':
                return player_node
            else:
                CursesFunctions.curses_center(stdscr, "Invalid Input", 8, 0)
                y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 8, 0)
                stdscr.move(y_cursor, x_cursor)
                direction_input = stdscr.getch()
                direction = CursesFunctions.curses_getch_to_str(stdscr, direction_input)
                continue

    def move_validation(player_node, direction):
        if direction in ['f', 'F']:
            return player_node.next is not None
        elif direction in ['b', 'B']:
            return player_node.prev is not None
        
    def input_validation(list, selection, stdscr):
        if selection == 'r' or selection == 'R':
            return selection
        try:
            if selection == '':
                selection = len(list) + 1
            if 1 > int(selection) or len(list) < int(selection) or selection == str or selection == '' or selection == None:
                raise ValueError
        except ValueError:
            Game.event_hud(stdscr)
            #CursesFunctions.curses_center(stdscr, "Invalid Input", -2, 0)
            #y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 7, 0)
            exception_input = stdscr.getch()
            exception_input = CursesFunctions.curses_getch_to_str(stdscr, exception_input)
            return Game.input_validation(list, exception_input, stdscr)
            #return Game.input_validation(list, CursesFunctions.curses_input(CursesFunctions, stdscr, y_cursor, x_cursor, ''), stdscr)
        return int(selection) -1

    def player_life_check(self, stdscr):
        if self.player.health <= 0:
            stdscr.addstr("Game Over")
            exit()