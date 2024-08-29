import random
from program_loop.curses_functions import *
import program_loop.game

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
            program_loop.Game.redraw_event_hud(stdscr)
            program_loop.Game.redraw_ui(game, stdscr)
        return target.health

    def display_targets(self, target_list, stdscr):
        y_offset = 10
        for i, target in enumerate(target_list):
            y_offset -= 1
            CursesFunctions.curses_center(stdscr, f"Combatant {i+1}: Health - {target.health} | Stamina - {target.stamina} | Mana - {target.mana}", y_offset, 0)