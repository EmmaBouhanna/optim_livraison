import numpy as np
import pandas as pd
import random

def clients_aleatoires(k, df_points = df_garage_entrepôts) :

    """
    Fonction qui ajoute à une dataframe de points géographiques un certain nombre de points
    géographiques représentant des clients

    La fonction prend en entrée :
    - k : le nombre de clients qu'on veut générer aléatoirement
    - df_points : une dataframe de points géographiques (par exemple le garage et les entrepôts)
    Cette dataframe doit contenir des colonnes "Lat" et "Lon"
    

    La fonction retourne :
    - df_complete : la dataframe complétée par les clients aléatoires 
    - indices : un triplet de listes d'indices :
    (indices du/des garage(s), indices des entrepôts, indices des clients)
    """
    