#© 2024 Ryan Noel Buenaventura.

import random
from character.inventory import Inventory

class Item:
    # add special tags to unarmed and misc so that they work differently then normal items in inventory
    def __init__(self):
        self.misc_list = {
            'camping_supplies_1': ("Camping Supplies", [0, 1, 1], 'supplies', 15),
            'health_potion_1': ("Health Potion", [0, 1, 1], 'potion', 10),
            'stamina_potion_1': ("Stamina Potion", [0, 1, 1], 'potion', 10),
            'mana_potion_1': ("Mana Potion", [0, 1, 1], 'potion', 10),

            'fireball_book_1': ("Inigo Ball - Book", [0, 1, 1], 'book', 10),
            'healing_book_1': ("Light of Mending - Book", [0, 1, 1], 'book', 10),
            'ward_book_1': ("Ward of The Will - Book", [0, 1, 1], 'book', 10),

            'entropy_dagger_book_1': ("Dagger of Ordered Entropy - Book", [0, 1, 1], 'book', 10),
            # 'dark_debuff_book_1': ("Dark World - Book", [0, 1, 1], 'book'), # enemies cannot see, makes their att do 0 dmg for a turn
            # 'sound_ward_book_1': ("The Sound of Deflection - Book", [0, 1, 1], 'book'), # enemies damage is inflicted on themselves
            # 'time_book_1': ("Time Borrow - Book", [0, 1, 1], 'book') # allow you to flee 100 percent of time or kill one enemy at the cost of a 30 percent reduction of your max health with each use as it "ages you"
        }
        self.weapon_list = {
            'dagger_1': ("Rusted Dagger of The Old Kings", [2, 5, 5], 'dagger', 2),
            'wood_sword_1': ("Quixotic Oak Sword of Pedagogy", [1, 10, 10], 'sword', 4),
            'orc_sword_1': ("Orcish Sword", [3, 10, 10], 'sword', 8),
            'iron_sword_1': ("Iron Sword of Beeh Esse", [2, 10, 10], 'sword', 10),
            'bo_staff_1': ("Bo Staff", [4, 15, 15], 'blunt', 15),
            'lute_1': ("Lute", [5, 1, 1], 'blunt', 5),
            'rapier_1': ("Rapier of The Old Kings", [7, 12, 12], 'rapier', 30),
            'war_axe_1': ("Orcish War Axe", [6, 13, 13], 'axe', 30),
            'spear_1': ("Spear of Returning", [6, 15, 15], 'spear', 40),
            'bastard_sword_1': ("Basterd's Bastard Sword", [8, 17, 17], 'sword', 65),
            'katana_1': ("Bloodline Ending Katana", [9, 19, 19], 'sword', 80),
            'buster_ultra_greatsword_1': ("One-Handed Guillotine, BFS", [5, 25, 25], 'sword', 80),
            'dagger_2': ("Celestial Dagger of The Stars", [13, 25, 25], 'dagger', 85),
            'short_sword_1': ("Celestial Short Sword of The Stars", [15, 20, 20], 'sword', 90),
            'energy_blade_1': ("Unremitting Blade of Pure Energy", [10, 100, 100], 'sword', 100),
            'entropy_dagger_1': ("Dagger of Ordered Entropy - Spell", [6, 5, 5], 'dagger', 0)
        }
    
    def random_misc_item(self, character_item_list, stdscr, game):
        random_item_selected = random.choice(list(self.misc_list.keys()))
        self.add_item_to_inventory(random_item_selected, character_item_list, stdscr, game, self.misc_list)

    def random_misc_item_list(self, character_item_list, stdscr, game, store_list):
        for i in range(1, random.randint(3, 5)):
            random_item_selected = random.choice(list(self.misc_list.keys()))
            store_list.append(random_item_selected)
        
    def random_weapon_item(self, character_item_list, stdscr, game):
        random_item_selected = random.choice(list(self.weapon_list.keys()))
        self.add_item_to_inventory(random_item_selected, character_item_list, stdscr, game, self.weapon_list)

    def add_specific_weapon_item(self, character_item_list, stdscr, game, item_select):
        self.add_item_to_inventory(item_select, character_item_list, stdscr, game, self.weapon_list)

    def add_item_to_inventory(self, item_key, character_item_list, stdscr, game, item_list):
        item_name, item_stats, item_special, item_price = item_list[item_key]
        Inventory.add_item(character_item_list, item_key, item_name, item_stats, item_special, item_price, stdscr, game)

    def use_item(self, item_key, game, character_item_list, item_index):
        item = None
        if item_key in self.misc_list:
            item = self.misc_list[item_key]
        elif item_key in self.weapon_list:
            item = self.weapon_list[item_key]
        if item is not None:
            if item_key == 'health_potion_1':
                game.player.health += 10
                character_item_list.pop(int(item_index))
            elif item_key == 'stamina_potion_1':
                game.player.stamina += 10
                character_item_list.pop(int(item_index))
            elif item_key == 'mana_potion_1':
                game.player.mana += 10
                character_item_list.pop(int(item_index))
        else:
            return