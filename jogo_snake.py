'''
Primeiro jogo utilizando a biblioteca "PyGame"
SNAKE
'''

# pylint: disable=no-member
# pylint: disable=no-name-in-module

from sys import exc_info
import random
from pygame.constants import ( QUIT, KEYDOWN, K_UP, K_DOWN, K_LEFT, K_RIGHT )
import pygame

#Constantes do jogo
WIDTH = 640  #Largura da tela
HEIGHT = 480 #Altura da tela
UP = 0       #Sinalizador do sentido 'para cima'
RIGHT = 1    #Sinalizador do sentido 'para a direta'
DOWN = 2     #Sinalizador do sentido 'para baixo'
LEFT = 3     #Sinalizador do sentido 'para a esquerda'

def on_grid_random():
    '''Função para gerar as posições aleatórias de criação da maçã, sempre em múltiplos de 10'''
    pos_x = random.randint(0, 630)          #Gera um número aleatório para a posição 'X'
    pos_y = random.randint(0, 470)          #Gera um número aleatório para a posição 'Y'
    return (pos_x // 10 * 10, pos_y // 10 * 10) #Converte para múltiplos de 10 e retorna o resultado

def collision(pos_1, pos_2):
    '''Função para detectar colisão'''
    return pos_1[0] == pos_2[0] and pos_1[1] == pos_2[1] #Detecta os objetos com posição coincidente

def main():
    '''Função principal'''
    #Configurações da janela
    screen = pygame.display.set_mode((WIDTH, HEIGHT)) #Tamanho da tela
    pygame.display.set_caption('Jogo Um - SNAKE')     #Título do jogo

    #Criando a cobra
    snake = [(200, 200), (210, 200), (220, 200)] #Definindo o tamanho e a posição inicial
    snake_skin = pygame.Surface((10, 10))        #Definindo o formato
    snake_skin.fill((255, 255, 255))             #Preenchendo com a cor branca
    my_direction = LEFT                          #Definindo a direção inicial da cobra

    #Criando a maçã
    apple = pygame.Surface((10, 10)) #Definindo o tamanho da maçã
    apple.fill((255, 0, 0))          #Preenchendo com a cor vermelha
    apple_pos = on_grid_random()     #Definido a posição inicial da maçã

    #Relógio
    clock = pygame.time.Clock()

    #Laço infinito, enquanto o jogo estiver executando
    while True:

        clock.tick(15) #Controle da velocidade do jogo

        #Controle dos eventos que estão acontecendo no jogo
        for event in pygame.event.get():
            if event.type == QUIT:       #Evento de clicar no 'X' da janela
                pygame.quit()            #   comando para fechar o jogo
            if event.type == KEYDOWN:    #Evento de pressionar uma tecla
                if event.key == K_UP:    #   Pressionar a tecla 'Seta para cima'
                    my_direction = UP    #      seta a direção da cobra para cima
                if event.key == K_DOWN:  #   Pressionar a tecla 'Seta para baixo'
                    my_direction = DOWN  #      seta a direção da cobra para baixo
                if event.key == K_LEFT:  #   Pressionar a tecla 'Seta para a esquerda'
                    my_direction = LEFT  #      seta a direção da cobra para a esquerda
                if event.key == K_RIGHT: #   Pressionar a tecla 'Seta para a direita'
                    my_direction = RIGHT #      seta a direção da cobra para a direita

        #Testar se houve colisão da cobra com a maçã
        if collision(snake[0], apple_pos): #Se pegou a maçã
            apple_pos = on_grid_random()   #   gera um nova posição para a maçã
            snake.append((0, 0))           #   e aumenta o comprimento da cobra

        #Setando a direção que a cobra anda no cenário
        if my_direction == UP:                         #Se for para cima
            snake[0] = (snake[0][0], snake[0][1] - 10) #   mantém o 'X' e diminui uma posição no 'Y'
        if my_direction == DOWN:                       #Se for para baixo
            snake[0] = (snake[0][0], snake[0][1] + 10) #   mantém o 'X' e aumenta uma posição no 'Y'
        if my_direction == LEFT:                       #Se for para a esquerda
            snake[0] = (snake[0][0] - 10, snake[0][1]) #   diminui uma posição no 'X' e mantém o 'Y'
        if my_direction == RIGHT:                      #Se for para a direita
            snake[0] = (snake[0][0] + 10, snake[0][1]) #   aumenta uma posição no 'X' e mantém o 'Y'
        #Fazendo o corpo acompanhar a cabeça da cobra
        for i in range(len(snake) - 1, 0, -1):            #Para cada posição da cobra
            snake[i] = (snake[i - 1][0], snake[i - 1][1]) #   a última posição passa pra penúltima

        #Plotando na tela os objetos do jogo
        screen.fill((0, 0, 0))           #Limpa a tela
        screen.blit(apple, apple_pos)    #Representação da maçã na tela
        for pos in snake:                #Para cada posição da cobra
            screen.blit(snake_skin, pos) #   representa na tela os quadrados que compõe a cobra
        pygame.display.update()          #Atualiza a tela para que o jogo aconteça

#Inicialização o jogo
try:                             #Tenta executar
    pygame.init()                #   Inicializa a biblioteca
    main()                       #   Executa o jogo
except TypeError:                #Trata o erro
    print(f'Error {exc_info()}') #   Exibe o erro
