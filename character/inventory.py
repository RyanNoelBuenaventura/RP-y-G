from program_loop.curses_functions import *
import program_loop.game

# class Weapons:
#     def __init__(self):
#         self.weapon_array = []

#     def orc_weapon_list(self):
#         self.weapon_array.add_item("orc_sword_1", "Orc Sword", [2, 3])
#         self.weapon_array.add_item("orc_axe_1", "Orc Axe", [4, 1])

class Inventory:
    def __init__(self, character):
        self.item_array = []
        self.character = character

    def add_item(self, item_code, item_name, item_statistics, stdscr, game):
        #overencumber
        inventory_capacity = self.character.inventory_attributes()
        if len(self.item_array) >= inventory_capacity:
            program_loop.Game.redraw_event_hud(stdscr)
            program_loop.Game.redraw_ui(game, stdscr)
            CursesFunctions.curses_center(stdscr, "You Are Over-Encumbered", 10, 0)
            stdscr.getch()
            return False
        else:
            item = {"item_code": item_code, "item_name": item_name, "item_statistics": {"damage": item_statistics[0], "durability": item_statistics[1], "max_durability": item_statistics[2]}}
            self.item_array.append(item)
            return True
        
    def npc_add_item(self, item_code, item_name, item_statistics):
        item = {"item_code": item_code, "item_name": item_name, "item_statistics": {"damage": item_statistics[0], "durability": item_statistics[1], "max_durability": item_statistics[2]}}
        self.item_array.append(item)
        return True

    def drop_item(self, index):
        if 0 <= index < len(self.item_array):
            return self.item_array.pop(index)
        
    def loot_drop(self, item, original_array, stdscr):
        self.world_array.append(item)
        original_array.pop(item)
        stdscr.addst(self.world_array)

    def damage_retrieve(self, selected_item):
        return self.item_array[int(selected_item)]["item_statistics"]["damage"]
    
    def item_retrieve(self, selected_item):
        if 0 <= selected_item < len(self.item_array):
            return self.item_array[int(selected_item)]
        else:
            return

    def durability(self, selected_item, stdscr):
        self.item_array[int(selected_item)]["item_statistics"]["durability"] -= 1
        if self.item_array[int(selected_item)]["item_statistics"]["durability"] <= 0:
            item_name = self.item_array[selected_item]["item_name"]
            broken_message = f"{item_name} is Broken!"
            CursesFunctions.curses_center(stdscr, broken_message, -1, 0)
            stdscr.getch()
        for item in self.item_array:
            if item["item_statistics"]["durability"] <= 0:
                item["item_statistics"]["damage"] = 1
                item["item_statistics"]["durability"] = 0

    def display_inventory(self, stdscr):
        y_offset = 8
        for i, item in enumerate(self.item_array):
            CursesFunctions.curses_center(stdscr, f"{i+1} - {item["item_name"]} - {item["item_statistics"]["damage"]} - {item["item_statistics"]["durability"]}/{item["item_statistics"]["max_durability"]}", y_offset, 0)
            y_offset -= 1

    def display_hud_inventory(self, stdscr):
        y_offset = -7
        for i, item in enumerate(self.item_array):
            CursesFunctions.curses_center(stdscr, f"{i+1} - {item["item_name"]} - {item["item_statistics"]["damage"]} - {item["item_statistics"]["durability"]}/{item["item_statistics"]["max_durability"]}", y_offset, 15)
            y_offset -= 1