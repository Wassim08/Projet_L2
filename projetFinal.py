#_____________________IMPORT_______________________
from hillClimbing import *
from tkinter import *
from PIL import ImageTk, Image

#_____________________INITIALISATION_______________________

window = Tk()                                   #définition de la fenêtre tkinter
window.geometry("1280x720")                     #redimensionner la taille de la fenêtre
#SCALE : 7*W , 15*H (fullscreen => W=182 H=48)
window.title("Projet PIMA - Hill Climbing")     #titre de la fenêtre
window['bg'] = 'lightgray'                      #couleur de background de la fenêtre
window.resizable(height=False, width=False)     #bloquer le redimensionnement manuel de la fenêtre
#redimensionner une image (et l'initialiser)
cesar = Image.open("cesar.png")
resized = cesar.resize((500, 500), Image.ANTIALIAS)
cesar = ImageTk.PhotoImage(resized)

scytale = Image.open("scytale.png")
resized2 = scytale.resize((500, 500), Image.ANTIALIAS)
scytale = ImageTk.PhotoImage(resized2)

home = Image.open("home.png")
resized3 = home.resize((100, 100), Image.ANTIALIAS)
home = ImageTk.PhotoImage(resized3)

check = Image.open("check.png")
resized4 = check.resize((100, 100), Image.ANTIALIAS)
check = ImageTk.PhotoImage(resized4)

#_____________________VARIABLES_______________________

mainmenu = 0
titre = 0
description = 0
boutonSubstitution = 0
boutonTransposition = 0

strVariableS = StringVar()
substitution = 0
titreS = 0
consoleS = 0
alphabetS = 0
frameEntreeS = 0
labelEntreeS = 0
entreeS = 0
boutonValiderS = 0
boutonRetourS = 0

strVariableT = StringVar()
transposition = 0
titreT = 0
consoleT = 0
alphabetT = 0
frameEntreeT = 0
labelEntreeT = 0
entreeT = 0
boutonValiderT = 0
boutonRetourT = 0

#_____________________FONCTIONS_______________________

def getsize(widget):
    widget.update()
    return (widget.winfo_width(), widget.winfo_height())

def cleanWindow(window):
    for child in window.winfo_children():
        child.destroy()

def decrypteSubstitution():
    global substitution
    global strVariableS

    substitution.update()
    frameEntreeS.update()
    entreeS.update()
    message = entreeS.get()#strVariableS.get()
    cle = hill_climbing_substitution(message)
    messageDecrypte = translate(message, cle)
    consoleS["text"] = messageDecrypte
    alphabetS["text"] = "La clé de chiffrement est : " + cle
    substitution.update()

def decrypteTransposition():
    global transposition
    global strVariableT

    transposition.update()
    frameEntreeT.update()
    entreeT.update()
    message = entreeT.get()
    cle = hill_climbing_transposition_taillefixe(message)
    messageDecrypte = suppr_lettre(dechiffrement_transposition(message, cle), "&")
    consoleT["text"] = messageDecrypte
    alphabetT["text"] = "La clé de chiffrement est : " + cle
    transposition.update()

def updateMainMenu():
    global mainmenu
    global titre
    global description
    global boutonSubstitution
    global boutonTransposition

    cleanWindow(window)
    mainmenu = Frame(window, bg="lightgray")
    titre = Label(mainmenu, text="Projet PIMA - Hill Climbing", font="Times 40 italic bold", fg="gray", bg="lightgrey")
    titre.pack()

    description = Label(mainmenu, text="Veuillez sélectionner l'un des onglets ci-dessous :", font="Times 25 bold",
                        fg="gray", bg="lightgrey", pady=20)
    description.pack()

    boutonSubstitution = Button(mainmenu, image=cesar, command=updateSubstitution)
    boutonSubstitution.pack(side=LEFT, padx=55)

    boutonTransposition = Button(mainmenu, image=scytale, command=updateTransposition)
    boutonTransposition.pack(side=RIGHT, padx=55)
    mainmenu.pack(pady=25)

def updateSubstitution():
    global strVariableS
    global substitution
    global titreS
    global consoleS
    global alphabetS
    global frameEntreeS
    global labelEntreeS
    global entreeS
    global boutonValiderS
    global boutonRetourS

    cleanWindow(window)


    strVariableS = StringVar()

    substitution = Frame(window, bg="lightgrey", height=720)

    titreS = Label(substitution, text="Décryptage de chiffrement par substitution", font="Times 30 italic bold",
                  fg="gray", bg="lightgrey")
    titreS.pack()

    consoleS = Label(substitution, text="Le message déchiffré s'affichera ici-même",
                    font="Times 15 bold", fg="gray", bg="lightgrey", wraplength=1200, borderwidth=3, relief="groove",
                    width=100, height=20)
    consoleS.pack(pady=5)


    alphabetS = Label(substitution, text="L'alphabet/clé de chiffrement est : ABCDEFGHIJKLMNOPQRSTUVWXYZ",
                     font="Times 15 bold", fg="gray", bg="lightgrey", borderwidth=3, relief="groove", width=100,
                     height=1)
    alphabetS.pack()


    frameEntreeS = Frame(substitution, bg="lightgrey")

    labelEntreeS = Label(frameEntreeS, text="Veuillez entrer le message chiffré ici :", font="Times 18 bold underline",
                        fg="gray", bg="lightgray", width=30, height=1)
    labelEntreeS.pack(side=LEFT, anchor=NW, padx=16, pady=4)


    entreeS = Entry(frameEntreeS, textvariable=strVariableS, text="Entrer le message chiffré ici-même",
                   font="Times 15 bold", fg="gray", bg="lightgrey", borderwidth=3, relief="groove", width=90)
    entreeS.pack(padx=36, pady=5, anchor=NE)

    frameEntreeS.pack()

    boutonValiderS = Button(substitution, image=check, command=decrypteSubstitution)
    boutonValiderS.pack(side=LEFT, padx=50)

    boutonRetourS = Button(substitution, image=home, command=updateMainMenu)
    boutonRetourS.pack(side=RIGHT, padx=50)
    substitution.pack()

def updateTransposition():
    global strVariableT
    global transposition
    global titreT
    global consoleT
    global alphabetT
    global frameEntreeT
    global labelEntreeT
    global entreeT
    global boutonValiderT
    global boutonRetourT

    cleanWindow(window)

    strVariableT = StringVar()

    transposition = Frame(window, bg="lightgrey", height=720)

    titreT = Label(transposition, text="Décryptage de chiffrement par transposition", font="Times 30 italic bold",
                   fg="gray", bg="lightgrey")
    titreT.pack()

    consoleT = Label(transposition, text="Le message déchiffré s'affichera ici-même",
                     font="Times 15 bold", fg="gray", bg="lightgrey", wraplength=1200, borderwidth=3, relief="groove",
                     width=100, height=20)
    consoleT.pack(pady=5)

    alphabetT = Label(transposition, text="La clé de chiffrement est : 123456789",
                      font="Times 15 bold", fg="gray", bg="lightgrey", borderwidth=3, relief="groove", width=100,
                      height=1)
    alphabetT.pack()

    frameEntreeT = Frame(transposition, bg="lightgrey")

    labelEntreeT = Label(frameEntreeT, text="Veuillez entrer le message chiffré ici :", font="Times 18 bold underline",
                         fg="gray", bg="lightgray", width=30, height=1)
    labelEntreeT.pack(side=LEFT, anchor=NW, padx=16, pady=4)

    entreeT = Entry(frameEntreeT, textvariable=strVariableT, text="Entrer le message chiffré ici-même",
                    font="Times 15 bold", fg="gray", bg="lightgrey", borderwidth=3, relief="groove", width=90)
    entreeT.pack(padx=36, pady=5, anchor=NE)

    frameEntreeT.pack()

    boutonValiderT = Button(transposition, image=check, command=decrypteTransposition)
    boutonValiderT.pack(side=LEFT, padx=50)

    boutonRetourT = Button(transposition, image=home, command=updateMainMenu)
    boutonRetourT.pack(side=RIGHT, padx=50)
    transposition.pack()

#_____________________MAIN_MENU_______________________

mainmenu = Frame(window, bg="lightgray")
titre = Label(mainmenu, text="Projet PIMA - Hill Climbing", font="Times 40 italic bold", fg="gray", bg="lightgrey")
titre.pack()

description = Label(mainmenu, text="Veuillez sélectionner l'un des onglets ci-dessous :", font="Times 25 bold", fg="gray", bg="lightgrey", pady=20)
description.pack()

boutonSubstitution = Button(mainmenu, image=cesar, command=updateSubstitution)
boutonSubstitution.pack(side=LEFT, padx=55)

boutonTransposition = Button(mainmenu, image=scytale, command=updateTransposition)
boutonTransposition.pack(side=RIGHT, padx=55)
mainmenu.pack(pady=25)

#_____________________MAINLOOP_______________________

#boucle infinie
window.mainloop()