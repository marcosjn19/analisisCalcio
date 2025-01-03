import pandas as pd
import numpy  as np
import matplotlib.pyplot as pt
import tkinter as tkt
from tkinter import filedialog as fd
import scipy.signal as sg
import scipy.integrate as sce
import tabulate as tb
from filedialog import filedialog
#----------------   CARGA INICIAL DEL EXCEL  -------------------------
SAVGOL_STRENGTH = 30
SAVGOL_EXPO = 2
inicial = []
ax = None
times = None
valoresPromInicial = []
indicesTPendientesOg = []
maximosOg = []
indicesMitadOg = []
decrementosOg = []
def cargaInicial():
    global inicial
    global ax
    global times
    global valoresPromInicial
    file = filedialog.askopenfilename()
    print ( file )
    #print ( file )
    calcioData = pd.read_excel(file)   #Recuperamos los datos del Excel
    times = calcioData.get("Time")                      #Guardamos los 
    calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
    valoresProm = calcioData.mean(1)                    #Valor promedio inicial
    valoresProm = valoresProm.div(valoresProm.get(0))   #Dividimos sobre promedio inicial para dejar ese como 1
    arrayData = calcioData.values
    
    for i in arrayData:
        inicial.append(np.divide(i,arrayData[0]))
        
    inicial = np.array(inicial)
    valoresProm = np.mean(inicial,1)
    x = np.arange(len(times)) #Representar el tiempo
    fig, ax = pt.subplots()
    ax.set(xlabel='Tiempo', ylabel='Valor', title='Original - Raw Data')
    p1 = ax.plot ( x, inicial, color  = "black",   linewidth = '0.2', label="otros")
    p2 = ax.plot ( x, valoresProm, color = "red", linewidth = '1.5', label="prom")
    ax.figure.canvas.draw()
    fig.savefig("Original-RawData.png")

    fig2, bx = pt.subplots()
    filtrados = sg.savgol_filter     ( inicial, SAVGOL_STRENGTH, SAVGOL_EXPO )
    valoresProm = np.mean ( filtrados, 1 )
    valoresPromInicial = valoresProm
    bx.set(xlabel='Tiempo', ylabel='Valor', title='Original - Raw Data - Filtered')
    p1 = bx.plot ( x, filtrados, color  = "black",   linewidth = '0.2', label="otros")
    p2 = bx.plot ( x, valoresProm, color = "red", linewidth = '1.5', label="prom")
    fig2.savefig("Original - RawData - Filtered.png")
    bx.figure.canvas.draw()
    pt.show()

dx = None
salidaSeleccion = []
figura = None
valoresPromSeleccion = None
def doGraphics(eliminados):
    global dx
    global salidaSeleccion
    global figura
    global valoresPromSeleccion
    salidaSeleccion = None
    pt.cla()
    pt.clf()
    pt.close()
    salidaSeleccion = []
    calcioData = pd.read_excel("./Control_1408.xlsx")   #Recuperamos los datos del Excel
    times = calcioData.get("Time")                      #Guardamos los 
    calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
    for i in eliminados:
        calcioData = calcioData.drop(columns=f'#{i+1} (Blue)')
    
    valoresPromSeleccion = calcioData.mean(1)                    #Valor promedio inicial
    valoresPromSeleccion = valoresPromSeleccion.div(valoresPromSeleccion.get(0))   #Dividimos sobre promedio inicial para dejar ese como 1
    arrayData = calcioData.values
    arrayData = sg.savgol_filter(arrayData, SAVGOL_STRENGTH, SAVGOL_EXPO)
    for i in arrayData:
        salidaSeleccion.append(np.divide(i,arrayData[0]))
    salidaSeleccion = np.array(salidaSeleccion)
    valoresPromSeleccion     = np.mean(salidaSeleccion,1)
    x = np.arange(len(times)) #Representar el tiempo
    figura, dx = pt.subplots()
    dx.set(xlabel='Tiempo', ylabel='Valor', title='Seleccionados')
    p1 = dx.plot ( x, salidaSeleccion, color  = "black",   linewidth = '0.2', label="otros")
    p2 = dx.plot ( x, valoresPromSeleccion, color = "red", linewidth = '1.5', label="Promedio")
    pt.show()

def verCelula(i):
    salida = []
    calcioData = pd.read_excel("./Control_1408.xlsx")   #Recuperamos los datos del Excel
    times = calcioData.get("Time")                      #Guardamos los 
    calcioData = calcioData.drop(columns='Time')        #Eliminamos la columna tiempo
    desiredCel = calcioData.get(f'#{i+1} (Blue)')
    arrayData = desiredCel.values
    for j in arrayData:
        salida.append(np.divide(j, arrayData[0]))

    filtrados = sg.savgol_filter(salida, 60, 2)
    salida = np.array(salida)
    x = np.arange(len(times)) #Representar el tiempo
    fig, dx = pt.subplots()
    dx.set(xlabel='Tiempo', ylabel='Valor', title=f'Celula #{i+1}')
    p2 = dx.plot ( x, salida, color = "red", linewidth ='0.5', linestyle = "dotted", label=f"Celula #{i+1} Original")
    p3 = dx.plot ( x, filtrados, color = "green", linewidth = "0.8", label=f"Celula #{i+1} Filtrada SavGol")
    l = dx.legend(loc='upper right')
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
    doGraphics(eliminados)
    
def guardarSeleccionados():
    global figura
    figura.savefig(fname="Seleccion.png")

def guardarReporte():
    indicesCelulas = []
    indicesTMaximoOg = []
    global indicesTPendientesOg
    pt.cla()
    pt.clf()
    pt.close()
    for i in range(len(inicial[0])):
        indicesCelulas.append(f"Celula #{i+1}")
    dfInicial  = pd.DataFrame  (inicial)
    dfInicial  = dfInicial.set_axis   ( labels=indicesCelulas, axis=1 )
    dfInicial.insert(len(dfInicial.columns), "Celula Promedio", valoresPromInicial)
    dfOriginal = dfInicial
    for i in dfInicial.columns:  # Excluir "Celula Promedio" si es la última columna
        data = pd.to_numeric(dfInicial[i], errors='coerce').dropna().to_numpy()  # Convertir a numérico
        if len(data) > 0:  # Asegúrate de que no está vacío
            max_idx = np.argmax(data)  # Devuelve el índice del máximo
            indicesTMaximoOg.append(max_idx)
        
    #Maximos
    maxInicial = dfInicial.max()
    dfInicial.loc[len(dfInicial.index)+1] = maxInicial  
    dfCalculos = pd.DataFrame({'Promedio Maximos':[maxInicial.mean()]})
    dfInicial.rename(index={len(dfInicial.index):'Maximos'}, inplace=True)
    data = []

    #Amplitud
    maxInicial = maxInicial-1
    dfInicial.loc[len(dfInicial.index)+1] = maxInicial
    dfInicial.rename(index={len(dfInicial.index):'Amplitud'}, inplace=True)
    dfCalculos.insert(1, 'Promedio Amplitud', maxInicial.mean())
    
    #Velocidad subida
    getPendientesOg()
    getMitadOg()
    print ( indicesTMaximoOg ) 
    print ( "-------" ) 
    print ( indicesTPendientesOg)
    indicesTMaximoOg = np.array(indicesTMaximoOg)
    indicesTPendientesOg = np.array(indicesTPendientesOg)
    tiempo = indicesTMaximoOg-indicesTPendientesOg
    helper = []
    print ( tiempo )
    for i in tiempo:
        helper.append(i)
    helper = np.array(helper)
    helper = helper/10
    velocidades = maxInicial / helper
    dfInicial.loc[len(dfInicial.index)+1] = velocidades
    dfInicial.rename(index={len(dfInicial.index):'Velocidades Incremento'}, inplace=True)

    tiempo = indicesMitadOg - indicesTMaximoOg
    helper = []
    for i in tiempo:
        helper.append(i)
    helper = np.array(helper)
    helper = helper/10
    global decrementosOg
    velocidades = (maximosOg - decrementosOg) / helper
    #print ( velocidades )
    dfInicial.loc[len(dfInicial.index)+1] = velocidades
    dfInicial.rename(index={len(dfInicial.index):'Velocidades Decremento'}, inplace=True)
    
    #dfHelper = pd.DataFrame(sce.cumulative_trapezoid(helper) )
    areasBajoCurvaOg = []
    for i in dfOriginal.columns:
        areasBajoCurvaOg.append ( (sce.cumulative_simpson(dfOriginal[i]))[len(i)-1] )
    areasBajoCurvaOg = np.array(areasBajoCurvaOg)
    #print ( areasBajoCurvaOg )
    dfInicial.loc[len(dfInicial.index)+1] = areasBajoCurvaOg
    dfInicial.rename(index={len(dfInicial.index):'Areas bajo la curva'}, inplace=True )

    with pd.ExcelWriter('ReporteGeneral.xlsx') as writer:
        dfInicial.to_excel  (writer, sheet_name="original")
        dfCalculos.to_excel (writer, sheet_name="promediosOriginal")

    return

def getPendientesOg(): #Metodo util para obtener el ms donde inicia la tendencia al alza
    global inicial
    global indicesTPendientesOg
    global maximosOg
    dfInicial = pd.DataFrame(inicial)
    dfInicial.insert(len(dfInicial.columns), "Celula Promedio", valoresPromInicial)
    helper = dfInicial.values

    pendientes = np.gradient(helper)
    dfPendientes = pd.DataFrame(pendientes[0])
    dfPendientes.to_excel('Gradientes.xlsx', 'gradientes')
    
    for i in dfInicial:
        data = dfInicial[i].to_numpy()
        maximosOg.append(np.max(data))

    for i in dfPendientes.columns:  # Iterar sobre todas las columnas
        data = pd.to_numeric(dfPendientes[i], errors='coerce').dropna().to_numpy()  # Asegurarte de trabajar con números
        if len(data) > 0:  # Asegúrate de que no está vacío
            indicesTPendientesOg.append(np.argmax(data))

def getPendientesSel(): #Metodo util para obtener el ms donde inicia la tendencia al alza
    global salidaSeleccion
    global indicesTPendientesOg
    global maximosOg
    dfSeleccion = pd.DataFrame(salidaSeleccion)
    dfSeleccion.insert(len(dfSeleccion.columns), "Celula Promedio", )
    helper = dfSeleccion.values

    pendientes = np.gradient(helper)
    dfPendientes = pd.DataFrame(pendientes[0])
    dfPendientes.to_excel('Gradientes.xlsx', 'gradientes')
    
    for i in dfSeleccion:
        data = dfSeleccion[i].to_numpy()
        maximosOg.append(np.max(data))

    for i in dfPendientes:
        data = dfPendientes[i].to_numpy()
        indicesTPendientesOg.append(np.where(data == np.max(data))[0])

def getMitadOg():
    global inicial
    global indicesTPendientesOg
    global maximosOg
    global decrementosOg
    global indicesMitadOg
    dfInicial = pd.DataFrame(inicial)
    dfInicial.insert(len(dfInicial.columns), "Celula Promedio", valoresPromInicial)
    maximosOg = np.array(maximosOg)
    decrementosOg = (( maximosOg-1 )/2) + 1

    for i, idx in enumerate(indicesTPendientesOg):
        if ( i == 53) :
            break
        print ( idx )
        col_name = dfInicial.columns[i]
        dfInicial[col_name] = dfInicial[col_name][idx + 10:]

    dfInicial = dfInicial.reset_index(drop=True)
    for i, col in enumerate(dfInicial.columns):
        menores = dfInicial[col] < decrementosOg[i]
        if menores.any():
            indice = menores[menores].index[0]
        else:
            indice = None
        
        indicesMitadOg.append(indice)

#----------TKINTER DISPLAY--------------------------------
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

tkt.Button ( frame, text = "Guardar Seleccion", command=lambda *args: guardarSeleccionados()).grid(column=columna, row=renglon+1)
tkt.Button ( frame, text = "Generar Reporte",   command=lambda *args: guardarReporte()).grid(column=columna, row = renglon+2 )
tkt.Button ( frame, text = "TEST BUTTON",   command=lambda *args: getMitadOg()).grid(column=columna, row = renglon+3 )
tkt.Button ( frame, text="Salir", command=root.destroy).grid(column=0, row=len(nCelulas))
root.mainloop()


'''
GUARDAR EN EXCEL
-> Punto maximo                                                                                          ---> PROMEDIO e INDIVIDUAL //////
-> Velocidad de subida                                                                                   ---> PROMEDIO e INDIVIDUAL //////
-> Velocidad de decremento al 50% del pico maximo (Ejemplo: Si el pico es 2 cuanto tardo en llegar a 1)  ---> PROMEDIO e INDIVIDUAL //////
-> Area bajo la curva                                                                                    ---> PROMEDIO e INDIVIDUAL /////
'''