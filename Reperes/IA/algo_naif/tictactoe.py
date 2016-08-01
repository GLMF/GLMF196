import random

def jeton(valeur):
    if valeur == 0:
        return ' '
    elif valeur == 1:
        return 'X'
    else:
        return 'O'

def affiche(grille):
    print('  1 2 3')
    for ligne in range(3):
        print(str(ligne + 1) + ' ', end='')
        for colonne in range(3):
            if colonne != 0:
                print('|', end='')
            print(jeton(grille[ligne][colonne]), end='')
        print()
        if ligne != 2:
            print('  ' + '-' * 5)

def estLibre(grille, ligne, colonne):
    if ligne < 0 or ligne > 2 or colonne < 0 or colonne > 2:
        return False
    else:
        return grille[ligne][colonne] == 0

def estGagnantLigne(grille, ligne, colonne, typePion):
    for col in set(range(3)) - {colonne}:
        if grille[ligne][col] != typePion:
            return False
    return True

def estGagnantColonne(grille, ligne, colonne, typePion):
    for line in set(range(3)) - {ligne}:
        if grille[line][colonne] != typePion:
            return False
    return True

def estGagnantDiago_1(grille, ligne, colonne, typePion):
    for pos in set(range(3)) - {colonne}:
        if grille[pos][pos] != typePion:
            return False
    return True

def estGagnantDiago_2(grille, ligne, colonne, typePion):
    cases = {(0, 2), (1, 1), (2, 0)} - {(ligne, colonne)}
    for ligne, colonne in cases:
        if grille[ligne][colonne] != typePion:
            return False
    return True

def estGagnant(grille, ligne, colonne):
    if estGagnantLigne(grille, ligne, colonne, grille[ligne][colonne]):
        return True

    if estGagnantColonne(grille, ligne, colonne, grille[ligne][colonne]):
        return True

    if ligne == colonne:
        if ligne == 1:
            return estGagnantDiago_1(grille, ligne, colonne, grille[ligne][colonne]) or \
                   estGagnantDiago_2(grille, ligne, colonne, grille[ligne][colonne])
        else:
            return estGagnantDiago_1(grille, ligne, colonne, grille[ligne][colonne])
    elif (ligne == 0 and colonne == 2) or (ligne == 2 and colonne == 0):
        return estGagnantDiago_2(grille, ligne, colonne, grille[ligne][colonne])
    else:
        return False

def saisie_joueur(joueur):
    valide = False
    while not valide:
        try:
            ligne, colonne = map(int, input('Joueur {}:'.format(joueur + 1)).split(' '))
            valide = True
        except ValueError:
            print('Saisie non valide, veuillez recommencer')
    return (ligne, colonne) 

def casesLibres(grille):
    liste = []
    for ligne in range(3):
        for colonne in range(3):
            if grille[ligne][colonne] == 0:
                liste.append((ligne, colonne))
    return liste

def danger(grille):
    cases_libres = casesLibres(grille)
    for ligne, colonne in cases_libres:
        if estGagnantLigne(grille, ligne, colonne, 1):
            return (ligne, colonne)
        if estGagnantColonne(grille, ligne, colonne, 1):
            return (ligne, colonne)
        if (ligne, colonne) in ((0, 0), (1, 1), (2, 2)):        
            if estGagnantDiago_1(grille, ligne, colonne, 1):
                return (ligne, colonne)
        if (ligne, colonne) in ((0, 2), (1, 1), (2, 0)):
            if estGagnantDiago_2(grille, ligne, colonne, 1):
                return (ligne, colonne)

    return (None, None)

def saisie_ordinateur(grille):
    ligne, colonne = danger(grille)
    if ligne is None:
        cases_possibles = casesLibres(grille)
        ligne, colonne = cases_possibles[random.randint(0, len(cases_possibles) - 1)]
    return (ligne, colonne)    

def demarrerJeu():
    grille = [[0] * 3 for x in range(3)]
    tours = 0
    gagnant = False
    joueur = random.randint(0, 1)

    while not gagnant and tours < 9:
        if joueur == 0:
            affiche(grille)
        valide = False
        while not valide:
            if joueur == 0:
                ligne, colonne = saisie_joueur(joueur)
                ligne = ligne - 1
                colonne = colonne - 1
                valide = estLibre(grille, ligne, colonne )
                if not valide:
                    print('La case ({}, {}) n\'est pas libre !'.format(ligne + 1, colonne + 1))
            else:
                ligne, colonne = saisie_ordinateur(grille)
                valide = True
        grille[ligne][colonne] = joueur + 1
        gagnant = estGagnant(grille, ligne, colonne)
        joueur = (joueur + 1) % 2
        tours += 1

    affiche(grille)

    if gagnant:
        joueur = (joueur + 1) % 2
        print('Le joueur {} a gagné !'.format(joueur + 1))
    else:
        print('Match nul')



if __name__ == '__main__':
    demarrerJeu()
