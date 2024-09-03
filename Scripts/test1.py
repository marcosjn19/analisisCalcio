'''
REQUIREMENTS
numpy
pandas
scipy
xlrd
openpyxl
matplotlib
'''
import pandas as pd
import numpy  as np
import matplotlib.pyplot as pt


calcioData = pd.read_excel("./Control_1408.xlsx")   #Recuperamos los datos del Excel
times = calcioData.get("Time")                      #Guardamos los 
calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
valoresProm = calcioData.mean(1)                    #Valor promedio inicial
valoresProm = valoresProm.div(valoresProm.get(0))   #Dividimos sobre promedio inicial para dejar ese como 1
arrayData = calcioData.values

salida = []
for i in arrayData:
    salida.append(np.divide(i,arrayData[0]))
'''
medias = np.mean(salida, 0)
print (medias)
zS = np.abs(stats.zscore(medias))
tE = 0
for i in range(len(zS)):
    if ( zS[i] > 1 ):
        salida = np.delete(salida, [i-tE], 1 )
        tE += 1
'''
print ( len(salida[0]) )
valoresProm = np.mean(salida,1)
valroesProm = valoresProm/valoresProm[0]
x = np.arange(len(times)) #Representar el tiempo
fig, ax = pt.subplots()
ax.set(xlabel='Tiempo', ylabel='Valor', title='Test #1')
p1 = ax.plot ( x, salida, color  = "black",   linewidth = '0.2', label="otros")
p2 = ax.plot ( x, valoresProm, color = "red", linewidth = '1.5', label="prom")

ax.figure.canvas.draw()

pt.show()
'''
MOSTRAR PROMEDIO DE TODAS
fig, ax = pt.subplots()
ax.plot(times, valoresProm)
ax.set(xlabel='Tiempo', ylabel='Valor', title='Test #1' )
fig.savefig("Test1.png")
pt.show()
'''