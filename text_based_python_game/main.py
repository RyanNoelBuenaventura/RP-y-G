#Ryan Noel Buenaventura

import curses
from curses.textpad import rectangle
import random
import keyboard

class MapDoublyNode:
    def __init__(self, val, event = None, event_completed = False, event_looted = False, flee_occur = False, flee_direction = None, node_loot = None, next = None, prev = None):
        self.val = val
        self.event = event
        self.event_completed = event_completed
        self.event_looted = event_looted
        self.flee_occur = flee_occur
        self.flee_direction = flee_direction
        self.node_loot = node_loot
        self.next = next
        self.prev = prev

    def __str__(self):
        return str(self.val)

class MapDoublyLinkedList:
    def display(head, stdscr):
        curr = head
        elements = []
        while curr:
            elements.append(str(curr.val))
            curr = curr.next
        stdscr.addstr(' <-> '.join(elements))

    def display_event(head, stdscr):
        curr = head
        elements = []
        while curr:
            elements.append(curr.event)
            curr = curr.next
        stdscr.addstr(elements)

    def insert_at_beginning(head, tail, val, event):
        new_node = MapDoublyNode(val, event, next = head)
        head.prev = new_node
        return new_node, tail
            
    def insert_at_end(head, tail, val, event):
        new_node = MapDoublyNode(val, event, prev = tail)
        tail.next = new_node
        return head, new_node

class Character:
    def __init__(self, health, stamina, mana, strength, agility, intelligence):
        self.health = health
        self.stamina = stamina
        self.mana = mana
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence

    def strength_attributes(self):
        pass

    def agility_attributes(self):
        pass

    def intelligence_attributes(self):
        pass

    def inventory_attributes(self):
        inventory_capacity = 2
        for _ in range(self.strength):
            inventory_capacity += 1
        #inventory_capacity = (.5 * self.strength) * 5
        return int(inventory_capacity)

    def attack(self, target, selected_item, inventory, game, stdscr):
        item_damage = inventory.damage_retrieve(selected_item)
        damage = random.randint(0,5)
        damage *= (item_damage + self.strength)
        CursesFunctions.curses_center(stdscr, f"Attack Did {damage} Points Of Damage", 1, 0)
        stdscr.getch()
        target.health -= damage
        if damage > 0:
            inventory.durability(selected_item, stdscr)
            game.player_inventory.display_hud_inventory(stdscr)
            Game.redraw_event_hud(stdscr)
        return target.health

    def display_targets(self, target_list, stdscr):
        y_offset = 10
        for i, target in enumerate(target_list):
            y_offset -= 1
            CursesFunctions.curses_center(stdscr, f"Combatant {i+1}: Health - {target.health} | Stamina - {target.stamina} | Mana - {target.mana}", y_offset, 0)

class Inventory:
    def __init__(self, character):
        self.item_array = []
        self.character = character

    def add_item(self, item_code, item_name, item_statistics, stdscr):
        #overencumber
        inventory_capacity = self.character.inventory_attributes()
        if len(self.item_array) >= inventory_capacity:
            Game.redraw_event_hud(stdscr)
            CursesFunctions.curses_center(stdscr, "You Are Over-Encumbered", 10, 0)
            stdscr.getch()
            return False
        else:
            item = {"item_code": item_code, "item_name": item_name, "item_statistics": {"damage": item_statistics[0], "durability": item_statistics[1], "max_durability": item_statistics[2]}}
            self.item_array.append(item)
            return True
        
    def npc_add_item(self, item_code, item_name, item_statistics, stdscr):
        item = {"item_code": item_code, "item_name": item_name, "item_statistics": {"damage": item_statistics[0], "durability": item_statistics[1], "max_durability": item_statistics[2]}}
        self.item_array.append(item)
        return True
    
    def add_item(self, item_code, item_name, item_statistics, stdscr):
        #overencumber
        inventory_capacity = self.character.inventory_attributes()
        if len(self.item_array) >= inventory_capacity:
            Game.redraw_event_hud(stdscr)
            CursesFunctions.curses_center(stdscr, "You Are Over-Encumbered", 10, 0)
            stdscr.getch()
            return False
        else:
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
        #stdscr.refresh()

    def display_hud_inventory(self, stdscr):
        y_offset = -7
        for i, item in enumerate(self.item_array):
            CursesFunctions.curses_center(stdscr, f"{i+1} - {item["item_name"]} - {item["item_statistics"]["damage"]} - {item["item_statistics"]["durability"]}/{item["item_statistics"]["max_durability"]}", y_offset, 15)
            y_offset -= 1
        #stdscr.refresh()

# class Weapons:
#     def __init__(self):
#         self.weapon_array = []

#     def orc_weapon_list(self):
#         self.weapon_array.add_item("orc_sword_1", "Orc Sword", [2, 3])
#         self.weapon_array.add_item("orc_axe_1", "Orc Axe", [4, 1])

class Event:
    # def __init__(self):
    #     self.world = Character(None, None, None, 1000, None, None)
    #     self.loot = Inventory(self.world)

    def random_event():
        event_array = [Event.orc_attack, Event.chest_encounter, None]
        return random.choice(event_array)
    
    def trigger_event(node, game, stdscr):
        Game.redraw_event_hud(stdscr)
        if node == None:
            return
        else:
            if node.event:
                if node.event == Event.chest_encounter:
                    node.event(node, game.player_inventory, game.player, stdscr)
                elif node.event == Event.orc_attack:
                    node.event(node, game, stdscr)
                elif node.event == Event.loot_event:
                    node.event(node, game, stdscr)

    def display_node_event(node, game, stdscr):
        events = []
        event_index = 0
        if node.event == Event.orc_attack and node.event_completed == False:
            event_index += 1
            CursesFunctions.curses_center(stdscr, f"{event_index} - Orc Attack", 10 - int(event_index), 0)
            events.append(Event.orc_attack)
        elif node.event == Event.loot_event and node.event_looted == False:
            event_index += 1
            CursesFunctions.curses_center(stdscr, f"{event_index} - Loot", 10 - int(event_index), 0)
            events.append(Event.loot_event)
        elif node.event == Event.chest_encounter and node.event_completed == False:
            event_index += 1
            CursesFunctions.curses_center(stdscr, f"{event_index} - Chest", 10 - int(event_index), 0)
            events.append(Event.chest_encounter)
        if events:
            while True:
                CursesFunctions.curses_center(stdscr, f"Choose Event (1-{event_index}) or Return (r)", 11, 0)
                y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 9 - int(event_index), 0)
                stdscr.move(y_cursor, x_cursor)
                event_input = stdscr.getch()
                event_choice = CursesFunctions.curses_getch_to_str(stdscr, event_input)
                if event_choice.isdigit():
                    selected_index = int(event_choice) - 1
                    if 0 <= selected_index < len(events):
                        if events[selected_index] == Event.chest_encounter:
                            events[selected_index](node, game.player_inventory, game.player, stdscr)
                            break
                        else:
                            events[selected_index](node, game, stdscr)
                            break
                elif event_choice == 'r' or event_choice == 'R':
                    break
                else:
                    CursesFunctions.curses_center(stdscr, "Invalid Input", 8 - int(event_index), 0)
                    continue
        else:
            CursesFunctions.curses_center(stdscr, "No Events In Current Area", 10, 0)
            stdscr.getch()

    def select_target(node, game, max_target, stdscr):
        Game.redraw_event_hud(stdscr)
        Character.display_targets(node.orc_character_list, node.orc_character_list, stdscr)
        CursesFunctions.curses_center(stdscr, f"Select Target (1-{max_target}) Or Return (r)", -1, 0)
        selected_target_input = stdscr.getch()
        selected_target = CursesFunctions.curses_getch_to_str(stdscr, selected_target_input)
        selected_target = Game.input_validation(node.orc_character_list, selected_target, stdscr)
        if selected_target == "r" or selected_target == "R":
            return None
        else:
            return selected_target
        
    def select_item(node, game, max_item, stdscr):
        Game.redraw_event_hud(stdscr)
        Character.display_targets(node.orc_character_list, node.orc_character_list, stdscr)
        CursesFunctions.curses_center(stdscr, f"Select Item (1-{max_item}) Or Return (r)", -1, 15)
        selected_item_input = stdscr.getch()
        selected_item = CursesFunctions.curses_getch_to_str(stdscr, selected_item_input)
        selected_item = Game.input_validation(game.player_inventory.item_array, selected_item, stdscr)
        if selected_item == "r" or selected_item == "R":
            return None
        else:
            return selected_item

    def orc_attack(node, game, stdscr):
        node.flee_occur = False
        if not hasattr(node, 'orc_character_list'):
            node.orc_character_list = []
            node.orc_inventory_list = []
        if node.event_completed == False and not node.orc_character_list:
            for _ in range (random.randint(1,3)):
                orc = Character(random.randint(10,15), 75, 50,3,2,3)
                node.orc_character_list.append(orc)
                orc_weapon_list = Inventory(orc)
                node.orc_inventory_list.append(orc_weapon_list)
                Inventory.npc_add_item(orc_weapon_list, "orc_sword_1", "Orc Sword", [2, 3, 3], stdscr)

        while node.orc_character_list:
            node.event_looted = True
            Game.redraw_event_hud(stdscr)
            Character.display_targets(node.orc_character_list, node.orc_character_list, stdscr)
            CursesFunctions.curses_center(stdscr, "1 - Attack\n2 - Flee", -1, 0)
            event_input = stdscr.getch()
            event_choice = CursesFunctions.curses_getch_to_str(stdscr, event_input)
            if event_choice == '1':
                while node.orc_character_list:
                    orc_amount = len(node.orc_character_list)
                    item_amount = len(game.player_inventory.item_array)
                    selected_target = Event.select_target(node, game, orc_amount, stdscr)
                    if selected_target == None:
                        break
                    selected_item = Event.select_item(node, game, item_amount, stdscr)
                    if selected_item == None:
                        continue
                    Game.redraw_event_hud(stdscr)
                    game.player.attack(node.orc_character_list[selected_target], selected_item, game.player_inventory, game, stdscr)
                    if node.orc_character_list[selected_target].health <= 0:
                        orc_inventory = node.orc_inventory_list[selected_target]
                        while orc_inventory.item_array:
                            dropped_item = orc_inventory.drop_item(0)
                            Event.add_to_loot_event(dropped_item, node, stdscr)
                        node.orc_character_list.pop(selected_target)
                        node.orc_inventory_list.pop(selected_target)
                        #node.node_loot = self.loot
                game.player_life_check(stdscr)
                #node.event_looted = False
                if not node.orc_character_list:

                    node.event_completed = True
                    node.event = Event.loot_event


            elif event_choice == '2':
                while True:
                    Game.redraw_event_hud(stdscr)
                    Character.display_targets(node.orc_character_list, node.orc_character_list, stdscr)
                    CursesFunctions.curses_center(stdscr, "Forward/Backward (f/b) Or Return (r)", -1, 0)
                    direction_input = stdscr.getch()
                    direction = CursesFunctions.curses_getch_to_str(stdscr, direction_input)

                    if direction == 'f' or direction == 'b' or direction == 'F' or direction == 'B':
                        if not Game.move_validation(game.player_position, direction):
                            CursesFunctions.curses_center(stdscr, "No Space", -2, 0)
                            stdscr.getch()
                            Game.redraw_event_hud(stdscr)
                            continue 
                        flee_chance = 1 + game.player.agility
                        flee_success = random.randint(1,10)
                        if flee_chance >= flee_success:
                            CursesFunctions.curses_center(stdscr, "Flee Success", 15, 0)
                            node.flee_occur = True
                            node.flee_direction = direction
                            return
                        else:
                            CursesFunctions.curses_center(stdscr, "Flee Failed", 15, 0)
                            game.player.health -= 10
                            game.player.stamina -= 10
                            Event.orc_attack(node, game, stdscr)
                    elif direction == 'r' or direction == 'R':
                        Event.orc_attack(node, game, stdscr)
                        break

                    else:
                        continue
            else:
                Event.orc_attack(node, game, stdscr)
        if not node.orc_character_list:
            Event.loot_event(node, game, stdscr)

    def add_to_loot_event(dropped_item, node, stdscr):
        if not hasattr(node, 'node_loot') or node.node_loot is None:
            node.node_loot = Inventory(None)
        node.node_loot.npc_add_item(dropped_item["item_code"], dropped_item["item_name"], [dropped_item["item_statistics"]["damage"], dropped_item["item_statistics"]["durability"], dropped_item["item_statistics"]["max_durability"]], stdscr)
        #node.node_loot = self.loot
        if node.event != Event.orc_attack:
            node.event = Event.loot_event
        node.event_looted = False

    def loot_event(node, game, stdscr):
        while node.node_loot:
            if not node.node_loot.item_array:
                node.event_looted = True
                return
            Game.redraw_event_hud(stdscr)
            node.node_loot.display_inventory(stdscr)
            max_loot = len(node.node_loot.item_array)
            CursesFunctions.curses_center(stdscr, f"Select Loot To Take (1-{max_loot}) Or Return (r)", 10, 0)
            selected_loot = stdscr.getch()
            selected_loot = CursesFunctions.curses_getch_to_str(stdscr, selected_loot)
            selected_loot = Game.input_validation(node.node_loot.item_array, selected_loot, stdscr)
            if selected_loot == 'r' or selected_loot == 'R':
                return node
            retrieved_loot = node.node_loot.item_retrieve(selected_loot)
            if game.player_inventory.add_item(retrieved_loot["item_code"], retrieved_loot["item_name"], [retrieved_loot["item_statistics"]["damage"], retrieved_loot["item_statistics"]["durability"], retrieved_loot["item_statistics"]["max_durability"]], stdscr) == True:
                game.player_inventory.display_hud_inventory(stdscr)
                node.node_loot.drop_item(selected_loot)
            else:
                # Game.redraw_event_hud(stdscr)
                # CursesFunctions.curses_center(stdscr, "You Are Over-Encumbered", 10, 0)
                # stdscr.getch()
                continue
                #stdscr.addstr("You Are Over-Encumbered")
                #game.player_inventory.display_inventory(stdscr)
                #player_drop_select = CursesFunctions.curses_input(Game, stdscr, 2, 2, "Drop Item (1-) Or Return (r)")
                #player_drop_select = Game.input_validation(game.player_inventory.item_array, player_drop_select, stdscr)
                #if player_drop_select == 'r' or player_drop_select == 'R':
                #    break
                #player_drop = game.player_inventory.drop_item(int(player_drop_select))
                #self.loot.add_item(player_drop["item_code"], player_drop["item_name"], [player_drop["item_statistics"]["damage"], player_drop["item_statistics"]["durability"], player_drop["item_statistics"]["max_durability"]])
        else:
            return

    def chest_encounter(node, inventory_array, character, stdscr):
        chest_ascii = r"""
*******************************************************************************
          |                   |                  |                     |
 _________|________________.=""_;=.______________|_____________________|_______
|                   |  ,-"_,=""     `"=.|                  |
|___________________|__"=._o`"-._        `"=.______________|___________________
          |                `"=._o`"=._      _`"=._                     |
 _________|_____________________:=._o "=._."_.-="'"=.__________________|_______
|                   |    __.--" , ; `"=._o." ,-"'"-._ ".   |
|___________________|_._"  ,. .` ` `` ,  `"-._"-._   ". '__|___________________
          |           |o`"=._` , "` `; .". ,  "-._"-._; ;              |
 _________|___________| ;`-.o`"=._; ." ` '`."\` . "-._ /_______________|_______
|                   | |o;    `"-.o`"=._``  '` " ,__.--o;   |
|___________________|_| ;     (#) `-.o `"=.`_.--"_o.-; ;___|___________________
____/______/______/___|o;._    "      `".o|o_.--"    ;o;____/______/______/____
/______/______/______/_"=._o--._        ; | ;        ; ;/______/______/______/_
____/______/______/______/__"=._o--._   ;o|o;     _._;o;____/______/______/____
/______/______/______/______/____"=._o._; | ;_.--"o.--"_/______/______/______/_
____/______/______/______/______/_____"=.o|o_.--""___/______/______/______/____
/______/______/______/______/______/______/______/______/______/______/______/_
*******************************************************************************
"""
        if node.event_completed == False:
            CursesFunctions.curses_clear_to_row(stdscr, 40)
            CursesFunctions.curses_center(stdscr, chest_ascii, 15, 0)
            Game.event_hud(stdscr)
            curses.echo(0)
            CursesFunctions.curses_center(stdscr, "You Discover A Chest\nOpen Chest (y/n)", 3, 0)
            chest_input = stdscr.getch()
            chest_choice = CursesFunctions.curses_getch_to_str(stdscr, chest_input)
            if chest_choice == 'y' or chest_choice == 'Y':
                inventory_capacity = character.inventory_attributes()
                # if len(inventory_array.item_array) >= inventory_capacity:
                #     CursesFunctions.curses_center(stdscr, "Unable to add item, You Are Over-Encumbered", 2, 0)
                #     return node
                #else:
                over_encumber = inventory_array.add_item("diamondsword1", "Diamond Sword", [4, 2, 2], stdscr)
                if over_encumber == False:
                    return node
                node.event_completed = True
                CursesFunctions.curses_center(stdscr, f"You Found {inventory_array}", 2, 0)
            elif chest_choice == 'n' or chest_choice == 'N':
                #CursesFunctions.curses_center(stdscr, "You Did Not Open The Chest", 4, 0)
                return
            else:
                CursesFunctions.curses_center(stdscr, "Invalid Input", 2, 0)
                Event.chest_encounter(node, inventory_array, character, stdscr)
        else:
            return
        
class Game:
    def __init__(self):
        self.head, self.tail = self.generate_world()
        self.player_position = self.head
        self.world = Character(None, None, None, 1000, None, None)
        self.loot = Inventory(self.world)
        self.max_health = 100
        self.max_stamina = 75
        self.max_mana = 50
        self.player = Character(self.max_health, self.max_stamina, self.max_mana, 1110, 10, 3)
        self.player_inventory = Inventory(self.player)
        self.menu_choice = ''
        self.player_name = ''

    def generate_world(self):
        self.head = self.tail = MapDoublyNode(1, Event.random_event())
        for i in range (2, 11):
            self.head, self.tail = MapDoublyLinkedList.insert_at_end(self.head, self.tail, i, Event.random_event())
        return self.head, self.tail

    def start_game(self, stdscr):
        stdscr.clear()
        curses.start_color()
        curses.init_color(1, 500, 500, 500) # grey color
        curses.init_pair(2, 1, curses.COLOR_BLACK)
        title_string = r"""
____________  __    __  _____ 
| ___ \ ___ \/ /    \ \|  __ \
| |_/ / |_/ / |_   _ | | |  \/
|    /|  __/| | | | || | | __ 
| |\ \| |   | | |_| || | |_\ \
\_| \_\_|   | |\__, || |\____/
             \_\__/ /_/       
               |___/          
"""
        bold_attr = curses.A_BOLD
        while True:
            curses.curs_set(0)
            stdscr.clear()
            stdscr.attron(bold_attr)
            CursesFunctions.curses_center(stdscr, title_string, 0, 0)
            stdscr.attroff(bold_attr)
            stdscr.attron(curses.color_pair(2))
            CursesFunctions.curses_center(stdscr, "Enter Any Key to Start", -5, 0)
            stdscr.attroff(curses.color_pair(2))
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
                stdscr.attron(curses.color_pair(2))
                CursesFunctions.curses_center(stdscr, "Invalid Input", -5, 0)
                stdscr.attroff(curses.color_pair(2))
                continue
            else:
                break
        self.player_inventory.add_item("unarmed", "Unarmed", [0, float('inf'), float('inf')], stdscr)
        stdscr.clear()

        # trigger event in first node
        # Event.trigger_event(self.player_position, self, stdscr)
        # if self.player_position.flee_occur:
        #     self.player_position = Game.move(self.player_position, self.player_position.flee_direction, stdscr)

    def menu(self, stdscr):
        curses.curs_set(0)
        curses.echo(0)
        menu_string = "1 - Area\n2 - Move\n3 - Rest\n4 - Gear\n5 - Exit"
        hud_height = -8
        stdscr.clear()
        CursesFunctions.curses_center(stdscr, menu_string, hud_height, 0)
        CursesFunctions.curses_box(stdscr, 8, 21, hud_height, 0)
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
            Event.display_node_event(self.player_position, self, stdscr)
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
                self.player_position = Game.move(self.player_position, direction_choice, stdscr)
                if direction_choice not in ['r', 'R']:
                    Event.trigger_event(self.player_position, self, stdscr)
                while self.player_position.flee_occur:
                    self.player_position = Game.move(self.player_position, self.player_position.flee_direction, stdscr)
                    Event.trigger_event(self.player_position, self, stdscr)
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
                    CursesFunctions.curses_center(stdscr, "Invalid Input", 8, 0)
                    continue
        else:
            self.menu(stdscr)

    def stat_hud(self, stdscr):
        character_ascii = r"""
      _,.
    ,` -.)
   ( _/-\\-._
  /,|`--._,-^|            ,
  \_| |`-._/||          ,'|
    |  `-, / |         /  /
    |     || |        /  /
     `r-._||/   __   /  /
 __,-<_     )`-/  `./  /
'  \   `---'   \   /  /
    |           |./  /
    /           //  /
\_/' \         |/  /
 |    |   _,^-'/  /
 |    , ``  (\/  /_
  \,.->._    \X-=/^
  (  /   `-._//^`
   `Y-.____(__}
    |     {__)
          ()
"""
        CursesFunctions.curses_center(stdscr, character_ascii, -15, -15)
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
        stdscr.move(-15, 10)
        stdscr.clrtoeol()
        CursesFunctions.curses_box(stdscr, 22, 35, -15, 30)

    def inventory_interact(self, node, stdscr):
        if len(self.player_inventory.item_array) != 0:
            CursesFunctions.curses_center(stdscr, f"Select Item To Drop (1-{len(self.player_inventory.item_array)}) Or Return (r)", 10, 0)
            y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 8, 0)
            drop_select = CursesFunctions.curses_input(self, stdscr, y_cursor, x_cursor, '')
            drop_select = Game.input_validation(self.player_inventory.item_array, drop_select, stdscr)
            if drop_select == 'r' or drop_select == 'R':
                return
            dropped_item = self.player_inventory.drop_item(int(drop_select))
            Event.add_to_loot_event(dropped_item, node, stdscr)
            Game.redraw_event_hud(stdscr)

            # if node.node_loot is None:
            #     node.node_loot = Inventory(self.world)
            #self.loot.add_item(dropped_item["item_code"], dropped_item["item_name"], [dropped_item["item_statistics"]["damage"], dropped_item["item_statistics"]["durability"], dropped_item["item_statistics"]["max_durability"]], stdscr)
            #self.loot.display_inventory(stdscr)
            #stdscr.getch()
        else:
            CursesFunctions.curses_center(stdscr, "Inventory Empty", 9, 0)
            stdscr.getch()

    def event_hud(stdscr):
        CursesFunctions.curses_box(stdscr, 30, 100, 12, 0) #name box

    def redraw_event_hud(stdscr):
        CursesFunctions.curses_clear_to_row(stdscr, 48) # clears screen until top of hud
        Game.event_hud(stdscr)
        #stdscr.refresh()

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
            #stdscr.refresh()
            exit()

class CursesFunctions:
    def curses_input(self, stdscr, r, c, prompt):
        curses.echo()
        stdscr.addstr(r,c,prompt)
        #stdscr.refresh()
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
        #stdscr.refresh()

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
        #stdscr.refresh()
    
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

# def main_pre_curses():
#     game = Game()
#     game.generate_world()
#     game.start_game()
#     game.menu()

#main_pre_curses()

# def main(stdscr):
#     curses.curs_set(0)
#     stdscr.clear()

#     game = Game()
#     game.menu(stdscr)


#     stdscr.refresh()
#     stdscr.getch()
#     curses.wrapper(main)

def main(stdscr):
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.echo(0)

    game = Game()
    game.generate_world()
    game.start_game(stdscr)
    game.menu(stdscr)
    
if __name__ == "__main__":
    keyboard.press_and_release('f11')
    curses.wrapper(main)
