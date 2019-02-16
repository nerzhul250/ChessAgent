from model.Game import Game

game = Game()
game.show()

lin = input("Ingresar jugada: ")

while lin != "E":
    if lin.isdecimal():
        entrada = int(lin)
        if len(lin) == 4:
            if entrada < 0 or entrada > 7777:
                print("La entrada debe estar entre 0000 y 7777")
            else:
                try:
                    game.mover(entrada)
                except Exception as e:
                    print(e)
                finally:    
                    game.show()
        elif len (lin) == 2:
            if entrada < 0 or entrada > 77:
                print("La entrada debe estar entre 00 y 77")
            else:
                try:
                    game.seleccionarFicha(entrada)
                except Exception as e:
                    print(e)
                finally:    
                    game.show()
        else:
            print("Ingrese una cordenada para seleccionar ficha o dos para mover")
    else:
        print("La entrada debe ser numerica")
    lin = input("Ingresar jugada: ")
else:
    print("Programa terminado")
    