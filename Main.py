from Wumpus_class import Wumpus_class
import random



#--ERROR-CHECK-FUNCTIONS---------------------------------------#

''' Controll input for letter and lenght 1 '''
def letter_controller(answer):              
    # Dubbel while loop that only breaks of both criteria is True
    while True:
        while True:
            # Checks if int? If IT IS asks again. If not break loop ONE
            try:
                answer = int(answer)        
                answer = input("Wrong answer, answer needs to be a letter. Try again: ")
            except:                         
                break
        
        # Checks if lenght is one? If it is break loop TWO. If not asks again and restsart loop one
        if len(answer) == 1:                
            break
        else:                               
            answer = input("Answer may only consist of one letter. Try again: ")
    return answer

''' Controll input for interger and lenght 1 '''
def int_controller(answer):                 
    # Dubbel while loop that only breaks of both criteria is True
    while True:
        while True:          
            # Checks if int?, if it is make it str to check lenght. Break loop ONE if answer is a nummber 
            try:
                answer = int(answer)        
                answer = str(answer)                        
                break                                      
            except:                              
                answer = input("Svar måste vara ett heltal, vänligen ange ett: ")       

        # Checks if lenght is one? If it is break loop TWO
        if len(answer) == 1:                
            break
        else:
            answer = input("Answer may only consist of one number. Try again: ")
        # Return as interger
    return int(answer)                      
        
#----Start-Functions------------------------------------------#

''' Creat objects for every room and conncet them randomly to eachother '''
def room_list(hole_chance, bat_chance):
    # - through classmetods. Finaly Returns a list of objects of rooms

    # Makes the objects of the rooms and store them in list
    room_obj_list = [Wumpus_class(i) for i in range(1,21)]  

    # Makes random order of room in NORTH direction and EAST direction
    connection_north = creat_connection_list()              
    connection_east = creat_connection_list()               

    # Use methods to connect object to eachother acording to mall
    staticmethod(Wumpus_class.set_north(room_obj_list, connection_north))   
    staticmethod(Wumpus_class.set_east(room_obj_list, connection_east))     
    
    # Creats a attribute of all the OBJECTS of adjecent rooms that is connected to the object
    # Set contet of objects/rooms (holes and bats)
    for room in room_obj_list:
        room.set_adjacent_rooms()
        room.set_contet(hole_chance, bat_chance)

    # Sets wumpus and player to a random room (wumpus removes bat and DONT get placed in hole-room)
    # Player get only placed in room without bat, hole and wumpus
    room.set_wumpus(room_obj_list)
    room.set_player(room_obj_list)
    return room_obj_list

''' Creats a random list of 20 numbers '''
def creat_connection_list():    
    connection_list = list(range(1,21))
    random.shuffle(connection_list)
    return connection_list

''' Opens txt-file and take out information '''
def read_file(file):                        
    return_list = []                          
    score_list = []                           
    score_file = open(file, "r")                    
    score_list = score_file.readlines()     

    # Every row put in list split på ","      
    for row in score_list:         
        row_split = row.split(",")                 
        row_score = [int(row_split[0]), row_split[1]]
        return_list.append(row_score)              
    score_file.close 

    # Return list                                  
    return return_list

''' Saves list to file, each element on a new row '''
def write_file(file, score_matrix):         
    score_file = open(file, "w")
    for high_score in score_matrix:
        score_file.writelines(str(high_score[0]) + "," + high_score[1] + "," + "\n")
    score_file.close()

''' Takes new score and sort it in list for selcted file, print it then saves it back'''
def make_score_board(score, player_name, file):
    score_matrix = read_file(file)

    # If None dont save new score only prints higescore list, only save 10 scores
    if score != None:
        new_score = [score, player_name]
        score_matrix.append(new_score)
        score_matrix.sort(reverse=True)
        try:
            score_matrix.pop(10)
        except:
            pass

    # Print High score list
    print("Top 10 scores for this level and difficulty is:")
    position = 0
    for high_score in score_matrix:
        position += 1
        print(str(position) + ". " + high_score[1] + " - " + str(high_score[0]))
    print("")

    write_file(file, score_matrix)

''' Sets diificulty '''
def set_difficulty():
    # Prints out difficculty options
    print("1. Peacful - Only Wumpus can kill you (No bats or bottomless holes) and 100 Arrows")
    print("2. Eazy - 10% chance for bottomless holes and 20% for bats and 10 Arrows")
    print("3. Normal - 20% chance for bottomless holes and 30% for bats and 5 Arrows. STANDARD")
    print("4. Hard - 25% chance for bottomless holes and 35% for bats and 5 Arrows. WUMPUS CAN MOVE")

    # Asks for choice
    difficulty = int_controller(input("Choose difficulty: "))
    while difficulty not in [1 , 2 , 3 , 4]:
        difficulty = input("Not valid answer, must be 1, 2, 3 or 4. Try again: ")

    # Return choice
    # hole_chance, bat_chace, arrows, wumpus_moves, saves_file
    if difficulty == 1:
        return 0, 0, 100, False, "score_saves\score_list_1.txt"
    elif difficulty == 2:
        return 0.1, 0.2, 10, False, "score_saves\score_list_2.txt"
    elif difficulty == 3:
        return 0.2, 0.3, 5, False, "score_saves\score_list_3.txt"
    else:
        return 0.25, 0.35, 5, True, "score_saves\score_list_4.txt"

#-----GAME-FUNCTIONS--------------------------------------#

''' Prints a string of room object for game '''
def print_room_string(room_obj):    
    # As following -- You are in room nummber x. You can move to following rooms x x x x --
    adj_rooms = [obj.number for obj in room_obj.adjacent_rooms]
    adj_rooms.sort()
    print("You are in room nummber" , str(room_obj.number) , end="")
    print(". You can move to following rooms:" , *adj_rooms) 

''' Check nearby rooms for dangers and returns warning messages '''
def nearby_dangers(room):     
    # holes, bats and wumpus
    dangers = ["hole", "bat", "wumpus"]
    return_list = []

    # Makes a list (dangers) with every "danger" in adjacent rooms
    for adj_room in room.adjacent_rooms:
        if adj_room.hole == True:
            dangers.append("hole")
        elif adj_room.bat == True:
            dangers.append("bat")
        elif adj_room.wumpus == True:
            dangers.append("wumpus")

    # Turns list to dictonary with number of each danger 
    dict_dangers = dict((dang, dangers.count(dang)) for dang in dangers)

    # Prints diffrent depending on dictonary 1 means it is zero (becuse of how list is made)
    if dict_dangers["bat"] == 2:
        return_list.append("You can hear a bat!")
    elif dict_dangers["bat"] >= 3:
        return_list.append("You can hear bats!")

    if dict_dangers["hole"] == 2:
        return_list.append("You feel the gust of wind!")
    elif dict_dangers["hole"] >= 3:
        return_list.append("You feel strong gust of winds!")

    if dict_dangers["wumpus"] >= 2:
        return_list.append("You can smell the abominable smell of wumpus!")
    
    #return list of strings ready to print 
    for strings in return_list:
        print(strings)

''' Asks for input (direction) and returns answer if valid'''
def get_direction():
    # Input goes true function that checks if letter one lenght 1 to give personalied wrong input message
    direction = letter_controller(input("What direction? (N, S, E, W): ")).upper()

    # Asks again if answer is not walid
    while direction not in ["N" , "S" , "E" , "W"]:
        direction = letter_controller(input("Not valid answer, must be N, S, E or W. Try again: ")).upper()
    return direction

''' Moves arrow troughe three rooms from player room after and check result '''
def shoot_arrow(arrow_room, room_obj_list):
    ordinal_numbers = ["first", "second", "third"]

    # Moves three rooms and print meassge and asks for new direction after each
    for num_str in ordinal_numbers:
        print("The arrow leaves the", num_str, "room. ", end="")
        direction = get_direction()
        arrow_room = arrow_room.move_arrow(direction, room_obj_list)

        # Checks result for arrow in each room it is in
        for room in room_obj_list:
            if room.arrow and room.wumpus:
                room.wumpus = False
                room.hole = True
                return "win"
            elif room.player and room.arrow:
                return "fail"

''' Checks room list for room with player in it and returns it '''
def find_cur_room(room_obj_list):
    for room in room_obj_list:
        if room.player == True:
            return room

''' Prints game rules '''
def game_rules():
    print("You're locked in the culverts below CSC, where the voracious Wumpus lives.") 
    print("To avoid being eaten up and unlocking the door, you need to shoot Wumpus with your bow and arrow.") 
    print("The culverts have 20 rooms that are connected by narrow corridors.") 
    print("You can move north, east, south or west from one room to another.")
    print("")
    print("However, there are dangers lurking here. In some rooms there are bottomless holes.") 
    print("If you step into one, you die immediately. In other rooms there are bats that lift you up,") 
    print("fly a bit and drop you into an arbitrary room. In one of the rooms is Wumpus,") 
    print("and if you venture into that room you will immediately be eaten up.") 
    print("Fortunately, from the rooms next door you can feel the gust of wind from an bottomless hole") 
    print("or the smell of Wumpus. You also get the numbers of each room which are adjacent.")
    print("")
    print("To win the game, you must shoot Wumpus and find the way out. When you shoot an arrow, it moves through three rooms") 
    print("- you can control which direction the arrow should choose in each room.") 
    print("Do not forget that the tunnels wind in unexpected ways. You may shoot yourself ...")
    print("You have a limited supplie of arrows. Good luck!")


''' Cotrolls lv_1 of game '''
def lv1(hole_chance, bat_chance, arrows, wumpus_moves, save_file):
    # Staring score (goes down for every arrow or move player makes) and creat room maze
    score = 100                 
    room_obj_list = room_list(hole_chance, bat_chance)
    player_name = input("What is the you're name traveller: ")

    # Main loop lv 1
    while True:
        # Finds current room and checks if game over
        cur_room = find_cur_room(room_obj_list)
        gameover = cur_room.turn_out(room_obj_list)
        if gameover == True:
            break
        else:
            pass

        # If on "Hard" Wumpus will move
        if wumpus_moves == True:

            # If possible moves Wumpus
            staticmethod(Wumpus_class.move_wumpus(room_obj_list)) 

            # If wumpus moves in in my current room prints follwing LOSE message
            for room in room_obj_list:
                if room.player == True and room.wumpus == True:
                    print("You step into the room and it's empty, you exhale.") 
                    print("You feel the floor start to shake, Wumpus is on the move.") 
                    print("The door to your room opens and the terrifying Wumpus enters the room.")
                    print("You stand still in the hope that he doesn't see you.") 
                    print("Just as you think you'll make it, Wumpu's tail wraps around you,")
                    print("he then lifts you upp swallows you whole.")
                    print("GAME OVER")
                    return "level faild", room_obj_list

        # Print information of current room on screen
        cur_room = find_cur_room(room_obj_list)
        print_room_string(cur_room)
        nearby_dangers(cur_room)

        # Check if player wants to move or shoot
        while True: 
            action = letter_controller(input("Do you want to move or shoot (M / S)?: ")).upper() 
            while action not in ["M" , "S"]:
                action = letter_controller(input("Not valid answer, must be M or S. Try again: ")).upper()

            # If you want to shoot remove 1 arrow and call function to move arrow
            if action == "S":
                arrows -= 1
                fallout = shoot_arrow(cur_room, room_obj_list)
                score -= 1

                # Checks reusult of shotting
                if fallout == "win":
                    # Print for winning and saves and print highe score list
                    print("\nWumpus dies in agony, the door out of CSC unlocks and you can leave,")
                    print("if you can find the way out that is ...")
                    print("Level 1 cleard")
                    print(player_name + ", you're score is: " + str(score) + "\n")
                    make_score_board(score, player_name, save_file)
                    return "level cleard", room_obj_list

                elif fallout == "fail":
                    # Print for loosing
                    print("You have shoot you're self in the back and are now bleeding on the floor")
                    print("GAME OVER")
                    return "level faild", room_obj_list

                elif arrows == 0:
                    # Prints for running out of arrows (loosing)
                    print("You missed, and now have run out of arrows in your quiver.") 
                    print("Which means your chances of killing Wumpus are over. You are now slowly dying of hunger.") 
                    print("GAME OVER")
                    return "level faild", room_obj_list
                else:
                    # Prints for missing arrow shoot
                    print("You missed but still have ", arrows , " arrows left")
            else:
                break
        
        # When player have shot move player
        direction = get_direction()
        cur_room.move_player(direction)
        score -= 1
        print("")

    print("GAME OVER")
    return "level faild", room_obj_list

''' Cotrolls lv_1 of game (extra level) NOT COMMENTED ON YET'''
def lv2(room_obj_list, hole_chance):
    moves = 10
    print("Everything starts to shake uncontrollably, you fall to the ground and can't get back up.") 
    print("You hear the floors in the rooms around cracking. There must be more bottomless holes now than before.")
    print("You probably need to hurry back to room 1 where the door out is, before the whole place has collapsed")
    for room in room_obj_list:
        if room.hole == False and room.bat == False and room.player == False and room.number == 1:
            chance = random.random()
            if chance <= hole_chance:
                hole = True
    while True:
        cur_room = find_cur_room(room_obj_list)
        gameover = cur_room.turn_out(room_obj_list)
        cur_room = find_cur_room(room_obj_list)
        if gameover == True:
            break
        elif moves == 5:
            print("Another strong shake, I have to hurry")
        elif cur_room.number == 1:
            print("You find the way out and just as you step out the door, the room behind collapses.")
            print("You step out the culvert outer door and see your whole world lying in flames.") 
            print("The smell of Wumpu's dead body has spread through the ventilation and mixed with")
            print("the high carbon dioxide content and then formed a highly hallucinated drug.") 
            print("The drug spread around the world in a matter of seconds and drove everyone completely insane.") 
            print("A nuclear war broke out in 2 minutes ...")
            print("CONGRATS YOU HAVE COMPLETED THE GAME")
            return
        elif moves == 0:
            print("Another strong shake, this time the ground drops beneath you're feets")
            print("and you fall into a bottomless pit. Never to be seen again")
            break
                   
        print_room_string(cur_room)
        nearby_dangers(cur_room)
        direction = get_direction()
        cur_room.move_player(direction)
        moves -= 1
        print("")
    print("GAME OVER")

''' Controlls game '''
def main():
    # Sets standard gamemode
    hole_chance = 0.2
    bat_chance = 0.3
    arrows = 5
    wumpus_moves = False
    save_file = "score_saves\score_list_3.txt"

    # Prints Start message
    print("Welcome to the game of Wumpus, a game of life and death")

    # Main loop for the main function
    while True:
        # Prints menu and chices
        print("")
        print("1. Game Rules")
        print("2. Set Difficulty")
        print("3. Start Game")
        print("4. Scoreboard (Current difficulty)")
        print("5. Quit")

        # Checks for input (1-5)
        answer = int_controller(input("Choose option: "))
        while answer not in [1 , 2 , 3 , 4, 5]:
            answer = input("Not valid answer, must be 1, 2, 3, 4 or 5. Try again: ")
        print("")

        # Controlls what happens when choice is made
        if answer == 1:
            # Show rules
            game_rules()
        elif answer == 2:
            # Asks for difficulty and saves new difficulty
            hole_chance, bat_chance, arrows, wumpus_moves, save_file = set_difficulty()
        elif answer == 3:
            # Start lv_! if clerad start lv_2
            cleard, room_obj_list = lv1(hole_chance, bat_chance, arrows, wumpus_moves, save_file)
            if cleard == "level cleard":
                lv2(room_obj_list, hole_chance)
            else:
                pass
        elif answer == 4:
            # Prints score board without cahnging in it
            make_score_board(None, None, save_file)
        else:
            return

# Start main
main()
        








#-------------------------------T-E-S-T-I-N-G----S-T-A-R-T-------------------------------------#

#room_obj_list = [Wumpus_class(i) for i in range(1,21)]
#room_obj_list[0].bat = True
#print(room_obj_list[0].bat)
#print(room_obj_list[0].number)
#print(room_obj_list[0])
#print(room_obj_list)
#print(num_adjacent_rooms(room_obj_list[0]))
#print_room_string(room_obj_list[0])
#print(room_obj_list[0].__dict__)

#-------------------------------T-E-S-T-I-N-G----E-N-D-----------------------------------------#
