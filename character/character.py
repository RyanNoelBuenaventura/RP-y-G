import random
import math
from program_loop.curses_functions import *
import program_loop.game

class Character:
    def __init__(self, health, stamina, mana, max_health, max_stamina, max_mana, base_health, base_stamina, base_mana, strength, agility, intelligence, level):
        self.health = health
        self.stamina = stamina
        self.mana = mana
        self.max_health = max_health
        self.max_stamina = max_stamina
        self.max_mana = max_mana
        self.base_health = base_health
        self.base_stamina = base_stamina
        self.base_mana = base_mana
        self.strength = strength
        self.agility = agility
        self.intelligence = intelligence
        self.level = level

    def strength_attributes(self):
        self.health = self.base_health
        self.max_health = self.base_health
        for _ in range(self.strength):
            self.health += 5
            self.max_health += 5

    def agility_attributes(self):
        self.stamina = self.base_stamina
        self.max_stamina = self.base_stamina
        for _ in range(self.agility):
            self.stamina += 5
            self.max_stamina += 5

    def intelligence_attributes(self):
        self.mana = self.base_mana
        self.max_mana = self.base_mana
        for _ in range(self.intelligence):
            self.mana += 5
            self.max_mana += 5

    def inventory_attributes(self):
        inventory_capacity = 2
        for _ in range(self.strength):
            inventory_capacity += 1
        #inventory_capacity = (.5 * self.strength) * 5
        return int(inventory_capacity)

    #fully refill attributes
    def refresh_attributes(self):
        self.strength_attributes()
        self.agility_attributes()
        self.intelligence_attributes()
        self.inventory_attributes()
    
    #update attributes without altering current health, stamina, mana
    def update_attributes(self):
        current_health = self.health
        current_stamina = self.stamina
        current_mana = self.mana
        self.strength_attributes()
        self.agility_attributes()
        self.intelligence_attributes()
        self.inventory_attributes()
        self.health = current_health
        self.stamina = current_stamina
        self.mana = current_mana

    def attack(self, target, selected_item, inventory, game, stdscr):
        item_damage = inventory.damage_retrieve(selected_item)
        damage = random.randint(0,5)
        damage *= (item_damage + self.strength)
        if damage == 0:
            CursesFunctions.curses_center(stdscr, "Attack Missed!", 2, 0)
        else:
            damage = Character.mitigate(target, damage, stdscr)
        CursesFunctions.curses_center(stdscr, f"Attack Did {damage} Points Of Damage", 1, 0)
        stdscr.getch()
        target.health -= damage
        if damage > 0:
            inventory.durability(selected_item, stdscr)
            game.player_inventory.display_hud_inventory(stdscr)
            program_loop.Game.redraw_event_hud(stdscr)
            program_loop.Game.redraw_ui(game, stdscr)
        return target.health
    
    def mitigate(self, damage, stdscr):
        mitigated_damage = damage
        mit_chance = 1 + self.agility
        mit_success = random.randint(5, 15)
        if mit_chance > mit_success:
            mitigated_damage = math.ceil(damage * 0.10)
            mitigated_string = damage - mitigated_damage
            CursesFunctions.curses_center(stdscr, f"Mitigated {mitigated_string} Points of Damage", 2, 0)
            stdscr.getch()
        return mitigated_damage       

    def display_targets(self, target_list, stdscr):
        y_offset = 10
        for i, target in enumerate(target_list):
            y_offset -= 1
            CursesFunctions.curses_center(stdscr, f"Combatant {i+1}: Health - {target.health} | Stamina - {target.stamina} | Mana - {target.mana}", y_offset, 0)