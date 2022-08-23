def voisins(liste, case: tuple) -> list[tuple]:
    voisin: list[tuple] = []
    if case[0] + 1 < len(liste[0]):
        # bas
        voisin.append((case[0] + 1, case[1]))
    if case[0] - 1 >= 0:
        # haut
        voisin.append((case[0] - 1, case[1]))
    if case[1] + 1 < len(liste[0]):
        # droite
        voisin.append((case[0], case[1] + 1))
    if case[1] - 1 >= 0:
        # gauche
        voisin.append((case[0], case[1] - 1))

    return voisin


def parcourt_profondeur(liste, depart):
    pile = [depart]
    nb = 1
    while len(pile) > 0:
        case = pile.pop()
        print(f"case : {case}")
        liste[case[0]][case[1]] = nb
        nb += 1
        for v in voisins(liste, case):
            if liste[v[0]][v[1]] == 0 and v not in pile:
                pile.append(v)
        print(pile)
        affiche_liste(liste,entete=True)
    print(liste)


def parcourt_largeur(liste, depart):
    file = [depart]
    liste[depart[0]][depart[1]] = 1
    while len(file) > 0:
        case = file.pop(0)
        print(f"case : {case}")

        # nb += 1
        for v in voisins(liste, case):
            if liste[v[0]][v[1]] == 0 and v not in file:
                file.append(v)
                liste[v[0]][v[1]] = liste[case[0]][case[1]] + 1
        print(file)
        affiche_liste(liste,entete=True)
    print(liste)


def affiche_liste(liste: list,**kwargs):
    d = lens(liste)
    entete = kwargs.get('entete',False)
    largeur = kwargs.get('largeur_colonne',4)
    separateur = kwargs.get('separateur',',')
    if len(d) > 0 and entete is True:
        print(f"{' ':{largeur}}{'j':^{(largeur+1)*(d[0]+1)}}")
        s = f"{separateur:>{(largeur+2)}}"
        for j in range(d[0]):
            s += f"{j:^{largeur}}{separateur}"
        print(s)

    if len(d) == 0:
        print(liste)
    elif len(d) == 1:
        if entete:
            s = f"i{'0':^{largeur}}{separateur}"
        else:
            s=""
        for j in range(d[0]):
            s += f"{liste[j]:{largeur}}{separateur}"
        print(s)
    else:
        for i in range(len(liste)):
            if entete:
                if i==0:
                    s = f"i{'0':^{largeur}}{separateur}"
                else:
                    s = f" {i:^{largeur}}{separateur}"
            else:
                s=""
            for j in range(len(liste[0])):
                s += f"{liste[i][j]:{largeur}}{separateur}"
            print(s)


def lens(liste: list) -> list:
    """retourne la liste des dimensions de liste sous forme d'une liste
    ex l =[[1,2,3],[4,5,6]]
    lens(l)->[2,3]
    Si l n'est pas une liste la fonction retourne un tableau vide"""
    dimensions = []
    if isinstance(liste, list):
        dimensions.append(len(liste))
        l = liste[0]
        while isinstance(l, list):
            dimensions.append(len(l))
            l = l[0]
    return dimensions


liste = [[0 for j in range(5)] for i in range(5)]
liste[1][1] = -1
liste[1][2] = -1
parcourt_profondeur(liste, (2, 2))
liste = [[0 for j in range(5)] for i in range(5)]
liste[1][1] = -1
liste[1][2] = -1
parcourt_largeur(liste, (2, 2))
print(lens([1, 2, 3]))
affiche_liste([1, 2, 3],entete=True)
