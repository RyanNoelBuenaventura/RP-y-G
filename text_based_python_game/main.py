#Ryan Noel Buenaventura

import random

class MapDoublyNode:
    def __init__(self, val, event = None, event_completed = False, flee_occur = False, flee_direction = None, node_loot = None, next = None, prev = None):
        self.val = val
        self.event = event
        self.event_completed = event_completed
        self.flee_occur = flee_occur
        self.flee_direction = flee_direction
        self.node_loot = node_loot
        self.next = next
        self.prev = prev

    def __str__(self):
        return str(self.val)

class MapDoublyLinkedList:
    def display(head):
        curr = head
        elements = []
        while curr:
            elements.append(str(curr.val))
            curr = curr.next
        print(' <-> '.join(elements))

    def display_event(head):
        curr = head
        elements = []
        while curr:
            elements.append(curr.event)
            curr = curr.next
        print(elements)

    def insert_at_beginning(head, tail, val, event):
        new_node = MapDoublyNode(val, event, next = head)
        head.prev = new_node
        return new_node, tail
            
    def insert_at_end(head, tail, val, event):
        new_node = MapDoublyNode(val, event, prev = tail)
        tail.next = new_node
        return head, new_node



class Character:
    def __init__(self, health, stamina, mana, strength, stealth, intelligence):
        self.health = health
        self.stamina = stamina
        self.mana = mana
        self.strength = strength
        self.stealth = stealth
        self.intelligence = intelligence

    def strength_attributes(self):
        pass

    def stealth_attributes(self):
        pass

    def intelligence_attributes(self):
        pass

    def inventory_attributes(self):
        inventory_capacity = 2
        for _ in range(self.strength):
            inventory_capacity += 1
        #inventory_capacity = (.5 * self.strength) * 5
        return int(inventory_capacity)

    def attack(self, target, selected_item, inventory):
        item_damage = inventory.damage_retrieve(selected_item)
        damage = random.randint(0,5)
        damage *= item_damage + self.strength
        print('\ndamage\n', damage)
        target.health -= damage
        if damage > 0:
            inventory.durability(selected_item)
        return target.health

    def display_targets(self, target_list):
        for i, target in enumerate(target_list):
            print(f"Target {i+1}: Health={target.health}, Stamina={target.stamina}, Mana={target.mana}")



class Inventory:
    def __init__(self, character):
        self.item_array = []
        self.character = character

        

    def add_item(self, item_code, item_name, item_statistics):
        #overencumber
        inventory_capacity = player.inventory_attributes()
        if len(self.item_array) >= inventory_capacity:
            return False
        else:
            item = {"item_code": item_code, "item_name": item_name, "item_statistics": {"damage": item_statistics[0], "durability": item_statistics[1]}}
            self.item_array.append(item)
            return True

    def damage_retrieve(self, selected_item):
        return self.item_array[int(selected_item)]["item_statistics"]["damage"]
    
    def item_retrieve(self, selected_item):
        return self.item_array[int(selected_item)]


    def drop_item(self, index):
        if 0 <= index < len(self.item_array):
            return self.item_array.pop(index)

    def display_inventory(self):
        for item in self.item_array:
            print(item["item_name"])
            print(item["item_statistics"]["damage"])

    def loot_drop(self, item, original_array):
        self.world_array.append(item)
        original_array.pop(item)

        print(self.world_array)

    def durability(self, selected_item):
        self.item_array[int(selected_item)]["item_statistics"]["durability"] -= 1
        if self.item_array[int(selected_item)]["item_statistics"]["durability"] <= 0:
            print(self.item_array[int(selected_item)]["item_name"], "is Broken!")
        for item in self.item_array:
            if item["item_statistics"]["durability"] <= 0:
                item["item_statistics"]["damage"] = 1
                item["item_statistics"]["durability"] = 0



# class Weapons:
#     def __init__(self):
#         self.weapon_array = []

#     def orc_weapon_list(self):
#         self.weapon_array.add_item("orc_sword_1", "Orc Sword", [2, 3])
#         self.weapon_array.add_item("orc_axe_1", "Orc Axe", [4, 1])

class Event:
    def select_target(node):
        Character.display_targets(node.orc_character_list, node.orc_character_list)
        print("Select Target:\n")
        selected_target = input()
        selected_target = input_validation(node.orc_character_list, selected_target)
        if selected_target == "back":
            Event.orc_attack(node)

    def orc_attack(node):
        world = Character(None, None, None, 1000, None, None)
        loot = Inventory(world)

        if not hasattr(node, 'orc_character_list'):
            print("hello human")

            node.orc_character_list = []
            node.orc_inventory_list = []

        if node.event_completed == False and not node.orc_character_list:
            for _ in range (random.randint(1,3)):
                orc = Character(random.randint(10,15), 75, 50,3,2,3)
                node.orc_character_list.append(orc)
                orc_weapon_list = Inventory(orc)
                node.orc_inventory_list.append(orc_weapon_list)
                Inventory.add_item(orc_weapon_list, "orc_sword_1", "Orc Sword", [2, 3])

        if node.orc_character_list:
            Character.display_targets(node.orc_character_list, node.orc_character_list)
            event_choice = input('\n1. Attack\n2. Flee')
            
            if event_choice == '1':
                while node.orc_character_list:
                    Character.display_targets(node.orc_character_list, node.orc_character_list)
                    print("Select Target:\n")
                    selected_target = input()
                    selected_target = input_validation(node.orc_character_list, selected_target)
                    if selected_target == "back":
                        Event.orc_attack(node)

                    print("Select Item For Attack:\n")
                    player_inventory.display_inventory()
                    selected_item = input()
                    selected_item = input_validation(player_inventory.item_array, selected_item)
                    if selected_item == "back":
                        Event.select_target(node)
                
                    player.attack(node.orc_character_list[selected_target], selected_item, player_inventory)

                    print("Orc", selected_target+1, " vs human Did damage leaving orc with: ", f"{node.orc_character_list[selected_target].health}")

                    if node.orc_character_list[selected_target].health <= 0:
                        
                        orc_inventory = node.orc_inventory_list[selected_target]
                        while orc_inventory.item_array:
                            dropped_item = orc_inventory.drop_item(0)
                            loot.add_item(dropped_item["item_code"], dropped_item["item_name"], [dropped_item["item_statistics"]["damage"], dropped_item["item_statistics"]["durability"]])


                        node.orc_character_list.pop(selected_target)
                        node.orc_inventory_list.pop(selected_target)
                        
                        print("\n")
                        node.node_loot = loot
                player_life_check()
                node.event_completed = True

            elif event_choice == '2':
                direction = input ("forward=f ||| backward=b")

                while direction != 'f' and direction != 'b':
                    direction = input ("forward=f ||| backward=b")


                if direction == 'back':
                    Event.orc_attack(node)
                flee_chance = 1 + player.stealth
                flee_success = random.randint(1,10)
                print("test")
                if flee_chance >= flee_success:
                    print("You Fled")
                    node.flee_occur = True
                    node.flee_direction = direction
                    return
                else:
                    print("Flee Failed")
                    Event.orc_attack(node)

            else:
                print("invalid att/flee input")
                Event.orc_attack(node)
        
        while node.node_loot:
            node.node_loot.display_inventory()
            print("Select Items from Loot to take")
            selected_loot = input()
            selected_loot = input_validation(node.node_loot.item_array, selected_loot)
            if selected_loot == "back":
                return node
            retrieved_loot = loot.item_retrieve(selected_loot)
            if player_inventory.add_item(retrieved_loot["item_code"], retrieved_loot["item_name"], [retrieved_loot["item_statistics"]["damage"], retrieved_loot["item_statistics"]["durability"]]) == True:
                player_inventory.add_item(retrieved_loot["item_code"], retrieved_loot["item_name"], [retrieved_loot["item_statistics"]["damage"], retrieved_loot["item_statistics"]["durability"]])
                node.node_loot.drop_item(selected_loot)
            else:
                print("overecnumbered")
                player_inventory.display_inventory()
                player_drop_select = input("select item to drop (or n to not drop any):")
                player_drop_select = input_validation(player_inventory.item_array, player_drop_select)
                if player_drop_select == 'n':
                    break
                player_drop = player_inventory.drop_item(int(player_drop_select))
                loot.add_item(player_drop["item_code"], player_drop["item_name"], [player_drop["item_statistics"]["damage"], player_drop["item_statistics"]["durability"]])
            if not node.node_loot.item_array:
                node.event_completed = True
                break
                
        
        
        else:
            return

    def chest_encounter(node, inventory_array, character):
        if node.event_completed == False:
            chest_input = input("You Found A Chest, Open? (y/n)")
            if chest_input == 'y':
                inventory_capacity = character.inventory_attributes()
                if len(inventory_array.item_array) >= inventory_capacity:
                    print("Overencumbered, would you like to remove an item to take the item from the chest?")
                    return
                else:
                    inventory_array.add_item("diamondsword1", "Diamond Sword", [1, 2])
                    node.event_completed = True
                    print("you got")
            elif chest_input == 'n':
                print("You did not open the chest")
                return
            else:
                print("invalid input")
                Event.chest_encounter(node, inventory_array, character)
        else:
            return


    def random_event():
        event_array = [Event.orc_attack, Event.chest_encounter, None]
        return random.choice(event_array)
    
    def trigger_event(node):
        if node == None:
            return
        else:
            if node.event:
                if node.event == Event.chest_encounter:
                    node.event(node, player_inventory, player)
                else:
                    node.event(node)


def input_validation(list, selection):
    if selection == 'back':
        return selection
    
    try:
        if selection == '':
            selection = len(list) + 1
        if 1 > int(selection) or len(list) < int(selection) or selection == str or selection == '' or selection == None:
            raise ValueError
    except ValueError:
        return input_validation(list, input("Invalid select out of range"))
    return int(selection) -1



def player_life_check():
    if player.health <= 0:
        print("Game Over")
        exit()

def enemy_life_check():
    if player.health <= 0:
        pass


def status():
    print(player_name + "'s Status:")
    print(f"{player.health}")
    print(f"{player.stamina}")
    print(f"{player.mana}")

def move(player_node, direction):
    if direction == 'f':
        if player_node.next:
            return player_node.next
        else:
            print("invalid, no spavce in front")
            return player_node

    elif direction == 'b':
        if player_node.prev:
            return player_node.prev
        else:
            print("invalid, no spavce behind")
            return player_node
        
    else:
        print("invalid input")
        return player_node
       

#map gen
head = tail = MapDoublyNode(1, Event.random_event())

#start at first node
player_position = head

for i in range (2, 11):
    head, tail = MapDoublyLinkedList.insert_at_end(head, tail, i, Event.random_event())
    MapDoublyLinkedList.display(head)
    MapDoublyLinkedList.display_event(head)








player = Character(100, 75, 50,0,10,3)
orc = Character(100, 75, 50,1,2,3)

player_inventory = Inventory(player)

player_inventory.add_item("unarmed", "Unarmed", [0, float('inf')])





menu_choice = input("Enter Any Key to Begin New Game")

player_name = input("Enter Name:")


print("\n")
# Event.chest_encounter(player_position, player_inventory, player)
# Event.chest_encounter(player_position, player_inventory, player)
# Event.chest_encounter(player_position, player_inventory, player)
# Event.chest_encounter(player_position, player_inventory, player)
# Event.chest_encounter(player_position, player_inventory, player)
# Event.chest_encounter(player_position, player_inventory, player)
# Event.chest_encounter(player_position, player_inventory, player)
# Event.chest_encounter(player_position, player_inventory, player)
print("\n")

# Event.orc_attack(player_position)
Event.trigger_event(player_position)





while menu_choice != 'quit':

    menu_choice = input("\n1. Player Status\n2. Surrounding Area\n3. Move\n4. Rest\nquit. Exit\n6. Check Inventory\n\n")

    if menu_choice == '1':
        status()

    elif menu_choice == '2':
        print(player_position)
        

    elif menu_choice == '3':
        direction = input ("forward=f ||| backward=b")

        player_position = move(player_position, direction)
        Event.trigger_event(player_position)
        if player_position.flee_occur:
            player_position =move(player_position, player_position.flee_direction)
        


    elif menu_choice == '4':
        player.inventory_attributes()

    elif menu_choice == '5':
        pass

    elif menu_choice == '6':
        player_inventory.display_inventory()

    elif menu_choice == '7':
        pass
