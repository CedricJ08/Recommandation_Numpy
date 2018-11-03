# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 18:31:37 2018

@author: Alu
"""

import time
from scipy import spatial
import numpy as np
import matplotlib.pyplot as plt

#C'est un algo hybride qui utilise le content base et le colaborative filtering utilisateur, donc il y a ces deux algos et seul la fonction rating change
# on calcul dans un premier temps les n utilisateurs les plus proches de l'utilisateur j avec les deux methodes puis si il y a suffisament d'utilisateur similaire en commun, on calcul la note moyen uniquement avec les utilisateurs similaire qui sont en commun, sinon on fait le calcul de la note avec les utilisateurs similaires trouvé en content base. on peu regler combien d'utilisateur similaire en commun on souhaite pour se lancer sur le calcu avec uniquement les users de cette intersection.



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
#    a=0
    N=len(U)
    T=np.zeros((N,N))
    for i in range (N):
#        if a != int((i*100)/N):
#            a= int((i*100)/N)
#            print ('trianglesimiUCF : ' + str(a)+'%')
        for j in range (i+1,N):
            T[i][j]=1 - spatial.distance.cosine(U[j],U[i])
    return (T)

 
def fullsimiUCF(n,U):
#    a=0
    T = trianglesimiUCF(n,U)
    N=len(U)
    I=[]
    for j in range (N):
#        if a != int((j*100)/N):
#            a= int((j*100)/N)
#            print ('fullsimiUCF : ' + str(a)+'%')
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


def convers2(l):
    L=[[]]
    k=len(l[0])-1
    for i in range (1,39):
        if l[0][k-i]!='|':
            L[0].append (int(l[0][k-i]))
    i=0
    while l[0][i]!='|':
        i+=1
    L.insert(0,int(l[0][0:i]))
    return (L)


def Mise_en_forme_data2():
    m= open('C:/Users/Alu/Documents/ml-100k/u.item')
    M=[]
    for lines in m :
        M.append(convers2([lines]))
    return M


def mean(l):
    p=0.
    m=0.
    for i in range (len(l)):
        if l[i] !=0:
            p=p+1
            m=m+l[i]
    return (m/p)
            

def profiluser(U):
    L=Mise_en_forme_data2()
    P=[]
    L=tri(L)
    for j in range (len(U)):
        m=mean(U[j])
        M=np.zeros(len(L[0][1]))
        p=0.
        for i in range (len(U[0])):
            if U[j][i] != 0:
                p=p+1
                M=M+(U[j][i]-m)*np.array(L[i][1])
        P.append([j,(1/p)*M])
    return (P)



def trianglesimiUCB(n,U):
#    a=0
    P=profiluser(U)
    T=np.zeros((nb_user,nb_user))
    for i in range (nb_user):
#        if a != int((i*100)/nb_user):
#            a= int((i*100)/nb_user)
#            print ('trianglesimiUCB : ' + str(a)+'%')
        for j in range (i+1,nb_user):
            T[i][j]=1 - spatial.distance.cosine(P[j][1],P[i][1])
    return (T)

 
def fullsimiUCB(n,U):
#    a=0
    T = trianglesimiUCB(n,U)
    I=[]
    for i in range (nb_user):
#        if a != int((i*100)/nb_user):
#            a= int((i*100)/nb_user)
#            print ('fullsimiUCB : ' + str(a)+'%')
        L=[]
        for j in range (i):
            L.append([T[j][i],j])
        for j in range (i+1,nb_user):
            L.append([T[i][j],j])
        D=tri(L)
        N=len(D)
        if N<=n:
            I.append (D)
        else : 
            I.append (D[(N-n):])
    return (I)



def RatingMix1 (User,Usecu,j,U,N):
    u=len(User)
    if u < N :
        D=Usecu
    else :
        D=User
    r=0.
    p=0.
    le=len(D)
    for k in range (le):
        a=U[D[k]][j]
        r+=a
        if a !=0 :
            p+=1
    if p != 0:
        return (r/p)
    return (0)

def extract (U):
    L=[]
    for i in range (len(U)):
        L.append(U[i][1])
    return (L)

def RatingMix2 (UCFi,UCBi,j,U):
    D=UCFi+UCBi
    r=0.
    p=0.
    le=len(D)
    for k in range (le):
        a=U[D[k]][j]
        r+=a
        if a !=0 :
            p+=1
    if p != 0:
        return (r/p)
    return (0)


def test (n,N):
    deb=time.time()
#    a=0
    e1=0.
    e2=0.
    k=0.
    U=Mise_en_forme_data('u1.base')
    V=Mise_en_forme_data('u1.test')
#    print ('calcul de UCF')
    UCF= fullsimiUCF(n,U)
#    print ('calcul de UCB')
    UCB= fullsimiUCB(n,U)
#    print ('process du test')
    for i in range (nb_user):
#        if a != int((i*100)/nb_user):
#            a= int((i*100)/nb_user)
#            print ('test : ' + str(a)+'%')
        UCFi = extract(UCF[i])
        UCBi = extract(UCB[i])
        User= [val for val in UCFi if val in UCBi] 
        Usecu=extract(UCB[i])
        for j in range (nb_film):
            if V[i][j]!=0:
                e1+=abs(V[i][j]-RatingMix1 (User,Usecu,j,U,N))
                e2+=abs(V[i][j]-RatingMix2 (UCFi,UCBi,j,U))
                k+=1
    fin = time.time()
    print (fin-deb)
    return (e2/k)



