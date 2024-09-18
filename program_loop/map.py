#© 2024 Ryan Noel Buenaventura.

class MapDoublyNode:
    def __init__(self, val, event = None, event_completed = False, event_looted = False, flee_occur = False, flee_direction = None, node_loot = None, next = None, prev = None):
        self.val = val
        self.event = event
        self.events = []
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
        stdscr.addstr(" <-> ".join(elements))

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