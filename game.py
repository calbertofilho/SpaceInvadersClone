'''
Jogo Space Invaders em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 19/05/2021
'''
# pylint: disable=no-member
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=too-many-statements
# pylint: disable=c-extension-no-member
# pylint: disable=no-name-in-module

# Bibliotecas
from os import kill, path, environ
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
SPEED = 10                           # Velocidade do jogo
START_SPEED = 5                      # Velocidade para inicio do jogo
FPS = 30                             # Frames por segundo
START_GAME = (0, 0)
GET_READY = (163, 525)
SET_ENEMIES = (108, 525)
KILLEM_ALL = (140, 525)
SET_COUNTER = (282, 580)
HIGH_SCORE = (0, 0)
GAME_OVER = (0, 0)

class Spaceship(pygame.sprite.Sprite):
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
        self.center = (SCREEN_WIDTH / 2) - (self.image.get_width() / 2)
        self.bottom = SCREEN_HEIGHT - self.image.get_height()
        self.rect[0] = self.center
        self.rect[1] = self.bottom
        self.reset_pos = 0

    def update(self):
        '''Função que representa como a nave se comporta em cada interação no jogo'''
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        if self.reset_pos == 1:
            if (self.rect[0] // 10) * 10 > (self.center // 10) * 10:
                self.rect[0] -= START_SPEED if (self.rect[0] // 10) * 10 > (self.center // 10) * 10 else 0
            elif (self.rect[0] // 10) * 10 < (self.center // 10) * 10:
                self.rect[0] += START_SPEED if (self.rect[0] // 10) * 10 < (self.center // 10) * 10 else 0
            else:
                self.rect[0] = self.center
                self.reset_pos = 0

    def shoot(self, laser_fx, explosion_fx, invaders, lasers):
        '''Função que representa a ação de atirar com a nave'''
        pygame.mixer.Sound.play(laser_fx)
        return Laser(self.rect[0] + 33, self.rect[1] - 28, explosion_fx, invaders, lasers)

    def reset_position(self):
        '''Função que reinicia a posição da nave'''
        self.reset_pos = 1

    def get_width(self):
        '''Função que retorna a largura da nave'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento da nave'''
        return self.image.get_size()[1]

class Laser(pygame.sprite.Sprite):
    '''Classe que representa o laser da nave'''
    def __init__(self, pos_x, pos_y, sound, invaders_group, laser_group):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            f'{BASE_DIR}/assets/sprites/player/bullet.png'
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = pos_x
        self.rect[1] = pos_y
        self.speed = SPEED
        self.laser_group = laser_group
        self.invaders_group = invaders_group
        self.explosion = sound

    def update(self):
        '''Função que representa o que acontece na trajetória do laser'''
        self.rect[1] -= self.speed
        if pygame.sprite.groupcollide(self.laser_group, self.invaders_group, True, True, pygame.sprite.collide_mask):
            pygame.mixer.Sound.play(self.explosion)
        if (((self.rect[1]) // 10) * 10) == -((self.get_height() // 10) * 10):
            self.kill()

    def get_width(self):
        '''Função que retorna a largura do laser'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento do laser'''
        return self.image.get_size()[1]

class Invaders(pygame.sprite.Sprite):
    '''Classe que representa os inimigos'''
    def __init__(self, alien, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.enemies = (
            (
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/White-Enemy1.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/White-Enemy1_.png').convert_alpha()
            ),
            (
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Green-Enemy2.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Green-Enemy2_.png').convert_alpha()
            ),
            (
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Yellow-Enemy3.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Yellow-Enemy3_.png').convert_alpha()
            )
        )
        self.enemy = self.enemies[alien]
        self.current_image = 0
        self.image = self.enemy[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = (SCREEN_WIDTH / 2) - (self.image.get_width() / 2)
        self.rect[1] = SCREEN_HEIGHT / 2
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.move_counter = 0
        self.move_direction = 1
        self.last_count = pygame.time.get_ticks()

    def update(self):
        '''Função que representa como a nave inimiga se comporta em cada interação no jogo'''
        counter = pygame.time.get_ticks()
        if counter - self.last_count > 300:
            self.current_image = (self.current_image + 1) % 2
            self.last_count = counter
        self.image = self.enemy[self.current_image]
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction

    def death(self, alien, pos_x, pos_y, sound):
        self.images = (
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/White-Enemy-Burst.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Green-Enemy-Burst.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Yellow-Enemy-Burst.png').convert_alpha()
        )
        self.image = self.images[alien]
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        pygame.mixer.Sound.play(sound)
        self.kill()

def main():
    '''Função principal que trata de toda a execução do jogo'''
    # Centraliza a janela do jogo no monitor
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
    splash = True
    run = False
    rows = 3
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
    sounds = (
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/death.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/explosion.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/{sound_type}/shot.{sound_type}')
    )
    # Criação das mensagens do jogo
    messages = (
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/start_game.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/get_ready.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/set_enemies.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/kill\'em_all.png').convert_alpha()
#        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/game_over.png').convert_alpha()
#        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/high_score.png').convert_alpha()
    )
    # Criação dos números
    numbers = (
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_0-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_1-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_2-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_3-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_4-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_5-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_6-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_7-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_8-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_9-.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_0+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_1+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_2+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_3+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_4+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_5+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_6+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_7+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_8+.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/numbers/num_9+.png')
    )
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
    ship = Spaceship()
    ship_group.add(ship)
    invaders_group = pygame.sprite.Group()
    def create_invaders(rows, cols):
        for row in range(rows):
            invader = randint(0, 2)
            for item in range(cols):
                enemy = Invaders(invader, 100 + item * 100, 100 + row * 70)
                invaders_group.add(enemy)
    def has_invaders():
        return len(invaders_group) != 0
    laser_group = pygame.sprite.Group()
    # Criação do controle de tempo do jogo
    clock = pygame.time.Clock()
    # Laço da tela de abertura do jogo
    ship.rect[1] -= 400
    while splash:
        # Controle da velocidade do jogo
        clock.tick(FPS)
        screen.blit(background, (0, 0))
        screen.blit(messages[0], START_GAME)
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

    start = False
    level = 1
    countdown = 3
    last_count = pygame.time.get_ticks()
    screen_limit_left = 0
    screen_limit_right = ((SCREEN_WIDTH - ship.get_width()) // 10) * 10
    screen_limit_bottom = ((SCREEN_HEIGHT - ship.get_height()) // 10) * 10

    def next_level():
        ship.reset_position()
        laser_group.empty()
        if rows < 8:
            new_rows = rows + 1
        else:
            new_rows = 8
        new_level = level + 1
        return new_level, new_rows


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
                if event.key == K_SPACE and countdown == 0:
                    laser_group.add(ship.shoot(sounds[2], sounds[1], invaders_group, laser_group))

        commands = pygame.key.get_pressed()
        # Teste para saber se a tecla é "SETA PARA A ESQUERDA"
        if commands[K_LEFT] and countdown == 0:
            ship.rect[0] -= SPEED if ((ship.rect[0] // 10) * 10) != screen_limit_left else 0
        # Teste para saber se a tecla é "SETA PARA A DIREITA"
        if commands[K_RIGHT] and countdown == 0:
            ship.rect[0] += SPEED if ((ship.rect[0] // 10) * 10) != screen_limit_right else 0

        background = backgrounds[level]
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Desenho da imagem de fundo do jogo
        screen.blit(background, (0, 0))
        ship_group.update()
        laser_group.update()
        invaders_group.update()
        ship_group.draw(screen)
        laser_group.draw(screen)
        invaders_group.draw(screen)
        ship.rect[1] += START_SPEED if ((ship.rect[1] // 10) * 10) != screen_limit_bottom else 0

        if countdown != 0:
            counter = pygame.time.get_ticks()
            if level == 1:
                if countdown >= 3:
                    screen.blit(messages[1], GET_READY)
                elif countdown >= 2:
                    screen.blit(messages[2], SET_ENEMIES)
                    start = True
                elif countdown >= 1:
                    screen.blit(messages[3], KILLEM_ALL)
            else:
                screen.blit(messages[1], GET_READY)
                if countdown >= 3:
                    screen.blit(numbers[13], SET_COUNTER)
                elif countdown >= 2:
                    screen.blit(numbers[12], SET_COUNTER)
                elif countdown >= 1:
                    screen.blit(numbers[11], SET_COUNTER)
            if counter - last_count > 1000:
                countdown -= 1
                last_count = counter

        if (len(invaders_group) == 0) and (countdown == 2):
            create_invaders(rows, 5)
        if start and (len(invaders_group) == 0):
            level, rows = next_level()
            create_invaders(rows, 5)
            countdown = 3

        pygame.display.update()

try:
    while True:
        main()
except (ValueError, TypeError, ZeroDivisionError) as exc:
    print(f"Oops! {exc.__class__} occurred.\n{exc.args}")
else:
    if info()[0] is not None:
        print(f"Oops! {info()[0]} occurred.")
finally:
    pygame.quit()
    ext()
