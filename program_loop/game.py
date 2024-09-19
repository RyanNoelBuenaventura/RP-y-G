#© 2024 Ryan Noel Buenaventura.

import random
import sys
from main import *
from character import *
from program_loop import *
from program_loop.item import *
from program_loop.magic import *

class Game:
    def __init__(self):
        self.head, self.tail = self.generate_world()
        self.player_position = self.head
        self.world = Character(None, None, None, None, None, None, None, None, None, 1000, None, None, None)
        self.loot = Inventory(self.world)
        self.base_health = 100
        self.base_stamina = 75
        self.base_mana = 25
        self.max_health = 0
        self.max_stamina = 0
        self.max_mana = 0
        self.health = 0
        self.stamina = 0
        self.mana = 0
        self.player_level = 1
        self.player_level_progress = 0
        self.player = Character(self.health, self.stamina, self.mana, self.max_health, self.max_stamina, self.max_mana, self.base_health, self.base_stamina, self.base_mana, 3, 3, 3, self.player_level)
        self.player_inventory = Inventory(self.player)
        self.player_spells = Magic(self.player)
        self.player_race = ''
        self.player_background = ''
        self.player_name = ''
        self.menu_choice = ''
        self.player_gold = 0

    def generate_world(self):
        self.head = self.tail = program_loop.MapDoublyNode(1, program_loop.Event.random_event())
        end_world = random.randint(15, 20)
        for i in range (2, end_world):
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
            CursesFunctions.curses_center(stdscr, "Enter Any Key to Start - Exit (esc)", -6, 0)
            stdscr.attroff(attribute_manager.grey_on_black)
            start_input = stdscr.getch()
            if start_input == 27:
                curses.endwin()
                keyboard.press_and_release('f11')
                sys.exit()
            if start_input == curses.KEY_RESIZE or start_input == curses.KEY_F11:
                continue
            else:
                break
        stdscr.clear()
        self.character_creation(stdscr)
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

        self.player_inventory.add_item('unarmed', "Unarmed", [0, float('inf'), float('inf')], 'unarmed', 0, stdscr, self)
        # trigger event in first node
        curses.curs_set(0)
        curses.echo(0)
        program_loop.Event.trigger_event(self.player_position, self, stdscr)
        if self.player_position.flee_occur:
            self.player_position = Game.move(self.player_position, self.player_position.flee_direction, stdscr)

    def character_creation(self, stdscr):
        while True:
            curses.curs_set(0)
            curses.echo(0)
            stdscr.clear()
            CursesFunctions.curses_center(stdscr, "Select Race (1-3) Or Return (r)", 0, 0)
            CursesFunctions.curses_center(stdscr, "Elven", -2, -10)
            CursesFunctions.curses_center(stdscr, "Human", -2, 0)
            CursesFunctions.curses_center(stdscr, "Orcish", -2, 10)
            race_input = stdscr.getch()
            race_selection = CursesFunctions.curses_getch_to_str(stdscr, race_input)
            if race_selection == '1':
                while True:
                    CursesFunctions.curses_center(stdscr, "With rich history and customs rooted in the arcane arts, Elves are magically gifted at the cost of being less physically imposing than other races.", -4, 0)
                    CursesFunctions.curses_center(stdscr, "+2 Intelligence\n-1 Strength", -7, 0)
                    CursesFunctions.curses_center(stdscr, "(y/n)", -9, 0)
                    confirm_input = stdscr.getch()
                    confirm_selection = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
                    if confirm_selection.lower() == 'y':
                        self.player_race = 'Elf'
                        self.player.intelligence += 2
                        self.player.strength -= 1
                        break
                    elif confirm_selection.lower() == 'n':
                        break
                    else:
                        continue
                if confirm_selection.lower() == 'y':
                    break
            elif race_selection == '2':
                while True:
                    CursesFunctions.curses_center(stdscr, "Through time, the endurance and cunning of man in addition to their shorture stature has allowed the human race to thrive and conquer with their strong and nimble traits.", -4, 0)
                    CursesFunctions.curses_center(stdscr, "+1 Agility\n+1 Strength\n-1 Intelligence", -7, 0)
                    CursesFunctions.curses_center(stdscr, "(y/n)", -10, 0)
                    confirm_input = stdscr.getch()
                    confirm_selection = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
                    if confirm_selection.lower() == 'y':
                        self.player_race = 'Human'
                        self.player.agility += 1
                        self.player.strength += 1
                        self.player.intelligence = 1
                        break
                    elif confirm_selection.lower() == 'n':
                        break
                    else:
                        continue
                if confirm_selection.lower() == 'y':
                    break
            elif race_selection == '3':
                while True:
                    CursesFunctions.curses_center(stdscr, "Cursed by the Gods and astrayed from their original Elven ancestry, the Orcish race has overcome their lack of divinity through physical strength, nothing is more commanding than the Orcish spirit.", -4, 0)
                    CursesFunctions.curses_center(stdscr, "+2 Strength\n-1 Intelligence", -7, 0)
                    CursesFunctions.curses_center(stdscr, "(y/n)", -9, 0)
                    confirm_input = stdscr.getch()
                    confirm_selection = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
                    if confirm_selection.lower() == 'y':
                        self.player_race = 'Orc'
                        self.player.strength += 2
                        self.player.intelligence = 1
                        break
                    elif confirm_selection.lower() == 'n':
                        break
                    else:
                        continue
                if confirm_selection.lower() == 'y':
                    break
            elif race_selection.lower() == 'r':
                raise RestartException()
            else:
                continue

        stdscr.clear()
        while True:
            curses.curs_set(0)
            curses.echo(0)
            stdscr.clear()
            CursesFunctions.curses_center(stdscr, "Select Background (1-3) Or Return (r)", 0, 0)
            CursesFunctions.curses_center(stdscr, "Noble", -2, -10)
            CursesFunctions.curses_center(stdscr, "Outsider", -2, 0)
            CursesFunctions.curses_center(stdscr, "Commoner", -2, 10)
            background_input = stdscr.getch()
            background_selection = CursesFunctions.curses_getch_to_str(stdscr, background_input)
            if background_selection == '1':
                while True:
                    CursesFunctions.curses_center(stdscr, "Gold and glory, coming from a long lineage of wealth your adventure to the other side of the country brings something money cannot buy.", -4, 0)
                    CursesFunctions.curses_center(stdscr, "+100 Gold", -6, 0)
                    CursesFunctions.curses_center(stdscr, "(y/n)", -8, 0)
                    confirm_input = stdscr.getch()
                    confirm_selection = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
                    if confirm_selection.lower() == 'y':
                        self.player_background = 'Noble'
                        self.player_gold += 100
                        break
                    elif confirm_selection.lower() == 'n':
                        break
                    else:
                        continue
                if confirm_selection.lower() == 'y':
                    break
            elif background_selection == '2':
                while True:
                    CursesFunctions.curses_center(stdscr, "Hailing from distant lands you find yourself in the land of temp_country seeking the other side which is talked of as the greatest adventure one could seek.", -4, 0)
                    CursesFunctions.curses_center(stdscr, "+1 Agility", -6, 0)
                    CursesFunctions.curses_center(stdscr, "(y/n)", -8, 0)
                    confirm_input = stdscr.getch()
                    confirm_selection = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
                    if confirm_selection.lower() == 'y':
                        self.player_background = 'Outsider'
                        self.player.agility += 1
                        break
                    elif confirm_selection.lower() == 'n':
                        break
                    else:
                        continue
                if confirm_selection.lower() == 'y':
                    break
            elif background_selection == '3':
                while True:
                    CursesFunctions.curses_center(stdscr, "You are no stranger to hard work but you are a stranger to adventuring as you finally leave your home village in search of more than the working mans life through adventuring across temp_country.", -4, 0)
                    CursesFunctions.curses_center(stdscr, "+1 Strength", -6, 0)
                    CursesFunctions.curses_center(stdscr, "(y/n)", -8, 0)
                    confirm_input = stdscr.getch()
                    confirm_selection = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
                    if confirm_selection.lower() == 'y':
                        self.player_background = 'Commoner'
                        self.player.strength += 1
                        break
                    elif confirm_selection.lower() == 'n':
                        break
                    else:
                        continue
                if confirm_selection.lower() == 'y':
                    break
            elif background_selection.lower() == 'r':
                Game.character_creation(self, stdscr)
            else:
                continue
        
        self.player.refresh_attributes()
        stdscr.clear()

    def menu(self, stdscr):
        Game.player_life_check(self, stdscr)
        curses.curs_set(0)
        curses.echo(0)
        stdscr.clear()
        Game.level(self, stdscr)
        self.player.update_attributes()
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
            # stdscr.addstr(str(self.player_position))
            program_loop.Event.display_node_event(self.player_position, self, stdscr)
            self.menu(stdscr)
        elif self.menu_choice == '2':
            while True:
                attribute_manager = design.AttributeManager()
                attribute_manager.initialize_attribute()
                stdscr.attron(attribute_manager.grey_on_black)
                Game.menu_hud(stdscr)
                stdscr.attroff(attribute_manager.grey_on_black)
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
            Game.rest(self, stdscr)
            self.menu(stdscr)
        elif self.menu_choice == '4':
            Game.inventory_interact(self, self.player_position, stdscr)
            self.menu(stdscr)
        elif self.menu_choice == '5':
            while True:
                study_choice = True
                while study_choice:
                    Game.redraw_lower_hud(self, stdscr)
                    study_choice = Magic(self).read(self.player_inventory.item_array, stdscr, self, '', 0, Game)
                    if study_choice == 'r' or study_choice == 'c':
                        break
                    break
                if study_choice == 'r':
                    self.menu(stdscr)
                Game.redraw_lower_hud(self, stdscr)
                if study_choice == 'c':
                    while True:
                        #Game.draw_magic_hud(self, stdscr)
                        selected_target = program_loop.Event.select_target(self, 0, 0, None, stdscr, None)
                        if selected_target == None:
                            break
                        elif selected_target == 0:
                            selected_target = self.player
                        else:
                            continue
                        while True:
                            selected_spell = Magic(self).select_spell(self, self.player_spells.spell_array, stdscr)
                            if selected_spell is None:
                                break
                            event_in_progress = False
                            Character.cast(self.player, stdscr, selected_spell, selected_target, self.player_spells, self.player_inventory, self, event_in_progress)
                            Game.redraw_lower_hud(self, stdscr)
                            continue
                    continue
                else:
                    continue
                # self.menu(stdscr)
        elif self.menu_choice == '6':
            while True:
                Game.redraw_ui(self, stdscr)
                CursesFunctions.curses_center(stdscr, "Confirm Exit (y/n)", 10, 0)
                y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 8, 0)
                stdscr.move(y_cursor, x_cursor)
                exit_input = stdscr.getch()
                exit_choice = CursesFunctions.curses_getch_to_str(stdscr, exit_input)
                if exit_choice.lower() == 'y':
                    raise RestartException()
                    break
                elif exit_choice.lower() == 'n':
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
        menu_string = "1 - Area\n2 - Move\n3 - Rest\n4 - Gear\n5 - Study\n6 - Exit"
        hud_height = -8
        CursesFunctions.curses_center(stdscr, menu_string, hud_height, 0)
        CursesFunctions.curses_box(stdscr, 8, 21, hud_height, 0)

    def stat_hud(self, stdscr):
        CursesFunctions.curses_center(stdscr, design.character_ascii, -17, -15)
        CursesFunctions.curses_center(stdscr, f" {self.player_name}", -15, 0)
        CursesFunctions.curses_center(stdscr, self.player_race, -16, 0)
        CursesFunctions.curses_center(stdscr, self.player_background, -17, 0)
        CursesFunctions.curses_center(stdscr, f"XP - {self.player_level} - {self.player_level_progress} / 100", -18, 0)
        CursesFunctions.curses_center(stdscr, f"Health - {self.player.health} / {self.player.max_health}", -20, 0)
        CursesFunctions.curses_center(stdscr, f"Stamina - {self.player.stamina} / {self.player.max_stamina}", -21, 0)
        CursesFunctions.curses_center(stdscr, f"Mana - {self.player.mana} / {self.player.max_mana}", -22, 0)
        CursesFunctions.curses_center(stdscr, f"Strength - {self.player.strength}", -24, 0)
        CursesFunctions.curses_center(stdscr, f"Agility - {self.player.agility}", -25, 0)
        CursesFunctions.curses_center(stdscr, f"Intelligence - {self.player.intelligence}", -26, 0)
        CursesFunctions.curses_box(stdscr, 15, 21, -21, 0) # stat box

    def inventory_hud(self, stdscr):
        if len(self.player_inventory.item_array) != 0:
            self.player_inventory.display_hud_inventory(stdscr)
            stdscr.refresh()
        CursesFunctions.curses_center(stdscr, "Item | Damage | Durability", -6, 17)
        CursesFunctions.curses_center(stdscr, f"Gold - {int(self.player_gold)}", -26, 15)
        CursesFunctions.curses_box(stdscr, 24, 40, -16, 33)

    def redraw_inventory_hud(stdscr):
        try:
            stdscr.move(-15, 10)
            stdscr.clrtoeol()
            CursesFunctions.curses_box(stdscr, 24, 40, -16, 33)
        except curses.error:
            pass

    def inventory_interact(self, node, stdscr):
        if len(self.player_inventory.item_array) != 0:
            while True:
                Game.redraw_event_hud(stdscr)
                attribute_manager = design.AttributeManager()
                attribute_manager.initialize_attribute()
                stdscr.attron(attribute_manager.grey_on_black)
                Game.menu_hud(stdscr)
                stdscr.attroff(attribute_manager.grey_on_black)
                CursesFunctions.curses_center(stdscr, design.backpack_ascii, 10, 0)
                CursesFunctions.curses_center(stdscr, f"Select Item (1-{len(self.player_inventory.item_array)}) Or Return (r)", -1, 15)
                # y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, -1, 0)
                # item_select = CursesFunctions.curses_input(self, stdscr, y_cursor, x_cursor, '')
                item_select_input = stdscr.getch()
                item_select = CursesFunctions.curses_getch_to_str(stdscr, item_select_input)
                item_select = Game.input_validation(self.player_inventory.item_array, item_select, stdscr)
                if str(item_select).lower() == 'r':
                    break
                Game.redraw_event_hud(stdscr)
                CursesFunctions.curses_center(stdscr, f"Drop (d) Use (u) Return (r)", 10, 0)
                #item_use_choice = CursesFunctions.curses_input(self, stdscr, y_cursor, x_cursor, '')
                item_use_input = stdscr.getch()
                item_use_choice = CursesFunctions.curses_getch_to_str(stdscr, item_use_input)
                if item_use_choice.lower() == 'd':
                    dropped_item = self.player_inventory.drop_item(int(item_select))
                    program_loop.Event.add_to_loot_event(dropped_item, node, stdscr, self)
                    Game.redraw_event_hud(stdscr)
                    Game.redraw_lower_hud(self, stdscr)
                    continue
                elif item_use_choice.lower() == 'u':
                    selected_item_key = Inventory.item_key_retrieve(self.player_inventory, item_select)
                    Item().use_item(selected_item_key, self, self.player_inventory.item_array, item_select, stdscr)
                    continue
                elif item_use_choice.lower() == 'r':
                    continue
        else:
            CursesFunctions.curses_center(stdscr, "Inventory Empty", 9, 0)
            stdscr.getch()

    def event_hud(stdscr):
        CursesFunctions.curses_box(stdscr, 30, 100, 12, 0) # name box

    def redraw_event_hud(stdscr):
        CursesFunctions.curses_clear_to_row(stdscr, 48) # clears screen until top of hud
        Game.event_hud(stdscr)

    def redraw_lower_hud(self, stdscr):
        stdscr.clear()
        Game.level(self, stdscr)
        self.player.update_attributes()
        attribute_manager = design.AttributeManager()
        attribute_manager.initialize_attribute()
        stdscr.attron(attribute_manager.grey_on_black)
        Game.menu_hud(stdscr)
        stdscr.attroff(attribute_manager.grey_on_black)
        self.stat_hud(stdscr)
        self.inventory_hud(stdscr)
        Game.event_hud(stdscr)

    def redraw_attack_ui(self, stdscr):
        attribute_manager = design.AttributeManager()
        attribute_manager.initialize_attribute()
        CursesFunctions.curses_clear_to_row(stdscr, 60) # clears screen until top of hud
        CursesFunctions.curses_box(stdscr, 38, 100, 16, 0) # name box
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
        
    def draw_magic_hud(self, stdscr):
        Game.redraw_attack_ui(self, stdscr)
        CursesFunctions.curses_center(stdscr, design.magic_ascii, 10, 0)
        
    
    def move(player_node, direction, stdscr):
        while True:
            if direction.lower() == 'f':
                if player_node.next:
                    return player_node.next
                else:
                    CursesFunctions.curses_clear_to_row(stdscr, 49)
                    CursesFunctions.curses_center(stdscr, design.end_ascii, 15, 0)
                    CursesFunctions.curses_center(stdscr, "Concluding Your Journey Across The Country, You Look Back Onto The Blazing Sunshine. The Rest Of The Day Is Yours, Temporarily Anyhow.", -1, 0)
                    stdscr.getch()
                    keyboard.press_and_release('f11')
                    exit()
                    # return player_node
            elif direction.lower() == 'b':
                if player_node.prev:
                    return player_node.prev
                else:
                    CursesFunctions.curses_center(stdscr, "No Space Behind", 8, 0)
                    stdscr.getch()
                    return player_node
            elif direction.lower() == 'r':
                return player_node
            else:
                CursesFunctions.curses_center(stdscr, "Invalid Input", 8, 0)
                y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 8, 0)
                stdscr.move(y_cursor, x_cursor)
                direction_input = stdscr.getch()
                direction = CursesFunctions.curses_getch_to_str(stdscr, direction_input)
                continue

    def move_validation(player_node, direction):
        if str(direction).lower() == 'f':
            return player_node.next is not None
        elif str(direction).lower() == 'b':
            return player_node.prev is not None
        
    def input_validation(list, selection, stdscr):
        if str(selection).lower() == 'r':
            return selection
        try:
            if selection == '':
                selection = len(list) + 1
            if 1 > int(selection) or len(list) < int(selection) or selection == str or selection == '' or selection == None:
                raise ValueError
        except ValueError:
            Game.event_hud(stdscr)
            # CursesFunctions.curses_center(stdscr, "Invalid Input", -2, 0)
            # y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 7, 0)
            exception_input = stdscr.getch()
            exception_input = CursesFunctions.curses_getch_to_str(stdscr, exception_input)
            return Game.input_validation(list, exception_input, stdscr)
        return int(selection) -1

    def level(self, stdscr):
        while self.player_level_progress >= 100:
            self.player_level += 1
            player_level_progress_extra = self.player_level_progress - 100
            self.player_level_progress = 0
            while True:
                stdscr.clear()
                CursesFunctions.curses_center(stdscr, "Level Up. Select Attribute To Increase (1-3)", 11, 0)
                CursesFunctions.curses_center(stdscr, "Strength", 9, -10)
                CursesFunctions.curses_center(stdscr, "Agility", 9, 0)
                CursesFunctions.curses_center(stdscr, "Intelligence", 9, 10)
                attribute_input = stdscr.getch()
                attribute_selection = CursesFunctions.curses_getch_to_str(stdscr, attribute_input)
                if attribute_selection == '1':
                    confirm_selection = Game.confirm_function(stdscr)
                    if confirm_selection == 'y':
                        self.player.strength += 1
                        break
                elif attribute_selection == '2':
                    confirm_selection = Game.confirm_function(stdscr)
                    if confirm_selection == 'y':
                        self.player.agility += 1
                        break
                elif attribute_selection == '3':
                    confirm_selection = Game.confirm_function(stdscr)
                    if confirm_selection == 'y':
                        self.player.intelligence += 1
                        break
                else:
                    continue
            self.player_level_progress += player_level_progress_extra
            if self.player_level_progress < 100:
                Game.redraw_event_hud(stdscr)
                return

    def confirm_function(stdscr):
        while True:
            CursesFunctions.curses_center(stdscr, "(y/n)", 7, 0)
            confirm_input = stdscr.getch()
            confirm_selection = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
            if confirm_selection.lower() in ['y', 'n']:
                return confirm_selection.lower()

    def xp_gain(self, min_xp_gain, max_xp_gain, stdscr):
        xp_gain = random.randint(min_xp_gain, max_xp_gain)
        self.player_level_progress += xp_gain
        # CursesFunctions.curses_center(stdscr, f"You Gained {xp_gain}", 10, 0)


    def player_life_check(self, stdscr):
        if self.player.health <= 0:
            stdscr.clear()
            CursesFunctions.curses_center(stdscr, design.skull_2_ascii, 0, 0)
            stdscr.getch()
            raise RestartException()

    def rest(self, stdscr):
        Game.inventory_hud(self, stdscr)
        has_camping_supplies = False
        for item in self.player_inventory.item_array:
            if item['item_code'] == 'camping_supplies_1':
                has_camping_supplies = True
                break
        if has_camping_supplies:
            while True:
                attribute_manager = design.AttributeManager()
                attribute_manager.initialize_attribute()
                stdscr.attron(attribute_manager.grey_on_black)
                Game.menu_hud(stdscr)
                stdscr.attroff(attribute_manager.grey_on_black)
                CursesFunctions.curses_center(stdscr, "Use Camping Supplies To Rest?", 8, 0)
                confirm_selection = Game.confirm_function(stdscr)
                if confirm_selection == 'y':
                    self.player.health = self.player.max_health
                    self.player.stamina = self.player.max_stamina
                    self.player.mana = self.player.max_mana
                    self.player_inventory.item_array.remove(item)
                    CursesFunctions.curses_center(stdscr, design.camp_ascii, 11, 0)
                    # CursesFunctions.curses_center(stdscr, "As You Gaze Upon The Stars Your Vitality Returns To You", 11, 0)
                    CursesFunctions.curses_center(stdscr, "Your Vitality Returns As You Let The Stars Magnificance Enfold You", -1, 0)
                    stdscr.getch()
                    break
                elif confirm_selection == 'n':
                    return
                else:
                    continue
        else:
            CursesFunctions.curses_center(stdscr, "You Do Not Have The Supplies Required To Camp", 8, 0)
            stdscr.getch()
            return