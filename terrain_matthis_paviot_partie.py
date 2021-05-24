####################

# PROJET GENERATION DE TERRRAIN

# MPCI TD 07

# AKINCI Seline
# PAVIOT Mathis
# ORLHAC Maxime
# LUDIONGO Jordan
# ZTOTI Chahineze
# EL ALLALI Hicham

# https://github.com/uvsq21802998/Projet-de-generation-d-un-terrain-de-jeu-video.git

####################

# Import des librairies

import tkinter as tk
import random as rd
from tkinter import *
from tkinter import ttk

####################

# CONSTANTES

HEIGHT = 1000
WIDTH = 1000
COTE = 20
COUL_GRILLE = "grey"
COUL_EAU = "cornflower blue"
COUL_TERRE = "DarkOrange3"
COUL_CHARACTER = "Black"
N = 4
T = 5
k = 1
carre = 0

####################

# Fonctions du Programme

def create_lists():
    """ genere des tableaux de la taille du canvas """
    l = list(range(WIDTH // COTE))
    for i in l:
        l[i] = list(range(WIDTH // COTE))
        for j in range(WIDTH // COTE):
            l[i][j] = 0
    return l

def grille():
    """ Dessine le grillage GRIS """
    x, y = 0, 0

    while y <= HEIGHT:
        canvas.create_line((0, y), (WIDTH, y), fill = COUL_GRILLE)
        y += COTE

    while x <= WIDTH:
        canvas.create_line((x, 0), (x,HEIGHT), fill = COUL_GRILLE)
        x += COTE

def generate_water(x, y):
    """ transforme la case en eau si elle n'est pas deja attribuee """
    i, j = x, y 
    
    if etat_case[i][j] == 0:
        a = i * COTE
        b = j * COTE
        eau = canvas.create_rectangle((a, b), (a + COTE, b + COTE), fill = COUL_EAU, outline = COUL_EAU)
        etat_case[i][j] = 2
        #nature[i][j] = carre

def generate_land(x, y):
    """ transforme la case en terre si elle n'est pas deja attribuee """
    i, j = x, y
    print("pute")

    if etat_case[i][j] != 2:
        
        a = i * COTE
        b = j * COTE
        terre = canvas.create_rectangle((a, b), (a + COTE, b + COTE), fill = COUL_TERRE, outline = COUL_TERRE)
        etat_case[i][j] = 3
        #nature[i][j] = carre

def coord_case(x, y):
    """ donne les coord de la case du tableau selectionnee """
    #print("case de coord (", x//COTE, ",", y//COTE, ")")
    return x // COTE, y // COTE

def generate_character(x, y):
    """ transforme la case en Personnage si elle n'est pas deja attribuee """
    global char
    global carre

    position_char[0], position_char[1] = x, y
    i, j = position_char[0], position_char[1]
    
    if etat_case[i][j] != 2 and char == 0 and etat_case[i][j] != 0:
        a = i * COTE
        b = j * COTE
        carre = canvas.create_rectangle((a, b), (a + COTE, b + COTE), fill = COUL_CHARACTER, outline = COUL_CHARACTER)
        etat_case[i][j] = 3
        char = 1 # temoigne de l'existence du personnage a fin de ne pas pouvoir en placer un autre
        print(position_char[0], position_char[1])
        #nature[i][j] = carre

def get_char_click(event):
    """ place le personnage au click, et le supprime si re-click """
    a, b = coord_case(event.x, event.y)
    global char
    global carre
    #print(a, b)
    position_click[0], position_click[1] = a, b # liste temporaire

    if char == 1 and position_click[0] == position_char[0] and position_click[1] == position_char[1]:
        char = 0
        canvas.delete(carre)

    else:
        generate_character(a, b)

def detect_eau(x, y):
    """ compte le nombre de plans d'eau autour de la case """
    i, j = x, y
    n = 0

    if i >= 1:

        if j >= 1:

            if etat_case[i-1][j-1] == 2:
                n += 1

        if etat_case[i-1][j] == 2:
            n += 1
        
        if j <= len(etat_case) - 2:

            if etat_case[i-1][j+1] == 2:
                n += 1
            
    if j <= len(etat_case) - 2:
        if etat_case[i][j+1] == 2:
            n += 1

    if j >= 1:

        if etat_case[i][j-1] == 2:
            n += 1

        if i <= len(etat_case) - 2:

            if etat_case[i+1][j-1] == 2:
                n += 1
            
    if i <= len(etat_case) - 2:
        if etat_case[i+1][j] == 2:
            n += 1

    if i <= len(etat_case) - 2 and j <= len(etat_case) - 2:
        if etat_case[i+1][j+1] == 2:
            n += 1

    return n
    
def generate_full_map():
    """ Genere integralement la map """
    generate_map() # genere la map avant de lancer l'automate
    #generate_land_map() # genere les champs

def generate_map():
    """ genere l'eau avec une probabilite de 0,5, puis lance l'automate """
    i = 0

    for i in range(HEIGHT//COTE):
        for j in range(HEIGHT//COTE):

            etangs[i][j] = detect_eau(i, j)
            proba = [1] + 1 * [0]
            choix = rd.choice(proba)

            if choix == 1:
                generate_water(i, j)
            
            else:
                generate_land(i, j)
    
    automate()

def automate():
    """ repete n fois """
    k = 0

    for k in range(N):
        for i in range(HEIGHT//COTE):
            for j in range(HEIGHT//COTE):

                if etangs[i][j] >= T:

                    if etat_case[i][j] != 2:
                        generate_water(i, j)

def haut(event):
    """ recupere la touche pressee et reagit adequatement """
    i, j = position_char[0], position_char[1]
    global carre
    global char

    if j >= 1 and etat_case[i][j-1] != 2 and char == 1:
        #print(i, j-1)
        char = 0 # autorise la creation d'une nouvelle case personnage
        #print(char) 
        canvas.delete(carre)
        generate_character(i, j-1)
        
def bas(event):
    """ recupere la touche pressee et reagit adequatement """
    i, j = position_char[0], position_char[1]
    global carre
    global char

    if j <= HEIGHT and etat_case[i][j+1] != 2 and char == 1:
        #print(i, j-1)
        char = 0 # autorise la creation d'une nouvelle case personnage
        #print(char) 
        canvas.delete(carre)
        generate_character(i, j+1)

def droite(event):
    """ recupere la touche pressee et reagit adequatement """
    i, j = position_char[0], position_char[1]
    global carre
    global char

    if i <= WIDTH and etat_case[i+1][j] != 2 and char == 1:
        #print(i, j-1)
        char = 0 # autorise la creation d'une nouvelle case personnage
        #print(char) 
        canvas.delete(carre)
        generate_character(i+1, j)

def gauche(event):
    """ recupere la touche pressee et reagit adequatement """
    i, j = position_char[0], position_char[1]
    global carre
    global char

    if i >= 1 and etat_case[i-1][j] != 2 and char == 1:
        #print(i, j-1)
        char = 0 # autorise la creation d'une nouvelle case personnage
        #print(char) 
        canvas.delete(carre)
        generate_character(i-1, j)

def annuler_mouvement():
    """ bouton pour revenir d'une case """
    





####################

# Variables Globales

etat_case = create_lists() # tableau qui contient l'etat de la case (0 vide, 1 foret, 2 eau, 3 prairie, 4 feu, 5 cendret, 6 cendresn)
case_autour = create_lists() # tableau qui contient le nb de voisins en feu autour de la case
arbres = create_lists() # tableau qui contient le nb d'arbres voisins pour chaque case
etangs = create_lists() # tableau qui contient le nb d'etangs voisins pour chaque case
position_char = create_lists() # tableau qui contient les coord du personnage
position_click = create_lists() # liste temporaire pour comparer les coord du clicl
position_precedente = create_lists() # liste qui enregistre la derniere position du personnage
char = 0 # egal à 1 si personnage deja present sur une case

####################

# Programme Principal

racine = tk.Tk() # Creation de la fenetre
racine.title("TERRAIN") # Titre de la fenetre

canvas = tk.Canvas(racine, bg = "white", height = HEIGHT, width = WIDTH) # Creation du Canvas
canvas.grid()

grille() # Creation de la grille

generer_map = tk.Button(racine, text = "GENERER MAP", command = generate_full_map, font = ("helvetica", "10")) #bouton genere map
generer_map.grid(row = 0, column = 2 ) #positionnement bouton " generer map "

annuler_mouv = tk.Button(racine, text = "ANNULER MOUVEMENT", command = annuler_mouvement, font = ("helvetica", "10")) # bouton annuler mouv
annuler_mouv.grid(row = 0, column = 3)

canvas.focus_force()
canvas.bind("<1>", get_char_click)
canvas.bind("<Up>", haut) # Flèche du haut
canvas.bind("<Down>", bas) # Flèche du Bas
canvas.bind("<Left>", gauche) # Flèche de Gauche
canvas.bind("<Right>", droite) # Flèche de Droite

racine.mainloop()