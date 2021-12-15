import random
class Wumpus_class:
    ''' Makes obeject without dangers '''
    def __init__(self, number):
        self.number = number
        self.wumpus = False
        self.bat = False
        self.hole = False
        self.player = False
        self.adjacent_rooms = []

    ''' Connects objects with eachother STATIC '''   
    def set_east(rooms, connection):
        # Sets east room acording to connection list and connect them 
        for i in range(len(connection)):
            east_num = connection[i]
            east_room = rooms[east_num-1]
            west_num = connection[i-1]
            west_room = rooms[west_num-1]
            # Links self with east_room
            west_room.east = east_room
            east_room.west = west_room   

    ''' Connects objects with eachother STATIC '''
    def set_north(rooms, connection):
        # Sets north room acording to connection list and connect them 
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
    
        for room in adj_rooms:
            if room not in self.adjacent_rooms:
                self.adjacent_rooms.append(room)
            else:
                pass
                

    ''' Sets dangers to room according to premitted settings '''
    def set_contet(self, hole_chance, bat_chance):
        # Sets hole and bat = True for some object according to settings
        hole = hole_chance
        bat = (hole+bat_chance)
        chance = random.random()
        if chance <= hole:
            self.hole = True
        elif chance <= bat:
            self.bat = True
        else:
            pass
    
    ''' Sets wumpus in a room that dosent have a hole '''
    def set_wumpus(self, rooms):
        room = random.choice(rooms)
        while room.hole == True:
            room = random.choice(rooms)
        room.wumpus = True
        room.bat = False

    ''' Sets player in a room that are free from dangers'''
    def set_player(self, rooms):
        room = random.choice(rooms)
        while room.hole == True or room.bat == True or room.wumpus == True:
            room = random.choice(rooms)
        room.player = True

    ''' Moves player a room according to direction'''
    def move_player(self, direction):
        self.player = False
        if direction == "N":
            self.north.player = True
        elif direction == "S":
            self.south.player = True
        elif direction == "E":
            self.east.player = True
        else:
            self.west.player = True
    
    ''' moves arrow in rooms '''
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
        else:
            self.west.arrow = True
            return self.west

    ''' Moves wumpus if possible '''
    def move_wumpus(rooms):
        direction = []

        # Checks for Wumpus possile directions and apped it to list
        for room in rooms:
            if room.wumpus == True:
                if room.north.hole == False:
                    direction.append(room.north)
                if room.south.hole == False:
                    direction.append(room.south)
                if room.east.hole == False:
                    direction.append(room.east)
                if room.west.hole == False:
                    direction.append(room.west)
                
                # cheks if wumpus can choose a direction to move to
                try:
                    new_room = direction[random.randrange(0, len(direction))]
                    room.wumpus = False
                    print("You feel the floor shake as Wumpus moves, but you can not figure out where.")
                    new_room.wumpus = True
                    new_room.bat = False
                    return

                # If not do nothing and print follwing
                except:
                    print("You hear Wumpus screaming in frustration")

    ''' Check reult of moving '''            
    def turn_out(self, rooms):
        gameover = True

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
                print("You feel bat wings against your cheek and before you have gotten time to react, ", end="") 
                print("you are lifted up into the air.")
                print("After a short flight, you are dropped down to room number", str(new_room.number))
                gameover = False
            # If dropped at Wumpus => Losses
            else:
                print("You feel bat wings against your cheek and before you have gotten time to react, ", end="") 
                print("you are lifted up into the air. Then flown to Wumpus and sacrificed")

        # If in a Hole room => losses
        elif self.hole == True:
            print("You stepped into a bottomless pit. To never be found again.")

        # If in a Wumpuses room => losses
        elif self.wumpus == True:
            print("You step into the room which is full of foul-smelling smoke.")
            print("But before you have time to hold your breath, the most vile gap you have ever seen")
            print("appears over you and devours you completely.")

        else:
            gameover = False
        
        return gameover
        






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