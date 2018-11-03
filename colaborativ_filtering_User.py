# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 18:56:40 2018

@author: Alu
"""


from scipy import spatial
import numpy as np


# c'est mot pour mot le meme algo que colaborative filtering item en utilisant la transposee de la matrice d'utilite pour calculer les distances utilisateurs a la place des distances items

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



def trianglesimiUCF(n,U):
    a=0
    N=len(U)
    T=np.zeros((N,N))
    for i in range (N):
        if a != int((i*100)/N):
            a= int((i*100)/N)
            print ('trianglesimiUCF : ' + str(a)+'%')
        for j in range (i+1,N):
            T[i][j]=1 - spatial.distance.cosine(U[j],U[i])
    return (T)

 
def fullsimiUCF(n,U):
    a=0
    T = trianglesimiUCF(n,U)
    N=len(U)
    I=[]
    for j in range (N):
        if a != int((j*100)/N):
            a= int((j*100)/N)
            print ('fullsimiUCF : ' + str(a)+'%')
        L=[]
        for i in range (j):
            L.append([T[i][j],i])
        for i in range (j+1,N):
            L.append([T[j][i],i])
        D=tri(L)
        M=len(D)
        if M<=n:
            I.append (D)
        else : 
            I.append (D[(M-n):])
    return (I)


def rating (D,j,U):
    N=len(D)
    r=0.
    p=0.
    for k in range (N):
        a=U[D[k][1]][j]
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
    I= fullsimiUCF(n,U)
    for i in range (nb_user):
       for j in range (nb_film):
            if V[i][j]!=0:
                e+=abs(V[i][j]-rating (I[i],j,U))
                k+=1
    return (e/k)
