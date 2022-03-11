from random import *
from math import *

#traduction
def translate(s, alphabet):
    dict_alphabet = {}
    for i in range(len(alphabet)):
        dict_alphabet[alphabet[i]] = chr(i + 65)
    s_translated = ""
    for c in s:
        s_translated += dict_alphabet[c]
    return s_translated


#dico theorique (fourni par l'encadrante):
def charge_table (fic):
    """Charge dans un dictionnaire les informations du fichier fic."""
    tab = dict()
    for ligne in fic:
        donnees = ligne.rstrip('\n\r').split(";")
        tab[donnees[0]] = int(donnees[1])
    return tab

def get_dict_theo(nom_fichier):
    return charge_table(open(nom_fichier, "r"))

#fitness function ancienne v1
"""
def fitness(alphabet, s):
    dict_theo = get_dict_theo('nb_tetra_fr.xls')
    dict_s = get_dico(alphabet, s, dict_theo)
    for key in dict_s:
        if key not in dict_theo:
            dict_theo[key] = 0
    somme = 0
    nb_tetra_t = 0
    nb_tetra_s = 0
    for tetra in dict_s:
        nb_tetra_s += dict_s[tetra]
    for tetra in dict_theo:
        nb_tetra_t += dict_theo[tetra]
    for tetra in dict_s:
        somme += abs((dict_s[tetra]/nb_tetra_s)-(dict_theo[tetra]/nb_tetra_t))
    return somme
"""
#fitness function ancienne v2
"""
def fitness(alphabet, s, dict_theo):
    dict_s = get_dico(alphabet, s, dict_theo)
    somme = 0
    nb_tetra_t = 0
    nb_tetra_s = 0
    for tetra in dict_s:
        nb_tetra_s += dict_s[tetra]
    for tetra in dict_theo:
        nb_tetra_t += dict_theo[tetra]
    for tetra in dict_s:
        if tetra in dict_theo:
            somme += abs((dict_s[tetra]/nb_tetra_s)-(dict_theo[tetra]/nb_tetra_t))
        else:
            somme += dict_s[tetra]/nb_tetra_s
    return somme
"""

#fitness function finale (substitution)
def fitness_substitution(s, alphabet, dict_theo):
    somme = 0
    s_translated = translate(s, alphabet)
    for i in range(len(s_translated) - 3):
        ts = ""
        for j in range(4):
            ts += s_translated[i + j]
        if ts in dict_theo:
            somme += log10(dict_theo[ts])
        else:
            somme += 0.001
    return somme

def suppr_lettre(msg, c):
    strfinal = ""
    for e in msg:
        if e != c:
            strfinal += e
    return strfinal

#fitness function finale (transposition)
def fitness_transposition(message, cle, char_padding, dict_theo):
    somme = 0
    msg = dechiffrement_transposition(message, cle, char_padding)
    index = 1

    while (msg[-index] == char_padding):
        somme += 1000
        if (index+1 != len(msg)):
            index += 1
    msgclean = suppr_lettre(msg, char_padding)

    for i in range(len(msgclean) - 3):
        ts = ""
        for j in range(4):
            ts += msgclean[i + j]
        if ts in dict_theo:
            somme += log10(dict_theo[ts])
        else:
            somme += 0.001

    return somme

#echange de deux caracteres dans un str
def swap(s, i, j):
    sf = ""
    for k in range(len(s)):
        if k != i and k != j:
            sf += s[k]
        elif k == i:
            sf += s[j]
        else:
            sf += s[i]
    return sf

def hill_climbing_substitution(s, epsilon = 0.5 ,alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
    dict_theo = get_dict_theo('nb_tetra_fr.csv')
    fit = fitness_substitution(s, alphabet, dict_theo)
    alpha = alphabet[:]
    freeze = 0
    while freeze < 1000:
        i, j = 0, 0
        while i == j:
            i = randint(0, len(alpha) - 1)
            j = randint(0, len(alpha) - 1)
        fit2 = fitness_substitution(s, swap(alpha, i, j), dict_theo)
        if (abs(fit - fit2) <= epsilon) or fit >= fit2:
            freeze += 1
        else:
            fit = fit2
            alpha = swap(alpha, i, j)
            freeze = 0
    return alpha

#transposition
def transposition(message, cle, char_padding):
    #copie du str message
    msg = message[:]

    #ajouter les caracteres au message pour effectuer le padding, si nécessaire
    if (len(msg) % len(cle)) != 0:
        for i in range(len(cle) - (len(msg) % len(cle))):
            msg += char_padding

    #creation de la matrice du clair
    matrice_cl = []
    for i in range(len(msg) // len(cle)):
        tmp_str = ""
        for j in range(len(cle)):
            tmp_str += msg[i*len(cle)+j]
        matrice_cl.append(tmp_str)

    #creation du message final (chiffré)
    msg_fin = ""
    for i in range(len(cle)):
        for j in range(len(msg) // len(cle)):
            msg_fin += matrice_cl[j][int(cle[i])-1]

    #retour du message final
    return msg_fin

def dechiffrement_transposition(message, cle, char_padding="&"):
    #copie du message chiffré
    msg = message[:]

    #creation de la matrice du chiffre
    matrice_ch = []
    for i in range(len(cle)):
        tmp_str = ""
        for j in range(len(msg) // len(cle)):
            tmp_str += msg[i*(len(msg) // len(cle))+j]
        matrice_ch.append(tmp_str)

    #creation du message final (dechiffre)
    msg_fin = ""
    for i in range(len(msg) // len(cle)):
        for j in range(len(cle)):
            msg_fin += matrice_ch[cle.index(str(j+1))][i]

    #retour du message
    return msg_fin

def nb_padding_manquant(msg_dechiffre, char_padding):
    nb_char_pdg = 0
    for e in msg_dechiffre:
        if e == char_padding:
            nb_char_pdg += 1
    for i in range(1, nb_char_pdg + 1):
        if msg_dechiffre[-i] == char_padding:
            nb_char_pdg -= 1
    return nb_char_pdg

def hill_climbing_transposition_taillefixe(message, char_padding = "&", cle = "123456789", epsilon = 0.5):
    #copie de la cle et du message
    key = cle[:]
    msg = message[:]

    #chargement du dictionnaire theorique
    dict_theo = get_dict_theo('nb_tetra_fr.csv')

    #initialisation des valeurs initiales de fit et de freeze
    msg_dechiffre = dechiffrement_transposition(msg, key, char_padding)
    nb_pdg = nb_padding_manquant(msg_dechiffre, char_padding)

    #on commence par poser la condition de rassembler les caracteres de padding à la fin
    while nb_pdg != 0:
        i, j = 0, 0
        while i == j:
            i = randint(0, len(key) - 1)
            j = randint(0, len(key) - 1)
        msg_dechiffre = dechiffrement_transposition(msg, swap(key, i, j), char_padding)
        nb_pdg2 = nb_padding_manquant(msg_dechiffre, char_padding)
        if nb_pdg2 <= nb_pdg:
            nb_pdg = nb_pdg2
            key = swap(key, i, j)

    #initialisation des valeurs initiales de fit et de freeze
    fit = fitness_transposition(msg, key, char_padding, dict_theo)
    freeze = 0

    #boucle principale
    while freeze < 15000:
        i, j = 0, 0
        while i == j:
            i = randint(0, len(key) - 1)
            j = randint(0, len(key) - 1)
        fit2 = fitness_transposition(msg, swap(key, i, j), char_padding, dict_theo)
        if (abs(fit - fit2) <= epsilon) or fit >= fit2:
            freeze += 1
        else:
            fit = fit2
            key = swap(key, i, j)
            freeze = 0
    return key