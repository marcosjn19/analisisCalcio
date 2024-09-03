import pandas as pd
import numpy  as np
import matplotlib.pyplot as pt
import tkinter as tkt

#----------------   CARGA INICIAL DEL EXCEL  -------------------------
calcioData = pd.read_excel("./Control_1408.xlsx")   #Recuperamos los datos del Excel
times = calcioData.get("Time")                      #Guardamos los 
calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
valoresProm = calcioData.mean(1)                    #Valor promedio inicial
valoresProm = valoresProm.div(valoresProm.get(0))   #Dividimos sobre promedio inicial para dejar ese como 1
arrayData = calcioData.values

salida = []
for i in arrayData:
    salida.append(np.divide(i,arrayData[0]))
salida = np.array(salida)
#------------------------ METODOS GRAFICA -------------------------------
valoresProm = np.mean(salida,1)
valroesProm = valoresProm/valoresProm[0]
x = np.arange(len(times)) #Representar el tiempo
fig, ax = pt.subplots()
ax.set(xlabel='Tiempo', ylabel='Valor', title='Test #1')
p1 = ax.plot ( x, salida, color  = "black",   linewidth = '0.2', label="otros")
p2 = ax.plot ( x, valoresProm, color = "red", linewidth = '1.5', label="prom")

#------------------     METODOS INTERFAZ    -------------------------
root = tkt.Tk()
frame = tkt.Frame(root)
frame.grid()
nCelulas = []
for i in range ( len( salida[0] )):
    nCelulas.append(tkt.IntVar(frame, 1))
        
def seleccion():
    global salida
    ax.clear()
    ax.set(xlabel='Tiempo', ylabel='Valor', title='Test #1')
    for i in range(len(nCelulas)):
        if (nCelulas[i].get() == 0):
            print (f'Celula {i} desactivada')
    #pt.show()

columna = 0
renglon = 0
for i in range ( len(nCelulas) ):
    test = tkt.Checkbutton(frame, text = "Celula #"+str(i), variable=nCelulas[i], onvalue=1, offvalue=0, command=seleccion)
    test.grid(column=columna, row = (i - renglon))
    if ( i % 15 == 0 and i != 0):
        columna+=1
        renglon += 15

tkt.Button(frame, text="Salir", command=root.destroy).grid(column=0, row=len(nCelulas))

#-------------------------------------------------------------------------
root.mainloop()
