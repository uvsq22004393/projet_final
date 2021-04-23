# AKINCI Seline
# PAVIOT Mathis
# ORLHAC Maxime
# LUDIONGO Jordan
# ZTOTI Chahineze
# EL ALLALI Hicham
#
#
# https://github.com/uvsq21802998/Projet-de-generation-d-un-terrain-de-jeu-video.git
#########################################
# Prochaines etapes
# placer un personnage sur une case de terre en cliquant dessus,
# puis le déplacer sur des zones de terre avec les flèches du clavier;
# il ne doit pas pouvoir se déplacer sur une case d’eau;
# le personnage doit pouvoir être retiré et replacé.
#
#
# le personnage est crée mais ne se déplace pas (!! à lire !!)
#
# Le choix des widgets et de leur placement est libre.
#########################################
import tkinter as tk
import random
##################
# Constantes
LARGEUR = 1000  # int(input("choisir la largeur de la grille : "))
# Defini la LARGEUR sur le nombre choisis par l'utilisateur
HAUTEUR = 1000  # int(input("choisir la hauteur de la grille : "))
# Defini la HAUTEUR sur le nombre choisis par l'utilisateur
Nbr_case = 50
# Defini le nombre de case
LARG_CASE = LARGEUR//Nbr_case
# Defini la Largeur des cases
HAUT_CASE = HAUTEUR//Nbr_case
# Defini la hauteur des cases
# Variables
p = 0.5  # float(input("Entrée la probabilité d'eau : "))
# Defini la probabilité p sur le nombre decimal entre 0 et 1 choisis par l'utilisateur
n = 4  # int(input("Entrée le nombre d'utilisation de l'automate : "))
# Defini le nombre de fois que l'automate va etre utilisé par l'utilisateur
T = 5  # int(input("Entrée le nombre de case d'eau voisin que la case doit avoir pour devenir de l'eau : "))
# Defini le nombre de voisin d'eau qu'il faut pour etre converti par l'utilisateur
k = 1  # int(input("Entrée le nombre de voisinage de Moore que doit avoir la case : "))
# Defini le nombre de voisin de Moore de d'ordre k par l'utilisateur
terrain = [Nbr_case*[0] for i in range(Nbr_case)]
# Defini la taille du terrain
Perso = False  # indique si le personnage est sur le terrain ou non
###################
# Fonctions


def init_grille():
    """Initie les cases a leur type et les affiches sur la grille"""
    global terrain, p, Nbr_case, LARG_CASE, HAUT_CASE  # Importe les variable globale terrain, p et Nbr_case
    """Parcour la grille"""
    for i in range(Nbr_case):
        for j in range(Nbr_case):
            a = random.random()  # affecte à a une valeur comprise entre 0 et 1
            """Definie la probabilité que la case soit de l'eau ou de la terre"""
            if a <= p:
                terrain[j][i] = (0, 0)  # affecte la case a 0 qui sera l'eau
                canvas.create_rectangle((j*LARG_CASE)+1, (i*HAUT_CASE)+1, ((j+1)*LARG_CASE)-1, ((i+1)*HAUT_CASE)-1, fill='blue')
                # Creation de la case bleu pour l'eau
            else:
                terrain[j][i] = (1, 0)  # affecte la case a 1 qui sera la terre
                canvas.create_rectangle((j*LARG_CASE)+1, (i*HAUT_CASE)+1, ((j+1)*LARG_CASE)-1, ((i+1)*HAUT_CASE)-1, fill='green')
                # Creation de la case verte pour la terre


def automate():
    """Lance le nombre n de fois le convertisseur de case"""
    global n, Nbr_case, LARG_CASE, HAUT_CASE  # Importe la variable global n et Nbr_case
    for a in range(n):
        for i in range(Nbr_case):
            for j in range(Nbr_case):
                convert(j, i)  # Lance la fonction convert() avec pour parametre i et j
        for i in range(Nbr_case):
            for j in range(Nbr_case):
                if terrain[j][i][1] >= T :
                    terrain[j][i] = (0, 0)  # affecte la case a 0 qui sera l'eau
                    canvas.create_rectangle((j*LARG_CASE)+1, (i*HAUT_CASE)+1, ((j+1)*LARG_CASE)-1, ((i+1)*HAUT_CASE)-1, fill='blue')
                    # creation d'une case bleu pour l'eau
                else:
                    terrain[j][i] = (1, 0)  # affecte la case a 1 qui sera la terre
                    canvas.create_rectangle((j*LARG_CASE)+1, (i*HAUT_CASE)+1, ((j+1)*LARG_CASE)-1, ((i+1)*HAUT_CASE)-1, fill='green')
                    # creation d'une case verte pour l'herbe


def convert(x, y):
    """Converti la case en eau ou en terre par rapport a ses voisin en fonction de k"""
    global k, terrain, T, Nbr_case  # Importe les variable globale k, terrain, T et Nbr_case
    eau = 0  # Creation du compteur de voisin d'eau de Moore d'ordre k
    xb, xh = x - k, x + k  # affectation des valeurs xbas et xhaut qui seront les valeurs minimum et maximum de x
    yb, yh = y - k, y + k  # affectation des valeurs ybas et yhaut qui seront les valeurs minimum et maximum de y
    """si la valeur minimum de x est inferieur a 0 la retablir a 0"""
    if xb < 0:
        xb = 0
    """si la valeur minimum de y est inferieur a 0 la retablir a 0"""
    if yb < 0:
        yb = 0
    """si la valeur maximum de x est superieur a Nbr_case la retablir a Nbr_case"""
    if xh > Nbr_case:
        xh = Nbr_case
    """si la valeur maximum de y est superieur a Nbr_case la retablir a Nbr_case"""
    if yh > Nbr_case:
        yh = Nbr_case
    for i in range(yb-1, yh, 1):
        for j in range(xb-1, xh, 1):
            if i != y or j != x:
                if terrain[j][i][0] == 0:
                    eau += 1  # Compteur
    if terrain[x][y][0] == 1:
        terrain[x][y] = (1, eau)
    else:
        terrain[x][y] = (0, eau)


def config_perso(event):
    """Lance toute les actions liées au personnage"""
    global Nbr_case, LARG_CASE, HAUT_CASE, Perso, personnage
    """Si le personnage n'est pas crée"""
    if Perso == False:
        personnage = create_personnage(event.x, event.y)  # Personnage prend la valeur retourné de la fonction 'create_personnage' (besoin d'un clic droit)
    else:
        efface_personnage(event.x, event.y)  # Lance la fonction 'efface_personnage' qui a besoin du clic gauche


def create_personnage(x, y):
    """Creation du personnage sur la zone cliquer"""
    global Nbr_case, LARG_CASE, HAUT_CASE, Perso
    for i in range(Nbr_case):
        for j in range(Nbr_case):
            """Condition que x et y se trouve dans la case selectionnée"""
            if j*LARG_CASE <= x and x <= (j+1)*LARG_CASE and i*HAUT_CASE <= y and y <= (i+1)*HAUT_CASE:
                """Condition que le terrain soit de la terre"""
                if terrain[j][i][0] == 1:
                    """Regle le rayon du personnage en fonction du plus petit côté"""
                    if LARG_CASE <= HAUT_CASE:
                        rayon = LARG_CASE // 4  # Defini le rayon du personnage en fonction de la largeur
                    else:
                        rayon = HAUT_CASE // 4  # Defini le rayon du personnage en fonction de la hauteur
                    x, y = LARG_CASE//2 + j*LARG_CASE, HAUT_CASE//2 + i*HAUT_CASE  # x et y prenne la valeur au milieu de la case
                    cercle = canvas.create_oval((x-rayon, y-rayon),
                                                (x+rayon, y+rayon),
                                                fill="black")  # Creation d'un cercle noir au milieu de la case qui representera la personnage
                    Perso = True  # Le personnage est crée
                    print(Perso)
                    return [cercle, j, i]  # Retourne le cercle, et la position du personnage sous forme de tableau


def efface_personnage(x, y):
    """Efface le personnage de la map"""
    global personnage, LARG_CASE, HAUT_CASE, Perso
    if personnage[1]*LARG_CASE <= x and x <= (personnage[1]+1)*LARG_CASE and personnage[2]*HAUT_CASE <= y and y <= (personnage[2]+1)*HAUT_CASE:
        canvas.delete(personnage[0])  # Efface le cercle du personnage
        Perso = False


def bouge_perso(event):
    global personnage
    print("1")
    print(event.Keysym)
    if event.Keysym == 'Up':
        canvas.delete(personnage[0])  # Efface le cercle du personnage
        personnage[1] += 1
        create_personnage(personnage[1], personnage[2])
    elif event.Keysym == 'Down':
        canvas.delete(personnage[0])  # Efface le cercle du personnage
        personnage[1] -= 1
        create_personnage(personnage[1], personnage[2])
    elif event.Keysym == 'Right':
        canvas.delete(personnage[0])  # Efface le cercle du personnage
        personnage[2] += 1
        create_personnage(personnage[1], personnage[2])
    elif event.Keysym == 'Left':
        canvas.delete(personnage[0])  # Efface le cercle du personnage
        personnage[2] -= 1
        create_personnage(personnage[1], personnage[2])


def save(terrain, Nbr_case):
    fic = open("Save", "w")  # Ouvre le fichier "Save" en mode ecriture
    for i in range(Nbr_case):
        for j in range(Nbr_case):
            fic.write(str(terrain[j][i][0]) + "\n")  # Inscrit le terrain sur le fichier ouvert
    fic.close()  # Ferme le fichier "Save"


def load(HAUT_CASE, LARG_CASE, terrain):
    fic = open("Save", "r")  # Ouvre le fichier "Save" en mode lecture
    ligne = 0  # Affecte a Ligne la valeur 0 en temps que compteur
    for i in range(Nbr_case):
        for j in range(Nbr_case):
            ligne += 1  # A chaque case la ligne est incrementée de 1
            terrain[j][i][0] = int(fic.readline(ligne))  # Le terrain est mit a la valeur de la sauvegarde
            if terrain[j][i][0] == 0:
                canvas.create_rectangle((j*LARG_CASE)+1, (i*HAUT_CASE)+1, ((j+1)*LARG_CASE)-1, ((i+1)*HAUT_CASE)-1, fill='blue')
                # creation d'une case bleu pour l'eau
            else:
                canvas.create_rectangle((j*LARG_CASE)+1, (i*HAUT_CASE)+1, ((j+1)*LARG_CASE)-1, ((i+1)*HAUT_CASE)-1, fill='green')
                # creation d'une case verte pour l'herbe
    fic.close()  # Ferme le fichier "Save"


def generer():
    racine_2 = tk.Tk()
    canvas_2 = tk.Canvas(racine_2, bg="white", width=200, height=200)
    canvas_2.grid(row=0, rowspan=10)
    racine_2.mainloop()
######################
# programme principal


racine = tk.Tk()
canvas = tk.Canvas(racine, bg="white", width=LARGEUR, height=HAUTEUR)
canvas.grid(row=1, column=0)
button_generer = tk.Button(racine, text="generer", command=generer)
button_generer.grid(row=1, column=2)
init_grille()
automate()
racine.bind("<Button-1>", config_perso)  # Rentre dans la config du personnage (besoin d'un clic droit)
# racine.unbind("<Button-1>")
if Perso:
    print("1")
    racine.bind("<KeyPress>", bouge_perso)
racine.mainloop()
