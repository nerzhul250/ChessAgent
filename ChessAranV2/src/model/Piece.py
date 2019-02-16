class Piece():

    def __init__(self, tipo, color, pos):
        self.__type = tipo
        self.__color = color
        self.pos = pos
        self.movimientos = []
        self.amenazadas = []
        self.posiblesCapturas = []
        self.capturada = False
        
    def __str__(self):
        return self.__type + str(self.__color)
    
    def tipo(self):
        return self.__type
    
    def color(self):
        return self.__color
    
    def mover(self, f):
        if f in self.movimientos:
            self.pos = f
        else:
            raise Exception("La pieza no se puede mover a la casilla seleccionada")

    def code(self):
        if not self.__color:
            if self.__type == "K":
                return "\u2654"
            elif self.__type == "Q":
                return "\u2655"
            elif self.__type == "R":
                return "\u2656"
            elif self.__type == "B":
                return "\u2657"
            elif self.__type == "N":
                return "\u2658"
            elif self.__type == "P":
                return "\u2659"
        else:
            if self.__type == "K":
                return "\u265A"
            elif self.__type == "Q":
                return "\u265B"
            elif self.__type == "R":
                return "\u265C"
            elif self.__type == "B":
                return "\u265D"
            elif self.__type == "N":
                return "\u265E"
            elif self.__type == "P":
                return "\u265F"
            