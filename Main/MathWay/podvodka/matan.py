import math

def transpose(x):
    xT = [[0 for i in range(len(x))] for j in range(len(x[0]))]
    for i in range(len(x)):
        for j in range(len(x[0])):
            xT[j][i]=x[i][j]
    return xT

def multiplMatrix(x, y):
    res = []  
    for i in range(len(x)):
        row = []
        for j in range(len(y[0])):
            el = 0
            for k in range(len(y)):
                el+=x[i][k]*y[k][j]
            row.append(round(el, 4))
        res.append(row)
    return res

def minor(x, i, j):
    m = [row[:] for row in x]
    for row in m:
        row.pop(j)
    m.pop(i)
    return m

def AlgAd(x):
    M_AlgAd = []
    for i in range(len(x[0])):
        row = []
        for j in range(len(x)):
            M = minor(x, i, j)
            a = round(det(M)*((-1)**((i+1)+(j+1))), 3)
            row.append(a)
        M_AlgAd.append(row)
    return M_AlgAd

def det(x): 
    if len(x) == 1:
        return (x[0][0])
    D = 0
    for i in range(len(x[0])):
        A = det(minor(x, 0, i))
        D+=(x[0][i])*A*((-1)**(i))
    
    return round(float(D), 3)

def average(x):
    return sum(x)/len(x)

def UmnojNaNum(x, k):
    res = [[x[i][j]*k for j in range(len(x[0]))] for i in range(len(x))]
    return res

def difference(x, y):
    res = [[round(x[i][j]-y[i][j], 2) for j in range(len(x[0]))] for i in range(len(x))]
    return res

X = [[1, 17, 130, 523, 2517], 
     [1, 22,  180, 518, 2801], 
     [1, 18,  217, 510, 2573],  
     [1, 24, 103, 516, 2643], 
     [1, 19, 171, 511, 2801], 
     [1, 20, 180, 471, 2815], 
     [1, 17,  140, 523, 2527], 
     [1, 21, 92, 498, 2735], 
     [1, 18,  173, 542, 2817], 
     [1, 22,  87, 501, 2736], 
     [1, 20,  93, 471, 2682], 
     [1, 17, 210, 523, 2593],
     [1, 15, 110, 538, 2627], 
     [1, 21, 86, 472, 2532],
     [1, 15, 175, 467, 2693]]

Y = [[401],
     [452],
     [478], 
     [397], 
     [453], 
     [427], 
     [396], 
     [399], 
     [418], 
     [413], 
     [412], 
     [423], 
     [393], 
     [381], 
     [401]]
 
n = len(Y)
m = 4

Xt = transpose(X)

XX = multiplMatrix(Xt, X)
detX = det(XX)
invXX = (transpose(AlgAd(XX)))

INV = []
for r in invXX:
    row = []
    for el in r:
        row.append(el/detX)
    INV.append(row)

XX_Xt = multiplMatrix(INV, Xt)

B = multiplMatrix(XX_Xt, Y)

print(f'1/{round(det(XX), 3)}\n')
print("Inverted Matrix X'X")
for row in invXX:
    print(row)
print('\n Transposed X:')
for row in Xt:
    print(row)
print('\n Matrix Y:')
for row in Y:
    print(row)
print('\n Matrix B:')
for row in B:
    print(row)
print('')

TrB = transpose(B)
bX = multiplMatrix(TrB, Xt)
bXy = int(multiplMatrix(bX, Y)[0][0])
#print(f'B*X*Y = {bXy}')

AvY = sum(Y[i][0] for i in range(n))/n

nY2 = n*AvY

YtY = int(multiplMatrix(transpose(Y), Y)[0][0])

#print(f"Y'*Y = {YtY}")

R2 = round(1-((YtY-bXy)/(YtY-nY2)), 3)

#Расчёт переменной Epsilon, необходимой в расчётах

Eps = difference(Y, multiplMatrix(X, B))
print(f'Epsilon = Y - X*B:')
for el in Eps:
    print(el)

print(f'\nEpsilon^2: ')
SumEps = 0
for el in Eps:
    print(f'[{round(el[0]**2, 4)}]')
    SumEps+=round(el[0]**2, 4)

S2E = SumEps/(n-m-1)

print(f'\nS2E - Сумма квадратов всех эл-тов матрицы Eps,', 
      f'\nделённая на (n-m-1) - равна: {S2E} ')

Sy = round(math.sqrt(YtY/n - AvY**2), 4)

print('')

SB = []
for i in range(len(invXX)):
    Bii = S2E*invXX[i][i]/detX 
    el = round(math.sqrt(Bii), 3)
    print(f'S^2B{i} = S2E*b{i+1}{i+1}', 
          f'= {round(S2E, 4)}*{round(invXX[i][i]/detX, 4)}', 
          f'= {round(Bii,4)}, SB{i} = {el}')
    SB.append(el)

print(f'\nR^2 = {R2}\n')

K = []
for i in range(1, len(X[0])):
    print(f'a{i} = {B[i][0]}*({SB[i]}/{Sy})', 
          f'= {round(B[i][0]*(SB[i]/Sy), 4)}')
    el = round(B[i][0]*(SB[i]/Sy), 4)
    K.append(el)

maxInfluence = 0
index = 0
for i in range(len(K)):
    maxInfluence = max(maxInfluence, abs(K[i]))
for el in K:
    if maxInfluence==abs(el):
        index = K.index(el)+1
print(f'Максимально эффективно влияет элемент Xi{index}')
print(SB)