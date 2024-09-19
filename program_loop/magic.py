#© 2024 Ryan Noel Buenaventura.

from program_loop.game import *
from character.inventory import Inventory
from .curses_functions import *
from program_loop.item import Item
from design.ascii import study_ascii
from design.ascii import magic_ascii

class Magic:
    def __init__(self, character):
        self.spell_array = []
        self.character = character
        self.spell_list = {
            'healing_book_1': ("Light of Mending - Spell", [10, 15], 'defense'),
            'fireball_book_1': ("Inigo Ball - Spell", [10, 17], 'offense'),
            'ward_book_1': ("Ward of The Will - Spell", [5, 5], 'defense'),

            'entropy_dagger_book_1': ("Dagger of Ordered Entropy - Spell", [0, 10], 'offense'),
            'dark_debuff_book_1': ("Dark World - Spell", [0, 1], 'attack_situation'), # enemies cannot see, makes their att do 0 dmg for a turn
            'sound_ward_book_1': ("The Sound of Deflection - Spell", [0, 1], 'attack_situation'), # enemies damage is inflicted on themselves
            'time_book_1': ("Time Borrow - Spell", [1, 1], 'attack_situation')
        }

    def read(self, inventory, stdscr, reader, item_key, item_index, game):
        if inventory:
            CursesFunctions.curses_center(stdscr, study_ascii, 10, 0)
            CursesFunctions.curses_center(stdscr, f"Select Item To Read (1-{len(inventory)}) Or Continue To Casting (c) Or Return (r)", -1, 0)
            read_input = stdscr.getch()
            read_select = CursesFunctions.curses_getch_to_str(stdscr, read_input)
            if str(read_select).lower() == 'c':
                return 'c'
            read_select_valid = game.input_validation(inventory, read_select, stdscr)
            if str(read_select_valid).lower() == 'r':
                return 'r'

            else:
                item_index = int(read_select_valid)
                selected_item_key = Inventory.item_key_retrieve(reader.player_inventory, read_select_valid)
                selected_item_special = Inventory.item_special_retrieve(reader.player_inventory, read_select_valid)
            learned_spell = None
            Magic.clear_magic_hud(stdscr)
            CursesFunctions.curses_center(stdscr, study_ascii, 10, 0)
            book_contents = {
                'healing_book_1': "Bend light to your will in order to mend damage.",
                'fireball_book_1': "Tame the inigo to be used as a flaming projectile.",
                'ward_book_1': "If there is a will, there is a way. Ones will is fully realized through the arcane arts to create a protective ward.",
                'entropy_dagger_book_1': "Organize entropy to create a blade of pure energy.",
                'dark_debuff_book_1': "Immerse foes in a debilitating darkness leaving them unable to attack.",
                'sound_ward_book_1': "Channel sound waves to create a disturbance that reflects enemies attacks onto themselves",
                'time_book_1': "Sacrifice your youth to escape even the most dangerous situation, everyone is on your time."
            }
            if 'book' in selected_item_special:
                if reader.player.intelligence >= 5:
                    if selected_item_key in book_contents:
                        CursesFunctions.curses_center(stdscr, book_contents[selected_item_key], -1, 0)
                        stdscr.getch()

                        learned_spell = Magic(reader).spell_list[selected_item_key]
                        self.add_spell(learned_spell, reader, stdscr)
                    while True:
                        game.redraw_event_hud(stdscr)
                        CursesFunctions.curses_center(stdscr, study_ascii, 10, 0)
                        CursesFunctions.curses_center(stdscr, "Drop Book (y/n)", -1, 0)
                        drop_input = stdscr.getch()
                        drop_select = CursesFunctions.curses_getch_to_str(stdscr, drop_input)
                        if drop_select.lower() == 'y':
                            # inventory.pop(item_index)
                            from program_loop.event import Event
                            dropped_item = reader.player_inventory.drop_item(int(item_index))
                            Event.add_to_loot_event(dropped_item, reader.player_position, stdscr, self)
                            break
                        elif drop_select.lower() == 'n':
                            break
                        else:
                            continue
                else:
                    CursesFunctions.curses_center(stdscr, "You Lack The Intellect Required To Study This Material", -1, 0)
                    stdscr.getch()
            else:
                CursesFunctions.curses_center(stdscr, "After Much Effort, You Find Yourself Unable To Decipher This Item", -1, 0)
                stdscr.getch()
                return
        else:
            CursesFunctions.curses_center(stdscr, "Inventory Empty", 0, 0)
            stdscr.getch()
            return
        game.redraw_event_hud(stdscr)

    def add_spell(self, learned_spell, reader, stdscr):
        spell_name, spell_statistics, spell_special = learned_spell
        new_spell = {'spell_name': spell_name, 'spell_statistics': {'damage/heal': spell_statistics[0], 'cost': spell_statistics[1]}, 'spell_special': spell_special}
        spell_learned = any(existing_spell['spell_name'] == new_spell['spell_name'] for existing_spell in reader.player_spells.spell_array)
        if not spell_learned:
            reader.player_spells.spell_array.append(new_spell)
        else:
            Magic.clear_magic_hud(stdscr)
            CursesFunctions.curses_center(stdscr, "Spell Already Learned", -1, 0)
            stdscr.getch()

    def display_spells(self, stdscr, game):
        y_offset = len(self.spell_list) + 5
        for i, spell in enumerate(game.player_spells.spell_array):
            CursesFunctions.curses_center(stdscr, f"{i+1} - {spell['spell_name']} - DMG/HP: {spell['spell_statistics']['damage/heal']} - MP: {spell['spell_statistics']['cost']}", y_offset, 0)
            y_offset -= 1

    def spell_input_validation(self, list, selection, stdscr, game):
        if str(selection).lower() == 'r':
            return selection
        try:
            if selection == '':
                selection = len(list) + 1
            if 1 > int(selection) or len(list) < int(selection) or selection == str or selection == '' or selection == None:
                raise ValueError
        except ValueError:
            CursesFunctions.curses_box(stdscr, 30, 100, 12, 0)
            exception_input = stdscr.getch()
            exception_input = CursesFunctions.curses_getch_to_str(stdscr, exception_input)
            return Magic.spell_input_validation(self, list, exception_input, stdscr, game)
        return int(selection) -1

    def clear_magic_hud(stdscr):
        CursesFunctions.curses_clear_to_row(stdscr, 48) # clears screen until top of hud
        CursesFunctions.curses_box(stdscr, 30, 100, 12, 0) # name box

    def select_spell(self, game, spell_list, stdscr):
        Magic.clear_magic_hud(stdscr)
        CursesFunctions.curses_center(stdscr, magic_ascii, 19, 0)
        if len(game.player_spells.spell_array) <= 0:
            CursesFunctions.curses_center(stdscr, "You Know No Spells", -1, 0)
            stdscr.getch()
            return None
        CursesFunctions.curses_center(stdscr, f"Select Spell To Cast (1-{len(game.player_spells.spell_array)}) Or Return (r)", -1, 0)
        self.display_spells(stdscr, game)
        selected_spell_input = stdscr.getch()
        selected_spell = CursesFunctions.curses_getch_to_str(stdscr, selected_spell_input)
        selected_spell = self.spell_input_validation(game.player_spells.spell_array, selected_spell, stdscr, game)
        if str(selected_spell).lower() == 'r':
            return None
        else:
            return selected_spell