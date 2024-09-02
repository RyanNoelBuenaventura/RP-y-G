import random
from .game import *
from .curses_functions import *
from character import *

class Event:
    def random_event():
        event_array = [Event.orc_attack, Event.chest_encounter, None]
        return random.choice(event_array)
    
    def trigger_event(node, game, stdscr):
        Game.redraw_event_hud(stdscr)
        Game.redraw_ui(game, stdscr)
        if node == None:
            return
        else:
            if node.event:
                if node.event == Event.chest_encounter:
                    node.event(node, game.player_inventory, game.player, stdscr, game)
                elif node.event == Event.orc_attack:
                    node.event(node, game, stdscr)
                elif node.event == Event.loot_event:
                    node.event(node, game, stdscr)

    def display_node_event(node, game, stdscr):
        event_index = 0
        for event in node.events:
            #use below code for debugging
            #CursesFunctions.curses_center(stdscr, f"{event_index} - {event} - {node.event_looted}", 10 - int(event_index), 0)
            if event == Event.orc_attack and node.event_completed == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Orc Attack", 10 - int(event_index), 0)
            elif event == Event.loot_event and node.event_looted == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Loot", 10 - int(event_index), 0)
            elif event == Event.chest_encounter and node.event_completed == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Chest", 10 - int(event_index), 0)
                
        if event_index > 0:
            while True:
                CursesFunctions.curses_center(stdscr, f"Choose Event (1-{event_index}) or Return (r)", 11, 0)
                y_cursor, x_cursor = CursesFunctions.curses_center_insertion_point(stdscr, 9 - int(event_index), 0)
                stdscr.move(y_cursor, x_cursor)
                event_input = stdscr.getch()
                event_choice = CursesFunctions.curses_getch_to_str(stdscr, event_input)
                if event_choice.isdigit():
                    selected_index = int(event_choice) - 1
                    if 0 <= selected_index < len(node.events):
                        if node.events[selected_index] == Event.chest_encounter:
                            node.events[selected_index](node, game.player_inventory, game.player, stdscr, game)
                            break
                        else:
                            node.events[selected_index](node, game, stdscr)
                            break
                elif event_choice.lower() == 'r':
                    break
                else:
                    CursesFunctions.curses_center(stdscr, "Invalid Input", 8 - int(event_index), 0)
                    continue
        else:
            CursesFunctions.curses_center(stdscr, "No Events In Current Area", 10, 0)
            stdscr.getch()

    def select_target(node, game, max_target, combatant_list, stdscr):
        Game.redraw_event_hud(stdscr)
        # CursesFunctions.curses_center(stdscr, design.orc_ascii, 22, 0)
        Character.display_targets(combatant_list, combatant_list, stdscr)
        CursesFunctions.curses_center(stdscr, f"Select Target (1-{max_target}) Or Return (r)", -1, 0)
        selected_target_input = stdscr.getch()
        selected_target = CursesFunctions.curses_getch_to_str(stdscr, selected_target_input)
        selected_target = Game.input_validation(node.orc_character_list, selected_target, stdscr)
        if selected_target == "r" or selected_target == "R":
            return None
        else:
            return selected_target
        
    def select_item(node, game, max_item, combatant_list, stdscr):
        Game.redraw_event_hud(stdscr)
        # CursesFunctions.curses_center(stdscr, design.orc_ascii, 22, 0)
        Character.display_targets(combatant_list, combatant_list, stdscr)
        CursesFunctions.curses_center(stdscr, f"Select Item (1-{max_item}) Or Return (r)", -1, 15)
        selected_item_input = stdscr.getch()
        selected_item = CursesFunctions.curses_getch_to_str(stdscr, selected_item_input)
        selected_item = Game.input_validation(game.player_inventory.item_array, selected_item, stdscr)
        if selected_item == "r" or selected_item == "R":
            return None
        else:
            return selected_item

    def attack_player(combatant_list, combatant_inventory_list, game, stdscr):
        for i, combatant in enumerate(combatant_list):
            Game.redraw_event_hud(stdscr)
            CursesFunctions.curses_center(stdscr, design.fight_ascii, 8, 0)
            CursesFunctions.curses_center(stdscr, f"Combatant {i + 1} Attacks", 3, 0)
            stdscr.getch()
            #attack player, use first item in inventory, use the corresponding combatants inventory list, game, curses functionality
            combatant.attack(game.player, 0, combatant_inventory_list[i], game, stdscr)
        Game.player_life_check(game, stdscr)
        return

    def orc_attack(node, game, stdscr):
        """
        \n@purpose\n
        
        \n@param\n
        you dtry speaking with the orc but they are unresponsive
        \n@return\n

        \n@notes\n
        orc_ascii - Kaslanba via GitHub
        """
        node.flee_occur = False
        if not hasattr(node, 'orc_character_list'):
            node.orc_character_list = []
            node.orc_inventory_list = []
        if node.event_completed == False and not node.orc_character_list:
            for _ in range (random.randint(1,3)):
                orc_max_health = random.randint(10,15)
                orc = Character(orc_max_health, 75, 50, orc_max_health, 75, 50, orc_max_health, 75, 50, 3,2,3, 5)
                node.orc_character_list.append(orc)
                orc_weapon_list = Inventory(orc)
                node.orc_inventory_list.append(orc_weapon_list)
                Inventory.npc_add_item(orc_weapon_list, "orc_sword_1", "Orc Sword", [2, 3, 3])

        while node.orc_character_list:
            if node.event not in node.events:
                node.events.append(node.event)
            node.event_looted = True
            Game.redraw_orc_ui(game, stdscr)
            CursesFunctions.curses_center(stdscr, design.orc_ascii, 22, 0)
            Character.display_targets(node.orc_character_list, node.orc_character_list, stdscr)
            CursesFunctions.curses_center(stdscr, "1 - Attack\n2 - Flee", -1, 0)
            event_input = stdscr.getch()
            event_choice = CursesFunctions.curses_getch_to_str(stdscr, event_input)
            if event_choice == '1':
                while node.orc_character_list:
                    Game.redraw_orc_ui(game, stdscr)
                    CursesFunctions.curses_center(stdscr, design.orc_ascii, 22, 0)
                    orc_amount = len(node.orc_character_list)
                    item_amount = len(game.player_inventory.item_array)
                    selected_target = Event.select_target(node, game, orc_amount, node.orc_character_list, stdscr)
                    if selected_target == None:
                        break
                    selected_item = Event.select_item(node, game, item_amount, node.orc_character_list, stdscr)
                    if selected_item == None:
                        continue
                    Game.redraw_orc_ui(game, stdscr)
                    CursesFunctions.curses_center(stdscr, design.orc_ascii, 22, 0)
                    game.player.attack(node.orc_character_list[selected_target], selected_item, game.player_inventory, game, stdscr)
                    Event.attack_player(node.orc_character_list, node.orc_inventory_list, game, stdscr)
                    if node.orc_character_list[selected_target].health <= 0:
                        orc_inventory = node.orc_inventory_list[selected_target]
                        while orc_inventory.item_array:
                            dropped_item = orc_inventory.drop_item(0)
                            Event.add_to_loot_event(dropped_item, node, stdscr, game)
                        node.orc_character_list.pop(selected_target)
                        node.orc_inventory_list.pop(selected_target)
                        Game.xp_gain(game, 105, 106, stdscr)
                #game.player_life_check(stdscr)
                if not node.orc_character_list:
                    if node.event in node.events:
                        node.events.remove(Event.orc_attack)
                    node.event_completed = True
                    node.event_looted = False
                    node.event = Event.loot_event


            elif event_choice == '2':
                while True:
                    Game.redraw_event_hud(stdscr)
                    Game.redraw_ui(game, stdscr)
                    Character.display_targets(node.orc_character_list, node.orc_character_list, stdscr)
                    CursesFunctions.curses_center(stdscr, "Forward/Backward (f/b) Or Return (r)", -1, 0)
                    direction_input = stdscr.getch()
                    direction = CursesFunctions.curses_getch_to_str(stdscr, direction_input)
                    if direction.lower() == 'f' or direction.lower() == 'b':
                        if not Game.move_validation(game.player_position, direction):
                            CursesFunctions.curses_center(stdscr, "No Space", -2, 0)
                            stdscr.getch()
                            Game.redraw_event_hud(stdscr)
                            Game.redraw_ui(game, stdscr)
                            continue 
                        flee_chance = 1 + game.player.agility
                        flee_success = random.randint(1,10)
                        if flee_chance >= flee_success:
                            CursesFunctions.curses_center(stdscr, "Flee Success", 1, 0)
                            stdscr.getch()
                            node.flee_occur = True
                            node.flee_direction = direction
                            node.event = Event.orc_attack
                            return
                        else:
                            CursesFunctions.curses_center(stdscr, "Flee Failed", 1, 0)
                            stdscr.getch()
                            game.player.health -= 10
                            game.player.stamina -= 10
                            Game.stat_hud(game, stdscr)
                            continue
                    elif direction.lower() == 'r':
                        Event.orc_attack(node, game, stdscr)
                        break
                    else:
                        continue
            else:
                Event.orc_attack(node, game, stdscr)
        if not node.orc_character_list:
            Event.loot_event(node, game, stdscr)

    def add_to_loot_event(dropped_item, node, stdscr, game):
        if not hasattr(node, 'node_loot') or node.node_loot is None:
            node.node_loot = Inventory(None)
        node.node_loot.npc_add_item(dropped_item["item_code"], dropped_item["item_name"], [dropped_item["item_statistics"]["damage"], dropped_item["item_statistics"]["durability"], dropped_item["item_statistics"]["max_durability"]])
        node.event_looted = False
        if node.event != Event.orc_attack or node.event != Event.chest_encounter:
            node.event = Event.loot_event
        if node.event not in node.events:
            node.events.append(node.event)
        
        
    def loot_event(node, game, stdscr):
        while node.node_loot:
            if not node.node_loot.item_array:
                node.event_looted = True
                return
            Game.redraw_event_hud(stdscr)
            Game.redraw_ui(game, stdscr)
            node.node_loot.display_inventory(stdscr)
            max_loot = len(node.node_loot.item_array)
            CursesFunctions.curses_center(stdscr, f"Select Loot To Take (1-{max_loot}) Or Return (r)", 10, 0)
            selected_loot = stdscr.getch()
            selected_loot = CursesFunctions.curses_getch_to_str(stdscr, selected_loot)
            selected_loot = Game.input_validation(node.node_loot.item_array, selected_loot, stdscr)
            if str(selected_loot).lower() == 'r':
                return node
            retrieved_loot = node.node_loot.item_retrieve(selected_loot)
            if game.player_inventory.add_item(retrieved_loot["item_code"], retrieved_loot["item_name"], [retrieved_loot["item_statistics"]["damage"], retrieved_loot["item_statistics"]["durability"], retrieved_loot["item_statistics"]["max_durability"]], stdscr, game) == True:
                game.player_inventory.display_hud_inventory(stdscr)
                node.node_loot.drop_item(selected_loot)
            else:
                continue
        else:
            return

    def chest_encounter(node, inventory_array, character, stdscr, game):

        if node.event_completed == False:
            if node.event not in node.events:
                node.events.append(node.event)
            CursesFunctions.curses_clear_to_row(stdscr, 40)
            CursesFunctions.curses_center(stdscr, design.chest_ascii, 15, 0)
            Game.redraw_ui(game, stdscr)
            curses.echo(0)
            CursesFunctions.curses_center(stdscr, "You Discover A Chest\nOpen Chest (y/n)", 3, 0)
            chest_input = stdscr.getch()
            chest_choice = CursesFunctions.curses_getch_to_str(stdscr, chest_input)
            if chest_choice.lower() == 'y':
                inventory_capacity = character.inventory_attributes()
                over_encumber = inventory_array.add_item("diamondsword1", "Diamond Sword", [4, 2, 2], stdscr, game)
                if over_encumber == False:
                    return node
                if node.event in node.events:
                    event_index = node.events.index
                    node.events.remove(Event.chest_encounter)
                node.event_completed = True
                CursesFunctions.curses_center(stdscr, f"You Found {inventory_array}", 2, 0)
            elif chest_choice.lower() == 'n':
                #CursesFunctions.curses_center(stdscr, "You Did Not Open The Chest", 4, 0)
                return
            else:
                CursesFunctions.curses_center(stdscr, "Invalid Input", 2, 0)
                Event.chest_encounter(node, inventory_array, character, stdscr, game)
        else:
            return