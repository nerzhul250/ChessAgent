class Player():
    
    def __init__(self, color, game):
        self.__color = color
        self.__game = game
        self.__fichas = []
        self.__posiblesCapturas = []
        self.__capturadas = []
        
    def setAdversario(self, adversario):
        self.__adversario = adversario
        
    def agregarFicha(self, ficha):
        self.__fichas.append(ficha)
        
    def eliminarFicha(self, ficha):
        self.__fichas.remove(ficha)
        
    def captura(self, ficha):
        self.__capturadas.append(ficha)
        ficha.capturada = True
        
    def generarJugadas(self):
        for p in self.__fichas:
            self.generarJugadasFicha(p)
            
    def verificarJaque(self):
        return self.__fichas[0] in self.__adversario.posiblesCapturas()
            
    def generarJugadasFicha(self, ficha):
        ficha.movimientos = []
        ficha.posiblesCapturas = []
        ficha.amenazadas = []
        lista = [[],[],[]]
        jaque = self.verificarJaque()
        if not ficha.capturada:
            if ficha.tipo() == "K":
                lista = self.__generarJugadasK(ficha, jaque)
            elif ficha.tipo() == "N":
                lista = self.__generarJugadasN(ficha, jaque)
            elif ficha.tipo() == "B":
                lista = self.__generarJugadasB(ficha, jaque)
            elif ficha.tipo() == "R":
                lista = self.__generarJugadasR(ficha, jaque)
            elif ficha.tipo() == "Q":
                lista = self.__generarJugadasQ(ficha, jaque)
            elif ficha.tipo() == "P":
                lista = self.__generarJugadasP(ficha, jaque)
        
        ficha.movimientos = lista[0]
        ficha.posiblesCapturas = lista[1]
        ficha.amenazadas = lista[2]
            
    def __generarJugadasP(self, ficha, jaque):
        posiblesJugadas = []
        posiblesCapturas = []
        amenazadas = []
        if self.__color:
            mod = -10
            idx = 6
        else:
            mod = +10
            idx = 1
        pos = ficha.pos + mod
        validacion = self.__verificarPosicion(pos)
        if validacion == "E":
            if jaque:
                verifiacion = self.quitaJaque(ficha.pos, pos)
            if not jaque or verifiacion:
                posiblesJugadas.append(pos)
            pos = pos + mod
            validacion = self.__verificarPosicion(pos)
            if ficha.pos // 10 == idx and validacion == "E":
                if jaque:
                    verifiacion = self.quitaJaque(ficha.pos, pos)
                if not jaque or verifiacion:
                    posiblesJugadas.append(pos)
        modificadores = (+1, -1)
        for mod2 in modificadores:
            pos = ficha.pos + mod + mod2
            validacion = self.__verificarPosicion(pos)
            if validacion == (not self.__color):
                if jaque:
                    verifiacion = self.quitaJaque(ficha.pos, pos)
                if not jaque or verifiacion:
                    posiblesJugadas.append(pos)
                    posiblesCapturas.append(self.__game.darFicha(pos))
            if validacion != "O":
                amenazadas.append(pos)
        return posiblesJugadas, posiblesCapturas, amenazadas
    
    def __generarJugadasR(self, ficha, jaque):
        posiblesJugadas = []
        posiblesCapturas = []
        amenazadas = []
        modificadores = (+10, +1, -10, -1)
        for mod in modificadores:
            act = ficha.pos + mod
            validacion = self.__verificarPosicion(act)
            while validacion == "E":
                if jaque:
                    verifiacion = self.quitaJaque(ficha.pos, act)
                if not jaque or verifiacion:
                    posiblesJugadas.append(act)
                    amenazadas.append(act)
                act = act + mod
                validacion = self.__verificarPosicion(act)
            if validacion == (not self.__color):
                if jaque:
                    verifiacion = self.quitaJaque(ficha.pos, act)
                if not jaque or verifiacion:
                    posiblesJugadas.append(act)
                    posiblesCapturas.append(self.__game.darFicha(act))
            if validacion != "O":
                amenazadas.append(act)
        return posiblesJugadas, posiblesCapturas, amenazadas
    
    def __generarJugadasB(self, ficha, jaque):
        posiblesJugadas = []
        posiblesCapturas = []
        amenazadas = []
        modificadores = (+10 + 1, -10 + 1, -10 - 1, +10 - 1)
        for mod in modificadores:
            act = ficha.pos + mod
            validacion = self.__verificarPosicion(act)
            while validacion == "E":
                if jaque:
                    verifiacion = self.quitaJaque(ficha.pos, act)
                if not jaque or verifiacion:
                    posiblesJugadas.append(act)
                    amenazadas.append(act)
                act = act + mod
                validacion = self.__verificarPosicion(act)
            if validacion == (not self.__color):
                if jaque:
                    verifiacion = self.quitaJaque(ficha.pos, act)
                if not jaque or verifiacion:
                    posiblesJugadas.append(act)
                    posiblesCapturas.append(self.__game.darFicha(act))
            if validacion != "O":
                amenazadas.append(act)
        return posiblesJugadas, posiblesCapturas, amenazadas
                
    def __generarJugadasQ(self, ficha, jaque):
        lista = self.__generarJugadasR(ficha, jaque)
        lista1 = self.__generarJugadasB(ficha, jaque)
        lista[0].extend(lista1[0])
        lista[1].extend(lista1[1])
        lista[2].extend(lista1[2])
        return lista[0], lista[1], lista[2]
        
    def __generarJugadasN(self, ficha, jaque):
        posiblesJugadas = []
        posiblesCapturas = []
        amenazadas = []
        modificadores = (+20 + 1, +10 + 2, -10 + 2, -20 + 1, -20 - 1, -10 - 2, +10 - 2, +20 - 1)
        for mod in modificadores:
            pos = ficha.pos + mod
            validacion = self.__verificarPosicion(pos)
            if validacion != "O":
                if jaque and validacion != self.__color:
                    verifiacion = self.quitaJaque(ficha.pos, pos)
                if validacion == (not self.__color) and (not jaque or verifiacion):
                    posiblesJugadas.append(pos)
                    posiblesCapturas.append(self.__game.darFicha(pos))
                elif validacion == "E" and (not jaque or verifiacion):
                    posiblesJugadas.append(pos)    
                else:
                    amenazadas.append(pos)
                    
        return posiblesJugadas, posiblesCapturas, amenazadas
    
    def __generarJugadasK(self, ficha, jaque):
        posiblesJugadas = []
        posiblesCapturas = []
        amenazadas = []
        amenazadasEnemy = self.__adversario.amenazadas()
        modificadores = (+10, +10 + 1, +1, -10 + 1, -10, -10 - 1, -1, +10 - 1)
        for mod in modificadores:
            pos = ficha.pos + mod
            validacion = self.__verificarPosicion(pos)
            if not pos in amenazadasEnemy:
                if validacion == (not self.__color):
                    if jaque:
                        verifiacion = self.quitaJaque(ficha.pos, pos)
                    if not jaque or verifiacion:
                        posiblesJugadas.append(pos)
                        posiblesCapturas.append(self.__game.darFicha(pos))
                elif validacion == "E":
                    if jaque:
                        verifiacion = self.quitaJaque(ficha.pos, pos)
                    if not jaque or verifiacion:
                        posiblesJugadas.append(pos)
            if validacion != "O":
                amenazadas.append(pos)
        return posiblesJugadas, posiblesCapturas, amenazadas
    
    def __verificarPosicion(self, pos):
        i = pos // 10
        j = pos % 10
        if 0 <= i <= 7 and 0 <= j <= 7:
            llegada = self.__game.darFicha(pos)
            if llegada is None:
                return "E"
            else:
                return llegada.color()             
        else:
            return "O"
        
    def quitaJaque(self, o , f):
        fichao = self.__game.darFicha(o)
        fichaf = self.__game.darFicha(f)

        fichao.pos = f
        if fichaf is not None:
            fichaf.capturada = True
                
        self.__game.darBoard()[f] = fichao
        del(self.__game.darBoard()[o])
        
        self.__adversario.generarJugadas()
        resp = not self.verificarJaque()
        
        fichao.pos = o
        self.__game.darBoard()[o] = fichao
        
        if fichaf is not None:
            self.__game.darBoard()[f] = fichaf
            fichaf.capturada = False
        else:
            del(self.__game.darBoard()[f])
            
        self.__adversario.generarJugadas()
        return resp
        
    def posiblesCapturas(self):
        capturas = []
        for p in self.__fichas:
            capturas.extend(p.posiblesCapturas)
        return capturas
    
    def capturas(self):
        return self.__capturadas
    
    def fichas(self):
        return self.__fichas
    
    def darJugadas(self):
        jugadas = []
        for p in self.__fichas:
            for jug in p.movimientos:
                jugadas.append("{:0>2}".format(p.pos) + "{:0>2}".format(jug))
        return jugadas
    
    def amenazadas(self):
        amenazadas = []
        for p in self.__fichas:
            amenazadas.extend(p.amenazadas)
        return amenazadas
    
