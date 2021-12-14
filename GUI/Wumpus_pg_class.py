import random
class Wumpus_class:

    def __init__(self, number):
        self.number = number
        self.wumpus = False
        self.bat = False
        self.hole = False
        self.player = False
        self.adjacent_rooms = []
           
    def set_east(rooms, connection):      # Connects objects with eachother STATIC
        # Sets east room to random room other than self
        for i in range(len(connection)):
            east_num = connection[i]
            east_room = rooms[east_num-1]
            west_num = connection[i-1]
            west_room = rooms[west_num-1]
            # Links self with east_room
            west_room.east = east_room
            east_room.west = west_room   

    def set_north(rooms, connection):     # Connects objects with eachother STATIC
        # Sets north room to random room other than self
        for i in range(len(connection)):
            north_num = connection[i]
            north_room = rooms[north_num-1]
            south_num = connection[i-1]
            south_room = rooms[south_num-1]
            # Links self with north_room
            south_room.north = north_room
            north_room.south = south_room

    def set_adjacent_rooms(self):         # Makes an extra attributes that include all connected rooms
        # The connected rooms are connected as OBJECTS to OBJECTS
        adj_rooms = [self.north, self.south, self.west, self.east]
    
        for room in adj_rooms:
            if room not in self.adjacent_rooms:
                self.adjacent_rooms.append(room)
            else:
                pass        

    def set_contet(self, hole_chance, bat_chance):
        hole = hole_chance
        bat = (hole+bat_chance)
        chance = random.random()
        if chance <= hole:
            self.hole = True
        elif chance <= bat:
            self.bat = True
        else:
            pass
    
    def set_wumpus(self, rooms):
        room = random.choice(rooms)
        while room.hole == True:
            room = random.choice(rooms)
        room.wumpus = True
        room.bat = False

    def set_player(self, rooms):
        room = random.choice(rooms)
        while room.hole == True or room.bat == True or room.wumpus == True:
            room = random.choice(rooms)
        room.player = True

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

    def turn_out(self, rooms):
        if self.bat == True:
            for room in rooms:
                room.player = False
            new_room = random.choice(rooms)
            while new_room.hole == True or new_room.bat == True:
                new_room = random.choice(rooms)
            new_room.player = True
            if new_room.wumpus == False:
                effect = "flown"
            else:
                effect = "sacrificed"

        elif self.hole == True:
            effect = "falling"
            new_room = False

        elif self.wumpus == True:
            effect = "eaten"
            new_room = False

        else:
            effect = "none"
            new_room = False
        return effect
        






'''
ro = []
ro.append(Room(19))
ro.append(Room(2))



print(ro[0].east)
print(ro[0])
print(ro)

for room in ro:
    if room.number == 2:
        print(room)

'''