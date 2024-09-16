import pygame

from pygame.locals import *
from engine import Player
from engine import Game




pygame.init()
pygame.font.init()
pygame.display.set_caption("Battleship")
myfont= pygame.font.SysFont("freesansttf", 100)

#variables globales
SQ_SIZE = 30
H_MARGIN = SQ_SIZE * 4
V_MARGIN = SQ_SIZE
WIDHT = SQ_SIZE * 10 * 2 + H_MARGIN
HEIGHT = SQ_SIZE * 10 * 2 + V_MARGIN
SCREEN = pygame.display.set_mode((WIDHT,HEIGHT))
INDENT = 10
HUMAN1 = True
HUMAN2 = True

#colores 
AZUL = (50, 150, 200)
BLANCO = (255,250,250)
VERDE = (50,200,150)
PLOMO = (40,50,60)
ROJO = (250, 50, 100)
NARANJA = (250, 140, 20)
COLORS = {"U": PLOMO, "M": AZUL, "H": NARANJA, "S": ROJO}

#Para dibujar el grid
def draw_grid(player,left = 0,top = 0, search = False):
    for i in range(100):
        x = left + i % 10 * SQ_SIZE
        y = top + i // 10 * SQ_SIZE
        square = pygame.Rect(x, y, SQ_SIZE, SQ_SIZE)
        pygame.draw.rect(SCREEN, BLANCO, square, width= 3)
        if search:
            x += SQ_SIZE //2
            y += SQ_SIZE //2
            pygame.draw.circle(SCREEN, COLORS[player.search[i]], (x,y), radius= SQ_SIZE//4)

#funcion para dibujar naves en el grid
def draw_ships(self, player, left = 0, top = 0):
    for ship in player.ships:
        x = left + ship.col * SQ_SIZE + INDENT
        y = top + ship.row * SQ_SIZE + INDENT
        if ship.orientation == "h":
            width = ship.size * SQ_SIZE - 2 * INDENT
            heigth = SQ_SIZE - 2 * INDENT
        else:
            width = SQ_SIZE - 2 * INDENT
            heigth = ship.size * SQ_SIZE - 2 * INDENT
        rectangle = pygame.Rect(x, y, width, heigth)
        pygame.draw.rect(SCREEN, VERDE, rectangle, border_radius= 7)

player1 = Player()
player2 = Player()
game = Game(HUMAN1, HUMAN2)

# pygame loop
animating = True
pausing = False
while animating:

    #interaccion del usuario
    for event in pygame.event.get():

        #cierra la ventana
        if event.type == pygame.quit:
            animating = False

        #usario clickea el mouse
        if event.type == pygame.MOUSEBUTTONDOWN and not game.over:
            x,y = pygame.mouse.get_pos()
            if game.player1_turn and x < SQ_SIZE * 10 and y< 10*SQ_SIZE:
                row = y // SQ_SIZE
                col = x // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)
            elif not game.player1_turn and x > WIDHT - SQ_SIZE * 10 and y > SQ_SIZE * 10 + V_MARGIN:
                row = (y - SQ_SIZE*10 - V_MARGIN)// SQ_SIZE
                col = (x - SQ_SIZE*10 - H_MARGIN) // SQ_SIZE
                index = row * 10 + col
                game.make_move(index)

        #presionando tecla
        if event.type == pygame.KEYDOWN:
            
            #escape
            if event.key == pygame.K_ESCAPE:
                animating = False
            #pausar
            if event.key == pygame.K_SPACE:
                pausing = not pausing
            #reiniciar
            if event.key == pygame.K_RETURN:
                game = Game(HUMAN1, HUMAN2)
        
        #ejecutar el programa
        if not pausing:
            #draw background
            SCREEN.fill(PLOMO)
            #dibuja el grid
            draw_grid(game.player1, search= True)
            draw_grid(game.player2, search= True,left=(WIDHT * H_MARGIN)//2 + H_MARGIN, top=(HEIGHT * V_MARGIN) + V_MARGIN) 
            #grid de la posicion
            draw_grid(game.player1,top=(HEIGHT-V_MARGIN)//2 + V_MARGIN)
            draw_grid(game.player2,left=(WIDHT - H_MARGIN)//2 + H_MARGIN)
            #dibujar ships del jugador
            draw_ships(game.player1, player1, top=(HEIGHT-V_MARGIN)//2 + V_MARGIN )
            draw_ships(game.player2, player2, left=(WIDHT - H_MARGIN)//2 + H_MARGIN )

            #movimientos de la computadora
            if not game.over and game.computer_turn:
                game.random_ai()

            #mensaje de game over
            if game.over:
                text = "Player" + str(game.result) + "wins"
                textbox = myfont.render(text, False, PLOMO, BLANCO)
                SCREEN.blit(textbox, (WIDHT//2 - 240, HEIGHT//2 - 50))
            #actualizar la pantalla
            pygame.display.flip()
