# Pour un seul entrepot
# Pour N camions qui commencent leurs livraisons dans cet entrepot
# Pour n paquets à livrer, on note n_i le nombre de paquets livrés par le camion i
# On se restreint à un paquet par personne, quitte à augmenter la taille du paquet s'il y en a plusieurs

'''On se ramène en fait à un problème d'optimisation sous contraintes'''

from scipy import optimize
import numpy as np

# Pour un jour précis, on trouve un moyen unique pour passer des identifiants uniques à une numérotation entre 1 et n pour les paquets (encodage)
# C = matrice des coûts de passage de i à j (évaluée grâce aux routes)
# n_0 = 0 par définition
def cout(n_i_tableau, A):
    # n_i_tableau = représentation du nombre de clients livrés par le camion i
    # A_i = vecteur comportant les indices a_i des clients livrés dans l'ordre, pour chaque camion
    res = 0
    for i in range(N):
        for j in range(n_i_tableau[i], n_i_tableau[i+1] - n_i_tableau[i]):
            res += C[A[i], A[i+1]]
    return(res)

# T = matrice des temps pour passer de i à j
# t_tot = temps maximal de travail d'un camionneur
def contrainte_egalite(n_i_tableau, A):
    return(np.array([A[n_i_tableau[i+1] - n_i_tableau[i]] + [np.sum(n_i_tableau - n)]]))
# à la fin du trajet et au début du trajet du camion i, on retourne à l'

def contrainte_inegalite(n_i_tableau, A):
    return( np.array([np.sum(T[n_i_tableau[i+1] - n_i_tableau[i]]) for i in range(N)]))



# On a affaire à une programmation non linéaire à variables entières... Résolution déterministe?


        
