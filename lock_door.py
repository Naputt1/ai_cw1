from bbmodcache.bbSearch import SearchProblem, search
import networkx as nx
from copy import deepcopy
import matplotlib.pyplot as plt
import time

from puzzle import Door, ROOM_CONTENTS, ITEM_WEIGHT, DOORS, goal_item_locations, STARTING_ROOM



class Robot:
    def __init__(self, location, carried_items, strength):
        self.location      = location
        self.carried_items = carried_items
        self.strength      = strength

    def weight_carried(self):
        return sum([ITEM_WEIGHT[i] for i in self.carried_items])

    ## Define unique string representation for the state of the robot object
    def __repr__(self):
        return str( ( self.location,
                      self.carried_items,
                      self.strength ) )

class State:
    goal_item_locations = None
    __dependencies = {}
    
    def __init__( self, robot, doors, room_contents ):
        self.robot: Robot = robot
        self.room_contents = room_contents
        
        doors_dict = {}
        for i in range(len(doors)):
            doors[i].id = i
            doors_dict[i] = doors[i]
        self.doors:dict[Door] = doors_dict
        
        graph = nx.DiGraph()
        graph.add_nodes_from(room_contents.keys())
        
        for door in self.doors.values():
            doorList = list(door.goes_between)
            weight = 2 if door.locked else 1
            graph.add_edge(doorList[0], doorList[1], weight=weight, id=door.id)
            graph.add_edge(doorList[1], doorList[0], weight=weight, id=door.id)
            
        self.graph = graph
        
        self.__calculteLockDoorsWeigh()
            
                
    def __calculteLockDoorsWeigh(self):
        for door in self.doors.values():
            self.updateDoorWeigh(door.id)
            
    def pickUpItem(self, item):
        for door in self.doors.values():
            if item == door.doorkey:
                self.updateDoorWeigh(door.id)
                # plotGraph(self)
                break
            
    def updateDoorWeigh(self, id):
        door = self.doors[id]
        if door != None and door.locked:
            doorList = list(door.goes_between)
            key_room = self.__find_key_room(door.doorkey)
            
            self.__updateDiDoorWeigh(door, doorList[0], key_room)
            self.__updateDiDoorWeigh(door, doorList[1], key_room)
            
            self.__updateDependencies(door.id)
            
            
    def __updateDiDoorWeigh(self, door:Door, room, key_room): 
        other_room = door.other_loc[room]
        if not self.graph.has_edge(room, other_room):
            raise Exception(f"door not in graph: {room} -> {other_room}")
        
        doors_passed = []
        if door.doorkey in self.robot.carried_items:
            self.graph[room][other_room]['weight'] = 1
        else:
            self.graph[room][other_room]['weight'] = float("inf")
            
            path = nx.shortest_path(self.graph, source=room, target=key_room, weight="weight")
            doors_passed = [self.graph[path[i]][path[i+1]]['id'] for i in range(len(path)-1)]

        for door_pass_id in doors_passed:
            if door_pass_id == door.id:
              continue
            
            if self.doors[door_pass_id].locked:
                if door_pass_id in self.__dependencies:
                    self.__dependencies[door_pass_id].append((door.id, room))
                else:
                    self.__dependencies[door_pass_id] = [(door.id, room)]


    def __updateDependencies(self, id):
        if id in self.__dependencies:
            dependencies = self.__dependencies[id]
            del self.__dependencies[id]
            
            for update_door_obj in dependencies:
                update_door = self.doors[update_door_obj[0]]
                key_room = self.__find_key_room(update_door.doorkey)
                self.__updateDiDoorWeigh(update_door, update_door_obj[1], key_room)
                
    def __find_key_room(self, key):
        if key in self.robot.carried_items:
            return self.robot.location
        
        for room in self.room_contents.keys():
            if key in self.room_contents[room]:
                return room
            
        raise Exception(f"key don't exist {key}")
    
    def find_door(self, room1, room2):
        for door in self.doors:
            if door.goes_between == {room1, room2}:
                return door
            
        raise Exception(f"door don't exist between {room1} and {room2}")

    ## Define a string representation that will be uniquely identify the state.
    ## An easy way is to form a tuple of representations of the components of
    ## the state, then form a string from that:
    def __repr__(self):
        return str( ( self.robot.__repr__(),
                      [d.__repr__() for d in self.doors],
                      self.room_contents ) )
        
def plotGraph(state):
    plot_state = state
    pos = nx.circular_layout(plot_state.graph)

    # Draw the graph (nodes and edges)
    nx.draw(plot_state.graph, pos, with_labels=True, node_size=2000, node_color="skyblue", font_size=12, font_weight="bold", edge_color="gray")

    # Draw edge labels with weights
    edge_labels = nx.get_edge_attributes(plot_state.graph, 'weight')
    nx.draw_networkx_edge_labels(plot_state.graph, pos, edge_labels=edge_labels, font_size=10)

    # Show the graph
    plt.title("Weighted Graph")
    plt.show()
        
current_state = None
class RobotWorker( SearchProblem ):

    def __init__( self, state, goal_item_locations, bDynamic = True ):
        self.initial_state:State = state
        self.initial_state.goal_item_locations = goal_item_locations
        self.goal_item_locations = goal_item_locations
        self.bDynamic = bDynamic

    def possible_actions( self, state ):

        robot_location = state.robot.location
        strength       = state.robot.strength
        weight_carried = state.robot.weight_carried()

        actions = []
        # Can put down any carried item
        for i in state.robot.carried_items:
            actions.append( ("put down", i) )

        # Can pick up any item in room if strong enough
        for i in state.room_contents[robot_location]:
            if strength >= weight_carried + ITEM_WEIGHT[i]:
                actions.append( ("pick up", i))

        # If there is an unlocked door between robot location and
        # another location can move to that location
        for door in state.doors.values():
            if  (door.locked==False or (door.locked == True and door.doorkey in state.robot.carried_items)) and robot_location in door.goes_between:
                actions.append( ("move to", door.other_loc[robot_location]) )

        # Now the actions list should contain all possible actions
        return actions

    def successor( self, state, action):
        next_state:State = deepcopy(state)
        act, target = action
        if act== "put down":
            next_state.robot.carried_items.remove(target)
            next_state.room_contents[state.robot.location].add(target)
            
            if self.bDynamic:
                next_state.pickUpItem(target)
            
        if act == "pick up":
            next_state.robot.carried_items.append(target)
            next_state.room_contents[state.robot.location].remove(target)
            
            if self.bDynamic:
                next_state.pickUpItem(target)
            
        if act == "move to":
            next_state.robot.location = target

        return next_state

    def goal_test(self, state):
        for room, contents in self.goal_item_locations.items():
            for i in contents:
                if not i in state.room_contents[room]:
                    return False
        # plotGraph(state)
        return True

    def display_state(self,state):
        print("Robot location:", state.robot.location)
        print("Robot carrying:", state.robot.carried_items)
        print("Room contents:", state.room_contents)
    
    
    
rob = Robot(STARTING_ROOM, [], 15 )

t1 = time.perf_counter(), time.process_time()
state = State(rob, DOORS, ROOM_CONTENTS)

RW_PROBLEM_1 = RobotWorker( state, goal_item_locations )
t2 = time.perf_counter(), time.process_time()


print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")


t1 = time.perf_counter(), time.process_time()
state2 = State(rob, DOORS, ROOM_CONTENTS)
RW_PROBLEM_2 = RobotWorker( state2, goal_item_locations , False)
t2 = time.perf_counter(), time.process_time()


print(f" Real time: {t2[0] - t1[0]:.2f} seconds")
print(f" CPU time: {t2[1] - t1[1]:.2f} seconds")


def item_path_heuristic(state):
    sum = 0
    for room, items in state.goal_item_locations.items():
       for item in items:
            if item in state.room_contents[room]:
                continue

            location = ""
            if item in state.robot.carried_items:
                location = state.robot.location
            else:
                for item_room in state.room_contents:
                    if item in state.room_contents[item_room]:
                        sum += 1
                        location = item_room
                        break

            if location == "":
                raise Exception("item dom't exist: " + item)
            
            sum += nx.shortest_path_length(state.graph, source=location, target=room)
            
    return sum

# search( RW_PROBLEM_1, 'BF/FIFO', 100000, loop_check=True)
lock_result = search( RW_PROBLEM_1, 'BF/FIFO', 100000, loop_check=True, heuristic=item_path_heuristic, return_info=True)
lock_result2 = search( RW_PROBLEM_2, 'BF/FIFO', 100000, loop_check=True, heuristic=item_path_heuristic, return_info=True)
