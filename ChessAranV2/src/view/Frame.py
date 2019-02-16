from tkinter import Tk, Frame, Label, Button
from _functools import partial
from model.Game import Game
from mundo.Qnetwork import Qnetwork
import numpy as np
import tensorflow as tf
from tkinter.messagebox import showinfo

bg1 = "#4d2600"
bg2 = "#663300"

modelo = Game()
btns = []
lbls = []
pcs = []

tf.reset_default_graph()
mainQN = Qnetwork(500,[500,500,10])
init = tf.global_variables_initializer();
saver = tf.train.Saver()

sess = tf.Session()

sess.run(init)
ckpt = tf.train.get_checkpoint_state("../../dqn")
saver.restore(sess,ckpt.model_checkpoint_path)

def formatoLbl(lbl):
    lbl.config(bg = bg1, fg = "white", width = "3", height = "1")
    lbl.config(anchor = "center", justify = "center", font = ("Algerian", 16, "bold"))
  
def jugadaIA():
    _,estado=modelo.getStates()
    acciones=modelo.getActions(1)
    a2=0
    val=-500
    a=0
    for act in acciones:
        entrada=np.reshape(np.append(estado,act,axis=0),(1,164))
        tempVal=sess.run(mainQN.Qout,feed_dict={mainQN.inputs:entrada})
        print(str(act) + str(tempVal))
        if tempVal>val:
            a=a2
            val=tempVal
        a2+=1
    mov0=7-int(float(acciones[a][0]))
    mov1=int(float(acciones[a][1]))
    mov2=7-int(float(acciones[a][2]))
    mov3=int(float(acciones[a][3]))
    movimiento=str(mov0)+str(mov1)+str(mov2)+str(mov3)
    print(movimiento)
    modelo.mover(int(movimiento))  
  
def action(i,j):
    try:
        modelo.seleccionarFicha(i*10+j)
    except Exception as e:
        print(e)
        showinfo("Error", e)
    update() 
    if not modelo.isFinished() and modelo.getTurno():
        jugadaIA()
        update()   
    
def update():
    for i in range(0,8):
        for j in range(0,8):
            if (i+j)%2 == 0:
                btns[i][j].config(bg = "#dfbe9f", activebackground = "#dfbe9f")
            else:
                btns[i][j].config(bg = "#c68c53", activebackground = "#c68c53")
            ficha = modelo.darFicha(70-i*10+j)
            if not ficha is None:
                btns[i][j].config(text = ficha.code())
            else :
                btns[i][j].config(text = "")
    
    seleccionada = modelo.seleccionada()
    if not seleccionada is None:
        movs = seleccionada.movimientos
        caps = seleccionada.posiblesCapturas
        amen = []
        for p in caps:
            amen.append(p.pos)
        for pos in movs:
            i = pos//10
            j = pos%10
            if pos in amen:
                if (7-i+j)%2 == 0:
                    btns[7-i][j].config(bg = "#df9f9f")
                else:
                    btns[7-i][j].config(bg = "#c65353")
            else:
                if (7-i+j)%2 == 0:
                    btns[7-i][j].config(bg = "#9fcfdf")
                else:
                    btns[7-i][j].config(bg = "#53a9c6")

    i = 0
    for p in pcs[1]:
        if p in modelo.darCapturasJugB():
            lbls[1][i].config(fg = "black", font = ("Algerian", 24))
        i = i+1
   
    i = 0
    for p in pcs[0]:
        if p in modelo.darCapturasJugW():
            lbls[0][i].config(fg = "black", font = ("Algerian", 24))
        i = i+1
    
    if (modelo.isFinished()):
        for lin in btns:
            for b in lin:
                b.config(state = "disable")
        mensaje = "El jugador "
        if (modelo.getTurno()):
            mensaje = mensaje +"Blanco"
        else:
            mensaje = mensaje +"Negro"
        showinfo("Juego terminado", mensaje + " gana")
    
top = Tk()
top.title("ANN - Chess Master")
top.resizable(False, False)
top.iconbitmap("../data/icon.ico")
#top.geometry("400x400")

fr = Frame(top, bg = bg1)
fr.pack(side = "left")

lbl = Label(fr, text = "")
formatoLbl(lbl)
lbl.grid(row = 0, column = 10)
lbl = Label(fr, text = "")
formatoLbl(lbl)
lbl.grid(row = 10, column = 0)

letras = ("A","B","C","D","E","F","G","H")
for i in range(0,8):
    lbl = Label(fr, text = letras[i])
    formatoLbl(lbl)
    lbl.grid(row = 0, column = i+1)
    lbl = Label(fr, text = str(8-i))
    formatoLbl(lbl)
    lbl.grid(row = i+1, column = 0)

for i in range(0,8):
    btns.append([])
    for j in range(0,8):
        btn = Button(fr)
        btn.config(width = "3", height = "1",font = ("", 28))
        btn.config(command = partial(action, 7-i, j ), bd = 0)
        btn.grid(row = i+1, column = j+1)
        btns[i].append(btn)

fr2 = Frame(top, bg = bg2, width = "300", height = "620")
fr2.pack(expand = True, fill = "y", side = "right")

lbl = Label(fr2, text = "Capturas")
lbl.config(bg = bg2, fg = "white", width = "10", height = "1", pady = 25)
lbl.config(anchor = "center", justify = "center", font = ("Algerian", 18, "bold"))
lbl.grid(row = 1, column = 1, columnspan = 4)

lbl = Label(fr2, text = "Jugador Blanco")
lbl.config(bg = bg2, fg = "white", width = "20", height = "1", pady = 5)
lbl.config(anchor = "center", justify = "center", font = ("Algerian", 12))
lbl.grid(row = 2, column = 1, columnspan = 4)

lbl = Label(fr2)
lbl.config(bg = bg2)
lbl.grid(row = 3)

lbls.append([])
pcs.append([])
r = 4
c = 1
for p in modelo.darFichasJugB():
    lbl = Label(fr2, text = p.code())
    lbl.config(bg = bg2, fg = "#4d2800", width = "2", height = "1")
    lbl.config(anchor = "center", justify = "center", font = ("Algerian", 24))
    lbl.grid(row = r, column = c)
    lbls[0].append(lbl)
    pcs[0].append(p)
    if c < 4:
        c = c+1
    else:
        r = r+1
        c = 1
        
lbl = Label(fr2)
lbl.config(bg = bg2)
lbl.grid(row = 8, pady = 10)

lbl = Label(fr2, text = "Jugador Negro")
lbl.config(bg = bg2, fg = "white", width = "20", height = "1")
lbl.config(anchor = "center", justify = "center", font = ("Algerian", 12))
lbl.grid(row = 9, column = 1, columnspan = 4)

lbl = Label(fr2)
lbl.config(bg = bg2)
lbl.grid(row = 10)

lbls.append([])
pcs.append([])
r = 11
c = 1
for p in modelo.darFichasJugW():
    lbl = Label(fr2, text = p.code())
    lbl.config(bg = bg2, fg = "#4d2800", width = "2", height = "1")
    lbl.config(anchor = "center", justify = "center", font = ("Algerian", 24))
    lbl.grid(row = r, column = c)
    lbls[1].append(lbl)
    pcs[1].append(p)
    if c < 4:
        c = c+1
    else:
        r = r+1
        c = 1
        
update()

top.mainloop()
