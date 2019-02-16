from model.Piece import Piece
from model.Player import Player
import numpy as np

class Game ():
    
    def __init__(self):
        self.nuevo()
            
    def nuevo(self):
        self.__player = 0
        self.__board = {}
        self.__finished = False
        p0 = Player(False, self)
        p1 = Player(True, self)
        self.__players = {0:p0, 1:p1}
        p0.setAdversario(p1)
        p1.setAdversario(p0)
        self.__seleccionada = None
        self.__cargarPiezas("inicial")
        
    def seleccionada(self):
        return self.__seleccionada
    
    def getTurno(self):
        return self.__player  
    
    def isFinished(self):
        return self.__finished 
            
    def __cargarPiezas (self, archivo):        
        file = open("../data/" + archivo + ".txt", "r")
        lines = file.readlines()
        for lin in lines:
            dat = lin.split(";")
            idx = int(dat[0])
            ply = int(dat[2])
            p = Piece(dat[1], ply, idx)
            self.__board[idx] = p
            self.__players[ply].agregarFicha(p)
        file.close()
        del(file)
        self.__players[0].generarJugadas()
        self.__players[1].generarJugadas()
        
    def __validarIndices(self, idx):
        
        idxi = idx//10
        if idxi < 0 or idxi > 7:
            raise Exception("La fila indicada debe ser un numero entre 0 y 7")
        
        idxj = idx%10
        if idxj < 0 or idxj > 7:
            raise Exception("La columna indicada debe ser un numero entre 0 y 7")
        
        
    def __validarFormatoInput(self, o, f):
        
        if o == f:
            raise Exception("La casilla de destino debe ser diferente a la de llegada")
        
        try:
            self.__validarIndices(o)
        except Exception as e:
            raise Exception("Error en la posicion de inicio: " + str(e))
        
        try:
            self.__validarIndices(f)
        except Exception as e:
            raise Exception("Error en la posicion de llegada: " + str(e))
        
    def __validarSeleccionFicha(self, idx):
        
        if not idx in self.__board:
            raise Exception ("La casilla seleccionada no contiene ninguna ficha")
        
        ficha = self.__board[idx]
        
        if ficha.color() != self.__player:
            raise Exception ("No puede seleccionar esa ficha")
        
    def darFicha(self, pos):
        self.__validarIndices(pos)
        if pos in self.__board:
            return self.__board[pos]
        else:
            return None
        
    def darBoard(self):
        return self.__board
        
    def seleccionarFicha(self, idx):
        
        self.__validarIndices(idx)
        ficha = self.darFicha(idx)
        
        if self.__seleccionada is None:
            self.__validarSeleccionFicha(idx)
            self.__seleccionada = ficha
            self.__players[self.__player].generarJugadasFicha(ficha)
        else:
            if not ficha is None and self.__seleccionada.color() == ficha.color():
                if self.__seleccionada == ficha:
                    self.__seleccionada = None
                else:
                    self.__seleccionada = ficha
                    self.__players[self.__player].generarJugadasFicha(ficha)
            else:
                self.mover(self.__seleccionada.pos*100+idx)
        
    def mover(self, accion): 
        o = accion//100
        f = (accion%100)
        
        self.__validarFormatoInput(o, f)
        self.__validarSeleccionFicha(o)
        
        fichao = self.__board[o]
        fichao.mover(f)
        
        fichaf = self.darFicha(f)
        
        self.__board[f] = self.__board[o]
        del(self.__board[o])
        
        reward = 0
        
        if fichaf is not None:
            self.__players[self.__player].captura(fichaf)
            #self.__players[not self.__player].eliminarFicha(fichaf)
            if fichaf.tipo() == "K":
                ##Add reward
                self.__finished = True
                reward = 1
#                 if self.__player:
#                     print("Jugador 0 (blanco) pierde")
#                 else:
#                     print("Jugador 1 (negro) pierde")
            elif fichaf.tipo() == "P":
                reward=0.1
            elif fichaf.tipo() == "Q":
                reward=0.9
            elif fichaf.tipo() == "R":
                reward=0.7
            elif fichaf.tipo() == "B":
                reward=0.7
            elif fichaf.tipo() == "N":
                reward=0.7
        self.__seleccionada = None
        
        #Here too
        #if self.__players[self.__player].verificarJaque():
            #reward = -10
        #elif self.__players[not self.__player].verificarJaque():
        #    reward = 3
            
        self.__players[self.__player].generarJugadas()
        self.__player = not self.__player
        self.__players[self.__player].generarJugadas()
        
#         if self.__players[True].verificarJaque():
#             print("Jugador 1 (negro) en jaque")
#             
#         if self.__players[False].verificarJaque():
#             print("Jugador 0 (blanco) en jaque")
        
        if len(self.__players[self.__player].darJugadas()) == 0:
            self.__finished = True
            reward = 1
            print("Jaque mate a jug " + str(self.__player))
        return reward
        
        
    def show(self):
        movs = []
        amenazadas = []
        if not self.__seleccionada is None:
            movs = self.__seleccionada.movimientos
            amenazadas = self.__seleccionada.amenazadas
        seph = "   -------------------------------------------------"
        print(seph)
        for i in range(0,8):
            line = " " + str(7-i) + " | "
            for j in range (0, 8):
                idx = (7-i)*10+j
                if idx in self.__board:
                    line += str(self.__board[idx])
                else:
                    line += "  "
                if idx in movs and idx in amenazadas:
                    line += "*"
                elif idx in movs:
                    line += "+"
                elif idx in amenazadas:
                    line += "x"
                else:
                    line += " "
                line += " | "         
            print(line + "\n" + seph)
        line = "      "
        for i in range(0,8):
            line += str(i) + "     "
        print(line)
        
    def mostrarCapturas(self):
        print("Capturas")
        line = "0- "
        for p in self.__players[0].capturas():
            line += str(p) + " "
        print(line)
        line = "1- "
        for p in self.__players[1].capturas():
            line += str(p) + " "
        print(line)  
        
    def mostrarPosiblesCapturas(self):
        print("Posibles capturas")
        line = "0- "
        for p in self.__players[0].posiblesCapturas():
            line += str(p) + " "
        print(line)
        line = "1- "
        for p in self.__players[1].posiblesCapturas():
            line += str(p) + " "
        print(line)
    
    def darFichasJugW(self):
        return self.__players[0].fichas()
    
    def darFichasJugB(self):
        return self.__players[1].fichas()
    
    def darCapturasJugW(self):
        return self.__players[0].capturas()
    
    def darCapturasJugB(self):
        return self.__players[1].capturas()
    
    def darJugadasJugW(self):
        return self.__players[0].darJugadas()
    
    def darJugadasJugB(self):
        return self.__players[1].darJugadas()
        
    def getActions(self,player):
        if self.__player!=player:
            actions=np.zeros((1,4))
            for i in range(0,4):
                actions[0,i]=-1
            return actions
        jugadas=self.darJugadasJugW()
        if self.__player:
            jugadas=self.darJugadasJugB()
        actions=np.zeros((len(jugadas),4))
        for (x,y) in np.ndenumerate(actions):
            jag=int(jugadas[x[0]])
            if x[1]==0:
                num=jag//1000
                if player==1:
                    num=7-num
            elif x[1]==1:
                num=(jag//100)%10
            elif x[1]==2:
                num=(jag//10)%10
                if player==1:
                    num=7-num
            elif x[1]==3:
                num=jag%10
            actions[x[0],x[1]]=num
        return actions
    
    def getStates(self):
        initial=[[1,0],[2,0],[3,0],[3,0],[4,0],[4,0],[5,0],[5,0],[6,0],[6,0],[6,0],[6,0],[6,0],[6,0],[6,0],[6,0],
                 [1,1],[2,1],[3,1],[3,1],[4,1],[4,1],[5,1],[5,1],[6,1],[6,1],[6,1],[6,1],[6,1],[6,1],[6,1],[6,1]]
        state=np.zeros((32,5))
        for (x,y) in np.ndenumerate(state):
            if(x[1]==0):
                state[x[0],x[1]]=initial[x[0]][1]
            if(x[1]==1):
                state[x[0],x[1]]=0
            if(x[1]==2):
                state[x[0],x[1]]=initial[x[0]][0]
            if(x[1]==3):
                state[x[0],x[1]]=-1
            if(x[1]==4):
                state[x[0],x[1]]=-1
        for elem in self.__board:
            pos=16*self.__board[elem].color()
            if self.__board[elem].tipo()=="Q":
                pos+=1
            elif self.__board[elem].tipo()=="R":
                pos+=2
            elif self.__board[elem].tipo()=="B":
                pos+=4
            elif self.__board[elem].tipo()=="N":
                pos+=6
            elif self.__board[elem].tipo()=="P":
                pos+=8
            while(state[pos,1]==1):
                pos+=1
            state[pos,1]=1
            state[pos,3]=self.__board[elem].pos//10
            state[pos,4]=self.__board[elem].pos%10
        temp=np.split(np.copy(state),2)
        state1=np.append(temp[1],temp[0],axis=0)
        for (x,y) in np.ndenumerate(state1):
            if(x[1]==0):
                if state1[x[0],x[1]]==0:
                    state1[x[0],x[1]]=1
                else:
                    state1[x[0],x[1]]=0
            if(x[1]==3):
                state1[x[0],x[1]]=7-state1[x[0],x[1]]
        
        return np.reshape(state,160),np.reshape(state1,160)