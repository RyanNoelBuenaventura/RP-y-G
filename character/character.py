#© 2024 Ryan Noel Buenaventura.

import random
import math
from program_loop.curses_functions import *
import program_loop.game
from program_loop.magic import *

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
        # inventory_capacity = (.5 * self.strength) * 5
        return int(inventory_capacity)

    # fully refill attributes
    def refresh_attributes(self):
        self.strength_attributes()
        self.agility_attributes()
        self.intelligence_attributes()
        self.inventory_attributes()
    
    # update attributes without altering current health, stamina, mana
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
        
        # theoretically prevents stats from being negative, have not really tested
        if self.health < 0:
            self.health = 0
        if self.stamina < 0:
            self.stamina = 0
        if self.mana < 0:
            self.mana = 0

    def attack(self, target, selected_item, inventory, game, stdscr):
        if self.stamina > 0:
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
            self.stamina -= random.randint(0, 15 + self.level)
            self.stamina += random.randint(0, self.agility)
            if damage > 0:
                inventory.durability(selected_item, stdscr)
                game.player_inventory.display_hud_inventory(stdscr)
                program_loop.Game.redraw_event_hud(stdscr)
                program_loop.Game.redraw_ui(game, stdscr)
            return target.health
        else:
            CursesFunctions.curses_center(stdscr, "No Stamina!", 1, 0)
            stdscr.getch()
            return target.health
        
    def heal_target(target, heal):
        target.health += heal

    def damage_target(target, damage):
        target.health -= damage

    def cast(caster, stdscr, selected_spell_index, target, magic_instance, inventory, game, event_in_progress):
        if selected_spell_index == None:
            return
        if caster.mana <= 0:
            Magic.clear_magic_hud(stdscr)
            CursesFunctions.curses_center(stdscr, "No Mana!", -1, 0)
            stdscr.getch()
            return
        selected_spell = magic_instance.spell_array[selected_spell_index]
        if selected_spell['spell_special'] == 'attack_situation' and event_in_progress == False:
            Magic.clear_magic_hud(stdscr)
            CursesFunctions.curses_center(stdscr, "Spell Cannot Be Cast In This Situation", -1, 0)
            stdscr.getch()
            return
        spell_name = selected_spell['spell_name']
        spell_statistics = selected_spell['spell_statistics']
        spell_effect_amount = spell_statistics.get('damage/heal', 0)
        spell_effects = {
            "Light of Mending - Spell": lambda: Character.heal_target(target, spell_effect_amount),
            "Inigo Ball - Spell": lambda: Character.damage_target(target, spell_effect_amount),
            "Ward of The Will - Spell": lambda: Character.heal_target(target, spell_effect_amount),
            "Dagger of Ordered Entropy - Spell": lambda: Item().add_specific_weapon_item(inventory, stdscr, game, 'entropy_dagger_1'),
            "The Sound of Deflection - Spell": lambda: None,
            "Dark World - Spell": lambda: None,
            "Time Borrow - Spell": lambda: None
        }
        if spell_name in spell_effects:
            spell_effects[spell_name]()
        caster.mana -= spell_statistics['cost']

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