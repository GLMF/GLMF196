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
    else
        return grille[ligne][colonne] == 0

def estGagnantLigne(grille, ligne, colonne):
    typePion = grille[ligne][colonne]
    for col in range(3):
        if grille[ligne][col] != typePion:
            return False
    return True

def estGagnantColonne(grille, ligne, colonne):
    typePion = grille[ligne][colonne]
    for line in range(3):
        if grille[line][colonne] != typePion:
            return False
    return True

def estGagnantDiago_1(grille, ligne, colonne):
    typePion = grille[ligne][colonne]
    for pos in range(3):
        if grille[pos][pos] != typePion:
            return False
    return True

def estGagnantDiago_2(grille, ligne, colonne):
    typePion = grille[ligne][colonne]
    if grille[1][1] != typePion:
        return False
    if grille[0][2] != typePion or grille[2][0] != typePion:
        return False
    return True

def estGagnant(grille, ligne, colonne):
    if estGagnantLigne(grille, ligne, colonne):
        return True

    if estGagnantColonne(grille, ligne, colonne):
        return True

    if ligne == colonne:
        if ligne == 1:
            return estGagnantDiago_1(grille, ligne, colonne) or \
                   estGagnantDiago_2(grille, ligne, colonne)
        else:
            return estGagnantDiago_1(grille, ligne, colonne)
    elif (ligne == 0 and colonne == 2) or (ligne == 2 and colonne == 0):
        return estGagnantDiago_2(grille, ligne, colonne)
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


def demarrerJeu():
    grille = [[0] * 3 for x in range(3)]
    tours = 0
    gagnant = False
    joueur = 0

    while not gagnant and tours < 9:
        affiche(grille)
        valide = False
        while not valide:
            ligne, colonne = saisie_joueur(joueur)
            valide = estLibre(grille, ligne - 1, colonne - 1)
            if not valide:
                print('La case ({}, {}) n\'est pas libre !'.format(ligne, colonne))
        grille[ligne - 1][colonne - 1] = joueur + 1
        gagnant = estGagnant(grille, ligne - 1, colonne - 1)
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
