#© 2024 Ryan Noel Buenaventura.

import random
from program_loop.game import *
from .curses_functions import *
from character import *

class Event:
    def random_event():
        event_array = [Event.orc_attack, Event.chest_encounter, Event.shop, Event.smith, None]
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
                elif node.event == Event.shop:
                    node.event(node, game.player_inventory, game.player, stdscr, game)
                elif node.event == Event.smith:
                    node.event(node, game.player_inventory, game.player, stdscr, game)

    def display_node_event(node, game, stdscr):
        event_index = 0
        for event in node.events:
            # use below code for debugging
            # CursesFunctions.curses_center(stdscr, f"{event_index} - {event} - {node.event_looted}", 10 - int(event_index), 0)
            if event == Event.orc_attack and node.event_completed == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Orc Attack", 10 - int(event_index), 0)
            elif event == Event.loot_event and node.event_looted == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Loot", 10 - int(event_index), 0)
            elif event == Event.chest_encounter and node.event_completed == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Chest", 10 - int(event_index), 0)
            elif event == Event.shop and node.event_completed == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Shop", 10 - int(event_index), 0)
            elif event == Event.smith and node.event_completed == False:
                event_index += 1
                CursesFunctions.curses_center(stdscr, f"{event_index} - Smith", 10 - int(event_index), 0)    
            
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
                        elif node.events[selected_index] == Event.shop:
                            node.events[selected_index](node, game.player_inventory, game.player, stdscr, game)
                            break
                        elif node.events[selected_index] == Event.smith:
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

    def select_item(node, game, max_item, stdscr, event_ascii, select_inventory):
        if event_ascii is not None:
            CursesFunctions.curses_center(stdscr, event_ascii, 22, 0)
        if select_inventory == game.player_inventory:
            CursesFunctions.curses_center(stdscr, f"Select Item (1-{max_item}) Or Return (r)", -1, 15)
        else:
            CursesFunctions.curses_center(stdscr, f"Select Item (1-{max_item}) Or Return (r)", -1, 0)
        selected_item_input = stdscr.getch()
        selected_item = CursesFunctions.curses_getch_to_str(stdscr, selected_item_input)
        selected_item = Game.input_validation(select_inventory.item_array, selected_item, stdscr)
        if selected_item == 'r' or selected_item == 'R':
            return None
        else:
            return selected_item
        
    def items_interact(node, game, max_item, stdscr):
        while True:
            Game.redraw_event_hud(stdscr)
            CursesFunctions.curses_center(stdscr, f"Select Item (1-{max_item}) Or Return (r)", -1, 15)
            selected_item_input = stdscr.getch()
            selected_item = CursesFunctions.curses_getch_to_str(stdscr, selected_item_input)
            selected_item_validation = Game.input_validation(game.player_inventory.item_array, selected_item, stdscr)
            if selected_item.lower() == 'r':
                return None
            else:
                index = int(selected_item) - 1
                selected_item_key = Inventory.item_key_retrieve(game.player_inventory, selected_item_validation)
                Item().use_item(selected_item_key, game, game.player_inventory.item_array, index)

    def combat_select_target(node, game, max_target, combatant_list, stdscr, event_ascii):
        Game.redraw_event_hud(stdscr)
        Game.redraw_attack_ui(game, stdscr)
        CursesFunctions.curses_center(stdscr, event_ascii, 22, 0)
        Character.display_targets(combatant_list, combatant_list, stdscr)
        CursesFunctions.curses_center(stdscr, f"Select Target (1-{max_target}) - Select Self (0) - Return (r)", -1, 0)
        selected_target_input = stdscr.getch()
        selected_target = CursesFunctions.curses_getch_to_str(stdscr, selected_target_input)
        if selected_target == '0':
            selected_target = 0
            return selected_target
        selected_target = Game.input_validation(combatant_list, selected_target, stdscr)
        if selected_target == 'r' or selected_target == 'R':
            return None
        else:
            return selected_target
        
    def combat_select_item(node, game, max_item, combatant_list, stdscr, event_ascii):
        # Game.redraw_event_hud(stdscr)
        Game.redraw_attack_ui(game, stdscr)
        CursesFunctions.curses_center(stdscr, event_ascii, 22, 0)
        Character.display_targets(combatant_list, combatant_list, stdscr)
        CursesFunctions.curses_center(stdscr, f"Select Item (1-{max_item}) Or Return (r)", -1, 15)
        selected_item_input = stdscr.getch()
        selected_item = CursesFunctions.curses_getch_to_str(stdscr, selected_item_input)
        selected_item = Game.input_validation(game.player_inventory.item_array, selected_item, stdscr)
        if selected_item == 'r' or selected_item == 'R':
            return None
        else:
            return selected_item

    def attack_player(combatant_list, combatant_inventory_list, game, stdscr):
        for i, combatant in enumerate(combatant_list):
            Game.redraw_event_hud(stdscr)
            CursesFunctions.curses_center(stdscr, design.fight_ascii, 8, 0)
            CursesFunctions.curses_center(stdscr, f"Combatant {i + 1} Attacks", 3, 0)
            stdscr.getch()
            # attack player, use first item in inventory, use the corresponding combatants inventory list, game, curses functionality
            combatant.attack(game.player, 0, combatant_inventory_list[i], game, stdscr)
        Game.player_life_check(game, stdscr)
        return

    def attack_event(node, game, stdscr, combatant_health, combatant_stamina, combatant_mana, combatant_strength, combatant_agility, combatant_intelligence, combatant_level, event_ascii, combatant_character_list, combatant_inventory_list):
        """
        \n@purpose\n
        
        \n@param\n
        you dtry speaking with the orc but they are unresponsive
        \n@return\n

        \n@notes\n
        orc_ascii - Kaslanba via GitHub
        """

        node.combatant_character_list = combatant_character_list
        node.combatant_inventory_list = combatant_inventory_list
        combatant_full_amount = len(node.combatant_character_list)

        while node.combatant_character_list:
            if node.event not in node.events:
                node.events.append(node.event)
            node.event_looted = True
            Game.redraw_attack_ui(game, stdscr)
            CursesFunctions.curses_center(stdscr, event_ascii, 22, 0)
            Character.display_targets(node.combatant_character_list, node.combatant_character_list, stdscr)
            CursesFunctions.curses_center(stdscr, "1 - Attack\n2 - Flee\n3 - Use Item\n4 - Magic", 0, 0)
            event_input = stdscr.getch()
            event_choice = CursesFunctions.curses_getch_to_str(stdscr, event_input)
            if event_choice == '1':
                while node.combatant_character_list:
                    Game.redraw_lower_hud(game, stdscr)
                    Game.redraw_attack_ui(game, stdscr)
                    CursesFunctions.curses_center(stdscr, event_ascii, 22, 0)
                    combatant_amount = len(node.combatant_character_list)
                    item_amount = len(game.player_inventory.item_array)
                    selected_target = Event.combat_select_target(node, game, combatant_amount, node.combatant_character_list, stdscr, event_ascii)
                    if selected_target == None:
                        break
                    selected_item = Event.combat_select_item(node, game, item_amount, node.combatant_character_list, stdscr, event_ascii)
                    if selected_item == None:
                        continue
                    Game.redraw_attack_ui(game, stdscr)
                    CursesFunctions.curses_center(stdscr, event_ascii, 22, 0)
                    game.player.attack(node.combatant_character_list[selected_target], selected_item, game.player_inventory, game, stdscr)
                    Event.attack_player(node.combatant_character_list, node.combatant_inventory_list, game, stdscr)
                    if node.combatant_character_list[selected_target].health <= 0:
                        combatant_inventory = node.combatant_inventory_list[selected_target]
                        while combatant_inventory.item_array:
                            dropped_item = combatant_inventory.drop_item(0)
                            Event.add_to_loot_event(dropped_item, node, stdscr, game)
                        node.combatant_character_list.pop(selected_target)
                        node.combatant_inventory_list.pop(selected_target)
                        Game.xp_gain(game, 10, 20, stdscr)
                if not node.combatant_character_list:
                    if node.event in node.events:
                        node.events.remove(node.event)
                    for _ in range(combatant_full_amount):
                        gold = random.randint(0, 25)
                        game.player_gold += gold
                    node.event_completed = True
                    node.event_looted = False
                    node.event = Event.loot_event

            elif event_choice == '2':
                while True:
                    Game.player_life_check(game, stdscr)
                    if game.player.stamina > 0:
                        Game.redraw_lower_hud(game, stdscr)
                        Game.redraw_event_hud(stdscr)
                        Game.redraw_ui(game, stdscr)
                        Character.display_targets(node.combatant_character_list, node.combatant_character_list, stdscr)
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
                                node.event = Event.attack_event
                                return
                            else:
                                CursesFunctions.curses_center(stdscr, "Flee Failed", 1, 0)
                                stdscr.getch()
                                game.player.health -= 10
                                game.player.stamina -= 10
                                Game.stat_hud(game, stdscr)
                                continue
                        elif direction.lower() == 'r':
                            Event.attack_event(node, game, stdscr, node.combatant_health, node.combatant_stamina, node.combatant_mana, node.combatant_strength, node.combatant_agility, node.combatant_intelligence, node.combatant_level, node.event_ascii, node.combatant_character_list, node.combatant_inventory_list)
                            break
                        else:
                            continue
                    else:
                        CursesFunctions.curses_center(stdscr, "No Stamina!", 3, 0)
                        stdscr.getch()
                        node.flee_occur = False
                        break
            elif event_choice == '3':
                item_amount = len(game.player_inventory.item_array)
                selected_item = Event.items_interact(node, game, item_amount, stdscr)
            elif event_choice == '4':
                while True:
                    selected_target = Event.combat_select_target(node, game, node.combatant_amount, node.combatant_character_list, stdscr, event_ascii)
                    if selected_target == None:
                        break
                    selected_spell = Magic(game).select_spell(game, game.player_spells.spell_array, stdscr)
                    event_in_progress = True
                    if str(selected_target) == '0':
                        selected_target = game.player
                        Character.cast(game.player, stdscr, selected_spell, selected_target, game.player_spells, game.player_inventory, node, event_in_progress)
                        break
                    if selected_spell is not None:
                        Character.cast(game.player, stdscr, selected_spell, node.combatant_character_list[selected_target], game.player_spells, game.player_inventory, node, event_in_progress)
                        break
            else:
                Event.attack_event(node, game, stdscr, node.combatant_health, node.combatant_stamina, node.combatant_mana, node.combatant_strength, node.combatant_agility, node.combatant_intelligence, node.combatant_level, node.event_ascii, node.combatant_character_list, node.combatant_inventory_list)
        if not node.combatant_character_list:
            Event.loot_event(node, game, stdscr)

    def orc_attack(node, game, stdscr):
        if not hasattr(node, 'combatant_health'):
            node.combatant_character_list = []
            node.combatant_inventory_list = []
            node.combatant_amount = random.randint(1, 3)
        node.flee_occur = False
        if node.event_completed == False and not node.combatant_character_list:
            for _ in range(node.combatant_amount):
                node.combatant_health = random.randint(30, 50)
                node.combatant_stamina = random.randint(75, 100)
                node.combatant_mana = random.randint(25, 50)
                node.combatant_strength = random.randint(1, 3)
                node.combatant_agility = random.randint(2, 4)
                node.combatant_intelligence = random.randint(1, 3)
                node.combatant_level = random.randint(3, 5)
                node.event_ascii = design.orc_ascii
                combatant = Character(node.combatant_health, node.combatant_stamina, node.combatant_mana, node.combatant_health, node.combatant_stamina, node.combatant_mana, node.combatant_health, node.combatant_stamina, node.combatant_mana, node.combatant_strength, node.combatant_agility, node.combatant_intelligence, node.combatant_level)
                node.combatant_character_list.append(combatant)
                combatant_weapon_list = Inventory(combatant)
                node.combatant_inventory_list.append(combatant_weapon_list)
                Item().add_specific_weapon_item(combatant_weapon_list, stdscr, game, 'orc_sword_1')
        Event.attack_event(node, game, stdscr, node.combatant_health, node.combatant_stamina, node.combatant_mana, node.combatant_strength, node.combatant_agility, node.combatant_intelligence, node.combatant_level, node.event_ascii, node.combatant_character_list, node.combatant_inventory_list)
        if node.event == Event.attack_event:
            node.event = Event.orc_attack

    def add_to_loot_event(dropped_item, node, stdscr, game):
        if not hasattr(node, 'node_loot') or node.node_loot is None:
            node.node_loot = Inventory(None)
        if dropped_item:
            node.node_loot.npc_add_item(dropped_item['item_code'], dropped_item['item_name'], [dropped_item['item_statistics']['damage'], dropped_item['item_statistics']['durability'], dropped_item['item_statistics']['max_durability']], dropped_item['item_special'], dropped_item['item_price'])
            node.event_looted = False
            if node.event != Event.attack_event or node.event != Event.chest_encounter:
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
            if game.player_inventory.add_item(retrieved_loot['item_code'], retrieved_loot['item_name'], [retrieved_loot['item_statistics']['damage'], retrieved_loot['item_statistics']['durability'], retrieved_loot['item_statistics']['max_durability']], retrieved_loot['item_special'], retrieved_loot['item_price'], stdscr, game) == True:
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
            CursesFunctions.curses_center(stdscr, "You Encounter A Chest - Open (y/n)", 3, 0)
            chest_input = stdscr.getch()
            chest_choice = CursesFunctions.curses_getch_to_str(stdscr, chest_input)
            if chest_choice.lower() == 'y':
                inventory_capacity = character.inventory_attributes()
                over_encumber = Item().random_misc_item(game.player_inventory, stdscr, game)
                if over_encumber == False:
                    return node
                if node.event in node.events:
                    event_index = node.events.index
                    node.events.remove(Event.chest_encounter)
                node.event_completed = True
                CursesFunctions.curses_center(stdscr, f"You Found {inventory_array}", 2, 0)
            elif chest_choice.lower() == 'n':
                # CursesFunctions.curses_center(stdscr, "You Did Not Open The Chest", 4, 0)
                return
            else:
                CursesFunctions.curses_center(stdscr, "Invalid Input", 2, 0)
                Event.chest_encounter(node, inventory_array, character, stdscr, game)
        else:
            return
        
    def shop(node, inventory_array, character, stdscr, game):
        if node.event not in node.events:
            node.events.append(node.event)
            node.shop_item_list = Inventory(None)
            node.out_of_supply = False
        if not hasattr(node, 'shop_item_list') or not node.shop_item_list.item_array and node.out_of_supply == False:
            shop = Character(None, None, None, None, None, None, None, None, None, 1000, None, None, None)
            node.shop_item_list = Inventory(shop)
            for _ in range(1, random.randint(2, 4)):
                Item().random_weapon_item(node.shop_item_list, stdscr, game)
            for _ in range(1, random.randint(2, 4)):
                Item().random_misc_item(node.shop_item_list, stdscr, game)
                
        CursesFunctions.curses_clear_to_row(stdscr, 40)
        # CursesFunctions.curses_center(stdscr, design.shop_ascii, 15, 0)
        Game.redraw_ui(game, stdscr)
        curses.echo(0)
        CursesFunctions.curses_center(stdscr, "You Encounter A Shop - Enter (y/n)", 3, 0)
        shop_input = stdscr.getch()
        shop_choice = CursesFunctions.curses_getch_to_str(stdscr, shop_input)
        if shop_choice.lower() == 'y':
            while True:
                Game.redraw_event_hud(stdscr)
                CursesFunctions.curses_center(stdscr, "Buy Or Sell (b/s) Or Return (r)", 3, 0)
                buy_or_sell_input = stdscr.getch()
                buy_or_sell_select = CursesFunctions.curses_getch_to_str(stdscr, buy_or_sell_input)
                if buy_or_sell_select.lower() == 'b':
                    if len(node.shop_item_list.item_array) <= 0:
                        Game.redraw_event_hud(stdscr)
                        CursesFunctions.curses_center(stdscr, "Shop Out Of Supply", 3, 0)
                        stdscr.getch()
                        continue
                    else:
                        while True:
                            Game.redraw_event_hud(stdscr)
                            node.shop_item_list.display_inventory(stdscr)
                            buy_amount = len(node.shop_item_list.item_array)
                            CursesFunctions.curses_center(stdscr, f"Select Item (1-{buy_amount}) Or Return (r)", -1, 0)
                            buy_select = Event.select_item(node, game, buy_amount, stdscr, None, node.shop_item_list)
                            if buy_select == None:
                                break
                            Game.redraw_event_hud(stdscr)
                            CursesFunctions.curses_center(stdscr, f"Confirm Transaction Of {node.shop_item_list.item_array[buy_select]['item_price']} Gold (y/n)", 3, 0)
                            buy_confirm_input = stdscr.getch()
                            buy_confirm_select = CursesFunctions.curses_getch_to_str(stdscr, buy_confirm_input)
                            if buy_confirm_select.lower() == 'y':
                                inventory_capacity = character.inventory_attributes()
                                if inventory_capacity <= len(game.player_inventory.item_array):
                                    Game.redraw_event_hud(stdscr)
                                    CursesFunctions.curses_center(stdscr, "You Are Over-Encumbered", 10, 0)
                                    stdscr.getch()
                                    continue
                                price = int(node.shop_item_list.item_array[buy_select]['item_price'])
                                if price > game.player_gold:
                                    Game.redraw_event_hud(stdscr)
                                    CursesFunctions.curses_center(stdscr, "Too Expensive!", 3, 0)
                                    stdscr.getch()
                                    continue
                                else:
                                    game.player_gold -= price
                                    Inventory.add_item(game.player_inventory, node.shop_item_list.item_array[buy_select]['item_code'], node.shop_item_list.item_array[buy_select]['item_name'], [node.shop_item_list.item_array[buy_select]['item_statistics']['damage'], node.shop_item_list.item_array[buy_select]['item_statistics']['durability'], node.shop_item_list.item_array[buy_select]['item_statistics']['max_durability']], node.shop_item_list.item_array[buy_select]['item_special'], node.shop_item_list.item_array[buy_select]['item_price'], stdscr, game)
                                Inventory.drop_item(node.shop_item_list, buy_select)
                                Game.redraw_lower_hud(game, stdscr)
                                if len(node.shop_item_list.item_array) <= 0:
                                     node.out_of_supply = True
                                break
                            elif buy_confirm_select.lower() == 'n':
                                break
                            else:
                                continue
                        continue

                elif buy_or_sell_select.lower() == 's':
                    while True:
                        Game.redraw_event_hud(stdscr)
                        sell_amount = len(game.player_inventory.item_array)
                        sell_select = Event.select_item(node, game, sell_amount, stdscr, None, game.player_inventory)
                        if not game.player_inventory:
                            CursesFunctions.curses_center(stdscr, "Inventory Empty", 3, 0)
                            stdscr.getch()
                            break
                        elif sell_select == None:
                            break
                        elif 'unarmed' in inventory_array.item_array[sell_select]['item_special']:
                            Game.redraw_event_hud(stdscr)
                            CursesFunctions.curses_center(stdscr, "You Offer Your Fists To The Shop Owner, They Were Unpleased.", 3, 0)
                            stdscr.getch()
                            continue
                        while True:
                            Game.redraw_event_hud(stdscr)
                            CursesFunctions.curses_center(stdscr, f"Confirm Transaction Of {inventory_array.item_array[sell_select]['item_price']} Gold (y/n)", 3, 0)
                            sale_confirm_input = stdscr.getch()
                            sale_confirm_select = CursesFunctions.curses_getch_to_str(stdscr, sale_confirm_input)
                            if sale_confirm_select.lower() == 'y':
                                price = int(inventory_array.item_array[sell_select]['item_price'])
                                if int(inventory_array.item_array[sell_select]['item_statistics']['durability']) != int(inventory_array.item_array[sell_select]['item_statistics']['max_durability']):
                                    price -= random.randint(1, 5)
                                    if price <= 0:
                                        price = 1
                                game.player_gold += price
                                Inventory.npc_add_item(node.shop_item_list, inventory_array.item_array[sell_select]['item_code'], inventory_array.item_array[sell_select]['item_name'], [inventory_array.item_array[sell_select]['item_statistics']['damage'], inventory_array.item_array[sell_select]['item_statistics']['durability'], inventory_array.item_array[sell_select]['item_statistics']['max_durability']], inventory_array.item_array[sell_select]['item_special'], inventory_array.item_array[sell_select]['item_price'])
                                Inventory.drop_item(inventory_array, sell_select)
                                Game.redraw_lower_hud(game, stdscr)
                                break
                            elif sale_confirm_select.lower() == 'n':
                                break
                            else:
                                continue
                        continue
                elif buy_or_sell_select.lower() == 'r':
                    return
                else:
                    continue

        elif shop_choice.lower() == 'n':
            # CursesFunctions.curses_center(stdscr, "You Did Not Enter", 4, 0)
            return
        else:
            CursesFunctions.curses_center(stdscr, "Invalid Input", 2, 0)
            Event.shop(node, inventory_array, character, stdscr, game)

        
    def smith(node, inventory_array, character, stdscr, game):
        if node.event_completed == False:
            if node.event not in node.events:
                node.events.append(node.event)
            CursesFunctions.curses_clear_to_row(stdscr, 40)
            CursesFunctions.curses_center(stdscr, design.anvil_ascii, 15, 0)
            Game.redraw_ui(game, stdscr)
            curses.echo(0)
            CursesFunctions.curses_center(stdscr, "You Encounter A Smith - Enter (y/n)", 3, 0)
            smith_input = stdscr.getch()
            smith_choice = CursesFunctions.curses_getch_to_str(stdscr, smith_input)
            if smith_choice.lower() == 'y':
                while True:
                    Game.redraw_event_hud(stdscr)
                    CursesFunctions.curses_center(stdscr, design.anvil_ascii, 15, 0)
                    max_item = len(game.player_inventory.item_array)
                    CursesFunctions.curses_center(stdscr, f"Select Item For Repair (1-{max_item}) Or Return (r)", -1, 14)
                    selected_item_input = stdscr.getch()
                    selected_item = CursesFunctions.curses_getch_to_str(stdscr, selected_item_input)
                    selected_item = Game.input_validation(game.player_inventory.item_array, selected_item, stdscr)
                    if selected_item == 'r' or selected_item == 'R':
                        return None
                    elif inventory_array.item_array[selected_item]['item_statistics']['durability'] == inventory_array.item_array[selected_item]['item_statistics']['max_durability']:
                        Game.redraw_event_hud(stdscr)
                        CursesFunctions.curses_center(stdscr, design.anvil_ascii, 15, 0)
                        CursesFunctions.curses_center(stdscr, "Item Does Not Require Repair", 3, 0)
                        stdscr.getch()
                        continue
                    Game.redraw_event_hud(stdscr)
                    CursesFunctions.curses_center(stdscr, design.anvil_ascii, 15, 0)
                    node.repair_price = (inventory_array.item_array[selected_item]['item_price'] / 3) + random.randint(0, 5)
                    CursesFunctions.curses_center(stdscr, f"Repair For {int(node.repair_price)} (y/n)", 3, 0)
                    confirm_input = stdscr.getch()
                    confirm_choice = CursesFunctions.curses_getch_to_str(stdscr, confirm_input)
                    if confirm_choice.lower() == 'y' and game.player_gold >= node.repair_price:
                        game.player_gold -= int(node.repair_price)
                        inventory_array.item_array[selected_item]['item_statistics']['durability'] = inventory_array.item_array[selected_item]['item_statistics']['max_durability']
                        break
                    elif confirm_choice.lower() == 'n':
                        continue
                    elif game.player_gold < node.repair_price:
                        Game.redraw_event_hud(stdscr)
                        CursesFunctions.curses_center(stdscr, design.anvil_ascii, 15, 0)
                        CursesFunctions.curses_center(stdscr, f"Insufficient Funds", 3, 0)
                        stdscr.getch()
                        continue
                    else:
                        CursesFunctions.curses_center(stdscr, "Invalid Input", 2, 0)
                        continue
            elif smith_choice.lower() == 'n':
                # CursesFunctions.curses_center(stdscr, "You Did Not Enter", 4, 0)
                return
            else:
                CursesFunctions.curses_center(stdscr, "Invalid Input", 2, 0)
                Event.smith(node, inventory_array, character, stdscr, game)
        else:
            return
