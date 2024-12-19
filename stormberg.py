from chronometrage import *


def nb_chiffre(n: int) -> int:
    """Renvoie le nombre de chiffres de n"""
    compteur = 0
    while n > 0:
        n //= 10
        compteur += 1
    return compteur


def est_armstrong(n: int) -> bool:
    """Renvoie True si n est un nombre de Armstrong, False sinon"""
    somme = 0
    na = n
    nbc = nb_chiffre(n)
    for i in range(nbc):
        chiffre = na % 10
        somme += chiffre ** nbc
        na //= 10
    return somme == n


@chronometrage()
def affiche_armstrong(mini, maxi):
    """Affiche les nombres de Armstrong entre mini et maxi"""
    for i in range(mini, maxi + 1):
        if est_armstrong(i):
            print(i)


print(est_armstrong(153))
affiche_armstrong(0, 1000000)
