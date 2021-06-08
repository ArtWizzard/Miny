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
        self.field = []
        self.field_init()
    
    # Generating random field
    def field_init(self):
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
    
    # Draws field into the console
    def draw_field(self, ending):
        for y in range(y_cell_number):
            for x in range(x_cell_number):
                print(self.field[x][y], end=" ")
                # if ending or ("." in self.field[x][y]):
                #     print(self.field[x][y][:1], end=" ")
                # else:
                #     print("?", end=" ")
            print()
    
    # HMI
    def write_field(self, x, y):
        if mouse_presses[0]:
            if self.field[x][y] == "0":
                # showing empty field - i hit nothing
                self.near(x,y)
            elif self.field[x][y] == "m":
                # game over - I hit mine
                main.game_over()
            else:
                # I hit number (next to the mine)
                if not "." in self.field[x][y] and not "?" in self.field[x][y]:
                    self.field[x][y] += "."
        elif mouse_presses[2]:
            if not "." in self.field[x][y]:
                if "?" in self.field[x][y]:
                    self.field[x][y] = self.field[x][y].replace("?", "") # change box from "maybe mine" to unclicked
                    print("Bargr")
                else:
                    self.field[x][y] += "?"
        self.draw_field(True) # test drawing - shows what's in the battle field
                
    

        
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
                            
class MAIN():
    def __init__(self):
        self.clicked_box = pygame.image.load("Graphics/clicked_box.png").convert_alpha()
        self.unclicked_box = pygame.image.load("Graphics/unclicked_box.png").convert_alpha()
        self.mine_box = pygame.image.load("Graphics/mine_box.png").convert_alpha()
        self.number_color = {"1":(0, 0, 200),
                             "2":(0, 130, 0),
                             "3":(255, 60, 0),
                             "4":(190, 0, 10),
                             "5":(170, 0, 20),
                             "6":(130, 0, 50),
                             "7":(80, 0, 30),
                             "8":(30, 0, 30)}
          
    def game_over(self):
        # # Potřebuju vykreslit celé pole i s minama, když skončím
        # self.draw_field()
        # self.draw_elements(True)
        # pygame.display.update()
        
        # screen.fill((204, 204, 204))
        # self.draw_elements()
        # pygame.display.update()
        
        pygame.quit()
        sys.exit()
        
        
    def draw_elements(self):
        self.draw_field()
        self.draw_numbers()
        
    def draw_field(self):
        # grass_color = (167,209,61)
        for row in range(y_cell_number):
            for col in range(x_cell_number):
                x_pos = int(col * cell_size)
                y_pos = int(row * cell_size)
                box_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)
                
                if "." in field.field[col][row]:
                    screen.blit(self.clicked_box, box_rect)
                elif "?" in field.field[col][row]:
                    screen.blit(self.mine_box, box_rect)
                else:
                    screen.blit(self.unclicked_box, box_rect)
                
                # grass_rect = pygame.Rect(col*cell_size, row*cell_size, cell_size, cell_size)  # (x, y, w, h)
                # pygame.draw.rect(screen, grass_color, grass_rect)
                
    def draw_numbers(self):
        # score_text = "0"
        # number_color = mode[0]
        for row in range(y_cell_number):
            for col in range(x_cell_number):
                if "." in field.field[col][row]:
                    # change_number_color = 0
                    if "0" in field.field[col][row]:
                        number_text = ""
                    else:   
                        number_text = field.field[col][row][:1]
                        # if 49 <= ord(number_text) <= 57:
                            # change_number_color = 30*int(i)     
                    
                    # number_surface = game_font.render(number_text, True, (255, 255-change_number_color, 255-change_number_color))   # (text, aa, color)
                    number_surface = game_font.render(number_text, True, self.number_color.get(number_text, (0, 0, 0)))   # (text, aa, color)
                    number_x = int(cell_size * col + cell_size/2)
                    number_y = int(cell_size * row + cell_size/2)
                    number_rect = number_surface.get_rect(center = (number_x, number_y))
                    
                    screen.blit(number_surface, number_rect)        # (score_surface, position)
                
    # function for detection any reamaining save places - win
    def win(self):
        # print(self.field)
        remaining_places = 0
        for row in field.field:
            for item in row:
                if not "." in item and not "m" in item:
                    remaining_places += +1
            #     print(item, end = " ")
            # print()
        if remaining_places == 0:
            # field.draw_field(True) # True - show all
            print("You're a winner!")
            self.game_over()
            
        # field.draw_field(True)  # kontrola vykreslení - co se stane po kliknutí na políčko
        
# ----------------------------------------------------------------------------- Functions
def mouse_click():
    coordinates = pygame.mouse.get_pos()
    for x in range(x_cell_number):
        if coordinates[0] <= x * cell_size + cell_size:
            mouse_pos_x = x
            break
            
    for y in range(y_cell_number):
        if coordinates[1] <= y * cell_size + cell_size:
            mouse_pos_y = y
            break

    field.write_field(mouse_pos_x, mouse_pos_y)
    main.win()
    
# ----------------------------------------------------------------------------- Inicialization
pygame.init()
pygame.display.set_caption("Miny")

x_cell_number = 10
y_cell_number = 10
cell_size = 50

black_and_white = [0, 20, 70, 255]
mode = []
for color in black_and_white:
    mode.append((color, color, color))

game_font = pygame.font.Font('Fonts/Retro Gaming.ttf', 25)
screen = pygame.display.set_mode((x_cell_number * cell_size, y_cell_number * cell_size))
clock = pygame.time.Clock()

field = FIELD()
main = MAIN()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

# ----------------------------------------------------------------------------- Main - inifinity loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            main.game_over()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0] or mouse_presses[2]:    
                mouse_click()
                
                # # 0 ... left, 1 ... middle, 2 ... right
                # # print("Left Mouse key was clicked")   # vykreslení eventu myši
                # # print(pygame.mouse.get_pos())
                # coordinates = pygame.mouse.get_pos()
                # for x in range(x_cell_number):
                #     if coordinates[0] <= x * cell_size + cell_size:
                #         mouse_pos_x = x
                #         break
                        
                # for y in range(y_cell_number):
                #     if coordinates[1] <= y * cell_size + cell_size:
                #         mouse_pos_y = y
                #         break
                # field.write_field(mouse_pos_x, mouse_pos_y)
                # # print(mouse_pos_x, mouse_pos_y)
                # # if not field.write_field(mouse_pos_x, mouse_pos_y):
                # #     print("Game over")
                # #     break
                # main.win()
                #     # field.draw_field(True) # True - show all
                #     # print("You're a winner!")
                #     # main.game_over()
                #     # break
    
    screen.fill(mode[2])
    main.draw_elements()
    pygame.display.update()
    clock.tick(60)