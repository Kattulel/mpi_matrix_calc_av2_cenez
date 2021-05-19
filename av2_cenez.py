import numpy as np
from mpi4py import MPI
import time
from random import randint

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
workers = comm.Get_size() - 1

resultante = None
matrizes = list()
# quantidade de matrizes ...
for i in range(10000):
    obj =[[randint(1,9), randint(1,9)],[randint(1,9), randint(1,9)]]
    matrizes.append(obj)

def multiplicar(X,Y):
    result = [[0,0],[0,0]]
    for i in range(len(X)):
        for j in range(len(Y[0])):
            for k in range(len(Y)):
                result[i][j] += X[i][k] * Y[k][j]
    return result

checksum = None
for matriz in matrizes:
    if checksum is None:
        checksum = matriz
    else:
        checksum = multiplicar(checksum, matriz)

def doMaster():
    global resultante
    for x in range(1,workers+1):
        if resultante is None:
            resultante = comm.recv(tag=x)
        else:
            valor = comm.recv(tag=x)
            resultante = multiplicar(resultante, valor)

if __name__ == '__main__':
    if rank == 0: # se o rank for a master
        divisao = int(len(matrizes)/workers)
        current = 0
        for x in range(1,workers+1):
            data = matrizes[current:current+divisao]
            comm.send(data, dest=x, tag=x)
            current = current + divisao
        doMaster()
        print(resultante)
        print('-----------------')
        print(resultante==checksum)
    else:
        calcular = comm.recv(source=0, tag=rank)
        resultado = None
        for x in calcular:
            if resultado is None:
                resultado = x
            else:
                resultado = multiplicar(resultado, x)

        time.sleep(1)
        comm.send(resultado, dest=0, tag=rank)