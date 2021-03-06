import numpy as np
import random
import time


Semilla=0
A=np.loadtxt("matriz600.txt",dtype="int")# matriz con las m tareas y n subtareas, con n=m
B=np.loadtxt("profile600.txt",dtype="int") # profit en [0][x], peso/costo en [1][x]
C=np.loadtxt("matriz100.txt",dtype="int")
D=np.loadtxt("profile100.txt",dtype="int")
E=np.loadtxt("matriz200.txt",dtype="int")
F=np.loadtxt("profile200.txt",dtype="int")
G=np.loadtxt("matriz300.txt",dtype="int")
H=np.loadtxt("profile300.txt",dtype="int")
I=np.loadtxt("matriz400.txt",dtype="int")
J=np.loadtxt("profile400.txt",dtype="int")
K=np.loadtxt("matriz500.txt",dtype="int")
L=np.loadtxt("profile500.txt",dtype="int")
profits=[D,F,H,J,L,B]
matricez=[C,E,G,I,K,A]
Pesos=[11223,25630,38289,49822,63902,109943]
BestFO = 0
BestLocalFO = 0
BestPo = []
BestLocalPO = []
BestWeight = 999999
BestLocalWeight = 999999
Pob = []
NewPob = []
TamañoPo = 200


def var_decision(X,profit):
    if len(X) == 0:
        X=[0]*len(profit[0])
    return X

def FO(decision,matriz,profit): # calcula la Funcion Objetivo con dicha decision
    i = 0
    aux = 0
    while i<len(profit[0]):
        aux=aux+(decision[i]*profit[0][i])
        i=i+1
    return aux

def Weight(decision, matriz, profit): # Calcula el peso de las tareas
    i = 0
    weight = 0
    SubTask = []
    while i < len(decision):
        j = 0
        while j < len(decision):
            if len(SubTask) == 0 and decision[i] == 1:
                weight += profit[1][j]*decision[i]*matriz[i][j]
                SubTask.append(j)
            elif decision[i] == 1:
                igual = False
                for index in SubTask:
                    if index == j:
                        igual = True
                        break
                if igual == False:
                    weight += profit[1][j]*decision[i]*matriz[i][j]
                    SubTask.append(j)
            j += 1
        i=i+1
    return weight

def restriccion(decision,peso,matriz,profit):# calcula si dicha decision(variable binaria) cumple la restriccion
    weight = Weight(decision, matriz, profit)
    if weight > peso:
        return 0
    return 1

def Tareas_resueltas(indice,matriz,profit): #suma cuantas tareas son resueltas en la posicion indice de la matriz
    aux=0
    j=0
    while j<len(profit[0]):
        aux=aux+matriz[indice][j]
        j=j+1
    return aux

def probabilidad(prob,profit,matriz):#genera probabilidades segun profit/cantidad de subtareas resuletas en i, si esto es mayor, tiene mas chances de ser escogido
    i=0
    while i<len(profit[0]):
        aux=0
        proba=int(profit[0][i]/Tareas_resueltas(i,matriz,profit)) #profit/cantidad de subtareas resueltas, cuanto aporta la realizacion de cada subtarea
        aux=proba
        prob.append(int(aux))
        i=i+1
    return prob

def ruleta_greedy(proba):#Crea un arreglo que se repite m veces una posicion, sirve para seleccionar 1 de las posiciones, la cual sera elegida a la hora de seleccionar una tarea
    probab=[]
    i=0
    global Semilla
    while i<len(proba):
        j=0
        m=proba[i]
        while j<m:
            probab.append(i)
            j=j+1
        i=i+1
    random.seed(Semilla)
    aux=random.randint(0,len(probab)-1)
    Semilla=Semilla+1
    seleccion=probab[aux]
    return seleccion

def greedy(matriz,profit,peso,proba):
    i=0
    X=[]
    X=var_decision(X,profit)
    global Semilla
    while i<10:
        aux=ruleta_greedy(proba[:])
        X[aux]=1
        if restriccion(X[:],peso,matriz,profit)==1:
            i=i+1
        elif restriccion(X[:],peso,matriz,profit)==0:
            X[aux]=0
            return X
    return X

def PoblacionInicial(matriz,profit,peso,poblacion,proba): # Genera la poblacion inicial
    i=0
    global Pob
    global BestFO
    global BestPo
    global BestWeight
    start=time.time()
    while i<poblacion:
        aux=greedy(matriz,profit,peso,proba)
        Pob.append(aux)
        i=i+1
    end=time.time()
    for i in Pob:
        MejorFOPob = FO(i,matriz,profit)
        MenorWeight = Weight(i, matriz, profit)
        if MejorFOPob > BestFO:
            BestFO = MejorFOPob
            BestPo = i
            BestWeight = MenorWeight
        elif MejorFOPob == BestFO and MenorWeight < BestWeight:
            BestPo = i
            BestWeight = MenorWeight

def Mutacion(hijo): # Probabilidad de 1% de que haya motacion en un solo bit
    global Semilla
    random.seed(Semilla)
    num = random.randint(0, 99)
    Semilla += 1
    if num == 17:
        random.seed(Semilla)
        pos=random.randint(0, len(hijo) -1)
        Semilla += 1
        if hijo[pos] == 1:
            hijo[pos] = 0
        else:
            hijo[pos] = 1
    return hijo


def Cruzamiento(seleccion1, seleccion2,matriz,profit,Peso): # Realiza el cruzamiento y devuelve a dos hijos
    hijo1=[]
    hijo2=[]
    i = 0
    global BestLocalFO
    global BestLocalPO
    global BestLocalWeight
    global Semilla
    sel1=seleccion1[:]
    sel2=seleccion2[:]
    random.seed(Semilla)
    particion=random.randint(0,len(seleccion1)-1)
    Semilla=Semilla+1
    while i < len(seleccion1):
        if i <= particion:
            hijo1.append(seleccion1[i])
            hijo2.append(seleccion2[i])
        else:
            hijo1.append(seleccion2[i])
            hijo2.append(seleccion1[i])
        i += 1
    hijo1 = Mutacion(hijo1)
    hijo2 = Mutacion(hijo2)
    padre1=FO(sel1,matriz,profit)
    padre2=FO(sel2,matriz,profit)
    if restriccion(hijo1[:], Peso, matriz, profit) == 0:
        if padre1<=padre2:
            hijo1 = sel2[:]
        else:
            hijo1=sel1[:]
    if restriccion(hijo2[:], Peso, matriz, profit) == 0:
        if padre1<=padre2:
            hijo2 = sel2[:]
        else:
            hijo2=sel1[:]
    hijo1FO = FO(hijo1, matriz, profit)
    hijo2FO = FO(hijo1, matriz, profit)
    Hijo1Weight = Weight(hijo1, matriz, profit)
    Hijo2Weight = Weight(hijo2, matriz, profit)
    if hijo1FO > BestLocalFO:
        BestLocalFO = hijo1FO
        BestLocalPO = hijo1
        BestLocalWeight = Hijo1Weight
    if hijo2FO > BestLocalFO:
        BestLocalFO = hijo2FO
        BestLocalPO = hijo1
        BestLocalWeight = Hijo2Weight
    return hijo1, hijo2

def Torneo(Tamaño,matriz,profit): # Selecciona a un padre
    array = []
    Mejor = []
    global Semilla
    random.seed(Semilla)
    for i in range(0, int(Tamaño*0.3)):
        random.seed(Semilla)
        num = random.randint(0,Tamaño-1)
        Semilla += 1
        if len(array) == 0:
            array.append(num)
            Mejor.append(FO(Pob[num], matriz, profit))
        else:
            igual = False
            for j in array:
                if j == num:
                    igual = True
                    break
            if igual == False:
                array.append(num)
                Mejor.append(FO(Pob[num], matriz, profit))
    return Pob[array[Mejor.index(max(Mejor))]]

def Solver(A,B,Size,Tamaño):
    proba = []
    proba = probabilidad(proba, B, A)
    generacion=0
    start=time.time()
    PoblacionInicial(A,B,Size,Tamaño,proba[:])
    end=time.time()
    print("El greedy con tamaño " +str(len(B[0]))+" se demoro: "+str(end-start)+" segundos")
    global NewPob
    global Pob
    global BestFO
    global BestLocalFO
    global BestPo
    global BestLocalPO
    global BestWeight
    global BestLocalWeight
    count = 0
    while generacion<500:
        if len(NewPob) == Tamaño:
            if count == 30:
                break
            Pob = NewPob[:]
            NewPob = []
            if BestLocalFO > BestFO:
                BestFO = BestLocalFO
                BestPo = BestLocalPO
                BestWeight = BestLocalWeight
            count += 1
        else:
            seleccion1 = Torneo(Tamaño,A,B)
            seleccion2 = Torneo(Tamaño,A,B)
            hijos = Cruzamiento(seleccion1[:], seleccion2[:],A,B,Size)
            NewPob.append(hijos[0])
            NewPob.append(hijos[1])
        generacion=generacion+1
i=0
res6=[0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0]
res1=[0,1,1,1,0,0,0,1,0,0,0,1,1,0,0,0,0,1,0,1,0,1,0,0,0,0,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,1,0,0,1,0,1,1,0,0,1,1,0,0,0,1,0,0,0,1,0,0,1,0,0,1,0,1,0,0,1,1,1,1,1,0,0,0,1,1,1,0,0,1,1,1,1,1,0,1]
res2=[0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,1,0,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,1,0,0,0,0,0,0,0,0]
res3=[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,1,0,0,0,1,0]
res4=[0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
res5=[0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
respuestas=[res1,res2,res3,res4,res5,res6]
while i<len(Pesos):
    NewPob =[]
    Pob =[]
    BestFO = 0
    BestLocalFO = 0
    BestPo = []
    BestLocalPO = []
    BestWeight = 999999
    BestLocalWeight = 999999
    start=time.time()
    Solver(matricez[i],profits[i],Pesos[i],TamañoPo)
    end=time.time()
    print("En total el algoritmo genetico(incluido el greedy) con tamaño "+ str(len(respuestas[i]))+" se demoro: "+str(end-start)+" segundos")
    print("BestFO: ", BestFO)
    print("Weight: ", BestWeight)
    print(BestPo)
    print("Resultado FO esperado: "+str(FO(respuestas[i],matricez[i],profits[i])))
    print("Resultado peso esperado: "+str(Weight(respuestas[i],matricez[i],profits[i])))
    print("------------------------------------------------------------------------------------------------------------------------------")
    i=i+1