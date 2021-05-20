# -*- coding: utf-8 -*-
"""
Created on Thu May 20 08:47:02 2021
Python 3.8
@author: samot
"""

# import random, pygame

class POLE():
    def __init__(self):
        self.cell_number = 10
        self.pole = []
        self.pole_init()

    
    def pole_init(self):
        temp = []
        for i in range(self.cell_number):
            temp.append(0)
        for i in range(self.cell_number):
            self.pole.append(temp)
    
    def draw_pole(self):
        print(self.pole)

class HPI():
    def console_input_coordinates(self, souradnice):
        try:
            return_souradnice = int(input("Zadej "+str(souradnice)+"-ovou souřadnici: "))
            return return_souradnice
        except:
            print("Chybný formát souřadnic, souřadnice je celé číslo od 0 po "+str(pole.cell_number-1))


pole = POLE()
hpi = HPI()

while True:
    pole.draw_pole()
    
    hpi.console_input_coordinates("x")