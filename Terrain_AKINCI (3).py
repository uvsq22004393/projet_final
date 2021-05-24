#########################################
# groupe 2 MPCI 7
# SÉLIN AKINCI
# JORDAN LUDIONGO
# HICHAM EL ALLALI
# MATHIS PAVIOT
# MAXIME ORLHAC
# CHAHINEZE ZTOTI
# https://github.com/uvsq22004393/projet_final
#########################################

import tkinter as tk
import random

##################
# Variable

#--Float--------------------------------------------------------------------------
p = 0.5 #Defini la probabilité p par defaut

#--Int----------------------------------------------------------------------------
LARGEUR = 700 #Defini la LARGEUR du canvas
HAUTEUR =  700 #Defini la HAUTEUR du canvas
case = 50 #Defini le nombre de case de base a 50
LARG_CASE = LARGEUR//case #Defini la Largeur des cases en fct du nbr de case
HAUT_CASE = HAUTEUR//case #Defini la hauteur des cases en fct du nbr de case
n = 4 #Defini le nombre de fois que l'automate va etre utilisé par defaut
T = 5 #Defini le nombre de voisin d'eau qu'il faut pour etre converti par defaut
k = 1 #Defini le nombre de voisin de Moore de d'ordre k par defaut
perso = 1 #indique si le personnage est sur le terrain ou non
pion = 0 #tag du personnage

#--List---------------------------------------------------------------------------
terrain = [] #Grandeur du terrain en case*case
listeau = [] #liste des voisin d'eau
deppion = [] #liste des deplacement du pion
terchar = [] #liste de la sauvegarde du terrain

###################
# Fonctions


#---Widget---#--------------------------------------------------------------------------------------------------------------------

def creation_button():
    global proba, auto, voisin, Moore, casehaut
    #Label information-------------------------------------------------------------------------------
    information = tk.Label(menu, relief = "ridge", text="Si les valeurs ne sont pas changer, valeur par defaut", width = 35,  height = 2)
    information.grid(row=0, columnspan=3)
    #Bouton generation-------------------------------------------------------------------------------
    gene = tk.Button(menu, text="Generer", width = 35,  height = 2, command = generate)
    gene.grid(row=1, columnspan=3)
    #Reglage et label probabilité p------------------------------------------------------------------
    plabel = tk.Label(menu, text= "(defaut: 0.5) p = ")
    proba = tk.Spinbox(menu,from_ = 0.1, to = 0.9, increment= 0.1, wrap = True, command = change_p)
    plabel.grid(row=2, column=0)
    proba.grid(row=2, column = 1, columnspan=2)
    #Reglage et label automate n---------------------------------------------------------------------
    nlabel = tk.Label(menu, text= "(defaut: 4) n = ")
    auto = tk.Spinbox(menu,from_ = 1, to = 10, increment= 1, command = change_n)
    nlabel.grid(row=3, column=0)
    auto.grid(row=3, column = 1, columnspan=2)
    #Reglage et label du nombre de voisin d'eau T----------------------------------------------------
    Tlabel = tk.Label(menu, text= "(defaut: 5) T = ")
    voisin = tk.Spinbox(menu,from_ = 1, to = 50, increment= 1, command = change_T)
    Tlabel.grid(row=4, column=0)
    voisin.grid(row=4, column = 1, columnspan=2)
    #Reglage et label du nombre de voisin de Moore k-------------------------------------------------
    klabel = tk.Label(menu, text= "(defaut: 1) k = ")
    Moore = tk.Spinbox(menu,from_ = 1, to = 5, increment= 1, command = change_k)
    klabel.grid(row=5, column=0)
    Moore.grid(row=5, column = 1, columnspan=2)
    #Reglage et label du nombre de case du terrain---------------------------------------------------
    caseh = tk.Label(menu, text= "(defaut: 50) case = ")
    casehaut = tk.Spinbox(menu,from_ = 10, to = 100, increment= 10, command = change_ch)
    caseh.grid(row=6, column=0)
    casehaut.grid(row=6, column = 1, columnspan=2)
    #Boutton charger pour charger une sauvegarde-----------------------------------------------------
    charger = tk.Button(menu, text="Charger", width=13, height=2, command = chargement)
    charger.grid(row=7, column=0)
    #Bouton Sauvegarder pour sauvegarder le jeu------------------------------------------------------
    save = tk.Button(menu, text="Sauvegarder", width=11, height=2, command = sauvegarde)
    save.grid(row=7, column=1)
    #Bouton Undo pour revenir a la derniere position du personnage-----------------------------------
    undob = tk.Button(menu, text="Undo", width=11, height=2, command = undo)
    undob.grid(row=7, column=2)
    
def change_p():
    global p 
    p = float(proba.get())

def change_n():
    global n
    n = int(auto.get())

def change_T():
    global T
    T = int(voisin.get())

def change_k():
    global k
    
    k = int(Moore.get())

def change_ch():
    global case
    case = int(casehaut.get())

#---Creation du terrain---#-------------------------------------------------------------------------------------------------------

def ter():
    global terrain, LARG_CASE, HAUT_CASE, HAUTEUR, LARGEUR
    LARG_CASE = LARGEUR//case #Defini la Largeur des cases
    HAUT_CASE = HAUTEUR//case #Defini la hauteur des cases
    if len(terrain) != 0:
        """detruit le terrain si il existe deja"""
        del terrain[:]
        canvas.delete("all")
    terrain = [case*[0] for i in range(case)]

def generate():
    global perso, pion
    ter() #crée l'espace de terrain vide
    init_grille(p) #Remplie l'espace de terrain
    automate(n, k) #Automatise l'espace de terrain
    canvas.delete(pion) #Supprime le personnage
    del deppion[:] #Supprime l'historique de deplacement du personnage
    perso = 1 #Indique que le personnage n'est plus sur le terrain

def init_grille(p):
    """Initie les cases a leur type et les affiches sur la grille"""
    for j in range (case):
        for i in range (case):
            a = random.random() #affecte a a un float compris entre 0 et 1
            """Definie la probabilité que la case soit de l'eau ou de la terre"""
            if a <= p:
                terrain[i][j] = 0 #affecte la case a 0 qui sera l'eau
                canvas.create_rectangle((i*LARG_CASE)+1, (j*HAUT_CASE)+1, ((i+1)*LARG_CASE)-1, ((j+1)*HAUT_CASE)-1, fill='blue')
                #Creation de la case bleu pour l'eau
            else :
                terrain[i][j] = 1 #affecte la case a 1 qui sera la terre
                canvas.create_rectangle((i*LARG_CASE)+1, (j*HAUT_CASE)+1, ((i+1)*LARG_CASE)-1, ((j+1)*HAUT_CASE)-1, fill='green')
                #Creation de la case verte pour la terre
     
def automate(n, k):
    """Lance le nombre n de fois le convertisseur de case"""
    for a in range (n):
        listeau 
        for j in range (case):
            for i in range (case):
                convert(i, j, k) #Lance la fonction convert() avec pour parametre i et j
        x = 0 #Compteur "x" pour savoir ou on se trouve dans la liste "listeau"
        for j in range (case):
            for i in range (case):
                if listeau[x] == 0 :
                    terrain[i][j] = 0 #affecte la case a 0 qui sera l'eau
                    canvas.create_rectangle((i*LARG_CASE)+1, (j*HAUT_CASE)+1, ((i+1)*LARG_CASE)-1, ((j+1)*HAUT_CASE)-1, fill='blue')
                    #Creation de la case bleu pour l'eau
                else :
                    terrain[i][j] = 1 #affecte la case a 1 qui sera la terre
                    canvas.create_rectangle((i*LARG_CASE)+1, (j*HAUT_CASE)+1, ((i+1)*LARG_CASE)-1, ((j+1)*HAUT_CASE)-1, fill='green')
                    #Creation de la case verte pour la terre
                x += 1
        del listeau[:] #Supprime la liste des cases apres leurs avoir attribuer leurs valeurs

def convert(x, y, k):
    """Converti la case en eau ou en terre par rapport a ses voisin en fonction de k"""
    eau = 0 #Creation du compteur de voisin d'eau de Moore d'ordre k
    xb, xh = x - k, x + k #affectation des valeurs xbas et xhaut qui seront les valeurs minimum et maximum de x
    yb, yh = y - k, y + k #affectation des valeurs ybas et yhaut qui seront les valeurs minimum et maximum de y

    """si la valeur minimum de x est inferieur a 0 la retablir a 0"""
    if xb < 0:
        xb = 0
    """si la valeur minimum de y est inferieur a 0 la retablir a 0"""
    if yb < 0:
        yb = 0
    """si la valeur maximum de x est superieur a case la retablir a case"""
    if xh > case:
        xh = case
    """si la valeur maximum de y est superieur a case la retablir a case"""
    if yh > case:
        yh = case

    for j in range (yb-1, yh, 1):
        for i in range (xb-1, xh, 1):
            if i != x or j != y:
                if terrain[i][j] == 0:
                    eau += 1 #Compteur 
    if eau >= T :
        listeau.append(0) #Si le nombre de voisin d'eau est superieur a T, listeau apprend 0 (case eau)
    else :
        listeau.append(1) #Si le nombre de voisin d'eau est inferieur a T, listeau apprend 1 (case terre)

#---Personnage---#---------------------------------------------------------------------------------------------------------------------

def personnage(event):
    global perso
    """Si le personnage n'est pas crée"""
    if perso :
        create_personnage(event.x, event.y) #Cree un personnage sur la case cliquer
    else :
        efface_personnage(event.x, event.y) #Efface le personnage crée
    
def create_personnage(x, y):
    global pion, perso
    i, j = x//LARG_CASE, y//HAUT_CASE
    if terrain[i][j] == 1:
        """Regle le rayon du personnage en fonction du plus petit coté"""
        if LARG_CASE <= HAUT_CASE:
            rayon = LARG_CASE // 4 #Defini le rayon du personnage en fonction de la largeur
        else:
            rayon = HAUT_CASE // 4 #Defini le rayon du personnage en fonction de la hauteur
        terrain[i][j] = 2 #La case du terrain prend la valeur "personnage" (2)
        x, y = LARG_CASE//2 + i*LARG_CASE, HAUT_CASE//2 + j*HAUT_CASE #x et y prenne la valeur au milieu de la case
        deppion.append((i, j)) #Deplacement de pion prend la premiere valeur du personnage
        pion = canvas.create_oval((x-rayon, y-rayon),
                                    (x+rayon, y+rayon),
                                    fill="black") #Creation d'un cercle noir au milieu de la case qui representera la personnage
        perso = 1 - perso #Le personnage est crée

def efface_personnage(x, y):
    """Efface le personnage de la map"""
    global pion, perso
    i, j = x//LARG_CASE, y//HAUT_CASE
    if terrain[i][j] == 2: #si le clique est effectuer sur le personnage
        terrain[i][j] = 1 #Le terrain prend la valeur de la "terre" (1)
        canvas.delete(pion) #Efface le cercle du personnage
        del deppion[:] #Supprime l'historique du deplacement du personnage
        perso = 1 - perso #Le perso est effacer

            
def move(event):
    key = event.keysym #key est egale a la touche appuyer sur le clavier
    if not perso : #Si le personnage est crée
        if key == "Up": #Si la touche fleche haut est presser
            if deppion[len(deppion)-1][1] != 0 : #Si le personnage n'est pas sur la bordure haute
                if terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]-1] == 1: #Si la case au dessus est de la terre
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 1 #La valeur du terrain de l'ancienne position est egale a de la terre (1)
                    deppion.append((deppion[len(deppion)-1][0], deppion[len(deppion)-1][1]-1)) #L'historique de deplacement apprend la nouvelle position
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 2 #La valeur du terrain de la nouvelle position est egale au personnage (2)
                    canvas.move(pion, 0, -HAUT_CASE) #Bouge le personnage d'une case vers le haut

        elif key == "Down": #Si la touche fleche bas est presser
            if deppion[len(deppion)-1][1] != case : #Si le personnage n'est pas sur la bordure basse
                if terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]+1] == 1: #Si la case en dessous est de la terre
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 1 #La valeur du terrain de l'ancienne position est egale a de la terre (1)
                    deppion.append((deppion[len(deppion)-1][0], deppion[len(deppion)-1][1]+1)) #L'historique de deplacement apprend la nouvelle position
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 2 #La valeur du terrain de la nouvelle position est egale au personnage (2)
                    canvas.move(pion, 0 , HAUT_CASE) #Bouge le personnage d'une case vers le bas

        elif key == "Left": #Si la touche fleche gauche est presser
            if deppion[len(deppion)-1][0] != 0 : #Si le personnage n'est pas sur la bordure gauche
                if terrain[deppion[len(deppion)-1][0]-1][deppion[len(deppion)-1][1]] == 1: #Si la case a gauche est de la terre
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 1 #La valeur du terrain de l'ancienne position est egale a de la terre (1)
                    deppion.append((deppion[len(deppion)-1][0]-1, deppion[len(deppion)-1][1])) #L'historique de deplacement apprend la nouvelle position
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 2 #La valeur du terrain de la nouvelle position est egale au personnage (2)
                    canvas.move(pion, -LARG_CASE, 0) #Bouge le personnage d'une case vers la gauche

        elif key == "Right": #Si la touche fleche droite est presser
            if deppion[len(deppion)-1][1] != case : #Si le personnage n'est pas sur la bordure droite
                if terrain[deppion[len(deppion)-1][0]+1][deppion[len(deppion)-1][1]] == 1: #si la case a droite est de la terre
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 1 #La valeur du terrain de l'ancienne position est egale a de la terre (1)
                    deppion.append((deppion[len(deppion)-1][0]+1, deppion[len(deppion)-1][1])) #L'historique de deplacement apprend la nouvelle position
                    terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 2 #La valeur du terrain de la nouvelle position est egale au personnage (2)
                    canvas.move(pion, LARG_CASE, 0) #Bouge le personnage d'une case vers la droite

        elif key == "BackSpace": #Si la touche retour en arriere est presser
            undo() #lance la fonction undo

        if len(deppion) > 9: #Si la longueur de l'historique de deplacement est superieur a 9
            del deppion[0] #Supprimer la premiere valeur de l'historique

    if key == "s": #Si la touche "s" est presser
        sauvegarde() #Lance la fonction sauvegarde

    elif key == "c": #Si la touche "c" est presser
        chargement() #Lance la fonction chargement

    elif key == "g": #Si la touche "g" est presser
        generate() #Lance la fonction chargement

def undo():
    if len(deppion) >= 2 : #Si la longueur de l'historique de deplacement est superieur ou egale a 2
        x = deppion[len(deppion)-2][0] - deppion[len(deppion)-1][0] #"x" prend la valeur de l'ancienne position - la nouvelle
        y = deppion[len(deppion)-2][1] - deppion[len(deppion)-1][1] #"y" prend la valeur de l'ancienne position - la nouvelle
        terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 1 #La valeur du  terrain de la nouvelle position est egale a la terre (1)
        del deppion[len(deppion)-1] #On supprime la nouvelle position
        terrain[deppion[len(deppion)-1][0]][deppion[len(deppion)-1][1]] = 2 #La valeur du terrain de l'ancienne position est egale au personnage (2)
        canvas.move(pion, x*LARG_CASE, y*HAUT_CASE) #Retourne le personnage vers l'ancienne position


#---Sauvegardes---#--------------------------------------------------------------------------------------------------------------------

def sauvegarde():
    fic = open("Save", "w") #Ouvre le fichier "Save.txt" en mode ecriture
    fic.write(str(len(deppion)) + "\n") #Ecrit sur la premiere ligne la longueur de l'historique de deplacement (puis retourne a la ligne)
    for i in range(len(deppion)): #Pour chaque deplacement
        fic.write(str(deppion[i][0]) + " " + str(deppion[i][1]) + "\n") #Ecrit les position x et y du deplacement (puis retourne a la ligne)

    fic.write(str(case) + "\n") #Ecrit le nombre de case (puis retourne a la ligne)

    for j in range(case):
        for i in range(case):
            fic.write(str(terrain[i][j]) + " ") #Ecrit la valeur de toutes les cases lignes par lignes
        fic.write("\n") #Retourne a la ligne
    
    fic.close() #Ferme le fichier "Save.txt"

def chargement():
    global perso, pion, terrain, case
    del deppion[:] #Supprime l'historique de deplacement actuelle
    canvas.delete("all") #Supprime le contenue du canvas
    fic = open("Save", "r") #Ouvre le fichier "Save.txt" en mode lecture
    length = int(fic.readline(1)) #La variable "Length" = a la valeur entiere de la prmeiere ligne (longueur de l'historique de deplacement)
    cpt = 1 #Crée un compteur a valeur initial 1
    if length: #Si 'length' a une autre valeur que 0 le personnage est deja crée
        perso = 0 #Indique que le personage est deja crée
    else :
        perso = 1 #Indique que le personnage n'est pas crée
    for x in fic: #Pour 'x' parcourant le fichier
        if cpt <= length+1 and cpt != 1: #Si le compteur est compris entre la premiere valeur de l'historique et la derniere
            deppion.append((int(x.split()[0]), int(x.split()[1]))) #La liste deplacement pion apprend les valeurs x et y pour chaque deplacement
        elif cpt == length + 2: #Si le compteur est egale a la ligne du nombre de case
            case = int(x) #Case = au nombre de case sauvegarder
            ter() #Crée l'espace de terrain vide
        elif cpt != 1 and cpt > length + 2: #Si le compteur est egale aux lignes des valeurs du terrain
            terchar.append((x.split())) #La liste TerChar apprend chaque ligne
        cpt += 1

    
    for j in range(case):
        for i in range(case):
            terrain[i][j] = int(terchar[j][i]) #La liste terrain apprend la valeur entiere de la liste terchar (soit 0 [Eau], 1 [Terre] ou 2 [Personnage] si elle existe)
            if terrain[i][j] == 0: #Si le terrain est egale a eau
                canvas.create_rectangle((i*LARG_CASE)+1, (j*HAUT_CASE)+1, ((i+1)*LARG_CASE)-1, ((j+1)*HAUT_CASE)-1, fill='blue') #Cree une parcelle d'eau
            else :
                canvas.create_rectangle((i*LARG_CASE)+1, (j*HAUT_CASE)+1, ((i+1)*LARG_CASE)-1, ((j+1)*HAUT_CASE)-1, fill='green') #Cree une parcelle de terre
    for j in range(case):
        for i in range(case):
            if terrain[i][j] == 2: #Si le terrain est egale au personnage
                if LARG_CASE <= HAUT_CASE:
                    rayon = LARG_CASE // 4 #Defini le rayon du personnage en fonction de la largeur
                else:
                    rayon = HAUT_CASE // 4 #Defini le rayon du personnage en fonction de la hauteur
                x, y = LARG_CASE//2 + i*LARG_CASE, HAUT_CASE//2 + j*HAUT_CASE #x et y prenne la valeur au milieu de la case
                pion = canvas.create_oval((x-rayon, y-rayon),
                                            (x+rayon, y+rayon),
                                            fill="black") #Creation d'un cercle noir au milieu de la case qui representera la personnage
    fic.close() #Ferme le fichier "Save.txt"

######################
# Programme Principal

#---------------------Fenetre------------------------#
racine = tk.Tk()

#----------------------Widget------------------------#

#---Canvas---#
canvas = tk.Canvas(racine, bg="white", width=LARGEUR, height=HAUTEUR)
canvas.grid(row=0, column=1)
#----Menu----#
menu = tk.Canvas(racine, bg="white", width=LARGEUR, height=HAUTEUR)
menu.grid(row=0, column=0)
#--Fonction--#
creation_button()

#-------------------Personnage-----------------------#

#--Fonction--#
canvas.bind("<Button-1>", personnage)
canvas.bind_all("<KeyPress>", move)


racine.mainloop()