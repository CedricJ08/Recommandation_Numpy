# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 20:27:28 2018

@author: Alu
"""


from scipy import spatial
import numpy as np
import matplotlib.pyplot as plt

# C'est un algo hybride qui utilise le content base et le colaborative filtering items, donc il y a ces deux algos et seul la fonction rating change
# On calcul la note avec les deux algo puis on fait une moyenne ponderee de ces deux notes, on optimise la ponderation en tracant la moyenne des ecarts types en fonction de la ponderation


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



def trianglesimiI(n,U):
    a=0
    V = np.transpose(U)
    T=np.zeros((nb_film,nb_film))
    O=[]
    for k in range (len(V)):
        if all([ v == 0 for v in V[k] ]) == True :
            O.append(k)
    for i in range (nb_film):
        if a != int((i*100)/nb_film):
            a= int((i*100)/nb_film)
            print ('trianglesimiI : ' + str(a)+'%')
        if i not in O :
            for j in range (i+1,nb_film):
                if j not in O :
                    T[i][j]=1 - spatial.distance.cosine(V[j],V[i])
    return (T)

 
def fullsimiI(n,U):
    a=0
    T = trianglesimiI(n,U)
    I=[]
    for i in range (nb_film):
        if a != int((i*100)/nb_film):
            a= int((i*100)/nb_film)
            print ('fullsimiI : ' + str(a)+'%')
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



def trianglesimiU(n,U):
    a=0
    P=profiluser(U)
    T=np.zeros((nb_user,nb_user))
    for i in range (nb_user):
        if a != int((i*100)/nb_user):
            a= int((i*100)/nb_user)
            print ('trianglesimiU : ' + str(a)+'%')
        for j in range (i+1,nb_user):
            T[i][j]=1 - spatial.distance.cosine(P[j][1],P[i][1])
    return (T)

 
def fullsimiU(n,U):
    a=0
    T = trianglesimiU(n,U)
    I=[]
    for i in range (nb_user):
        if a != int((i*100)/nb_user):
            a= int((i*100)/nb_user)
            print ('fullsimiU : ' + str(a)+'%')
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



def rating1 (D,i,U):
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
        

def rating2 (D,i,U):
    n=len(D)
    r=0.
    p=0.
    for k in range (n):
        a=U[D[k][1]][i]
        r+=a
        if a !=0 :
            p+=1
    if p != 0:
        return (r/p)
    return (0)

def RatingMix (i,j,Items,User,U,p) :
    ri=rating1 (Items,i,U)
    ru=rating2 (User,j,U)
    return (p*ri+(1-p)*ru)

        


def test (n,p):
    a=0
    e=0.
    k=0.
    U=Mise_en_forme_data('u1.base')
    V=Mise_en_forme_data('u1.test')
    print ('calcul de Items')
    Items= fullsimiI(n,U)
    print ('calcul de User')
    User= fullsimiU(n,U)
    print ('process du test')
    for i in range (nb_user):
        if a != int((i*100)/nb_user):
            a= int((i*100)/nb_user)
            print ('test : ' + str(a)+'%')
        for j in range (nb_film):
            if V[i][j]!=0:
                e+=abs(V[i][j]-RatingMix (i,j,Items[j],User[i],U,p))
                k+=1
    return (e/k)

#p opt = 0.65


