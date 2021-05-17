'''
Jogo Space Invaders em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 
'''
# pylint: disable=no-member
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module

# Bibliotecas
from os import path, environ
from random import randint, choice
from sys import platform as plat, exit as ext, exc_info as info
import pickle
import pygame
from pygame.constants import ( QUIT, KEYDOWN, K_ESCAPE, K_SPACE )
# Constantes
BASE_DIR = path.dirname(__file__)    # Diretorio do jogo
SCREEN_WIDTH = 600                   # Comprimento da tela
SCREEN_HEIGHT = 860                  # Altura da tela
GRAVITY = 1                          # Gravidade
GAME_SPEED = SPEED = 10              # Velocidades
FPS = 30                             # Frames por segundo

class Ship(pygame.sprite.Sprite):
    '''Classe que representa a nave do jogador'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = [
            pygame.image.load(
                f'{BASE_DIR}/assets/sprites/player/player.png'
            ).convert_alpha(),
            pygame.image.load(
                f'{BASE_DIR}/assets/sprites/player/player_.png'
            ).convert_alpha()
        ]
        self.speed = SPEED
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = (SCREEN_WIDTH / 2) - (self.image.get_width() / 2)
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self):
        '''Função que representa como o pássaro se comporta em cada interação no jogo'''
        self.speed += GRAVITY
        self.current_image = (self.current_image + 1) % 3
        self.image = pygame.transform.rotozoom(self.images[self.current_image], self.speed * -3, 1)
        self.rect[1] += self.speed

    def shoot(self):
        '''Função que representa a ação de voar do pássaro'''
        self.speed = -SPEED

    def get_width(self):
        '''Função que retorna o comprimento do pássaro'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna a altura do pássaro'''
        return self.image.get_size()[1]


def main():
    '''Função principal que trata de toda a execução do jogo'''
    # Centraliza a janela do jogo no monitor
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
    splash = True
    run = False
    # Criação da janela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icon = pygame.image.load(f'{BASE_DIR}/assets/sprites/icons/icon.png').convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption('Space Invaders v1.0')
    # Contador de pontuação do jogo
    score = 0
    # Testa o sistema em que o jogo está rodando
    sound_type = 'wav' if 'win' in plat else 'ogg'
    # Carregamento dos sons do jogo
    sounds = [
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/death.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/explosion.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/shot.{sound_type}')
    ]
    # Criação da imagem de fundo
    backgrounds = [
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg0.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg1.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg2.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg3.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg4.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg5.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg6.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg7.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg8.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg9.png')
    ]
    background = backgrounds[0]
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    # Criação do controle de tempo do jogo
    clock = pygame.time.Clock()
    # Laço da tela de abertura do jogo
    while splash:
#        splash = messages[0]
#        splash_x = SCREEN_WIDTH / 2 - splash.get_width() / 2
#        splash_y = SCREEN_HEIGHT / 2 - splash.get_height() / 2
        screen.blit(background, (0, 0))
#        screen.blit(splash, (splash_x, splash_y))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                ext()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    ext()
                if event.key == K_SPACE:
                    splash = False
                    run = True
    level = 1
    while run:
        # Controle da velocidade do jogo
        clock.tick(FPS)
        # Controle dos eventos do jogo
        for event in pygame.event.get():
            # Evento que fecha a janela
            if event.type == QUIT:
                pygame.quit()
                ext()
            # Evento que identifica a tecla pressionada
            if event.type == KEYDOWN:
                # Teste para saber se a tecla é "BARRA DE ESPAÇO"
                if event.key == K_SPACE:
                    #ship.shoot()
                    pygame.mixer.Sound.play(sounds[2])
        background = backgrounds[level]
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Desenho da imagem de fundo do jogo
        screen.blit(background, (0, 0))

        pygame.display.update()


try:
    while True:
        main()
except (ValueError, TypeError, ZeroDivisionError) as exc:
    print(f"Oops! {exc.__class__} occurred. {exc.args}")
else:
    if info()[0] is not None:
        print(f"Oops! {info()[0]} occurred.")
finally:
    pygame.quit()
    ext()