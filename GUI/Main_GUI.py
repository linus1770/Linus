from Wumpus_pg_class import Wumpus_class
import pygame as pg 
import random
import os
pg.font.init()

#-------Constants-for-pygame------#

''' Fonts and size for text, Pygame'''
font_menu = pg.font.SysFont("opensans", 60)
font_txt = pg.font.SysFont("opensans", 23)


width, height = 900, 600                            # Main window size
room_width, room_height = 600, 390                  # Room_picture size
window = pg.display.set_mode((width, height))
pg.display.set_caption("Wumpus")                    # Sets caption of game
pg.mouse.set_cursor(pg.cursors.diamond)

colors = {"WHITE" : (255, 255, 255), "BLACK" : (0, 0, 0), "GREEN" : (0, 255, 0), "YELLOW" : (249, 249, 50), "ORANGE" : (255, 128, 0), "RED" : (195, 26, 33), "BLUE" : (49, 184, 252)}

empty_room = pg.transform.scale(pg.image.load(os.path.join("Assets", "room.png")),(room_width, room_height))
shoot_room = pg.transform.scale(pg.image.load(os.path.join("Assets", "room_shoot.jpg")),(room_width, room_height))
hole_room = pg.transform.scale(pg.image.load(os.path.join("Assets", "room_hole.jpg")),(room_width, room_height))
wumpus_room = pg.transform.scale(pg.image.load(os.path.join("Assets", "room_wumpus.jpg")),(room_width, room_height))
victory_room = pg.transform.scale(pg.image.load(os.path.join("Assets", "room_victory.jpg")),(room_width, room_height))
arrows_pic = pg.transform.scale(pg.image.load(os.path.join("Assets", "arrows.png")),(75, 40))
bat = pg.transform.scale(pg.image.load(os.path.join("Assets", "bat.png")),(120, 70))

#-------Start-functions-------#

def room_list(hole_chance, bat_chance):  # Creat objects for every room and conncet them randomly to eachother
    # through classmetods. Finaly Returns the list of objects 
    room_obj_list = [Wumpus_class(i) for i in range(1,21)]

    connection_north = creat_connection_list()
    connection_east = creat_connection_list()

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

def creat_connection_list():
    connection_list = list(range(1,21))
    random.shuffle(connection_list)
    return connection_list

def read_file(file):                        # Opens txt-file and take out information.
    return_list = []                          
    score_list = []                           
    score_file = open(file, "r")                    
    score_list = score_file.readlines()          
    for row in score_list:         
        row_split = row.split(",")                 
        row_score = [int(row_split[0]), row_split[1]]
        return_list.append(row_score)              
    score_file.close                                   
    return return_list

def write_file(file, score_matrix):
    score_file = open(file, "w")
    for high_score in score_matrix:
        score_file.writelines(str(high_score[0]) + "," + high_score[1] + "," + "\n")
    score_file.close()

def make_score_board(score, player_name, file):
    score_matrix = read_file(file)
    if score != None:
        new_score = [score, player_name]
        score_matrix.append(new_score)
        score_matrix.sort(reverse=True)
        try:
            score_matrix.pop(10)
        except:
            pass
    position = 0
    list_for_print = []
    for high_score in score_matrix:
        position += 1
        list_for_print.append(str(position) + ". " + high_score[1] + " - " + str(high_score[0]))

    write_file(file, score_matrix)
    return list_for_print

#-------GAME-FUNCTIONS-------#

def print_room_string(cur_room, txt_rectangel):    # Prints a string for game
    room_info = "You are in room nummber " + str(cur_room.number) + ". You can move to following rooms:"    
    room_str = font_txt.render(room_info, 1, colors["BLACK"])
    window.blit(room_str, (txt_rectangel.x+5, txt_rectangel.y+5))
    adj_rooms = [adj_room.number for adj_room in cur_room.adjacent_rooms]
    adj_rooms.sort()
    for index, number in enumerate(adj_rooms):
        window.blit(font_txt.render(str(number), 1, colors["BLACK"]), (txt_rectangel.x+470+(22*index), txt_rectangel.y+5))

def nearby_dangers(room, txt_rectangel):     # Check nearby rooms for dangers and print a warning message
    # holes, bats and wumpus
    dangers = ["wumpus", "bat", "hole"]
    dangers_list = []
    for adj_room in room.adjacent_rooms:
        if adj_room.hole == True:
            dangers.append("hole")
        elif adj_room.bat == True:
            dangers.append("bat")
        elif adj_room.wumpus == True:
            dangers.append("wumpus")
    dict_dangers = dict((dang, dangers.count(dang)) for dang in dangers)

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
    
    nearby_bats_str = dangers_list[0]
    nearby_holes_str = dangers_list[1]
    nearby_wumpus_str = dangers_list[2]
    window.blit(font_txt.render(nearby_bats_str, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))
    window.blit(font_txt.render(nearby_holes_str, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+65))
    window.blit(font_txt.render(nearby_wumpus_str, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+85))

def shoot_arrow(arrow_room, room_obj_list, direction):
    hit = "nothing"
    arrow_room = arrow_room.move_arrow(direction, room_obj_list)
    for room in room_obj_list:
        if room.arrow and room.wumpus: #Why does this work?
            room.wumpus = False
            room.hole = True
            hit = "wumpus"
        elif room.player and room.arrow:
            hit = "yourself"
    return arrow_room, hit

def find_cur_room(room_obj_list):
    for room in room_obj_list:
        if room.player == True:
            return room

def get_direction(event, move_fire):
    direction = None
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_UP:
            direction = "N" 
        if event.key == pg.K_DOWN:
            direction = "S"
        if event.key == pg.K_RIGHT:
            direction = "E"
        if event.key == pg.K_LEFT:
            direction = "W"
    return direction, move_fire

def letter_input(event, string):
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
    if event.key == pg.K_BACKSPACE:
        string = string[:-1]
    return string

#-------GUI-DRAW-FUNCTIONS-------#

def print_flown(txt_rectangel, side_rectangel_l, game_state, move_fire):
    pg.draw.rect(window, colors["WHITE"], txt_rectangel)
    string_1 = "You feel bat wings against your cheek and before you have gotten time to react, " 
    string_2 = "you are lifted up into the air."
    string_3 = "After a short flight, you are dropped down in a new room"
    window.blit(font_txt.render(string_1, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+5))
    window.blit(font_txt.render(string_2, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+25))
    window.blit(font_txt.render(string_3, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))
    window.blit(bat, (side_rectangel_l.x+5, side_rectangel_l.y+room_height-90))
    print_keys(game_state, move_fire)
    pg.display.update()

def wumpus_moves_func(room_obj_list, txt_rectangel, game_state):
    direction = []
    for room in room_obj_list:
        if room.wumpus == True:
            #print("Wumpus--", room.number)         # FOR TESTING
            if room.north.hole == False:
                direction.append(room.north)
            if room.south.hole == False:
                direction.append(room.south)
            if room.east.hole == False:
                direction.append(room.east)
            if room.west.hole == False:
                direction.append(room.west)
            try:
                new_room = direction[random.randrange(0, len(direction))]
                room.wumpus = False
                new_room.wumpus = True
                new_room.bat = False
            except:
                pass
            if room.wumpus == True:
                wumpus_moves_str = "You hear Wumpus screaming in frustration"
            elif room.wumpus == False:
                wumpus_moves_str1 = "As you are about to move, you feel the floor shake as" 
                wumpus_moves_str2 = "Wumpus moves, but you can not figure out where."
            window.blit(font_txt.render(wumpus_moves_str1, 1, colors["RED"]),(txt_rectangel.x+5, txt_rectangel.y+125))
            window.blit(font_txt.render(wumpus_moves_str2, 1, colors["RED"]),(txt_rectangel.x+5, txt_rectangel.y+145))

            pg.display.update()

    for room in room_obj_list:
        if room.player == True and room.wumpus == True:
            game_state = "loss"
    
    return game_state

def print_keys(game_state, move_fire):
    side_rectangel_r = pg.Rect(width-((width-room_width)/2-10), 10, (width-room_width)/2-20, room_height)
    pg.draw.rect(window, colors["WHITE"], side_rectangel_r)

    window.blit(font_txt.render("Avalible moves", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+10))        
    if game_state == "start": 
        if move_fire == None:
            window.blit(font_txt.render("M. Move", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))        
            window.blit(font_txt.render("F. Fire", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
        if move_fire in ["move", "fire"]:    
            window.blit(font_txt.render("Up", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))        
            window.blit(font_txt.render("Down", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
            window.blit(font_txt.render("Left", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+80))        
            window.blit(font_txt.render("Right", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+100))
        if move_fire == "flown":
            window.blit(font_txt.render("SPACE -", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))
            window.blit(font_txt.render("To Continue", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
    if game_state in ["loss", "victory_2"]:
        window.blit(font_txt.render("SPACE. Menu", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))
        window.blit(font_txt.render("or click on", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
        window.blit(font_txt.render("Titel Menu", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+80))
    if game_state == "victory":
        window.blit(font_txt.render("Write name -", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+40))
        window.blit(font_txt.render("(eng letters)", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+60))
        window.blit(font_txt.render("Max 5 letters", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+80))
        window.blit(font_txt.render("Enter - Confirm", 1, colors["BLACK"]),(side_rectangel_r.x+10, side_rectangel_r.y+120))         

def draw_menu():
    window.fill(colors["BLACK"])
    
    rectagel_op1 = pg.Rect(10, 10, width-20, 100)
    one = pg.draw.rect(window, colors["YELLOW"], rectagel_op1)
    options_txt_1 = font_menu.render("1. Game Rules", 1, colors["BLACK"])
    window.blit(options_txt_1, (rectagel_op1.x+10, rectagel_op1.y+10))

    rectagel_op2 = pg.Rect(10, rectagel_op1.y+110, width-20, 100)
    two = pg.draw.rect(window, colors["ORANGE"], rectagel_op2)
    options_txt_2 = font_menu.render("2. Set Difficulty", 1, colors["BLACK"])
    window.blit(options_txt_2, (rectagel_op2.x+10, rectagel_op2.y+10))

    rectagel_op3 = pg.Rect(10, rectagel_op2.y+110, width-20, 100)
    three = pg.draw.rect(window, colors["GREEN"], rectagel_op3)
    options_txt_3 = font_menu.render("3. Start Game", 1, colors["BLACK"])
    window.blit(options_txt_3, (rectagel_op3.x+10, rectagel_op3.y+10))

    rectagel_op4 = pg.Rect(10, rectagel_op3.y+110, width-20, 100)
    four = pg.draw.rect(window, colors["BLUE"], rectagel_op4)
    options_txt_4 = font_menu.render("4. Scoreboard (Current difficulty)", 1, colors["BLACK"])
    window.blit(options_txt_4, (rectagel_op4.x+10, rectagel_op4.y+10))

    rectagel_op5 = pg.Rect(10, rectagel_op4.y+110, width-20, 100)
    five = pg.draw.rect(window, colors["RED"], rectagel_op5)
    options_txt_5 = font_menu.render("5. Quit", 1, colors["BLACK"])
    window.blit(options_txt_5, (rectagel_op5.x+10, rectagel_op5.y+10))

    pg.display.update()
    return one, two, three, four, five

def draw_game_rules():
    rectagel = pg.Rect(10, 10, width-20, height-20)
    pg.draw.rect(window, colors["YELLOW"], rectagel)

    rules_txt_1 = font_txt.render("You're locked in the culverts below CSC, where the voracious Wumpus lives.", 1, colors["BLACK"])
    rules_txt_2 = font_txt.render("To avoid being eaten up and unlocking the door, you need to shoot Wumpus with your bow and arrow.", 1, colors["BLACK"])
    rules_txt_3 = font_txt.render("The culverts have 20 rooms that are connected by narrow corridors.", 1, colors["BLACK"])
    rules_txt_4 = font_txt.render("You can move north, east, south or west from one room to another.", 1, colors["BLACK"])
    
    rules_txt_5 = font_txt.render("However, there are dangers lurking here. In some rooms there are bottomless holes.", 1, colors["BLACK"])
    rules_txt_6 = font_txt.render("If you step into one, you die immediately. In other rooms there are bats that lift you up,", 1, colors["BLACK"])
    rules_txt_7 = font_txt.render("fly a bit and drop you into an arbitrary room. In one of the rooms is Wumpus,", 1, colors["BLACK"])
    rules_txt_8 = font_txt.render("and if you venture into that room you will immediately be eaten up.", 1, colors["BLACK"])
    rules_txt_9 = font_txt.render("Fortunately, from the rooms next door you can feel the gust of wind from an bottomless hole", 1, colors["BLACK"])
    rules_txt_10 = font_txt.render("or the smell of Wumpus. You also get the numbers of each room which are adjacent.", 1, colors["BLACK"])
    
    rules_txt_11 = font_txt.render("To win the game, you must shoot Wumpus and find the way out. When you shoot an arrow, it moves through three rooms", 1, colors["BLACK"])
    rules_txt_12 = font_txt.render("- you can control which direction the arrow should choose in each room.", 1, colors["BLACK"])
    rules_txt_13 = font_txt.render("Do not forget that the tunnels wind in unexpected ways. You may shoot yourself ...", 1, colors["BLACK"])
    rules_txt_14 = font_txt.render("You have a limited supplie of arrows. Good luck!", 1, colors["BLACK"])

    return_txt = font_menu.render("Return with spacebar or click on screen", 1, colors["BLACK"])

    text_x = 15
    text_y = 15
    distance = 20

    window.blit(rules_txt_1, (text_x, text_y+(distance*0)))
    window.blit(rules_txt_2, (text_x, text_y+(distance*1)))
    window.blit(rules_txt_3, (text_x, text_y+(distance*2)))
    window.blit(rules_txt_4, (text_x, text_y+(distance*3)))
    window.blit(rules_txt_5, (text_x, text_y+(distance*4)))
    window.blit(rules_txt_6, (text_x, text_y+(distance*6)))
    window.blit(rules_txt_7, (text_x, text_y+(distance*7)))
    window.blit(rules_txt_8, (text_x, text_y+(distance*8)))
    window.blit(rules_txt_9, (text_x, text_y+(distance*9)))
    window.blit(rules_txt_10, (text_x, text_y+(distance*10)))
    window.blit(rules_txt_11, (text_x, text_y+(distance*12)))
    window.blit(rules_txt_12, (text_x, text_y+(distance*13)))
    window.blit(rules_txt_13, (text_x, text_y+(distance*14)))
    window.blit(rules_txt_14, (text_x, text_y+(distance*15)))
    window.blit(return_txt, (text_x, text_y+(distance*19)))

    pg.display.update()  

def draw_score_board(score, player_name, save_file):
    rectagel = pg.Rect(10, 10, width-20, height-20)
    pg.draw.rect(window, colors["BLUE"], rectagel)

    window.blit(font_menu.render("Top 10 scores", 1 , colors["BLACK"]), (90,15))

    high_scores = make_score_board(None, None, save_file)
    for index, score in enumerate(high_scores):
        window.blit(font_menu.render(score, 1, colors["BLACK"]), (100, 90+(40*index)))

    window.blit(font_menu.render("Return with spacebar or click on screen", 1, colors["BLACK"]),(50, 510))

    pg.display.update()  

def draw_set_difficulty():
    window.fill(colors["BLACK"])
    
    rectagel_op1 = pg.Rect(10, 10, width-20, 100)
    peacful = pg.draw.rect(window, colors["GREEN"], rectagel_op1)
    window.blit(font_menu.render("A. Peacful", 1, colors["BLACK"]),(rectagel_op1.x+10, rectagel_op1.y+10))
    window.blit(font_txt.render("Only Wumpus can kill you (No bats or bottomless holes) and 99 Arrows", 1, colors["BLACK"]),(rectagel_op1.x+10, rectagel_op1.y+60))

    rectagel_op2 = pg.Rect(10, rectagel_op1.y+110, width-20, 100)
    eazy = pg.draw.rect(window, colors["YELLOW"], rectagel_op2)
    window.blit(font_menu.render("B. Eazy", 1, colors["BLACK"]),(rectagel_op2.x+10, rectagel_op2.y+10))
    window.blit(font_txt.render("10% chance for bottomless holes and 20% for bats and 10 Arrows", 1, colors["BLACK"]),(rectagel_op2.x+10, rectagel_op2.y+60))

    rectagel_op3 = pg.Rect(10, rectagel_op2.y+110, width-20, 100)
    normal = pg.draw.rect(window, colors["ORANGE"], rectagel_op3)
    window.blit(font_menu.render("C. Normal", 1, colors["BLACK"]),(rectagel_op3.x+10, rectagel_op3.y+10))
    window.blit(font_txt.render("20% chance for bottomless holes and 30% for bats and 5 Arrows. STANDARD", 1, colors["BLACK"]),(rectagel_op3.x+10, rectagel_op3.y+60))

    rectagel_op4 = pg.Rect(10, rectagel_op3.y+110, width-20, 100)
    hard = pg.draw.rect(window, colors["RED"], rectagel_op4)
    window.blit(font_menu.render("D. Hard", 1, colors["BLACK"]),(rectagel_op4.x+10, rectagel_op4.y+10))
    window.blit(font_txt.render("25% chance for bottomless holes and 35% for bats and 5 Arrows. WUMPUS CAN MOVE", 1, colors["BLACK"]),(rectagel_op4.x+10, rectagel_op4.y+60))

    pg.display.update()
    return peacful, eazy, normal, hard

def draw_game(room_type, room_obj_list, arrows, move_fire, txt_rectangel, side_rectangel_l, rooms_traveld):
    window.fill(colors["BLACK"])

    window.blit(room_type, (width/2-room_width/2, 10))
    pg.draw.rect(window, colors["WHITE"], txt_rectangel)
    pg.draw.rect(window, colors["WHITE"], side_rectangel_l)

    window.blit(arrows_pic, (side_rectangel_l.x+1, side_rectangel_l.y+5))
    window.blit(font_menu.render(str(arrows), 1, colors["RED"]), (side_rectangel_l.x+80, side_rectangel_l.y+10))

    print_keys("start", move_fire)

    cur_room = find_cur_room(room_obj_list)
    result = cur_room.turn_out(room_obj_list)
    if result in ["sacrificed", "falling", "eaten", "flown"]:
        return result

    cur_room = find_cur_room(room_obj_list)

    print_room_string(cur_room, txt_rectangel)
    nearby_dangers(cur_room, txt_rectangel)

    if move_fire == "fire" and rooms_traveld != 3:
        ordinal_numbers = ["first", "second", "third"]
        shot_string = font_txt.render(f"The arrow leaves the {ordinal_numbers[rooms_traveld]} room. What direction?", 1, colors["BLACK"])
        window.blit(shot_string, (txt_rectangel.x+5, txt_rectangel.y+105))
    
    pg.display.update()    
        
def draw_victory(txt_rectangel, score, name, game_state):
    pg.draw.rect(window, colors["WHITE"], txt_rectangel)
    window.blit(victory_room, (width/2-room_width/2, 10))
    
    string_1 = "Wumpus dies in agony, the door out of CSC unlocks and you can leave,"
    string_2 = "if you can find the way out that is ..."
    string_3 = "Level 1 cleard"
    window.blit(font_txt.render(string_1, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+5))
    window.blit(font_txt.render(string_2, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+25))
    window.blit(font_txt.render(string_3, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))

    window.blit(font_txt.render(str(score), 1, colors["YELLOW"]),(width/2+20, height/4+23))

    print_keys(game_state, None)

    window.blit(font_txt.render("What is the you're name traveller: ", 1, colors["RED"]),(txt_rectangel.x+5, txt_rectangel.y+85))
    window.blit(font_txt.render(name, 1, colors["BLACK"]),(txt_rectangel.x+255, txt_rectangel.y+85))

    pg.display.update()    

def draw_loss(lose_condition, side_rectangel_l, txt_rectangel):
    string_2 = ""
    string_3 = ""
    if lose_condition == "sacrificed":
        room_type = wumpus_room        
        string_1 = "You feel bat wings against your cheek and before you have gotten time to react, "
        string_2 = "you are lifted up into the air. Then flown to Wumpus and sacrificed"
        window.blit(bat, (side_rectangel_l.x+5, side_rectangel_l.y+room_height-90))
    elif lose_condition == "falling":
        room_type = hole_room       
        string_1 = "You stepped into a bottomless pit. To never be found again."
    elif lose_condition == "eaten":
        room_type = wumpus_room
        string_1 = "You step into the room which is full of foul-smelling smoke."
        string_2 = "But before you have time to hold your breath, the most vile gap you have ever seen"
        string_3 = "appears over you and devours you completely."
    elif lose_condition == "shoot":
        room_type = shoot_room #Gonna change
        string_1 = "You have shoot you're self in the back and are now bleeding on the floor"
    elif lose_condition == "walk_in":
        room_type = wumpus_room
        string_1 = "You step into the room and it's empty, you exhale."
        string_2 = "You feel the floor start to shake, Wumpus is on the move."
        string_3 = "The door to your room opens and the terrifying Wumpus enters the room."
        string_4 = "You stand still in the hope that he doesn't see you."
        string_5 = "Just as you think you'll make it, Wumpu's tail wraps around you,"
        string_6 = "he then lifts you upp swallows you whole."
        window.blit(font_txt.render(string_4, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+65))
        window.blit(font_txt.render(string_5, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+85))
        window.blit(font_txt.render(string_6, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+105))
    if lose_condition in ["sacrificed", "falling", "eaten", "shoot", "walk_in"]:
        window.blit(room_type, (width/2-room_width/2, 10))
        pg.draw.rect(window, colors["WHITE"], txt_rectangel)
        window.blit(font_txt.render(string_1, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+5))
        window.blit(font_txt.render(string_2, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+25))
        window.blit(font_txt.render(string_3, 1, colors["BLACK"]),(txt_rectangel.x+5, txt_rectangel.y+45))

    print_keys("loss", None)

    pg.display.update()  


def main():
    difficultys_dict = {"peacful" : (0, 0, 99, False, "score_saves\score_list_1.txt") , "eazy" : (0.1, 0.2, 10, False, "score_saves\score_list_2.txt") , "normal" : (0.2, 0.3, 5, False, "score_saves\score_list_3.txt") , "hard" : (0.25, 0.35, 5, True, "score_saves\score_list_4.txt")}
    difficulty = difficultys_dict["normal"]

    FPS = 60

    txt_rectangel = pg.Rect(width/2-room_width/2, room_height+20, room_width, height-room_height-30)
    side_rectangel_l = pg.Rect(10, 10, (width-room_width)/2-20, room_height)

    game_state = "menu"
    move_fire = None
    direction = None
    rooms_traveld = 0
    arrows = difficulty[2]
    name = ""
    score = 100
    click = True
    
    #-------Controlls-Keys-------#

    clock = pg.time.Clock()
    while True:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()

            if event.type == pg.MOUSEBUTTONUP and event.button == 1 and click == False:
                click = True

            if game_state == "menu":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_1:
                        game_state = "rules"
                    if event.key == pg.K_2:
                        game_state = "difficulty"
                    if event.key == pg.K_3:
                        random_rooms = False
                        game_state = "start"
                    if event.key == pg.K_4:
                        game_state = "score"
                    if event.key == pg.K_5:
                        quit()

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click == True:
                    click = False
                    pos = pg.mouse.get_pos()
                    if menu_rect[0].collidepoint(pos):
                        game_state = "rules"
                    if menu_rect[1].collidepoint(pos):
                        game_state = "difficulty"
                    if menu_rect[2].collidepoint(pos):
                        random_rooms = False
                        game_state = "start"
                    if menu_rect[3].collidepoint(pos):
                        game_state = "score"
                    if menu_rect[4].collidepoint(pos): 
                        quit()

            if game_state in ["rules" , "score", "loss", "victory_2"]:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        game_state = "menu"

                if game_state in ["rules" , "score"]:
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click == True:
                        click = False
                        pos = pg.mouse.get_pos()
                        if 0 <= pos[0] <= width and 0 <= pos[1] <= height:
                            game_state = "menu"
                
                if game_state in ["loss", "victory_2"]:
                    if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click == True:
                        click = False
                        pos = pg.mouse.get_pos()
                        if 308 <= pos[0] <= 589 and 264 <= pos[1] <= 296:
                            game_state = "menu"

            if game_state == "difficulty":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_a:
                        game_state = "menu"
                        difficulty = difficultys_dict["peacful"]
                    if event.key == pg.K_b:
                        game_state = "menu"
                        difficulty = difficultys_dict["eazy"]
                    if event.key == pg.K_c:
                        game_state = "menu"
                        difficulty = difficultys_dict["normal"]
                    if event.key == pg.K_d:
                        game_state = "menu"
                        difficulty = difficultys_dict["hard"]
                    if game_state == "menu":
                        arrows = difficulty[2]                        

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click == True:
                    click = False
                    pos = pg.mouse.get_pos()
                    if difficulty_rect[0].collidepoint(pos):
                        game_state = "menu"
                        difficulty = difficultys_dict["peacful"]
                    if menu_rect[1].collidepoint(pos):
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

            if game_state == "start" and move_fire == None:
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_m:
                        move_fire = "move"
                    if event.key == pg.K_f:
                        move_fire = "fire"
                        rooms_traveld = 0
                
                if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and click == True:
                    click = False
                    pos = pg.mouse.get_pos()
                    cur_room = find_cur_room(room_obj_list)
                    if 377 <= pos[0] <= 480 and 44 <= pos[1] <= 240:
                        cur_room.move_player("N")
                        score -= 1                    
                    if 394 <= pos[0] <= 503 and 376 <= pos[1] <= 401:
                        cur_room.move_player("S")
                        score -= 1
                    if 579 <= pos[0] <= 751 and 10 <= pos[1] <= 380:
                        cur_room.move_player("E")
                        score -= 1                    
                    if 150 <= pos[0] <= 289 and 10 <= pos[1] <= 402:
                        cur_room.move_player("W")
                        score -= 1
                    if difficulty[3] == True:
                            move_fire = "move_wumpus"

                if event.type == pg.MOUSEBUTTONDOWN and event.button == 3 and click == True:
                    click = False
                    pos = pg.mouse.get_pos()
                    cur_room = find_cur_room(room_obj_list)
                    if 377 <= pos[0] <= 480 and 44 <= pos[1] <= 240:
                        cur_room.move_player("N")
                        score -= 1                    
                    if 394 <= pos[0] <= 503 and 376 <= pos[1] <= 401:
                        cur_room.move_player("S")
                        score -= 1
                    if 579 <= pos[0] <= 751 and 10 <= pos[1] <= 380:
                        cur_room.move_player("E")
                        score -= 1                    
                    if 150 <= pos[0] <= 289 and 10 <= pos[1] <= 402:
                        cur_room.move_player("W")
                        score -= 1

            if move_fire == "move":
                cur_room = find_cur_room(room_obj_list)
                direction, move_fire = get_direction(event, move_fire)
                if direction in ["N", "S", "E", "W"]:
                    cur_room.move_player(direction)
                    score -= 1                    
                    if difficulty[3] == True:
                        move_fire = "move_wumpus"
                    else:
                        move_fire = None
                        
            if game_state == "start" and move_fire == "move_wumpus":
                pg.time.wait(100)
                if event.type == pg.KEYDOWN:                       
                    game_state = wumpus_moves_func(room_obj_list, txt_rectangel, game_state)
                    pg.time.wait(2300)
                    move_fire = None
                    if game_state == "loss":
                        lose_condition = "walk_in"

            if move_fire == "fire":
                direction, move_fire = get_direction(event, move_fire)
                if direction != None and rooms_traveld != 3:
                    cur_room = find_cur_room(room_obj_list)
                    if rooms_traveld == 0:
                        arrow_room = cur_room
                    else: 
                        arrow_room = fallout[0]
                    fallout = shoot_arrow(arrow_room, room_obj_list, direction)
                    rooms_traveld += 1
                    if fallout[1] == "wumpus":
                        move_fire = None
                        game_state = "victory"
                    elif fallout[1] == "yourself":
                        move_fire = None
                        game_state = "loss"
                        lose_condition = "shoot"
                elif rooms_traveld == 3:
                    arrows -= 1
                    score -= 1
                    move_fire = None

            if move_fire == "flown":
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_SPACE:
                        move_fire = None

            if game_state == "victory":
                if event.type == pg.KEYDOWN and len(name) != 5:
                    name = letter_input(event, name)
                    if event.key == pg.K_RETURN:
                        game_state = "victory_2"
                        make_score_board(score, name, difficulty[4])
                if len(name) == 5:
                    if event.type == pg.KEYDOWN: 
                        if event.key == pg.K_BACKSPACE:
                            name = name[:-1]
                        if event.key == pg.K_RETURN:
                            make_score_board(score, name, difficulty[4])
                            game_state = "victory_2"

    #-------Controlls-Draw-Functions-------#

        if game_state == "menu":
            menu_rect = draw_menu()
        elif game_state == "rules":
            draw_game_rules()
        elif game_state == "difficulty":
            difficulty_rect = draw_set_difficulty()
        elif game_state == "score":
            draw_score_board(None, None, difficulty[4])
        elif game_state == "start":
            if move_fire != "flown":
                if random_rooms == False:
                    room_obj_list = room_list(difficulty[0], difficulty[1])
                    score = 100
                    random_rooms = True
                
                result = draw_game(empty_room, room_obj_list, arrows, move_fire, txt_rectangel, side_rectangel_l, rooms_traveld)
                new_room = find_cur_room(room_obj_list)

                if result in ["sacrificed", "falling", "eaten"]:
                    lose_condition = result
                    game_state = "loss"
                if result == "flown":
                    move_fire = "flown"
            if move_fire == "flown":
                print_flown(txt_rectangel, side_rectangel_l, game_state, move_fire)
        elif game_state in ["victory", "victory_2"]:
            random_rooms = False
            arrows = difficulty[2]
            draw_victory(txt_rectangel, score, name, game_state)
        elif game_state == "loss":
            random_rooms = False
            arrows = difficulty[2]
            draw_loss(lose_condition, side_rectangel_l, txt_rectangel)


main()