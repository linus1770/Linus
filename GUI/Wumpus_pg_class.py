import random

''' Class that controlls Rooms '''
class Wumpus_class:
    ''' Initilize start values for rooms '''
    def __init__(self, number):
        self.number = number
        self.wumpus = False
        self.bat = False
        self.hole = False
        self.player = False
        self.adjacent_rooms = []

    ''' Connects objects with eachother (STATIC) '''       
    def set_east(rooms, connection):
        # Sets east room to random room other than self, from a randomized list (connection)
        for i in range(len(connection)):
            east_num = connection[i]
            east_room = rooms[east_num-1]
            west_num = connection[i-1]
            west_room = rooms[west_num-1]

            # Links self with east_room
            west_room.east = east_room
            east_room.west = west_room   

    ''' Connects objects with eachother (STATIC) '''       
    def set_north(rooms, connection):
        # Sets north room to random room other than self, from a randomized list (connection)
        for i in range(len(connection)):
            north_num = connection[i]
            north_room = rooms[north_num-1]
            south_num = connection[i-1]
            south_room = rooms[south_num-1]

            # Links self with north_room
            south_room.north = north_room
            north_room.south = south_room

    ''' Makes an extra attributes that include all connected rooms '''
    def set_adjacent_rooms(self):
        # The connected rooms are connected as OBJECTS to OBJECTS
        adj_rooms = [self.north, self.south, self.west, self.east]

        # Only add ajacent room ones
        for room in adj_rooms:
            if room not in self.adjacent_rooms:
                self.adjacent_rooms.append(room)
            else:
                pass        

    ''' Sets dangers to room according to premitted settings '''
    def set_contet(self, hole_chance, bat_chance):
        # varible hole and bat sets to precent you want with "danger" ex. 0.2
        hole = hole_chance
        bat = (hole+bat_chance)

        # Sets danger acording to random number between 0 and 1
        chance = random.random()
        if chance <= hole:
            self.hole = True
        elif chance <= bat:
            self.bat = True
        else:
            pass

    ''' Sets wumpus in a room that dosent have a hole '''
    def set_wumpus(self, rooms):
        # Choose a random room
        room = random.choice(rooms)

        # While choice has hole choose a new one
        while room.hole == True:
            room = random.choice(rooms)
        
        # When room without hole is chosen
        room.wumpus = True
        room.bat = False

    ''' Sets player to random room '''
    def set_player(self, rooms):
        # Choose a random room
        room = random.choice(rooms)

        # While choice has hole, bat or wumpus choose a new one
        while room.hole == True or room.bat == True or room.wumpus == True:
            room = random.choice(rooms)

        # When room that dont have any of the above sets to player room
        room.player = True

    ''' Moves player a room according to direction '''
    def move_player(self, direction):
        self.player = False
        if direction == "N":
            self.north.player = True
        elif direction == "S":
            self.south.player = True
        elif direction == "E":
            self.east.player = True
        elif direction == "W":
            self.west.player = True
        else:
            self.player = True

    ''' Moves arrow a room according to direction'''
    def move_arrow(self, direction, rooms):
        for room in rooms:
            room.arrow = False
        if direction == "N":
            self.north.arrow = True
            return self.north
        elif direction == "S":
            self.south.arrow = True
            return self.south
        elif direction == "E":
            self.east.arrow = True
            return self.east
        elif direction == "W":
            self.west.arrow = True
            return self.west

    ''' Check reult of moving '''
    def turn_out(self, rooms):
        # If in a bat room - move to new room (not hole or bat) if wumpus GAME OVER else moves player there.
        if self.bat == True:
            for room in rooms:
                room.player = False
            new_room = random.choice(rooms)
            while new_room.hole == True or new_room.bat == True:
                new_room = random.choice(rooms)
            new_room.player = True

            # If dropped in danger free room
            if new_room.wumpus == False:
                effect = "flown"
            
            # If dropped at Wumpus => Losses
            else:
                effect = "sacrificed"

        # If in a Hole room => losses
        elif self.hole == True:
            effect = "falling"
            new_room = False

        # If in a Wumpuses room => losses
        elif self.wumpus == True:
            effect = "eaten"
            new_room = False

        # If empty returns none => conntinue playing
        else:
            effect = "none"
            new_room = False
            
        return effect