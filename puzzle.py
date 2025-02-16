import random

class Door:
    id = None
    
    def __init__(self, roomA, roomB, doorkey=None, locked=False):
        self.goes_between = {roomA, roomB}
        self.doorkey      = doorkey
        self.locked       = locked
        # Define handy dictionary to get room on other side of a door
        self.other_loc = {roomA:roomB, roomB:roomA}

    ## Define a unique string representation for a door object
    def __repr__(self):
        return str( ("door", self.goes_between, self.doorkey, self.locked) )

STARTING_ROOM = "room 1"

ROOM_CONTENTS = {
    'workshop': {'key 5', 'wrench'},
    'store room': {'bucket', 'suitcase'},
    'tool cupboard': {'sledge hammer', 'anvil', 'saw', 'screwdriver'},
    'room 1': {'flashlight', 'map'},
    'room 2': {'rope', 'wood plank'},
    'room 3': {'rusty key'},
    'room 4': {'crowbar', 'ladder'},
    'room 5': {'golden key', 'torch'},
    'room 6': {'hammer', 'pliers'},
    'room 7': {'compass', 'candle'},
    'room 8': {'dagger', 'lockpick'},
    'room 9': {'shield', 'helmet'},
    'room 10': {'rust remover'},
    'hidden chamber': {'ancient scroll', 'mystic orb'},
    'storage basement': {'iron key', 'old book'},
    'armory': {'sword', 'bow', 'arrows'},
    'library': {'spell book', 'quill', 'ink bottle'},
    'dining hall': {'golden goblet', 'silver plate'},
    'kitchen': {'knife', 'pan', 'spoon'},
    'guard room': {'armor', 'whistle'},
    'tunnel entrance': {'rope ladder'},
    'secret vault': {'diamond'},
    'alchemy lab': {'potion', 'elixir'},
    'observatory': {'telescope', 'star map'},
    'blacksmith': {'forge hammer', 'metal rod'},
    'mine': {'pickaxe', 'coal'},
    'dungeon': {'prison key', 'chains'},
    'torture chamber': {'iron maiden', 'skull'},
    'throne room': {'royal crown', 'scepter'},
    'hidden grotto': {'pearl', 'seashell'},
    'wizard tower': {'staff', 'magic crystal'},
    'portal chamber': {'teleportation rune'},
    'graveyard': {'shovel', 'bone'},
    'ancient ruins': {'stone tablet', 'carved idol'},
    'lost temple': {'sacred relic', 'golden idol'},
    'desert outpost': {'canteen', 'sand goggles'},
    'mountain peak': {'climbing gear', 'ice pick'},
    'frozen cave': {'frozen heart', 'snow boots'},
    'forest hut': {'herbs', 'mortar & pestle'},
    'bandit hideout': {'stolen treasure', 'mask'},
    'merchant guild': {'coin pouch', 'ledger'},
    'harbor': {'fishing net', 'boat oar'},
    'shipwreck': {'rusty compass', 'treasure map'},
}

ITEM_WEIGHT = {
    'rusty key': 0, 'key 5': 0, 'golden key': 0, 'iron key': 0, 'prison key': 0,
    'bucket': 2, 'suitcase': 4, 'screwdriver': 1, 'sledge hammer': 5, 'anvil': 12,
    'saw': 2, 'wrench': 3, 'flashlight': 1, 'map': 1, 'rope': 2, 'wood plank': 5,
    'crowbar': 6, 'ladder': 8, 'torch': 1, 'hammer': 3, 'pliers': 1, 'compass': 1,
    'candle': 1, 'dagger': 2, 'lockpick': 1, 'shield': 6, 'helmet': 3, 'rust remover': 2,
    'ancient scroll': 1, 'mystic orb': 4, 'old book': 2, 'sword': 5,
    'bow': 3, 'arrows': 1, 'spell book': 2, 'quill': 1, 'ink bottle': 1, 'golden goblet': 4,
    'silver plate': 3, 'knife': 2, 'pan': 3, 'spoon': 1, 'armor': 10, 'whistle': 1,
    'rope ladder': 4, 'diamond': 1, 'potion': 2, 'elixir': 2, 'telescope': 6, 'star map': 2,
    'forge hammer': 7, 'metal rod': 5, 'pickaxe': 6, 'coal': 3, 'shovel': 4, 'bone': 2,
    'stone tablet': 6, 'carved idol': 5, 'sacred relic': 4, 'golden idol': 6, 'canteen': 3,
    'sand goggles': 1, 'climbing gear': 8, 'ice pick': 4, 'frozen heart': 2, 'snow boots': 3,
    'herbs': 2, 'mortar & pestle': 3, 'stolen treasure': 7, 'mask': 1, 'coin pouch': 3,
    'ledger': 2, 'fishing net': 5, 'boat oar': 4, 'rusty compass': 1, 'treasure map': 2
}

DOORS = [
    Door('workshop', 'store room'),
    Door('store room', 'tool cupboard', doorkey='rusty key', locked=True),
    Door('store room', 'storage basement', doorkey='iron key', locked=True),
    Door('storage basement', 'armory', doorkey='iron key', locked=True),
    Door('storage basement', 'library', doorkey='old book', locked=True),
    Door('room 1', 'room 2'),
    Door('room 2', 'room 1'),
    Door('room 2', 'room 3'),
    Door('room 3', 'room 2'),
    Door('room 3', 'room 4', doorkey='crowbar', locked=True),
    Door('room 4', 'room 3'),
    Door('room 4', 'tool cupboard'),
    Door('store room', 'room 1'),
    Door('workshop', 'room 5', doorkey='key 5', locked=True),
    Door('room 5', 'room 6'),
    Door('room 6', 'room 5'),
    Door('room 6', 'room 7'),
    Door('room 7', 'room 6'),
    Door('room 7', 'room 8'),
    Door('room 8', 'room 7'),
    Door('room 8', 'room 9'),
    Door('room 9', 'room 8'),
    Door('room 9', 'room 10'),
    Door('room 10', 'room 9'),
    Door('room 10', 'room 3'),  # 🔥 Connecting Room 10 back to the main puzzle
    Door('secret vault', 'hidden chamber', doorkey='iron key', locked=True),
    Door('hidden chamber', 'library'),
    Door('library', 'observatory'),
    Door('observatory', 'library'),
    Door('library', 'dungeon'),
    Door('dungeon', 'library'),
    Door('dungeon', 'torture chamber', doorkey='prison key', locked=True),
    Door('armory', 'guard room'),
    Door('guard room', 'armory'),
    Door('kitchen', 'dining hall'),
    Door('dining hall', 'kitchen'),
    Door('dining hall', 'throne room'),
    Door('throne room', 'dining hall'),
    Door('throne room', 'wizard tower'),
    Door('wizard tower', 'throne room'),
    Door('wizard tower', 'portal chamber', doorkey='magic crystal', locked=True),
    Door('portal chamber', 'wizard tower'),
    Door('harbor', 'shipwreck', doorkey='boat oar', locked=True),
    Door('shipwreck', 'harbor'),
    Door('mine', 'blacksmith'),
    Door('blacksmith', 'mine'),
    Door('mine', 'graveyard'),  # 🔥 Connecting Mine to Graveyard
    Door('graveyard', 'mine'),
    Door('graveyard', 'ancient ruins'),  # 🔥 Connecting Graveyard to Ancient Ruins
    Door('ancient ruins', 'graveyard'),
    Door('ancient ruins', 'lost temple'),  # 🔥 Connecting Ancient Ruins to Lost Temple
    Door('lost temple', 'ancient ruins'),
    Door('lost temple', 'desert outpost'),  # 🔥 Connecting Lost Temple to Desert Outpost
    Door('desert outpost', 'lost temple'),
    Door('desert outpost', 'mountain peak'),  # 🔥 Connecting Desert Outpost to Mountain Peak
    Door('mountain peak', 'desert outpost'),
    Door('mountain peak', 'frozen peak'),  # 🔥 Connecting Mountain Peak to Frozen Peak
    Door('frozen peak', 'mountain peak'),
    Door('frozen peak', 'frozen cave'),  # 🔥 Connecting Frozen Peak to Frozen Cave
    Door('frozen cave', 'frozen peak'),
    Door('forest hut', 'merchant guild'),  # 🔥 Connecting Forest Hut to Merchant Guild
    Door('merchant guild', 'forest hut'),
    Door('forest hut', 'harbor'),  # 🔥 Connecting Forest Hut to Harbor
    Door('harbor', 'forest hut'),
    Door('forest hut', 'bandit hideout', doorkey='lockpick', locked=True),
    Door('bandit hideout', 'forest hut'),
    Door('shipwreck', 'room 1'),
    Door('tunnel entrance', 'mine'),
    Door('alchemy lab', 'mine'),
]


goal_item_locations = {
    "store room": {"sledge hammer", "screwdriver", "anvil"},
    "secret vault": {"diamond"},
    "room 4": {"rope", "flashlight"},
    "wizard tower": {"magic crystal"},
    "blacksmith": {"forge hammer", "metal rod"},
    "dungeon": {"prison key"},
    "shipwreck": {"treasure map"},
}


# ROOM_CONTENTS = {
#     f'room {i}': set() for i in range(1, 101)
# }

# ITEMS = [
#     'rusty key', 'golden key', 'silver key', 'diamond key', 'bronze key',
#     'bucket', 'suitcase', 'screwdriver', 'sledge hammer', 'anvil', 'saw',
#     'wrench', 'flashlight', 'rope', 'crowbar', 'map', 'torch', 'hammer',
#     'chisel', 'pickaxe', 'ladder', 'notebook', 'pen', 'compass', 'radio',
#     'batteries', 'water bottle', 'first aid kit', 'lockpick', 'mirror',
#     'clock', 'knife', 'pocket watch', 'binoculars', 'whistle', 'camera',
#     'lantern', 'shovel', 'matches', 'fuse', 'gloves', 'boots', 'helmet',
#     'jacket', 'parachute', 'telescope', 'rubber duck', 'syringe', 'rope ladder',
#     'toolbox', 'pliers', 'multimeter', 'test tube', 'beaker', 'magnifying glass',
#     'clipboard', 'chalk', 'eraser', 'measuring tape', 'stethoscope', 'thermometer',
#     'mask', 'goggles', 'life jacket', 'fire extinguisher', 'rope harness',
#     'safety pin', 'tweezers', 'can opener', 'canned food', 'flare gun', 'lighter',
#     'watch', 'amulet', 'ancient scroll', 'book', 'manual', 'paper', 'gold coin',
#     'silver coin', 'bronze coin', 'crystal ball', 'magic wand', 'mysterious box',
#     'USB drive', 'hard drive', 'SD card', 'keycard', 'security badge',
#     'handcuffs', 'walkie-talkie', 'passport', 'ID card', 'keyring', 'clipboard',
#     'fountain pen', 'envelope', 'notepad', 'CD', 'cassette tape', 'vinyl record'
# ]

# # Randomly distribute items across rooms
# random.shuffle(ITEMS)
# for i, item in enumerate(ITEMS):
#     ROOM_CONTENTS[f'room {random.randint(1, 100)}'].add(item)

# # Fixed weights for items
# ITEM_WEIGHT = {
#     item: random.randint(1, 10) for item in ITEMS
# }

# # Make keys weightless
# for key in ['rusty key', 'golden key', 'silver key', 'diamond key', 'bronze key']:
#     ITEM_WEIGHT[key] = 0

# # Define locked doors and open doors
# DOORS = []

# # Create connected rooms
# for i in range(1, 100):
#     DOORS.append(Door(f'room {i}', f'room {i+1}'))

# # Introduce locked doors
# locked_doors = [
#     ('room 10', 'room 20', 'rusty key'),
#     ('room 25', 'room 50', 'golden key'),
#     ('room 60', 'room 70', 'silver key'),
#     ('room 80', 'room 90', 'diamond key'),
#     ('room 95', 'room 100', 'bronze key')
# ]

# for room_a, room_b, key in locked_doors:
#     DOORS.append(Door(room_a, room_b, doorkey=key, locked=True))

# # Define goal item locations (move all valuables to 'room 100')
# goal_item_locations = {
#     'room 100': {'diamond key', 'golden key', 'ancient scroll', 'magic wand', 'gold coin'}
# }