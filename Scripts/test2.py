import tkinter as tkt

root = tkt.Tk()
frame = tkt.Frame(root)
frame.grid()

testing = []
testing.append(tkt.IntVar()) 

def seleccion():
    if ( testing[0].get() == 1):
        print("Activado")

tkt.Checkbutton(frame, text = "Test", variable=testing[0], onvalue=1, offvalue=0, command=seleccion).grid(column=0, row = 0)
tkt.Button(frame, text="Salir", command=root.destroy).grid(column=0, row=1)
if ( testing[0].get() ):
    print ( "Desactivado" )

root.mainloop()