import pandas as pd
import numpy  as np
import matplotlib.pyplot as pt
import tkinter as tkt
import statsmodels.api as stat
import scipy.signal as sg
#----------------   CARGA INICIAL DEL EXCEL  -------------------------
SM_TREND = 0.035
SM_LEVEL = 0.02
SM_EXPO = True

inicial = []
ax = None
times = None
pt.figure(figsize=(10,6))
def cargaInicial():
    global inicial
    global ax
    global times
    calcioData = pd.read_excel("./Control_1408.xlsx")   #Recuperamos los datos del Excel
    times = calcioData.get("Time")                      #Guardamos los 
    calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
    valoresProm = calcioData.mean(1)                    #Valor promedio inicial
    valoresProm = valoresProm.div(valoresProm.get(0))   #Dividimos sobre promedio inicial para dejar ese como 1
    arrayData = calcioData.values

    for i in arrayData:
        inicial.append(np.divide(i,arrayData[0]))
        
    inicial = np.array(inicial)
    for i in inicial.T:
        suavizado   = stat.tsa.Holt(i).fit()
        i = suavizado.fittedvalues

    #------------------------ METODOS GRAFICA -------------------------------
    valoresProm = np.mean(inicial,1)
    smoothing_model = stat.tsa.Holt(valoresProm).fit()
    smoothed_values = smoothing_model.fittedvalues
    x = np.arange(len(times)) #Representar el tiempo
    fig, ax = pt.subplots()
    ax.set(xlabel='Tiempo', ylabel='Valor', title='Test #1')
    p1 = ax.plot ( x, inicial, color  = "black",   linewidth = '0.2', label="otros")
    p2 = ax.plot ( x, smoothed_values, color = "red", linewidth = '1.5', label="prom")
    ax.figure.canvas.draw()
    fig.savefig("Original.png")
    pt.show()

dx = None
salida = []
figura = None
def doGraphics(eliminados):
    global dx
    global salida
    global figura
    del salida
    pt.cla()
    pt.clf()
    pt.close()
    salida = []
    calcioData = pd.read_excel("./Control_1408.xlsx")   #Recuperamos los datos del Excel
    times = calcioData.get("Time")                      #Guardamos los 
    calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
    for i in eliminados:
        calcioData = calcioData.drop(columns=f'#{i+1} (Blue)')
    
    valoresProm = calcioData.mean(1)                    #Valor promedio inicial
    valoresProm = valoresProm.div(valoresProm.get(0))   #Dividimos sobre promedio inicial para dejar ese como 1
    arrayData = calcioData.values
    for i in arrayData:
        salida.append(np.divide(i,arrayData[0]))
    salida = np.array(salida)
    #------------------------ METODOS GRAFICA -------------------------------
    valoresProm = np.mean(salida,1)
    valroesProm = valoresProm/valoresProm[0]
    x = np.arange(len(times)) #Representar el tiempo
    figura, dx = pt.subplots()
    dx.set(xlabel='Tiempo', ylabel='Valor', title='Seleccionados')
    p1 = dx.plot ( x, salida, color  = "black",   linewidth = '0.2', label="otros")
    p2 = dx.plot ( x, valoresProm, color = "red", linewidth = '1.5', label="prom")
    #dx.figure.canvas.draw()
    pt.show()

def verCelula(i):
    salida = []
    salidaF = []
    calcioData = pd.read_excel("./Control_1408.xlsx")   #Recuperamos los datos del Excel
    times = calcioData.get("Time")                      #Guardamos los 
    calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
    desiredCel = calcioData.get(f'#{i+1} (Blue)')

    arrayData = desiredCel.values
    

    for j in arrayData:
        salida.append(np.divide(j, arrayData[0]))

    filtrados = sg.savgol_filter(salida, 60, 2)
    salida = np.array(salida)
    #suavizado   = stat.tsa.ExponentialSmoothing(salidaF, trend="add").fit(use_brute=True)
    #suavizadoValues = suavizado.fittedvalues
    x = np.arange(len(times)) #Representar el tiempo
    fig, dx = pt.subplots()
    dx.set(xlabel='Tiempo', ylabel='Valor', title=f'Celula #{i+1}')
    p2 = dx.plot ( x, salida, color = "red", linewidth ='0.5', linestyle = "dotted", label=f"Celula #{i+1} Original")
    #p1 = dx.plot ( x, suavizadoValues, color  = "blue",   linewidth = '1', linestyle="dashed", label=f"Celula #{i+1} Suavizada")
    p3 = dx.plot ( x, filtrados, color = "green", linewidth = "0.8", label=f"Celula #{i+1} Filtrada SavGol")
    l = dx.legend(loc='upper right')
    #dx.figure.canvas.draw()
    pt.show()
#------------------     METODOS INTERFAZ    -------------------------
root = tkt.Tk()
frame = tkt.Frame(root)
frame.grid()
nCelulas = []
cargaInicial()
for i in range ( len( inicial[0] )):
    nCelulas.append(tkt.IntVar(frame, 1))
    
def seleccion():
    eliminados = []
    for i in range(len(nCelulas)):
        if (nCelulas[i].get() == 0):
            eliminados.append(i)
            #print (f'Celula {i} desactivada')
    doGraphics(eliminados)
    
def guardarSeleccionados():
    global figura
    figura.savefig(fname="Seleccionados.png")

columna = 0
renglon = 0

for i in range ( len(nCelulas) ):
    test = tkt.Checkbutton(frame, text = "Celula #"+str(i+1), variable=nCelulas[i], onvalue=1, offvalue=0, command=seleccion)
    test.grid(column=columna, row = (i - renglon))
    ver = tkt.Button(frame, text=f"Ver {i+1}", command=lambda idx = i:verCelula(idx))
    ver.grid(column=columna+1, row=(i-renglon))     
    if ( i % 15 == 0 and i != 0):
        columna+=2
        renglon += 15

tkt.Button(frame, text ="Guardar Seleccion", command=lambda *args: guardarSeleccionados()).grid(column=columna, row=renglon+1)
tkt.Button(frame, text="Salir", command=root.destroy).grid(column=0, row=len(nCelulas))

#ax.figure.canvas.draw()
#pt.show()
#-------------------------------------------------------------------------
root.mainloop()


'''
GUARDAR EN EXCEL
-> Punto maximo                                                                                          ---> PROMEDIO e INDIVIDUAL
-> Velocidad de subida                                                                                   ---> PROMEDIO e INDIVIDUAL
-> Velocidad de decremento al 50% del pico maximo (Ejemplo: Si el pico es 2 cuanto tardo en llegar a 1)  ---> PROMEDIO e INDIVIDUAL
-> Area bajo la curva                                                                                    ---> PROMEDIO e INDIVIDUAL
'''