#© 2024 Ryan Noel Buenaventura.

from program_loop.curses_functions import *
import program_loop.game

class Inventory:
    def __init__(self, character):
        self.item_array = []
        self.character = character

    def add_item(self, item_code, item_name, item_statistics, item_special, item_price, stdscr, game):
        # overencumber
        inventory_capacity = self.character.inventory_attributes()
        if len(self.item_array) >= inventory_capacity:
            program_loop.Game.redraw_event_hud(stdscr)
            program_loop.Game.redraw_ui(game, stdscr)
            CursesFunctions.curses_center(stdscr, "You Are Over-Encumbered", 10, 0)
            stdscr.getch()
            return False
        else:
            item = {'item_code': item_code, 'item_name': item_name, 'item_statistics': {'damage': item_statistics[0], 'durability': item_statistics[1], 'max_durability': item_statistics[2]}, 'item_special': item_special, 'item_price': item_price}
            self.item_array.append(item)
            return True
        
    def npc_add_item(self, item_code, item_name, item_statistics, item_special, item_price):
        item = {'item_code': item_code, 'item_name': item_name, 'item_statistics': {'damage': item_statistics[0], 'durability': item_statistics[1], 'max_durability': item_statistics[2]}, 'item_special': item_special, 'item_price': item_price}
        self.item_array.append(item)
        return True

    def drop_item(self, index):
        if self.item_array[index]['item_special'] == 'unarmed':
            return
        else:
            if 0 <= index < len(self.item_array):
                return self.item_array.pop(index)
            
    def loot_drop(self, item, original_array, stdscr):
        self.world_array.append(item)
        original_array.pop(item)
        stdscr.addst(self.world_array)

    def damage_retrieve(self, selected_item):
        return self.item_array[int(selected_item)]['item_statistics']["damage"]
    
    def item_retrieve(self, selected_item):
        if 0 <= selected_item < len(self.item_array):
            return self.item_array[selected_item]
        else:
            return
        
    def item_key_retrieve(self, selected_item):
        try:
            selected_item = int(selected_item)
        except ValueError:
            return None
        if 0 <= selected_item < len(self.item_array):
            return self.item_array[selected_item]['item_code']
        else:
            return None
        
    def item_special_retrieve(self, selected_item):
        try:
            selected_item = int(selected_item)
        except ValueError:
            return None
        if 0 <= selected_item < len(self.item_array):
            return self.item_array[selected_item]['item_special']
        else:
            return None

    def durability(self, selected_item, stdscr):
        self.item_array[int(selected_item)]['item_statistics']['durability'] -= 1
        if self.item_array[int(selected_item)]['item_statistics']['durability'] <= 0:
            item_name = self.item_array[selected_item]['item_name']
            broken_message = f"{item_name} is Broken!"
            CursesFunctions.curses_center(stdscr, broken_message, -1, 0)
            stdscr.getch()
        for item in self.item_array:
            if item['item_statistics']['durability'] <= 0:
                item['item_statistics']['damage'] = 1
                item['item_statistics']['durability'] = 0

    def display_inventory(self, stdscr):
        y_offset = 8
        for i, item in enumerate(self.item_array):
            # make inf not display if durability is infinite
            # if item['item_statistics']['durability'] == float('inf'):
            #     item['item_statistics']['durability'] = ''
            # if item['item_statistics']['max_durability'] == float('inf'):
            #     item['item_statistics']['max_durability'] = ''
            CursesFunctions.curses_center(stdscr, f"{i+1} - {item['item_name']} - {item['item_statistics']['damage']} - {item['item_statistics']['durability']}/{item['item_statistics']['max_durability']}", y_offset, 0)
            y_offset -= 1

    def display_hud_inventory(self, stdscr):
        y_offset = -8
        for i, item in enumerate(self.item_array):
            # make inf not display if durability is infinite
            # if item['item_statistics']['durability'] == float('inf'):
            #     item['item_statistics']['durability'] = ''
            # if item['item_statistics']['max_durability'] == float('inf'):
            #     item['item_statistics']['max_durability'] = ''
            CursesFunctions.curses_center(stdscr, f"{i+1} - {item["item_name"]} - {item['item_statistics']["damage"]} - {item['item_statistics']['durability']}/{item['item_statistics']['max_durability']}", y_offset, 16)
            y_offset -= 1