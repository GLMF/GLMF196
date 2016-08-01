import random
import copy

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
            ligne, colonne = map(int, input('Joueur {}:'.format(joueur)).split(' '))
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

def calculeBonus(humain, ordinateur, vide):
    score = 0
    if ordinateur == 2 and vide == 1:
        score += 50
    if humain == 2 and vide == 1:
        score -= 50
    if ordinateur == 1 and vide == 2:
        score += 20
    if humain == 1 and vide == 2:
        score -= 20
    return score

def decompte(liste):
    humain = 0
    ordinateur = 0
    vide = 0
    for elt in liste:
        if elt == 1:
            humain += 1 
        if elt == 2:
            ordinateur += 1 
        if elt ==0:
            vide += 1 
    return (humain, ordinateur, vide)

def score(grille, ligne, colonne):
    if estGagnant(grille, ligne, colonne):
        if grille[ligne][colonne] == 1:
            return -1000
        else:
            return 1000
    
    for ligne in range(3):
        if 0 in grille[ligne]:
            break
    else:
        return 0

    score = 0
    for ligne in range(3):
        humain, ordinateur, vide = decompte(grille[ligne])
        score += calculeBonus(humain, ordinateur, vide)
    
    for colonne in range(3):
        humain, ordinateur, vide = decompte([grille[0][colonne], grille[1][colonne], grille[2][colonne]])
        score += calculeBonus(humain, ordinateur, vide)

    humain, ordinateur, vide = decompte([grille[0][0], grille[1][1], grille[2][2]])
    score += calculeBonus(humain, ordinateur, vide)

    humain, ordinateur, vide = decompte([grille[2][0], grille[1][1], grille[0][2]])
    score += calculeBonus(humain, ordinateur, vide)
    
    return score         

def adversaire(joueur):
    if joueur == 1:
        return 2
    else:
        return 1

def calculeMinMax(grille, ligne, colonne, profondeur, joueur, minmax):
    if profondeur == 0 or estGagnant(grille, ligne, colonne):
        return score(grille, ligne, colonne)
    else:
        cases_libres = casesLibres(grille)
        if cases_libres == []:
            return score(grille, ligne, colonne)
        if minmax == 'max':
            limite = -32767
        else:
            limite = 32767
        for ligne, colonne in cases_libres:
            grille_copie = copy.deepcopy(grille)
            grille_copie[ligne][colonne] = joueur
            if minmax == 'max':
                valeur_fils = calculeMinMax(grille_copie, ligne, colonne, profondeur - 1, adversaire(joueur), 'min')
                limite = max(limite, valeur_fils)
            else:
                valeur_fils = calculeMinMax(grille_copie, ligne, colonne, profondeur - 1, adversaire(joueur), 'max')
                limite = min(limite, valeur_fils)

        return limite

def minmax(grille, profondeur, joueur=2):
    cases_libres = casesLibres(grille)
    maximum = -32767
    for ligne, colonne in cases_libres:
        grille_copie = copy.deepcopy(grille)
        grille_copie[ligne][colonne] = joueur
        valeur_max = calculeMinMax(grille_copie, ligne, colonne, profondeur - 1, adversaire(joueur), 'min')
        if valeur_max > maximum:
            maximum = valeur_max
            case = (ligne, colonne)

    return case

def saisie_ordinateur(grille):
    return minmax(grille, 6)    

def demarrerJeu():
    grille = [[0] * 3 for x in range(3)]
    tours = 0
    gagnant = False
    joueur = random.randint(1, 2)

    while not gagnant and tours < 9:
        if joueur == 1:
            affiche(grille)
        valide = False
        while not valide:
            if joueur == 1:
                ligne, colonne = saisie_joueur(joueur)
                ligne = ligne - 1
                colonne = colonne - 1
                valide = estLibre(grille, ligne, colonne )
                if not valide:
                    print('La case ({}, {}) n\'est pas libre !'.format(ligne + 1, colonne + 1))
            else:
                ligne, colonne = saisie_ordinateur(grille)
                valide = True
        grille[ligne][colonne] = joueur
        gagnant = estGagnant(grille, ligne, colonne)
        joueur = adversaire(joueur)
        tours += 1

    affiche(grille)

    if gagnant:
        joueur = adversaire(joueur)
        print('Le joueur {} a gagné !'.format(joueur))
    else:
        print('Match nul')



if __name__ == '__main__':
    demarrerJeu()
