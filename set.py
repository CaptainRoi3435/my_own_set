import itertools
import pygame
import sys
from random import randint as sample
from numpy import array

######################### Modulo cartas ##################################

class Cartas(pygame.sprite.Sprite):
    def __init__(self, numero, color, forma, relleno, imagen, coor_x = 0, coor_y = 0):
        super().__init__
        self.numero = numero
        self.color = color
        self.forma = forma
        self.relleno = relleno
        self.imagen = pygame.image.load(imagen) # Descargamos la imagen que reprenta la carta 
        self.coor_x = coor_x
        self.coor_y = coor_y
        self.rect = pygame.Rect(self.coor_x, self.coor_y, 237, 164) 
        self.visible = False
        self.estar = True 
        self.recuadro = True # Banderas

    # Al llamar a este metodo ponemos la imagen de la carta en la pantalla
    def draw_image(self, screen):
        if self.estar:
            screen.blit(self.imagen, (self.coor_x, self.coor_y))

    # Al llamar este metodo, se dibuja un recuadro que simula que la carta fue escogida
    def show_select(self, screen):
        if self.visible:
            pygame.draw.rect(screen, (135,206,250), (self.coor_x-5,self.coor_y-5,248,174), border_radius = 30)

    # Es metodo revisa si la carta fue clikeada
    def checkpoint(self, x, y):
        # collidepoint revisa si el el punto (x,y) está en self.rect
        if self.recuadro:
            return self.rect.collidepoint(x, y)
        else:
            return False

######################## verificadora de sets ###########################

def adecuada(conjunto):
    if len(conjunto) == 2:
        return 0
    else:
        return 1

def subsets(terna):
    numbers = [terna[i].numero for i in range(3)]
    colors = [terna[i].color for i in range(3)]
    shapes = [terna[i].forma for i in range(3)]
    fill = [terna[i].relleno for i in range(3)]
    subset = [numbers, colors, shapes, fill]

    return subset

def verificadora(terna):
    check = subsets(terna)
    contador = 0
    for lista in check:
        contador = contador + adecuada(set(lista))
    if contador == 4:
        # Es set
        return True
    else:
        # No es set
        return False

###################### Mesa valida #######################################

def mesa_valida(cartas):
    combinaciones = list(itertools.combinations(list(range(len(cartas))),3))
    ternas = []
    for indcom in combinaciones:
        a = []
        for j in indcom:
            a.append(cartas[j])
        ternas.append(a)

    valida = False
    for terna in ternas:
        if verificadora(terna):
            valida = True

    return valida

###################### Botones ###########################################

class Botones:
    def __init__(self, coor_x, coor_y, imagen):
        self.imagen = pygame.image.load(imagen)
        self.coor_x = coor_x
        self.coor_y = coor_y
        self.rect = pygame.Rect(self.coor_x, self.coor_y, 210, 132)
        self.selec = False
        self.visible = True 
        self.checar = True

    def seleccion(self, screen):
        if self.selec:
            pygame.draw.rect(screen, (135,206,250), (self.coor_x-5,self.coor_y-5, 215, 137), border_radius = 25)

    def visibles(self, screen):
        if self.visible:
            screen.blit(self.imagen, (self.coor_x, self.coor_y))

    def checkpoint(self, x, y):
        # collidepoint revisa si el el punto (x,y) está en self.rect
        if self.checar:
            return self.rect.collidepoint(x, y)
        else:
            return False


###################### Juego #################################
# Crear botones
boton_jugar = Botones(420, 183, "cartas/boton_jugar.png")
boton_como = Botones(420, 335, "cartas/boton_comojugar.png")
botones = [boton_jugar, boton_como]

# Crear las cartas
cartas = []
numeros = [1,2,3]
colores = ["morado", "rojo", "verde"]
formas = ["ovalo", "rombo", "ese"]
rellenos = ["solido", "sin", "rayas"]

# Iteramos en el orden de las listas
for num in numeros:
    for color in colores:
        for  forma in formas:
            for relleno in rellenos:
                imagen = "cartas/" + str(num) + color + forma + relleno + ".png"
                carta = Cartas(num, color, forma, relleno, imagen)
                cartas.append(carta)

# Escoger las primeras 12 cartas (El que haya set se revisara luego)
tablero = []
for i in range(12):
    a = sample(0,len(cartas)-1)
    b = cartas.pop(a)
    tablero.append(b)

# Anotamos las coordenadas de las posiciones de las cartas
posiciones1 = [(20, 20), (20+237+20, 20), (20+2*237+2*20, 20), (20+3*237+3*20, 20)]
posiciones2 = [(20, 20+165+20), (20+1*237+1*20, 20+165+20), (20+2*237+2*20, 20+165+20), (20+3*237+3*20, 20+165+20)]
posiciones3 = [(20, 20+2*165+2*20), (20+1*237+1*20, 20+2*165+2*20), (20+2*237+2*20, 20+2*165+2*20), (20+3*237+3*20, 20+2*165+2*20)]
posiciones4 = [(20, 20+3*165+3*20), (20+1*237+1*20, 20+3*165+3*20), (20+2*237+2*20, 20+3*165+3*20), (20+3*237+3*20, 20+3*165+3*20)]
posiciones = posiciones1 + posiciones2 + posiciones3 + posiciones4

# Iniciamos pygame

pygame.init()
width, height = 1050, 650 # Dimensiones de la ventana del juego
screen = pygame.display.set_mode((width, height)) # Creamos la ventana
pygame.display.set_caption('SET') # Titulo
clock = pygame.time.Clock() # Reloj

# Fuente para el texto del cronometro
font = pygame.font.Font(None, 36)

# Inicializar el cronometro
inicio = pygame.time.get_ticks()
tiempo = 0

# Puntaje
puntaje = 0

seleccionadas = []
sustitutos = []
existencia = []
descarte_final = []
bot = []

menu = 0

minutos = 0
segundos = 0 

boton_como.visible = False 

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Obtener la posición del mouse al hacer clic
            mouse_x, mouse_y = pygame.mouse.get_pos()

            # Crear el vector identificador
            for i in range(2):
                vv = botones[i].checkpoint(mouse_x, mouse_y)
                bot.append(vv)
            if bot.count(True) == 1:
                menu = 1
            bot.clear()
            for i in range(12):
                vv = tablero[i].checkpoint(mouse_x, mouse_y)
                existencia.append(vv)
            if existencia.count(True) == 1:
                vector_tabla = array(tablero)
                carta = vector_tabla[existencia][0]
                existencia.clear()
                if carta not in seleccionadas:
                    carta.visible = True
                    seleccionadas.append(carta)
                else:
                    carta.visible = False
                    seleccionadas.remove(carta)
            else:
                existencia.clear()

    if menu == 0:
        screen.fill((255, 255, 255))
        boton_jugar.visibles(screen)
        boton_como.visibles(screen)

    elif menu == 1:
        # Limpiar la pantalla  
        screen.fill((255, 255, 255))
        pygame.draw.rect(screen, (112, 48, 160), (0, 595, 1050, 55)) # rectangulo morado
        texto_puntaje = font.render(f"Puntaje: {puntaje}", True, (255, 255, 255))
        screen.blit(texto_puntaje, (20, 610))


        if len(cartas + tablero) > 20:
            # Revisar si ya hay suficientes cartas y revisar
            if len(seleccionadas) == 3:
                if verificadora(seleccionadas):
                    puntaje += 1
                    for carta in seleccionadas:
                        carta.visible = False
                    for i in range(3):
                        num_sus = sample(0, len(cartas)-1)
                        sustituto = cartas.pop(num_sus)
                        sustitutos.append(sustituto)
                    for i in range(3):
                        indice = tablero.index(seleccionadas[i])
                        tablero[indice] = sustitutos[i]
                    sustitutos.clear()
                else:
                    for carta in seleccionadas:
                        carta.visible = False
                seleccionadas.clear()

            # Poner 12 cartas
            if mesa_valida(tablero):
                for i in range(12):
                    coor = posiciones[i]
                    carta = tablero[i]
                    carta.coor_x = coor[0]
                    carta.coor_y = coor[1]
                    carta.rect = pygame.Rect(coor[0], coor[1], 237, 165)
                    carta.show_select(screen)
                    carta.draw_image(screen)
            else:
                Flag = True
                for i in tablero:
                    cartas.append(i)
                tablero.clear()
                while Flag: 
                    for i in range(12):
                        a = sample(0,len(cartas)-1) # El -1 es porque sample(a,b) escoge en el [a,b]
                        b = cartas.pop(a)
                        tablero.append(b)
                    if mesa_valida(tablero):
                        Flag = False
                    else:
                        for i in tablero:
                            cartas.append(i)
                        tablero.clear()
        else:
            if mesa_valida(cartas + tablero):
                if len(seleccionadas) == 3:
                    if verificadora(seleccionadas):
                        puntaje += 1
                        # En caso de ser set
                        if len(cartas) > 3:
                            for carta in seleccionadas:
                                carta.visible = False
                            for i in range(3):
                                num_sus = sample(0, len(cartas)-1)
                                sustituto = cartas.pop(num_sus)
                                sustitutos.append(sustituto)
                            for i in range(3):
                                indice = tablero.index(seleccionadas[i])
                                tablero[indice] = sustitutos[i]
                            sustitutos.clear()
                        else:
                            for carta in seleccionadas:
                                carta.visible = False
                                carta.estar = False
                                carta.recuadro = False
                                descarte_final.append(carta)
                            tablero_final = []
                            for carta in tablero:
                                if carta not in descarte_final:
                                    tablero_final.append(carta)
                            if mesa_valida(tablero_final):
                                pass
                            else:
                                menu = 2
                    else:
                        pygame.time.delay(1000)
                        for carta in seleccionadas:
                            carta.visible = False
                    seleccionadas.clear()

                # Poner 12 cartas
                if mesa_valida(tablero):
                    for i in range(12):
                        coor = posiciones[i]
                        carta = tablero[i]
                        carta.coor_x = coor[0]
                        carta.coor_y = coor[1]
                        carta.rect = pygame.Rect(coor[0], coor[1], 237, 165)
                        carta.show_select(screen)
                        carta.draw_image(screen)
                else:
                    Flag = True
                    for i in tablero:
                        cartas.append(i)
                    tablero.clear()
                    while Flag: 
                        for i in range(12):
                            a = sample(0,len(cartas)-1) # El -1 es porque sample(a,b) escoge en el [a,b]
                            b = cartas.pop(a)
                            tablero.append(b)
                        if mesa_valida(tablero):
                            Flag = False
                        else:
                            for i in tablero:
                                cartas.append(i)
                            tablero.clear()
            else:
                print("Final de juego")
                menu = 2

        # Cronometro
        actual = pygame.time.get_ticks()
        tiempo = actual - inicio

        # Convertir milisegundos a segundos y formatear como cadena de tiempo (mm:ss)
        segundos = tiempo // 1000
        minutos = segundos // 60
        segundos %= 60
        time_str = f"{minutos:02}:{segundos:02}"

        # Crear superficie de texto
        text_surface = font.render(time_str, True, (255, 255, 255))

        # Dibujar el texto del cronómetro en la pantalla
        screen.blit(text_surface, (950, 610))
    else:
        screen.fill((255, 255, 255))
        texto_final1 = font.render(f"Tiempo total: {minutos} minutos {segundos} segundos", True, (0, 0, 0))
        texto_final2 = font.render(f"Encontraste {puntaje} sets", True, (0,0,0))
        screen.blit(texto_final1, (310, 183))
        screen.blit(texto_final2, (400, 285))

    # Actualizar la pantalla
    pygame.display.flip()
    clock.tick(60)