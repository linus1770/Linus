from Wumpus_pg_class import Wumpus_class
import pygame as pg 
import random
import os


#-------Constants-for-pygame------#
'''  Main Class for Wumpus GUI '''
class Gui():
    ''' Initilize constants and some start values for pygame'''
    def __init__(self):
        # Fonts
        self.font_menu = pg.font.SysFont("opensans", 60)
        self.font_txt = pg.font.SysFont("opensans", 23)
        
        # Pixel sizes
        self.WIDTH = 900                             
        self.HEIGHT = 600
        self.ROOM_WIDTH = 600
        self.ROOM_HEIGHT = 390                  

        # Sets window
        self.window = pg.display.set_mode((self.WIDTH, self.HEIGHT))

        # Dictonary for coloures
        self.colors = {"WHITE" : (255, 255, 255), "BLACK" : (0, 0, 0), "GREEN" : (0, 255, 0), "YELLOW" : (249, 249, 50), "ORANGE" : (255, 128, 0), "RED" : (195, 26, 33), "BLUE" : (49, 184, 252)}

        # Scaled pictures
        self.empty_room = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "room_empty.jpg")),(self.ROOM_WIDTH, self.ROOM_HEIGHT))
        self.arrow_in_room = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "room_arrow.jpg")),(self.ROOM_WIDTH, self.ROOM_HEIGHT))
        self.shoot_room = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "room_shoot.jpg")),(self.ROOM_WIDTH, self.ROOM_HEIGHT))
        self.hole_room = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "room_hole.jpg")),(self.ROOM_WIDTH, self.ROOM_HEIGHT))
        self.wumpus_room = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "room_wumpus.jpg")),(self.ROOM_WIDTH, self.ROOM_HEIGHT))
        self.victory_room = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "room_victory.jpg")),(self.ROOM_WIDTH, self.ROOM_HEIGHT))
        self.arrows_pic = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "arrows.png")),(75, 40))
        self.bat = pg.transform.scale(pg.image.load(os.path.join("GUI", "Assets", "bat.png")),(120, 70))

    #-------Start-functions-------#

    ''' Creat objects for every room and conncet them randomly to eachother '''
    def room_list(self, hole_chance, bat_chance):
        # through classmetods. Finaly Returns the list of objects 

        # Makes the objects of the rooms and store them in list
        room_obj_list = [Wumpus_class(i) for i in range(1,21)]

        # Makes random order of room in NORTH direction and EAST direction
        connection_north = self.creat_connection_list()
        connection_east = self.creat_connection_list()

        # Use methods to connect object to eachother acording to mall
        staticmethod(Wumpus_class.set_north(room_obj_list, connection_north))
        staticmethod(Wumpus_class.set_east(room_obj_list, connection_east))     
        
        # Creats a attribute of all the OBJECTS of adjecent rooms that is connected to the object
        # Set contet of objects/rooms (holes and bats)
        for room in room_obj_list:
            room.set_adjacent_rooms()
            room.set_contet(hole_chance, bat_chance)

        # Sets wumpus and player to a random room (wumpus removes bat and dont get placed in hole-room)
        # Player get only placed in room without bat, hole and wumpus
        room.set_wumpus(room_obj_list)
        room.set_player(room_obj_list)
        return room_obj_list

    ''' Creats a random list of 20 numbers for order of rooms '''
    def creat_connection_list(self):
        connection_list = list(range(1,21))
        random.shuffle(connection_list)
        return connection_list

    ''' Opens txt-file and take out information '''
    def read_file(self, file): 
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
    def write_file(self, file, score_matrix):
        score_file = open(file, "w")
        for high_score in score_matrix:
            score_file.writelines(str(high_score[0]) + "," + high_score[1] + "," + "\n")
        score_file.close()

    ''' Takes new score and sort it in list for selcted file, print it then saves it back'''
    def make_score_board(self, player_name, file):
        score_matrix = self.read_file(file)

        # If None dont save new score only prints higescore list, only save 10 scores
        if player_name != None:
            new_score = [self.score, player_name]
            score_matrix.append(new_score)
            score_matrix.sort(reverse=True)
            try:
                score_matrix.pop(10)
            except:
                pass

        # makes list of high scores for printing
        position = 0
        list_for_print = []
        for high_score in score_matrix:
            position += 1
            list_for_print.append(str(position) + ". " + high_score[1] + " - " + str(high_score[0]))

        # Saves list to file
        self.write_file(file, score_matrix)
        return list_for_print

    #-------GAME-FUNCTIONS-------#

    ''' Prints string of room info in game '''
    def print_room_string(self, cur_room, txt_rectangel):    
        # Render string of current room for printing
        room_info = "You are in room nummber " + str(cur_room.number) + ". You can move to following rooms:"    
        room_str = self.font_txt.render(room_info, 1, self.colors["BLACK"])

        # Print String on screen 
        self.window.blit(room_str, (txt_rectangel.x+5, txt_rectangel.y+5))

        # Checks for nummber of adjacent rooms and put rhem in a list and sort it
        adj_rooms = [adj_room.number for adj_room in cur_room.adjacent_rooms]
        adj_rooms.sort()

        # Render and prints nummbers from list on screen after curent room string
        for index, number in enumerate(adj_rooms):
            self.window.blit(self.font_txt.render(str(number), 1, self.colors["BLACK"]), (txt_rectangel.x+470+(22*index), txt_rectangel.y+5))

    ''' Check nearby rooms for dangers and returns warning messages '''
    def nearby_dangers(self, room, txt_rectangel):     
        # holes, bats and wumpus
        dangers = ["wumpus", "bat", "hole"]
        dangers_list = []

        # Makes a list (dangers) with every "danger" in adjacent rooms
        for adj_room in room.adjacent_rooms:
            if adj_room.hole:
                dangers.append("hole")
            elif adj_room.bat:
                dangers.append("bat")
            elif adj_room.wumpus:
                dangers.append("wumpus")

        # Turns list to dictonary with number of each danger 
        dict_dangers = dict((dang, dangers.count(dang)) for dang in dangers)

        # Prints diffrent depending on dictonary 1 means it is zero (becuse of how list is made)
        if dict_dangers["bat"] == 2:
            dangers_list.append("You can hear a bat!")
        elif dict_dangers["bat"] >= 3:
            dangers_list.append("You can hear bats!")
        else:
            dangers_list.append("")

        if dict_dangers["hole"] == 2:
            dangers_list.append("You feel the gust of wind!")
        elif dict_dangers["hole"] >= 3:
            dangers_list.append("You feel strong gust of winds!")
        else:
            dangers_list.append("")

        if dict_dangers["wumpus"] >= 2:
            dangers_list.append("You can smell the abominable smell of wumpus!")
        else:
            dangers_list.append("")
        
        # Prints Warning mesages on game screen
        nearby_bats_str = dangers_list[0]
        nearby_holes_str = dangers_list[1]
        nearby_wumpus_str = dangers_list[2]
        self.window.blit(self.font_txt.render(nearby_bats_str, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))
        self.window.blit(self.font_txt.render(nearby_holes_str, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+65))
        self.window.blit(self.font_txt.render(nearby_wumpus_str, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+85))

    ''' Checks room list for room with player in it and returns it '''
    def find_cur_room(self, room_obj_list):
        for room in room_obj_list:
            if room.player:
                return room

    ''' Moves players current room '''
    def click_doors_player(self, cur_room, room_obj_list):
        # if not valid click position return moves = False
        moves = False
        pos = pg.mouse.get_pos()

        # Sets new current room to true and lower score by 1
        if 377 <= pos[0] <= 480 and 44 <= pos[1] <= 240:
            cur_room.move_player("N")
            self.score -= 1
            moves = True                    
        if 394 <= pos[0] <= 503 and 376 <= pos[1] <= 401:
            cur_room.move_player("S")
            self.score -= 1
            moves = True  
        if 579 <= pos[0] <= 751 and 10 <= pos[1] <= 380:
            cur_room.move_player("E")
            self.score -= 1   
            moves = True                   
        if 150 <= pos[0] <= 289 and 10 <= pos[1] <= 402:
            cur_room.move_player("W")
            self.score -= 1
            moves = True  

        # returns true if player moves to diffrent room
        return moves

    ''' Moves arrows current room '''
    def click_doors_arrow(self, cur_room, room_obj_list, game_state):
        # if not valid click position return moves = False
        moves = False
        pos = pg.mouse.get_pos()

        # Sets new current room to true and lower score by 1
        if 377 <= pos[0] <= 480 and 44 <= pos[1] <= 240:
            cur_room.move_arrow("N", room_obj_list)
            self.score -= 1
            moves = True                    
        if 394 <= pos[0] <= 503 and 376 <= pos[1] <= 401:
            cur_room.move_arrow("S", room_obj_list)
            self.score -= 1
            moves = True  
        if 579 <= pos[0] <= 751 and 10 <= pos[1] <= 380:
            cur_room.move_arrow("E", room_obj_list)
            self.score -= 1   
            moves = True                   
        if 150 <= pos[0] <= 289 and 10 <= pos[1] <= 402:
            cur_room.move_arrow("W", room_obj_list)
            self.score -= 1
            moves = True  
        # If arrow moves check if arrow hits. Return result in game_state
        if moves:
            for room in room_obj_list:
                if room.arrow and room.wumpus:
                    room.wumpus = False
                    room.hole = True
                    game_state = "victory"
                elif room.player and room.arrow:
                    game_state = "loss"

        # returns true if player moves to diffrent room and new or same game_state
        return moves, game_state

    ''' Lets player modify sting input with only letters '''
    def letter_input(self, event, string):
        # Adds Uppercase of clicked letter to string
        if event.key == pg.K_a:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_b:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_c:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_d:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_e:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_f:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_g:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_h:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_i:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_j:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_k:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_l:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_m:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_n:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_o:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_p:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_q:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_r:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_s:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_t:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_u:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_v:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_w:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_x:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_y:
            string += str(chr(event.key)).upper()
        if event.key == pg.K_z:
            string += str(chr(event.key)).upper()

        # Removes last letter from string
        if event.key == pg.K_BACKSPACE:
            string = string[:-1]
        
        # Returns string at current state
        return string

    #-------GUI-DRAW-FUNCTIONS-------#

    ''' Prints text of you been flown to a new empty room '''
    def print_flown(self, txt_rectangel, side_rectangel_l, game_state):
        # Makes a new empty white square 
        pg.draw.rect(self.window, self.colors["WHITE"], txt_rectangel)

        # Format strings for printing in square
        string_1 = "You feel bat wings against your cheek and before you have gotten time to react, " 
        string_2 = "you are lifted up into the air."
        string_3 = "After a short flight, you are dropped down in a new room"
        self.window.blit(self.font_txt.render(string_1, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+5))
        self.window.blit(self.font_txt.render(string_2, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+25))
        self.window.blit(self.font_txt.render(string_3, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))
        self.window.blit(self.bat, (side_rectangel_l.x+5, side_rectangel_l.y+self.ROOM_HEIGHT-90))

        # Prints avalible click options
        self.print_keys(game_state, True)

        # Update screen
        pg.display.update()

    ''' If gamemode is hard moves Wumpus '''
    def wumpus_moves_func(self, room_obj_list, txt_rectangel, game_state):
        direction = []
        # Checks for avalible direction for wumpus to move and ad it to direction
        for room in room_obj_list:
            if room.wumpus:
                if room.north.hole == False:
                    direction.append(room.north)
                if room.south.hole == False:
                    direction.append(room.south)
                if room.east.hole == False:
                    direction.append(room.east)
                if room.west.hole == False:
                    direction.append(room.west)

                # If it is a possible room to move to, chose one random and moves wumpus their
                # If new room has bat wumpus eats bat    
                try:
                    new_room = direction[random.randrange(0, len(direction))]
                    room.wumpus = False
                    new_room.wumpus = True
                    new_room.bat = False
                except:
                    pass

                # Prints text if Wumpus move else that he is trapped
                if room.wumpus:
                    wumpus_moves_str = "You hear Wumpus screaming in frustration"
                    wumpus_moves_str = ""
                elif room.wumpus == False:
                    wumpus_moves_str1 = "As you are about to move, you feel the floor shake as" 
                    wumpus_moves_str2 = "Wumpus moves, but you can not figure out where."
                self.window.blit(self.font_txt.render(wumpus_moves_str1, 1, self.colors["RED"]),(txt_rectangel.x+5, txt_rectangel.y+125))
                self.window.blit(self.font_txt.render(wumpus_moves_str2, 1, self.colors["RED"]),(txt_rectangel.x+5, txt_rectangel.y+145))

                # Update screen
                pg.display.update()

        # If wumpus moves in to you're room, changes game_state to loss
        for room in room_obj_list:
            if room.player and room.wumpus:
                game_state = "loss"
        
        # Returns new/same game_state
        return game_state

    ''' Print avalible moves for the player in game '''
    def print_keys(self, game_state, flown=False):
        # Resets right square in game window
        side_rectangel_r = pg.Rect(self.WIDTH-((self.WIDTH-self.ROOM_WIDTH)/2-10), 10, (self.WIDTH-self.ROOM_WIDTH)/2-20, self.ROOM_HEIGHT)
        pg.draw.rect(self.window, self.colors["WHITE"], side_rectangel_r)
        
        # Render and print txt
        self.window.blit(self.font_txt.render("Avalible moves", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+10))        
        
        # Print avalible options for when gamemode is start
        if game_state == "play": 
            # Avalible options is move (left click) and shot (right click)
            if not flown:
                self.window.blit(self.font_txt.render("Left click", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))        
                self.window.blit(self.font_txt.render("to move", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
 
                self.window.blit(self.font_txt.render("Right click", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+100))        
                self.window.blit(self.font_txt.render("to fire", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+120))

            # Prints avalible options when flown by bat (click)
            if flown:
                self.window.blit(self.font_txt.render("Left click", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))
                self.window.blit(self.font_txt.render("to Continue", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
        
        # Prints avalible options for when shotting
        if game_state == "fire":
            self.window.blit(self.font_txt.render("Right click", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+100))        
            self.window.blit(self.font_txt.render("to fire", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+120))

        # Prints avalible options for when you have loss or when wonn and written you're name
        if game_state in ["loss", "victory_2"]:
            self.window.blit(self.font_txt.render("Click on", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))
            self.window.blit(self.font_txt.render("Titel Menu", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
            self.window.blit(self.font_txt.render("to return", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+80))
        
        # Prints info for writing youre name
        if game_state == "victory":
            self.window.blit(self.font_txt.render("Write name -", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))
            self.window.blit(self.font_txt.render("(eng letters)", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
            self.window.blit(self.font_txt.render("Max 5 letters", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+80))
            self.window.blit(self.font_txt.render("Enter - Confirm", 1, self.colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+120))         

    ''' Draws menu on screen'''
    def draw_menu(self):
        # Resets the hole screen
        self.window.fill(self.colors["BLACK"])
        
        # Prints menu option one (Square and text) Game Rules
        rectagel_op1 = pg.Rect(10, 10, self.WIDTH-20, 100)
        one = pg.draw.rect(self.window, self.colors["YELLOW"], rectagel_op1)
        options_txt_1 = self.font_menu.render("1. Game Rules", 1, self.colors["BLACK"])
        self.window.blit(options_txt_1, (rectagel_op1.x+10, rectagel_op1.y+10))

        # Prints menu option two (Square and text) Set Difficulty
        rectagel_op2 = pg.Rect(10, rectagel_op1.y+110, self.WIDTH-20, 100)
        two = pg.draw.rect(self.window, self.colors["ORANGE"], rectagel_op2)
        options_txt_2 = self.font_menu.render("2. Set Difficulty", 1, self.colors["BLACK"])
        self.window.blit(options_txt_2, (rectagel_op2.x+10, rectagel_op2.y+10))

        # Prints menu option three (Square and text) Start game
        rectagel_op3 = pg.Rect(10, rectagel_op2.y+110, self.WIDTH-20, 100)
        three = pg.draw.rect(self.window, self.colors["GREEN"], rectagel_op3)
        options_txt_3 = self.font_menu.render("3. Start Game", 1, self.colors["BLACK"])
        self.window.blit(options_txt_3, (rectagel_op3.x+10, rectagel_op3.y+10))

        # Prints menu option four (Square and text) Scoreboard
        rectagel_op4 = pg.Rect(10, rectagel_op3.y+110, self.WIDTH-20, 100)
        four = pg.draw.rect(self.window, self.colors["BLUE"], rectagel_op4)
        options_txt_4 = self.font_menu.render("4. Scoreboard (Current difficulty)", 1, self.colors["BLACK"])
        self.window.blit(options_txt_4, (rectagel_op4.x+10, rectagel_op4.y+10))

        # Prints menu option five (Square and text) Quit option
        rectagel_op5 = pg.Rect(10, rectagel_op4.y+110, self.WIDTH-20, 100)
        five = pg.draw.rect(self.window, self.colors["RED"], rectagel_op5)
        options_txt_5 = self.font_menu.render("5. Quit", 1, self.colors["BLACK"])
        self.window.blit(options_txt_5, (rectagel_op5.x+10, rectagel_op5.y+10))

        pg.display.update()
        return one, two, three, four, five

    ''' Draws rule window on screen '''
    def draw_game_rules(self):
        # Makes a yellow square
        rectagel = pg.Rect(10, 10, self.WIDTH-20, self.HEIGHT-20)
        pg.draw.rect(self.window, self.colors["YELLOW"], rectagel)

        rules_txt_list = []
        # Adds rules to list
        rules_txt_list.append("You're locked in the culverts below CSC, where the voracious Wumpus lives.")
        rules_txt_list.append("To avoid being eaten up and unlocking the door, you need to shoot Wumpus with your bow and arrow.")
        rules_txt_list.append("The culverts have 20 rooms that are connected by narrow corridors.")
        rules_txt_list.append("You can move north, east, south or west from one room to another.")

        rules_txt_list.append("")
        rules_txt_list.append("However, there are dangers lurking here. In some rooms there are bottomless holes.")
        rules_txt_list.append("If you step into one, you die immediately. In other rooms there are bats that lift you up,")
        rules_txt_list.append("fly a bit and drop you into an arbitrary room. In one of the rooms is Wumpus,")
        rules_txt_list.append("and if you venture into that room you will immediately be eaten up.")
        rules_txt_list.append("Fortunately, from the rooms next door you can feel the gust of wind from an bottomless hole")
        rules_txt_list.append("or the smell of Wumpus. You also get the numbers of each room which are adjacent.")

        rules_txt_list.append("")
        rules_txt_list.append("To win the game, you must shoot Wumpus and find the way out. When you shoot an arrow, it moves through three rooms")
        rules_txt_list.append("- you can control which direction the arrow should choose in each room.")
        rules_txt_list.append("Do not forget that the tunnels wind in unexpected ways. You may shoot yourself ...")
        rules_txt_list.append("You have a limited supplie of arrows. Good luck!")

        text_x = 15
        text_y = 15
        distance = 20

        # Prints the Rules
        for index, string in enumerate(rules_txt_list):
            renderd_string = self.font_txt.render(string, 1, self.colors["BLACK"])
            self.window.blit(renderd_string, (text_x, text_y+(distance*index)))

        # Prints return text
        self.window.blit(self.font_menu.render("Click on screen to return", 1, self.colors["BLACK"]),(50, 510))

        # Updates the rules
        pg.display.update()  

    ''' Draws score board window on screen '''
    def draw_score_board(self, player_name, save_file):
        # Makes a blue square
        rectagel = pg.Rect(10, 10, self.WIDTH-20, self.HEIGHT-20)
        pg.draw.rect(self.window, self.colors["BLUE"], rectagel)

        # Render and prints top scores header
        self.window.blit(self.font_menu.render("Top 10 scores", 1 , self.colors["BLACK"]), (90,15))

        # Render and prints high score list
        high_scores = self.make_score_board(None, save_file)
        for index, self.score in enumerate(high_scores):
            self.window.blit(self.font_menu.render(self.score, 1, self.colors["BLACK"]), (100, 90+(40*index)))

        # Prints option for returning to menu
        self.window.blit(self.font_menu.render("Click on screen to return", 1, self.colors["BLACK"]),(50, 510))

        # Update screen
        pg.display.update()  

    ''' Draws set difficulty window on screen '''
    def draw_set_difficulty(self):
        # Reset screen
        self.window.fill(self.colors["BLACK"])
        
        # Prints difficuty option one (Square and text) Peacful
        rectagel_op1 = pg.Rect(10, 10, self.WIDTH-20, 100)
        peacful = pg.draw.rect(self.window, self.colors["GREEN"], rectagel_op1)
        self.window.blit(self.font_menu.render("A. Peacful", 1, self.colors["BLACK"]),(rectagel_op1.x+10, rectagel_op1.y+10))
        self.window.blit(self.font_txt.render("Only Wumpus can kill you (No bats or bottomless holes) and 99 Arrows", 1, self.colors["BLACK"]),(rectagel_op1.x+10, rectagel_op1.y+60))

        # Prints difficuty option two (Square and text) Eazy
        rectagel_op2 = pg.Rect(10, rectagel_op1.y+110, self.WIDTH-20, 100)
        eazy = pg.draw.rect(self.window, self.colors["YELLOW"], rectagel_op2)
        self.window.blit(self.font_menu.render("B. Eazy", 1, self.colors["BLACK"]),(rectagel_op2.x+10, rectagel_op2.y+10))
        self.window.blit(self.font_txt.render("10% chance for bottomless holes and 20% for bats and 10 Arrows", 1, self.colors["BLACK"]),(rectagel_op2.x+10, rectagel_op2.y+60))

        # Prints difficuty option three (Square and text) Normal
        rectagel_op3 = pg.Rect(10, rectagel_op2.y+110, self.WIDTH-20, 100)
        normal = pg.draw.rect(self.window, self.colors["ORANGE"], rectagel_op3)
        self.window.blit(self.font_menu.render("C. Normal", 1, self.colors["BLACK"]),(rectagel_op3.x+10, rectagel_op3.y+10))
        self.window.blit(self.font_txt.render("20% chance for bottomless holes and 30% for bats and 5 Arrows. STANDARD", 1, self.colors["BLACK"]),(rectagel_op3.x+10, rectagel_op3.y+60))

        # Prints difficuty option four (Square and text) Hard
        rectagel_op4 = pg.Rect(10, rectagel_op3.y+110, self.WIDTH-20, 100)
        hard = pg.draw.rect(self.window, self.colors["RED"], rectagel_op4)
        self.window.blit(self.font_menu.render("D. Hard", 1, self.colors["BLACK"]),(rectagel_op4.x+10, rectagel_op4.y+10))
        self.window.blit(self.font_txt.render("25% chance for bottomless holes and 35% for bats and 5 Arrows. WUMPUS CAN MOVE", 1, self.colors["BLACK"]),(rectagel_op4.x+10, rectagel_op4.y+60))

        # Update screen
        pg.display.update()

        # Returns the squeer for every option
        return peacful, eazy, normal, hard

    ''' Draws game window on screen '''
    def draw_game(self, room_obj_list, arrows, txt_rectangel, side_rectangel_l, south_rectangel, rooms_traveld):
        # Resets the screen
        self.window.fill(self.colors["BLACK"])

        # Draws the room and rectangels (left and botten)
        self.window.blit(self.empty_room, (self.WIDTH/2-self.ROOM_WIDTH/2, 10))
        pg.draw.rect(self.window, self.colors["WHITE"], txt_rectangel)
        pg.draw.rect(self.window, self.colors["WHITE"], side_rectangel_l)

        # Draws rectangel for clicking on for moving south
        pg.draw.rect(self.window, self.colors["RED"], south_rectangel)
        self.window.blit(self.font_txt.render("SOUTH", 1, self.colors["WHITE"]), (420, 382))

        # Draws arrows and number of arrows left
        self.window.blit(self.arrows_pic, (side_rectangel_l.x+1, side_rectangel_l.y+5))
        self.window.blit(self.font_menu.render(str(arrows), 1, self.colors["RED"]), (side_rectangel_l.x+80, side_rectangel_l.y+10))

        # Prints avalible option
        self.print_keys("play")

        # check current room for for dangers and returns result (end function)
        cur_room = self.find_cur_room(room_obj_list)
        result = cur_room.turn_out(room_obj_list)
        if result in ["sacrificed", "falling", "eaten", "flown"]:
            return result

        # Update current room
        cur_room = self.find_cur_room(room_obj_list)

        # Print room information and nearby danger information
        self.print_room_string(cur_room, txt_rectangel)
        self.nearby_dangers(cur_room, txt_rectangel)
        
        # Update screen
        pg.display.update()    

    ''' Draws game window on fire on screen '''
    def draw_fire(self, txt_rectangel, rooms_traveld):
        # Resets txt square, draws new room with arrow
        pg.draw.rect(self.window, self.colors["WHITE"], txt_rectangel)
        self.window.blit(self.arrow_in_room, (self.WIDTH/2-self.ROOM_WIDTH/2, 10))

        # Prints information on what (of 3) rooms the arrow is on it way to
        ordinal_numbers = ["", "second", "third"]
        shot_string = self.font_txt.render(f"The arrow leaves the {ordinal_numbers[rooms_traveld]} room. What direction?", 1, self.colors["BLACK"])
        self.window.blit(shot_string, (txt_rectangel.x+5, txt_rectangel.y+20)) 

        # Prints avalible options for player
        self.print_keys("fire")

        # Update the screen
        pg.display.update()        

    ''' Draws game victory window on fire on screen '''
    def draw_victory(self, txt_rectangel, name, game_state):
        # Resets txt square, and prints victory room
        pg.draw.rect(self.window, self.colors["WHITE"], txt_rectangel)
        self.window.blit(self.victory_room, (self.WIDTH/2-self.ROOM_WIDTH/2, 10))
        
        # Prints txt on txt square
        string_1 = "Wumpus dies in agony, the door out of CSC unlocks and you can leave,"
        string_2 = "if you can find the way out that is ..."
        string_3 = "Level 1 cleard"
        self.window.blit(self.font_txt.render(string_1, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+5))
        self.window.blit(self.font_txt.render(string_2, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+25))
        self.window.blit(self.font_txt.render(string_3, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))

        # Prints score on screen
        self.window.blit(self.font_txt.render(str(self.score), 1, self.colors["YELLOW"]),(self.WIDTH/2+20, self.HEIGHT/4+23))

        # Prints avalible option for player
        self.print_keys(game_state)

        # Prints players writen name while player is typing
        self.window.blit(self.font_txt.render("What is the you're name traveller: ", 1, self.colors["RED"]),(txt_rectangel.x+5, txt_rectangel.y+85))
        self.window.blit(self.font_txt.render(name, 1, self.colors["BLACK"]),(txt_rectangel.x+255, txt_rectangel.y+85))

        # Update screen
        pg.display.update()    

    ''' Draws game loose window on fire on screen '''
    def draw_loss(self, lose_condition, side_rectangel_l, txt_rectangel):
        # For when lose conditon only prints one string
        string_2 = ""
        string_3 = ""
        string_4 = ""
        string_5 = ""
        string_6 = ""

        # Sets strings depending on lose_condition for printing in txt screen and room_picture
        if lose_condition == "sacrificed":
            room_type = self.wumpus_room        
            string_1 = "You feel bat wings against your cheek and before you have gotten time to react, "
            string_2 = "you are lifted up into the air. Then flown to Wumpus and sacrificed"
            self.window.blit(self.bat, (side_rectangel_l.x+5, side_rectangel_l.y+self.ROOM_HEIGHT-90))
        elif lose_condition == "falling":
            room_type = self.hole_room       
            string_1 = "You stepped into a bottomless pit. To never be found again."
        elif lose_condition == "eaten":
            room_type = self.wumpus_room
            string_1 = "You step into the room which is full of foul-smelling smoke."
            string_2 = "But before you have time to hold your breath, the most vile gap you have ever seen"
            string_3 = "appears over you and devours you completely."
        elif lose_condition == "shoot":
            room_type = self.shoot_room
            string_1 = "You have shoot you're self in the back and are now bleeding on the floor"
        elif lose_condition == "walk_in":
            room_type = self.wumpus_room
            string_1 = "You step into the room and it's empty, you exhale."
            string_2 = "You feel the floor start to shake, Wumpus is on the move."
            string_3 = "The door to your room opens and the terrifying Wumpus enters the room."
            string_4 = "You stand still in the hope that he doesn't see you."
            string_5 = "Just as you think you'll make it, Wumpu's tail wraps around you,"
            string_6 = "he then lifts you upp swallows you whole."
        elif lose_condition == "no_arrows":
            string_1 = "You missed, and now have run out of arrows in your quiver."
            string_2 = "Which means your chances of killing Wumpus are over. You are now slowly dying of hunger."
        
        # Prints set strings and loss victory room picture
        if lose_condition in ["sacrificed", "falling", "eaten", "shoot", "walk_in"]:
            self.window.blit(room_type, (self.WIDTH/2-self.ROOM_WIDTH/2, 10))
            pg.draw.rect(self.window, self.colors["WHITE"], txt_rectangel)
            self.window.blit(self.font_txt.render(string_1, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+5))
            self.window.blit(self.font_txt.render(string_2, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+25))
            self.window.blit(self.font_txt.render(string_3, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))
            self.window.blit(self.font_txt.render(string_4, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+65))
            self.window.blit(self.font_txt.render(string_5, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+85))
            self.window.blit(self.font_txt.render(string_6, 1, self.colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+105))

        # Print avalible option for player
        self.print_keys("loss")

        # Update screen
        pg.display.update()

    ''' Main loop for pygame '''
    def main(self):
        # Set caption and curser
        pg.display.set_caption("Wumpus")                    
        pg.mouse.set_cursor(pg.cursors.diamond)

        # Defines difficulty dictonary and sets current difficulty
        difficultys_dict = {"peacful" : (0, 0, 99, False, "score_saves\score_list_1.txt") , "eazy" : (0.1, 0.2, 10, False, "score_saves\score_list_2.txt") , "normal" : (0.2, 0.3, 5, False, "score_saves\score_list_3.txt") , "hard" : (0.25, 0.35, 5, True, "score_saves\score_list_4.txt")}
        difficulty = difficultys_dict["normal"]

        # Constant set FPS
        FPS = 60

        # Defines rectangel (botten and left)
        txt_rectangel = pg.Rect(self.WIDTH/2-self.ROOM_WIDTH/2, self.ROOM_HEIGHT+20, self.ROOM_WIDTH, self.HEIGHT-self.ROOM_HEIGHT-30)
        side_rectangel_l = pg.Rect(10, 10, (self.WIDTH-self.ROOM_WIDTH)/2-20, self.ROOM_HEIGHT)
        south_rectangel = pg.Rect(394, 376, (503-394), (401-376))

        # Game_state controlls game loop (what to draw and click on)
        game_state = "menu"

        # Sets varibles that has to be defined in before hand
        flown = False
        direction = None
        rooms_traveld = 0
        arrows = difficulty[2]
        arrow_room = None
        name = ""
        self.score = 100
        click = True
        
        #-------Controlls-Keys-------#

        clock = pg.time.Clock()        
        # Game loop
        while True:
            clock.tick(FPS)

            # Checks for events
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    quit()

                # Resets mouse click after bottenup (so you can click)
                if event.type == pg.MOUSEBUTTONUP and click == False:
                    click = True

                # Checks if click on menu rectangel with leftbutton and chage game_state
                if game_state == "menu":
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click:
                        click = False
                        pos = pg.mouse.get_pos()
                        if menu_rect[0].collidepoint(pos):
                            game_state = "rules"
                        if menu_rect[1].collidepoint(pos):
                            game_state = "difficulty"
                        if menu_rect[2].collidepoint(pos):
                            random_rooms = False
                            game_state = "play"
                        if menu_rect[3].collidepoint(pos):
                            game_state = "score"
                        if menu_rect[4].collidepoint(pos): 
                            quit()

                # Check if click on screen sets game_state to menu
                if game_state in ["rules" , "score"]:
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click:
                        click = False
                        game_state = "menu"
                    
                # Check if click on title menu sets game_state to menu
                if game_state in ["loss", "victory_2"]:
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click:
                        click = False
                        pos = pg.mouse.get_pos()
                        if 308 <= pos[0] <= 589 and 264 <= pos[1] <= 296:
                            game_state = "menu"

                # Checks if click on difficulty rectangel with leftbutton and chage game_state back to menu
                # And chages to respective difficulty
                if game_state == "difficulty":
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click:
                        click = False
                        pos = pg.mouse.get_pos()
                        if difficulty_rect[0].collidepoint(pos):
                            game_state = "menu"
                            difficulty = difficultys_dict["peacful"]
                        if difficulty_rect[1].collidepoint(pos):
                            game_state = "menu"
                            difficulty = difficultys_dict["eazy"]
                        if difficulty_rect[2].collidepoint(pos):
                            random_rooms = False
                            game_state = "menu"
                            difficulty = difficultys_dict["normal"]
                        if difficulty_rect[3].collidepoint(pos):
                            game_state = "menu"
                            difficulty = difficultys_dict["hard"]
                        if game_state == "menu":
                            arrows = difficulty[2]

                # When in game_state "play" checks if clicks on door
                if game_state == "play":

                    # If it is left click moves
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click:
                        click = False

                        # Take out curent player number and moves througe clicked door
                        cur_room = self.find_cur_room(room_obj_list)
                        moves = self.click_doors_player(cur_room, room_obj_list)    

                        # If previous returns moves = True and difficulty[3] = True (wumpus moves or not)  
                        # move wumpus and prints that he does           
                        if difficulty[3] and moves:
                            pg.time.wait(100)                    
                            game_state = self.wumpus_moves_func(room_obj_list, txt_rectangel, game_state)
                            pg.time.wait(2300)

                            # If wumpus moves in to players room chages game_state loss
                            if game_state == "loss":
                                lose_condition = "walk_in"

                    # Checks if clicks on screen to return from flown on screen
                    if flown:
                        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                            click = False
                            flown = False

                    # If it right click on door shoot arrow
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and click:
                        click = False
                        cur_room = self.find_cur_room(room_obj_list)
                        result_fire = self.click_doors_arrow(cur_room, room_obj_list, game_state) 

                        # Sets game_state scording to arrow shoot
                        game_state = result_fire[1]

                        # Result if game_state is changed
                        if game_state == "loss":
                            lose_condition = "shoot"
                            arrows -= 1
                        elif game_state == "victory":
                            arrows -= 1

                        # If result_fire[0] is true, arrow is shoot
                        elif result_fire[0]:
                            game_state = "fire"
                            rooms_traveld = 1

                # Ater first shoot only option is to move arrow check for right click on doors
                if game_state == "fire" and rooms_traveld != 3:
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and click:
                        click = False
                        for room in room_obj_list:
                            if room.arrow:
                                arrow_room = room
                        result_fire = self.click_doors_arrow(arrow_room, room_obj_list, game_state)
                        game_state = result_fire[1]

                    # Check for result
                        if game_state == "loss":
                            lose_condition = "shoot"
                            arrows -= 1
                        elif game_state == "victory":
                            arrows -= 1
                        elif result_fire[0]:
                            game_state = "fire"
                            rooms_traveld += 1

                    # No arrow moves left back to "play" game_state       
                    if rooms_traveld == 3:
                        arrows -= 1
                        game_state = "play"

                    # If no arrows left loss game
                    if arrows == 0:
                        game_state = "loss"    
                        lose_condition = "no_arrows"          

                # Victory input options (when player is done go to game_state (victory_2))
                if game_state == "victory":
                    # Player prints name
                    if event.type == pg.KEYDOWN and len(name) != 5:
                        name = self.letter_input(event, name)
                        if event.key == pg.K_RETURN:
                            game_state = "victory_2"
                            # If player just click enter don't save score
                            if name == "":
                                name = None
                            self.make_score_board(name, difficulty[4])
                    if len(name) == 5:
                        if event.type == pg.KEYDOWN: 
                            if event.key == pg.K_BACKSPACE:
                                name = name[:-1]
                            if event.key == pg.K_RETURN:
                                self.make_score_board(name, difficulty[4])
                                game_state = "victory_2"

        #-------Controlls-Draw-Functions-------#
            # Draw screen for each game_state
            if game_state == "menu":
                menu_rect = self.draw_menu()
            elif game_state == "rules":
                self.draw_game_rules()
            elif game_state == "difficulty":
                difficulty_rect = self.draw_set_difficulty()
            elif game_state == "score":
                self.draw_score_board(None, difficulty[4])
            elif game_state == "play":
                if flown != True:

                    # If not randomiazed make randomized rooms
                    if random_rooms == False:
                        room_obj_list = self.room_list(difficulty[0], difficulty[1])
                        self.score = 100
                        random_rooms = True
                    
                    result = self.draw_game(room_obj_list, arrows, txt_rectangel, side_rectangel_l, south_rectangel, rooms_traveld)

                    # Check result 
                    if result in ["sacrificed", "falling", "eaten"]:
                        lose_condition = result
                        game_state = "loss"
                    if result == "flown":
                        flown = True
                if flown:
                    self.print_flown(txt_rectangel, side_rectangel_l, game_state)

            # Draws screen acording to game_state
            elif game_state == "fire":
                self.draw_fire(txt_rectangel, rooms_traveld)
            elif game_state in ["victory", "victory_2"]:
                random_rooms = False
                arrows = difficulty[2]
                self.draw_victory(txt_rectangel, name, game_state)
            elif game_state == "loss":
                random_rooms = False
                arrows = difficulty[2]
                self.draw_loss(lose_condition, side_rectangel_l, txt_rectangel)

if __name__ == "__main__":
    pg.font.init()
    Gui().main()
