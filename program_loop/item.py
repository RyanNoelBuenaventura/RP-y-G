import random
from character.inventory import Inventory

class Item:
    #add special tags to unarmed and misc so that they work differently then normal items in inventory
    def __init__(self):
        self.misc_list = {
            'camping_supplies_1': ("Camping Supplies", [0, 1, 1]),
            'health_potion_1': ("Health Potion", [0, 1, 1]),
            'stamina_potion_1': ("Stamina Potion", [0, 1, 1]),
            'mana_potion_1': ("Mana Potion", [0, 1, 1])
        }
        self.weapon_list = {
            'dagger_1': ("Rusted Dagger of The Old Kings", [2, 5, 5]),
            'wood_sword_1': ("Quixotic Oak Sword of Pedagogy", [1, 10, 10]),
            'iron_sword_1': ("Iron Sword of Beeh Esse", [2, 10, 10]),
            'bo_staff_1': ("Bo Staff", [4, 15, 15]),
            'lute_1': ("Lute", [5, 1, 1]),
            'rapier_1': ("Rapier of The Old Kings", [7, 12, 12]),
            'war_axe_1': ("Orcish War Axe", [6, 13, 13]),
            'spear_1': ("Spear of Returning", [6, 15, 15]),
            'bastard_sword_1': ("Basterd's Bastard Sword", [8, 17, 17]),
            'katana_1': ("Bloodline Ending Katana", [9, 19, 19]),
            'buster_ultra_greatsword_1': ("One-Handed Guillotine, BFS", [5, 25, 25]),
            'dagger_2': ("Celestial Dagger of The Stars", [13, 25, 25]),
            'short_sword_1': ("Celestial Short Sword of The Stars", [15, 20, 20]),
            'energy_blade_1': ("Unremitting Blade of Pure Energy", [10, 100, 100])
        }
    
    def random_misc_item(self, character_item_list, stdscr, game):
        random_item_selected = random.choice(list(self.misc_list.keys()))
        self.add_item_to_inventory(random_item_selected, character_item_list, stdscr, game, self.misc_list)

    def random_weapon_item(self, character_item_list, stdscr, game):
        random_item_selected = random.choice(list(self.weapon_list.keys()))
        self.add_item_to_inventory(random_item_selected, character_item_list, stdscr, game, self.weapon_list)

    def add_item_to_inventory(self, item_key, character_item_list, stdscr, game, item_list):
        item_name, item_stats = item_list[item_key]
        Inventory.add_item(character_item_list, item_key, item_name, item_stats, stdscr, game)