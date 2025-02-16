from bbmodcache.bbSearch import SearchProblem, search
import networkx as nx
from copy import deepcopy

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
    
    def __init__( self, robot, doors, room_contents ):
        self.robot = robot
        self.doors = doors
        self.room_contents = room_contents
        
        graph = nx.Graph()
        graph.add_nodes_from(ROOM_CONTENTS.keys())
        
        for door in doors:
            doorList = list(door.goes_between)
            graph.add_edge(doorList[0], doorList[1])
            
        self.graph = graph
        


    ## Define a string representation that will be uniquely identify the state.
    ## An easy way is to form a tuple of representations of the components of
    ## the state, then form a string from that:
    def __repr__(self):
        return str( ( self.robot.__repr__(),
                      [d.__repr__() for d in self.doors],
                      self.room_contents ) )
        
class RobotWorker( SearchProblem ):

    def __init__( self, state, goal_item_locations ):
        self.initial_state = state
        self.initial_state.goal_item_locations = goal_item_locations
        self.goal_item_locations = goal_item_locations

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
        for door in state.doors:
            if  (door.locked==False or (door.locked == True and door.doorkey in state.robot.carried_items)) and robot_location in door.goes_between:
                actions.append( ("move to", door.other_loc[robot_location]) )

        # Now the actions list should contain all possible actions
        return actions

    def successor( self, state, action):
        next_state = deepcopy(state)
        act, target = action
        if act== "put down":
            next_state.robot.carried_items.remove(target)
            next_state.room_contents[state.robot.location].add(target)

        if act == "pick up":
            next_state.robot.carried_items.append(target)
            next_state.room_contents[state.robot.location].remove(target)

        if act == "move to":
            next_state.robot.location = target

        return next_state

    def goal_test(self, state):
        for room, contents in self.goal_item_locations.items():
            for i in contents:
                if not i in state.room_contents[room]:
                    return False
        return True

    def display_state(self,state):
        print("Robot location:", state.robot.location)
        print("Robot carrying:", state.robot.carried_items)
        print("Room contents:", state.room_contents)
    

rob = Robot(STARTING_ROOM, [], 15 )

state = State(rob, DOORS, ROOM_CONTENTS)

RW_PROBLEM_1 = RobotWorker( state, goal_item_locations )

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
# simple_result = search( RW_PROBLEM_1, 'BF/FIFO', 100000, loop_check=True, return_info=True)

door_result = search( RW_PROBLEM_1, 'BF/FIFO', 100000, loop_check=True, heuristic=item_path_heuristic, return_info=True)
