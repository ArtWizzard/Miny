# -*- coding: utf-8 -*-
"""
Created on Thu May 20 08:47:02 2021
Python 3.8
@author: samot
"""

import random, pygame, sys
# ----------------------------------------------------------------------------- Classes
class FIELD():
    def __init__(self):
        self.field_init()
    
    # Generating random field
    def field_init(self):
        self.field = []
        for row in range(y_cell_number):
            temp = []
            for col in range(x_cell_number):
                temp.append("0")
            self.field.append(temp)         # hidden field with mine
        self.mine_field_init()
        self.numbers_of_danger()
       
    # Adds all mine to the self.pole
    def mine_field_init(self):
        mine_number = (x_cell_number + y_cell_number) // 2 # vydělíme dvěma pro rychlejší hru
        # mine_number = 1 # testing winning function - fast win
        
        # Draw defined number of mine
        while mine_number: 
            # random position mine
            x = random.randint(0, x_cell_number-1)
            y = random.randint(0, y_cell_number-1)
            # find out if this position is free
            if self.field[y][x] == "0":
                mine_number -= 1
                self.field[y][x] = "m"
    
    # Rewrite every "0" (spot) in self.pole to number of near mines
    def numbers_of_danger(self):
        for y in range(y_cell_number):
            for x in range(x_cell_number):
                if self.field[x][y] == "0": # for every 0 in field
                    # rewrite to number
                    self.field[x][y] = str(self.near_mine(x, y))
             
    # Return number of mine near the spot
    def near_mine(self, x, y):
        number = 0
        for y1 in range(-1, 2):
            for x1 in range(-1, 2):
                if 0 <= x + x1 < x_cell_number and 0 <= y + y1 < y_cell_number:
                    if self.field[x+x1][y+y1] == "m":
                        number += 1
        return number
    
    # HMI
    def write_field(self, x, y):
        if mouse_presses[0]:
            if self.field[x][y] == "0":
                # showing empty field - i hit nothing
                self.near(x,y)
            elif self.field[x][y] == "m":
                # change sun's look
                main.menu.actual_sun = main.menu.sad_sun
                
                # set game over
                main.game_over = True
            else:
                # I hit number (next to the mine)
                if not "." in self.field[x][y] and not "?" in self.field[x][y]:
                    self.field[x][y] += "."
        elif mouse_presses[2]:
            if not "." in self.field[x][y]:
                if "?" in self.field[x][y]:
                    self.field[x][y] = self.field[x][y].replace("?", "") # change box from "maybe mine" to unclicked
                    # print("Bagr")
                else:
                    self.field[x][y] += "?"
        # self.draw_field() # test drawing - shows what's in the battle field
        
    def click_in_field(self):
        coordinates = pygame.mouse.get_pos()
        if coordinates[1] >= 2 * cell_size:
            for x in range(x_cell_number):
                if coordinates[0] <= x * cell_size + cell_size:
                    mouse_pos_x = x
                    break
            
            for y in range(y_cell_number + menu_height):
                if coordinates[1] <= y * cell_size + cell_size + menu_height:
                    mouse_pos_y = y
                    break
                
            
            self.write_field(mouse_pos_x, mouse_pos_y)
            main.win()

    # "infinity" loop for showing empty field
    def near(self, x, y):
        self.field[x][y] += "."
        for y1 in range(-1, 2):
            for x1 in range(-1, 2):
                if 0 <= x + x1 < x_cell_number and 0 <= y + y1 < y_cell_number:
                    if not "?" in self.field[x+x1][y+y1]:
                        if self.field[x+x1][y+y1] == "0":
                            self.near(x+x1, y+y1)
                        else:
                            if not "." in self.field[x+x1][y+y1]:
                                self.field[x+x1][y+y1] += "."
    
    # # Draws field into the console
    # def draw_field(self):
    #     for y in range(y_cell_number):
    #         for x in range(x_cell_number):
    #             print(self.field[x][y], end=" ")
    #         print()
            
class MENU():
    def __init__(self):
        self.sad_sun = pygame.image.load("Graphics/sad_sun.png").convert_alpha()    # pictures
        self.happy_sun = pygame.image.load("Graphics/happy_sun.png").convert_alpha()
        self.surprised_sun = pygame.image.load("Graphics/surprised_sun.png").convert_alpha()
        self.sun_box = pygame.image.load("Graphics/sun_box.png").convert_alpha()
        self.like_a_boss_sun = pygame.image.load("Graphics/like_a_boss_sun.png").convert_alpha()
        
        self.actual_sun = self.happy_sun
        
        self.x_pos = ((x_cell_number * cell_size) - cell_size ) // 2    # position of sun - center of menu
        self.y_pos = cell_size // 2
        
    
    def draw_menu(self):
        # Draw background
        background_color = dark_mode[3]
        background_size_x = cell_size * x_cell_number
        background_size_y = menu_height
        background_rect = pygame.Rect(0, 0, background_size_x, background_size_y)
        pygame.draw.rect(screen,background_color, background_rect)
        
        sun_rect = pygame.Rect(self.x_pos, self.y_pos, cell_size, cell_size)
        screen.blit(self.sun_box, sun_rect)
        screen.blit(self.actual_sun, sun_rect)
        
    def click_in_menu(self):
        coordinates = pygame.mouse.get_pos()
        if self.x_pos <= coordinates[0] <= self.x_pos + cell_size and self.y_pos <= coordinates[1] <= self.y_pos + cell_size:  
            # change sun's look
            self.actual_sun = self.surprised_sun
            
            # function to reset field
            main.field.field_init()
            
            # reset game
            main.game_over = False
                            
class MAIN():
    def __init__(self):
        self.field = FIELD()
        self.menu = MENU()
        self.clicked_box = pygame.image.load("Graphics/clicked_box.png").convert_alpha()
        self.unclicked_box = pygame.image.load("Graphics/unclicked_box.png").convert_alpha()
        self.mine_box = pygame.image.load("Graphics/mine_box.png").convert_alpha()
        self.mine = pygame.image.load("Graphics/mine.png").convert_alpha()
        self.number_color = {"1":(0, 0, 200),   # switch to paint numbers
                             "2":(0, 130, 0),
                             "3":(255, 60, 0),
                             "4":(190, 0, 10),
                             "5":(170, 0, 20),
                             "6":(130, 0, 50),
                             "7":(80, 0, 30),
                             "8":(30, 0, 30)}
        self.game_over = False
          
    def game_quit(self):
        pygame.quit()
        sys.exit()
        
        
    def draw_elements(self):
        self.draw_field()
        self.draw_numbers()
        if self.game_over:
            self.draw_mine()
        self.menu.draw_menu()
        
    def draw_field(self):
        # grass_color = (167,209,61)
        for row in range(y_cell_number):
            for col in range(x_cell_number):
                x_pos = int(col * cell_size)
                y_pos = int(row * cell_size + menu_height)
                box_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                
                if "." in self.field.field[col][row] or ("m" in self.field.field[col][row] and self.game_over):
                    screen.blit(self.clicked_box, box_rect)
                elif "?" in self.field.field[col][row]:
                    screen.blit(self.mine_box, box_rect)
                else:
                    screen.blit(self.unclicked_box, box_rect)
                
                # grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)  # (x, y, w, h)
                # pygame.draw.rect(screen, grass_color, grass_rect)
                
    def draw_numbers(self):
        # score_text = "0"
        # number_color = dark_mode[0]
        for row in range(y_cell_number):
            for col in range(x_cell_number):
                if "." in self.field.field[col][row]:
                    # change_number_color = 0
                    if "0" in self.field.field[col][row]:
                        number_text = ""
                    else:   
                        number_text = self.field.field[col][row][:1]
                        # if 49 <= ord(number_text) <= 57:
                            # change_number_color = 30*int(i)     
                    
                    # number_surface = game_font.render(number_text, True, (255, 255-change_number_color, 255-change_number_color))   # (text, aa, color)
                    number_surface = game_font.render(number_text, True, self.number_color.get(number_text, (0, 0, 0)))   # (text, aa, color)
                    number_x = int(cell_size * col + cell_size/2)
                    number_y = int(cell_size * row + cell_size/2 + menu_height)
                    number_rect = number_surface.get_rect(center = (number_x, number_y))
                    
                    screen.blit(number_surface, number_rect)        # (score_surface, position)
            
    def draw_mine(self):
        for row in range(y_cell_number):
            for col in range(x_cell_number):
                # draw mine
                if "m" in self.field.field[col][row]:
                    x_pos = int(col * cell_size)
                    y_pos = int(row * cell_size + menu_height)
                    box_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                    screen.blit(self.mine, box_rect)
                
    # function for detection any reamaining save places - win
    def win(self):
        # print(self.field)
        remaining_places = 0
        for row in self.field.field:
            for item in row:
                if not "." in item and not "m" in item:
                    remaining_places += +1
            #     print(item, end = " ")
            # print()
        if remaining_places == 0:
            #print("You're a winner!")  # in console write win if win
            # set sun's look
            self.menu.actual_sun = self.menu.like_a_boss_sun
            
            # set variable game_over to True - end
            self.game_over = True
        
    def mouse_click(self):
        # print(self.game_over)
        if not self.game_over: # block clicking in file while game over
            self.field.click_in_field()
        self.menu.click_in_menu()

# ----------------------------------------------------------------------------- Inicialization
pygame.init()
pygame.display.set_caption("Miny")

x_cell_number = 10
y_cell_number = 10
cell_size = 50
menu_height = 100
# sun_is_pressed = False

black_and_white = [0, 20, 70, 150, 255]
dark_mode = []
for color in black_and_white:
    dark_mode.append((color, color, color))

game_font = pygame.font.Font('Fonts/Retro Gaming.ttf', 25)
screen = pygame.display.set_mode((x_cell_number * cell_size, y_cell_number * cell_size + menu_height))
clock = pygame.time.Clock()

main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# ----------------------------------------------------------------------------- Main - inifinity loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main.game_quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            # 0 ... left, 1 ... middle, 2 ... right
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0] or mouse_presses[2]:   
                main.mouse_click()
                
            # mouse_presses = pygame.mouse.get_pressed()
            # if mouse_presses[0]:
                 
        if event.type == pygame.MOUSEBUTTONUP:
            # restart click on the sun - if it was
            if main.menu.actual_sun == main.menu.surprised_sun:
                main.menu.actual_sun = main.menu.happy_sun  
                
    screen.fill(dark_mode[2])
    main.draw_elements()
    pygame.display.update()
    clock.tick(60)