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
import time
import pygame
from pygame.constants import ( K_LEFT, K_RIGHT, QUIT, KEYDOWN, K_ESCAPE, K_SPACE )
# Constantes
BASE_DIR = path.dirname(__file__)    # Diretorio do jogo
SCREEN_WIDTH = 600                   # Comprimento da tela
SCREEN_HEIGHT = 860                  # Altura da tela
SPEED = 10                           # Velocidades
FPS = 30                             # Frames por segundo

class Ship(pygame.sprite.Sprite):
    '''Classe que representa a nave do jogador'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = (
            pygame.image.load(f'{BASE_DIR}/assets/sprites/player/player.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/player/player_.png').convert_alpha()
        )
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = (SCREEN_WIDTH / 2) - (self.image.get_width() / 2)
        self.rect[1] = SCREEN_HEIGHT - self.image.get_height()

    def update(self):
        '''Função que representa como a nave se comporta em cada interação no jogo'''
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]

    def shoot(self, sound):
        '''Função que representa a ação de atirar com a nave'''
        pygame.mixer.Sound.play(sound)
        return Laser(self.rect[0] + 33, self.rect[1] - 28)

    def get_width(self):
        '''Função que retorna a largura da nave'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento da nave'''
        return self.image.get_size()[1]

class Laser(pygame.sprite.Sprite):
    '''Classe que representa o laser da nave'''
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            f'{BASE_DIR}/assets/sprites/player/bullet.png'
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = pos_x
        self.rect[1] = pos_y
        self.speed = SPEED

    def update(self):
        '''Função que representa a trajetória do laser'''
        self.rect[1] -= self.speed

    def get_width(self):
        '''Função que retorna a largura do laser'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento do laser'''
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
#    score = 0
    # Testa o sistema em que o jogo está rodando
    sound_type = 'wav' if 'win' in plat else 'ogg'
    # Carregamento dos sons do jogo
    sounds = (
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/death.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/explosion.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/shot.{sound_type}')
    )
    # Criação das mensagens do jogo
    messages = [
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/start_game.png').convert_alpha()
#        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/get_ready.png').convert_alpha()
#        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/game_over.png').convert_alpha()
#        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/high_score.png').convert_alpha()
    ]
    # Criação da imagem de fundo
    backgrounds = (
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg0_title-screen.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg1.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg2.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg3.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg4.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg5.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg6.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg7.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg8.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg9.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/bg10_big-boss.png')
    )
    background = backgrounds[0]
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ship_group = pygame.sprite.Group()
    ship = Ship()
    ship_group.add(ship)
    laser_group = pygame.sprite.Group()
    # Criação do controle de tempo do jogo
    clock = pygame.time.Clock()
    # Laço da tela de abertura do jogo
    ship.rect[1] -= 400
    while splash:
        # Controle da velocidade do jogo
        clock.tick(FPS)
        splash = messages[0]
        splash_x = 0
        splash_y = 0
        screen.blit(background, (0, 0))
        screen.blit(splash, (splash_x, splash_y))
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
        ship_group.update()
        ship_group.draw(screen)
        pygame.display.update()
    level = 1
    screen_limit_left = 0
    screen_limit_right = ((SCREEN_WIDTH - ship.get_width()) // 10) * 10
    screen_limit_bottom = ((SCREEN_HEIGHT - ship.get_height()) // 10) * 10
    start_time = [
        time.localtime()[3],
        time.localtime()[4],
        time.localtime()[5]
    ]
    elapsed_time = [
        start_time[0] - time.localtime()[3],
        start_time[1] - time.localtime()[4],
        start_time[2] - time.localtime()[5]
    ]
    print(elapsed_time)
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
                if event.key == K_SPACE and ((ship.rect[1] // 10) * 10) == screen_limit_bottom:
                    laser_group.add(ship.shoot(sounds[2]))

        commands = pygame.key.get_pressed()
        # Teste para saber se a tecla é "SETA PARA A ESQUERDA"
        if commands[K_LEFT] and ((ship.rect[1] // 10) * 10) == screen_limit_bottom:
            ship.rect[0] -= SPEED if ((ship.rect[0] // 10) * 10) != screen_limit_left else 0
        # Teste para saber se a tecla é "SETA PARA A DIREITA"
        if commands[K_RIGHT] and ((ship.rect[1] // 10) * 10) == screen_limit_bottom:
            ship.rect[0] += SPEED if ((ship.rect[0] // 10) * 10) != screen_limit_right else 0

        background = backgrounds[level]
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Desenho da imagem de fundo do jogo
        screen.blit(background, (0, 0))
        ship_group.update()
        laser_group.update()
        ship_group.draw(screen)
        laser_group.draw(screen)
        ship.rect[1] += SPEED if ((ship.rect[1] // 10) * 10) != screen_limit_bottom else 0

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
