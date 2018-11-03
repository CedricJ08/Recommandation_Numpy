# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 16:44:13 2018

@author: Alu
"""

# C'est le 1er algo qu'on a fait avec la partie hors ligne
#il y a eu essenciellenemt 2 modifs
# la premiere est dans mise en forme data, il y avait un probleme avec les indices c'est ca qui causait l'erreure du vecteur nul qui bloquai avec la norme
# ladeuxieme modif est le decoupage de l'algo qui calculait tous les similaires . l'objectif de ce decoupage est d,une part de reduire le temps de calcul et d'autre part faire une matrice intermediare utile pour incrementer les mise a jour sans tout recaluculer a chaque fois
# j'ai decoupe en 2, d'une part un premier algo qui calcul la matrice triangulaire superieure avec les distances entre chaque colones de la matrice d'utilite (les items)
# le deuxieme algo utilise la matrice triangulaire pour calculer les n itemes les plus proches de chaque item. il ressort la meme choses que l'ancien algo full simi



import marshal
import time
from scipy import spatial
import numpy as np
import matplotlib.pyplot as plt

nb_film=1682
nb_user=943



def tri (t):
    if len(t)<2:
        return t
    else :
        m=len(t)//2
        return (fusion (tri(t[:m]),tri(t[m:])))

def fusion (t1,t2):
    i1,i2,n1,n2=0,0,len(t1),len(t2)
    t=[]
    while (i1<n1 and i2<n2):
        if t1[i1][0]<t2[i2][0]:
            t.append(t1[i1])
            i1+=1
        else:
            t.append(t2[i2])
            i2+=1
    if i1==n1:
        t.extend(t2[i2:])
    else:
        t.extend (t1[i1:])
    return (t)

def convers(l):
    L=[]
    j=0
    k=0
    for i in range (len(l[0])):
        if l[0][i]=='\t':
            L.append (int(l[0][j:i]))
            j=i+1
            k+=1
        if k==3:
            return (L)


def Mise_en_forme_data(a):
    nb_film=1682
    nb_user=943
    m= open('C:/Users/Alu/Documents/ml-100k/'+a)
    M=[]
    for lines in m :
        M.append(convers([lines]))
    U=np.zeros((nb_user,nb_film))
    for i in range (len(M)):
        U[M[i][0]-1][M[i][1]-1]=M[i][2]
    return (U)



def trianglesimi(n,U):
    V = np.transpose(U)
    T=np.zeros((nb_film,nb_film))
    O=[]
    for k in range (len(V)):
        if all([ v == 0 for v in V[k] ]) == True :
            O.append(k)
    for i in range (nb_film):
#        print ((i*100)/1683 )
        if i not in O :
            for j in range (i+1,nb_film):
                if j not in O :
                    T[i][j]=1 - spatial.distance.cosine(V[j],V[i])
    return (T)

 
def fullsimi2(n,U):
    T = trianglesimi(n,U)
    I=[]
    for i in range (nb_film):
#        print ((i*100)/1683 )
        L=[]
        for j in range (i):
            L.append([T[j][i],j])
        for j in range (i+1,nb_film):
            L.append([T[i][j],j])
        D=tri(L)
        N=len(D)
        if N<=n:
            I.append (D)
        else : 
            I.append (D[(N-n):])
    return (I)



def rating2 (D,i,U):
    n=len(D)
    r=0.
    p=0.
    for k in range (n):
        a=U[i][D[k][1]]
        r+=a
        if a !=0 :
            p+=1
    if p != 0:
        return (r/p)
    return (0)
        

def test (n):

    e=0.
    k=0.
    U=Mise_en_forme_data('u1.base')
    V=Mise_en_forme_data('u1.test')
    I= fullsimi2(n,U)
    for i in range (nb_user):
        for j in range (nb_film):
            if V[i][j]!=0:
                e+=abs(V[i][j]-rating2 (I[j],i,U))
                k+=1
    
    return (e/k)



