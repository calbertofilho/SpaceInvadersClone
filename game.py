'''
Jogo Space Invaders em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 14/06/2021
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
from math import ceil
import pygame
from pygame.constants import ( K_PAUSE, QUIT, KEYDOWN, K_LEFT, K_RIGHT, K_ESCAPE, K_SPACE )

SCORE = 0
# Constantes
BASE_DIR = path.dirname(__file__)        # Diretorio do jogo
# Definições da tela
SCREEN_WIDTH = 600                       # Comprimento da tela
SCREEN_HEIGHT = 860                      # Altura da tela
CAPTION = 'Space Invaders v1.0'          # Título do jogo
WINDOW_ICON = f'{BASE_DIR}/res/assets/icons/icon.png'
# Definições do jogo
FPS = 30                                 # Frames por segundo
SPEED = 10                               # Velocidade do jogo
BULLET_SPEED = START_SPEED = SPEED // 2  # Velocidade para inicio do jogo e das balas dos inimigos
LASER_TIMING = 500                       # Tempo, em milissegundos, entre um disparo e outro
MIN_ENEMIES_ROWS = 3                     # Número mínimo de linhas na matriz de inimigos
MAX_ENEMIES_ROWS = 10                    # Número máximo de linhas na matriz de inimigos
MAX_BULLETS = 5                          # Quantidade de balas, ao mesmo tempo, na tela, do inimigo
ENEMY_ANIMATION_TIME = 300               # Tempo, em ms, entre as trocas das imagens do inimigo
BULLET_ANIMATION_TIME = 200              # Tempo, em ms, entre as trocas das imagens das balas
BULLET_TIMING = 2 * LASER_TIMING         # Tempo, em ms, entre uma bala e outra
# Definições das mensagens
BACKGROUND = START_GAME = PAUSE_GAME = (0, 0)  # Posição (x, y) do Background e da Splash Screen
LOADING = (459, 10)                            # Posição (x, y) da mensagem LOADING
GET_READY = (103, 525)                         # Posição (x, y) da mensagem GET READY
INVADING = (103, 525)                          # Posição (x, y) da mensagem INVADING
KILLEM_ALL = (103, 525)                        # Posição (x, y) da mensagem KILL'EM ALL
GAME_OVER = (103, 525)                         # Posição (x, y) da mensagem GAME OVER
LEVEL = (199, 399)                             # Posição (x, y) da mensagem LEVEL
LVL_NUMBER = (284, 457)                        # Posição (x, y) do número do LEVEL
LEVEL_PLAY = (10, 10)                          # Posição (x, y) da mensagem LEVEL na tela do jogo
LVL_PLAY_NUMBER = (113, 10)                    # Posição (x, y) do número do LEVEL na tela do jogo
SET_COUNTER = (282, 580)                       # Posição (x, y) do número da contagem
HIGH_SCORE = (0, 0)                            # Posição (x, y) da mensagem HIGH SCORE
# Definições de áudio
VOLUME_FX = 0.3                          # Volume dos efeitos especiais
VOLUME_BGM = 0.6                         # Volume da música de fundo
FADEOUT = 1500                           # Tempo de fade para parar a música de fundo

class Spaceship(pygame.sprite.Sprite):
    '''Classe que representa a nave do jogador'''
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images = (
            pygame.image.load(f'{BASE_DIR}/res/assets/player/player.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/res/assets/player/player_.png').convert_alpha()
        )
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.center = (SCREEN_WIDTH / 2) - (self.image.get_width() / 2)
        self.rect[0] = self.center
        self.rect[1] = SCREEN_HEIGHT - self.image.get_height() # Definição da base, onde fica a nave
        self.reset_pos = 0

    def update(self):
        '''Função que representa como a nave se comporta em cada interação no jogo'''
        self.current_image = (self.current_image + 1) % len(self.images)
        self.image = self.images[self.current_image]
        if self.reset_pos == 1:
            position = (self.rect[0] // 10) * 10
            if position > (self.center // 10) * 10:
                self.rect[0] -= START_SPEED if position > (self.center // 10) * 10 else 0
            elif position < (self.center // 10) * 10:
                self.rect[0] += START_SPEED if position < (self.center // 10) * 10 else 0
            else:
                self.rect[0] = self.center
                self.reset_pos = 0

    def shoot(self, laser_fx):
        '''Função que representa a ação de atirar com a nave'''
        laser_fx.set_volume(VOLUME_FX)
        pygame.mixer.Sound.play(laser_fx)
        return Laser((self.rect[0] + 33, self.rect[1] - 28))

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
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(
            f'{BASE_DIR}/res/assets/player/bullet.png'
        ).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = position[0]
        self.rect[1] = position[1]
        self.speed = SPEED

    def update(self):
        '''Função que representa o que acontece na trajetória do laser'''
        self.rect[1] -= self.speed
        if (((self.rect[1]) // 10) * 10) == -((self.get_height() // 10) * 10):
            self.kill()

    def get_width(self):
        '''Função que retorna a largura do laser'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento do laser'''
        return self.image.get_size()[1]

class Explosion(pygame.sprite.Sprite):
    '''Classe que representa a explosão da nave do jogador'''
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 74):
            self.images.append(pygame.image.load(
                f'{BASE_DIR}/res/assets/explosion/frm{i}.png'
            ).convert_alpha())
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.counter = 0

    def update(self):
        '''Função que representa o comportamento da animação da explosão'''
        explosion_speed = 1
        # Atualização da animação da explosão
        self.counter += 1
        if self.counter >= explosion_speed and self.current_image < len(self.images) - 1:
            self.counter = 0
            self.current_image += 1
            self.image = self.images[self.current_image]
        # Se a animação terminar, exclui a explosão
        if self.current_image >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

    def get_width(self):
        '''Função que retorna a largura do frame da explosão'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento do frame da explosão'''
        return self.image.get_size()[1]

class Invaders(pygame.sprite.Sprite):
    '''Classe que representa os inimigos'''
    def __init__(self, alien, position, sound, groups):
        pygame.sprite.Sprite.__init__(self)
        self.enemies = []
        for i in range(0, 10):
            self.enemies.append(
                (
                    pygame.image.load(
                        f'{BASE_DIR}/res/assets/enemies/invaders/enemy{i}.png'
                    ).convert_alpha(),
                    pygame.image.load(
                        f'{BASE_DIR}/res/assets/enemies/invaders/enemy{i}_.png'
                    ).convert_alpha()

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
        self.rect.center = position
        self.move_counter = 0
        self.move_direction = 1
        self.last_count = pygame.time.get_ticks()
        self.invaders_group = groups[0]
        self.laser_group = groups[1]
        self.burst_group = groups[2]
        self.explosion = sound
        self.explosion.set_volume(VOLUME_FX)
        self.value = 5

    def update(self):
        '''Função que representa como a nave inimiga se comporta em cada interação no jogo'''
        counter = pygame.time.get_ticks()
        if counter - self.last_count > ENEMY_ANIMATION_TIME:
            self.current_image = (self.current_image + 1) % 2
            self.last_count = counter
            self.image = self.enemy[self.current_image]
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
        if pygame.sprite.spritecollide(self, self.laser_group, True, pygame.sprite.collide_mask):
            pygame.mixer.Sound.play(self.explosion)
            set_score(self.value)
            burst = Burst(self.rect.center)
            self.burst_group.add(burst)
            self.kill()

    def get_width(self):
        '''Função que retorna a largura da nave do invasor'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento da nave do invasor'''
        return self.image.get_size()[1]

class Bullets(pygame.sprite.Sprite):
    '''Classe que representa a bala do inimigo'''
    def __init__(self, ship, explosion, position, sound):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 7):
            self.images.append(pygame.image.load(
                f'{BASE_DIR}/res/assets/enemies/invaders/bullet{i}.png'
            ).convert_alpha())
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = position[0] - (self.image.get_size()[0] // 2)
        self.rect[1] = position[1] - (self.image.get_size()[1])
        self.last_count = pygame.time.get_ticks()
        self.speed = BULLET_SPEED
        self.ship_group = ship
        self.explosion_group = explosion
        self.explosion = sound
        self.explosion.set_volume(VOLUME_FX)

    def update(self):
        '''Função que representa o que acontece na trajetória da bala do inimigo'''
        counter = pygame.time.get_ticks()
        if counter - self.last_count > BULLET_ANIMATION_TIME:
            self.current_image = (self.current_image + 1) % len(self.images)
            self.last_count = counter
        self.image = self.images[self.current_image]
        self.rect[1] += self.speed
        if (((self.rect[1]) // 10) * 10) == ((SCREEN_HEIGHT // 10) * 10):
            self.kill()
        if pygame.sprite.spritecollide(self, self.ship_group, False, pygame.sprite.collide_mask):
            self.kill()
            pygame.mixer.Sound.play(self.explosion)
            explosion = Explosion(self.ship_group.sprites()[0].rect.center)
            self.explosion_group.add(explosion)
            self.ship_group.empty()

    def get_width(self):
        '''Função que retorna a largura da bala do inimigo'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento da bala do inimigo'''
        return self.image.get_size()[1]

class Mothership(pygame.sprite.Sprite):
    '''Classe que representa a nave mãe dos inimigos'''
    def __init__(self, sound, groups):
        pygame.sprite.Sprite.__init__(self)
        self.enemy = (
            pygame.image.load(
                f'{BASE_DIR}/res/assets/enemies/mothership/mothership.png'
            ).convert_alpha(),
            pygame.image.load(
                f'{BASE_DIR}/res/assets/enemies/mothership/mothership_.png'
            ).convert_alpha(),
            pygame.image.load(
                f'{BASE_DIR}/res/assets/enemies/mothership/mothership-burst.png'
            ).convert_alpha()
        )
        self.current_image = 0
        self.image = self.enemy[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.x = -self.image.get_width()
        self.rect.y = 5 + self.image.get_height() // 2
        self.last_count = pygame.time.get_ticks()
        self.invaders_group = groups[0]
        self.laser_group = groups[1]
        self.burst_group = groups[2]
        self.explosion = sound
        self.explosion.set_volume(VOLUME_FX)
        self.value = 10

    def get_width(self):
        '''Função que retorna a largura da nave mãe'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento da nave mãe'''
        return self.image.get_size()[1]

    def update(self):
        '''Função que representa como a nave mãe se comporta em cada interação no jogo'''
        counter = pygame.time.get_ticks()
        if counter - self.last_count > ENEMY_ANIMATION_TIME:
            self.current_image = (self.current_image + 1) % 2
            self.last_count = counter
            self.image = self.enemy[self.current_image]
        self.rect.x += SPEED
        if ((self.rect.x // 10) * 10) == SCREEN_WIDTH:
            self.kill()
        if pygame.sprite.spritecollide(self, self.laser_group, True, pygame.sprite.collide_mask):
            pygame.mixer.Sound.play(self.explosion)
            set_score(self.value)
            burst = Burst(self.rect.center)
            self.burst_group.add(burst)
            self.kill()

class Bomb(pygame.sprite.Sprite):
    '''Classe que representa a bomba da nave mãe dos inimigos'''
    def __init__(self, ship, explosion, position, sound):
        pygame.sprite.Sprite.__init__(self)
        self.images = (
            pygame.image.load(
                f'{BASE_DIR}/res/assets/enemies/mothership/bomb.png'
            ).convert_alpha(),
            pygame.image.load(
                f'{BASE_DIR}/res/assets/enemies/mothership/bomb_.png'
            ).convert_alpha()
        )
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = position[0] - (self.image.get_size()[0] // 2)
        self.rect[1] = position[1] - (self.image.get_size()[1])
        self.last_count = pygame.time.get_ticks()
        self.speed = BULLET_SPEED * 2
        self.ship_group = ship
        self.explosion_group = explosion
        self.explosion = sound
        self.explosion.set_volume(VOLUME_FX)

    def update(self):
        '''Função que representa o que acontece na trajetória da bala do inimigo'''
        counter = pygame.time.get_ticks()
        if counter - self.last_count > BULLET_ANIMATION_TIME:
            self.current_image = (self.current_image + 1) % 2
            self.last_count = counter
        self.image = self.images[self.current_image]
        self.rect[1] += self.speed
        if (((self.rect[1]) // 10) * 10) == ((SCREEN_HEIGHT // 10) * 10):
            self.kill()
        if pygame.sprite.spritecollide(self, self.ship_group, False, pygame.sprite.collide_mask):
            self.kill()
            pygame.mixer.Sound.play(self.explosion)
            explosion = Explosion(self.ship_group.sprites()[0].rect.center)
            self.explosion_group.add(explosion)
            self.ship_group.empty()

    def get_width(self):
        '''Função que retorna a largura da bala do inimigo'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento da bala do inimigo'''
        return self.image.get_size()[1]

class Burst(pygame.sprite.Sprite):
    '''Classe que representa a explosão dos inimigos'''
    def __init__(self, position):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for i in range(1, 14):
            self.images.append(pygame.image.load(
                f'{BASE_DIR}/res/assets/burst/frm{i}.png'
            ).convert_alpha())
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.counter = 0

    def update(self):
        '''Função que representa o comportamento da animação da explosão do inimigo'''
        explosion_speed = 1
        # Atualização da animação da explosão
        self.counter += 1
        if self.counter >= explosion_speed and self.current_image < len(self.images) - 1:
            self.counter = 0
            self.current_image += 1
            self.image = self.images[self.current_image]
        # Se a animação terminar, exclui a explosão
        if self.current_image >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

    def get_width(self):
        '''Função que retorna a largura do frame da explosão do inimigo'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento do frame da explosão do inimigo'''
        return self.image.get_size()[1]

def set_score(value):
    global SCORE
    SCORE += value

def draw_score(sface, nums):
    value = list(str(SCORE))
    while len(value) != 5:
        value.insert(0, 0)
    sface.blit(nums[int(value[0])], (SCREEN_WIDTH - 95, 10))
    sface.blit(nums[int(value[1])], (SCREEN_WIDTH - 78, 10))
    sface.blit(nums[int(value[2])], (SCREEN_WIDTH - 61, 10))
    sface.blit(nums[int(value[3])], (SCREEN_WIDTH - 44, 10))
    sface.blit(nums[int(value[4])], (SCREEN_WIDTH - 27, 10))

def close_game():
    '''Função que encerra todas as bibliotecas e fecha o jogo'''
    pygame.display.quit()
    pygame.mixer.quit()
    pygame.quit()
    ext()

def main():
    '''Função principal que trata de toda a execução do jogo'''
    # Centraliza a janela do jogo no monitor
    environ['SDL_VIDEO_CENTERED'] = '1'
    pygame.init()
    pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)
    splash = True
    run = False
    rows = MIN_ENEMIES_ROWS
    # Criação da janela
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    icon = pygame.image.load(WINDOW_ICON).convert_alpha()
    pygame.display.set_icon(icon)
    pygame.display.set_caption(CAPTION)
    # Contador de pontuação do jogo
    paused = False
    # Testa o sistema em que o jogo está rodando
    sound_type = 'wav' if 'win' in plat else 'ogg'
    # Carregamento dos sons do jogo
    bgm = (
        f'{BASE_DIR}/res/sounds/bgm/midi/main.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level1.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level2.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level3.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level4.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level5.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level6.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level7.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level8.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/level9.mid',
        f'{BASE_DIR}/res/sounds/bgm/midi/boss.mid'
    )
    effects = (
        pygame.mixer.Sound(f'{BASE_DIR}/res/sounds/sfx/{sound_type}/death.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/res/sounds/sfx/{sound_type}/explosion.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/res/sounds/sfx/{sound_type}/shot.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/res/sounds/sfx/{sound_type}/burst.{sound_type}')
    )
    # Criação das mensagens do jogo
    messages = (
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/start_game.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/loading.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/get_ready.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/invading.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/kill\'em_all.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/game_over.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/high_score.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/level_start.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/level_play.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/res/assets/messages/pause_game.png').convert_alpha()
    )
    # Criação dos números
    numbers = []
    for i in range(0, 20):
        pos = f'{i}-' if len(str(i)) == 1 else f'{str(i)[1]}+'
        numbers.append(pygame.image.load(f'{BASE_DIR}/res/assets/numbers/num_{pos}.png'))
    # Criação da imagem de fundo
    backgrounds = (
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/main.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level1.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level2.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level3.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level4.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level5.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level6.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level7.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level8.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/level9.png'),
        pygame.image.load(f'{BASE_DIR}/res/assets/sceneries/boss.png')
    )
    background = backgrounds[0]
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ship_group = pygame.sprite.Group()
    ship = Spaceship()
    ship_group.add(ship)
    laser_group = pygame.sprite.Group()
    invaders_group = pygame.sprite.Group()
    mothership_come = -1
    def create_invaders(rows, cols):
        invader = rows - 1
        for row in range(rows):
            for item in range(cols):
                enemy = Invaders(
                    invader,
                    (100 + item * 100, 100 + row * 50),
                    effects[3],
                    (invaders_group, laser_group, burst_group)
                )
                invaders_group.add(enemy)
            invader -= 1
        return randint(1, len(invaders_group) - 1)
    bullets_group = pygame.sprite.Group()
    def play_bgm(track):
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load(bgm[track])
            pygame.mixer.music.set_volume(VOLUME_BGM)
            pygame.mixer.music.play()
    def pause_bgm(state):
        if pygame.mixer.music.get_busy():
            if state is True:
                pygame.mixer.music.pause()
        else:
            if state is False:
                pygame.mixer.music.unpause()
    def stop_bgm(delay):
        lstcnt = cnt = pygame.time.get_ticks()
        cntdown = 1 if (delay < 1000) else int((ceil(delay // 10) * 10) / 1000)
        pygame.mixer.music.fadeout(delay)
        if cnt - lstcnt > delay:
            cntdown -= 1
            if cntdown == 0:
                pygame.mixer.music.stop()
            lstcnt = cnt
    mothership_group = pygame.sprite.Group()
    bomb_group = pygame.sprite.Group()
    explosion_group = pygame.sprite.Group()
    burst_group = pygame.sprite.Group()
    # Criação do controle de tempo do jogo
    clock = pygame.time.Clock()
    ship.rect[1] -= 400

    # Laço da tela de abertura do jogo
    while splash:
        # Controle da velocidade do jogo
        clock.tick(FPS)
        screen.blit(background, (0, 0))
        screen.blit(messages[0], START_GAME)
        play_bgm(0)
        for event in pygame.event.get():
            if event.type == QUIT:
                close_game()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    close_game()
                if event.key == K_SPACE:
                    splash = False
                    run = True
                    stop_bgm(FADEOUT)
        ship_group.update()
        ship_group.draw(screen)
        pygame.display.update()

    start_enemies = start = False
    level = 1
    gameover_cntdown = 4
    countdown = 3
    last_count = laser_last_count = bullet_last_count = gameover_lstcnt = pygame.time.get_ticks()
    screen_limit_left = 0
    screen_limit_right = ((SCREEN_WIDTH - ship.get_width()) // 10) * 10
    screen_limit_bottom = ((SCREEN_HEIGHT - ship.get_height()) // 10) * 10

    def next_level():
        stop_bgm(FADEOUT)
        ship.reset_position()
        laser_group.empty()
        bullets_group.empty()
        mothership_group.empty()
        set_score(50)
        if rows < MAX_ENEMIES_ROWS:
            new_rows = rows + 1
        else:
            new_rows = MAX_ENEMIES_ROWS
        new_level = level + 1
        return new_level, new_rows

    while run:
        # Controle da velocidade do jogo
        clock.tick(FPS)
        # Controle dos eventos do jogo
        for event in pygame.event.get():
            # Evento que fecha a janela
            if event.type == QUIT:
                close_game()
            # Evento que identifica a tecla pressionada
            if event.type == KEYDOWN:
                # Teste para saber se a tecla é "BARRA DE ESPAÇO"
                if event.key == K_SPACE and countdown == 0 and len(ship_group) != 0:
                    laser_counter = pygame.time.get_ticks()
                    if laser_counter - laser_last_count > LASER_TIMING:
                        laser_group.add(ship.shoot(effects[2]))
                        laser_last_count = laser_counter

        commands = pygame.key.get_pressed()
        # Teste para saber se a tecla é "SETA PARA A ESQUERDA"
        if commands[K_LEFT] and countdown == 0:
            ship.rect[0] -= SPEED if ((ship.rect[0] // 10) * 10) != screen_limit_left else 0
        # Teste para saber se a tecla é "SETA PARA A DIREITA"
        if commands[K_RIGHT] and countdown == 0:
            ship.rect[0] += SPEED if ((ship.rect[0] // 10) * 10) != screen_limit_right else 0
        # Teste para saber se a tecla é "PAUSE"
        if commands[K_PAUSE] and countdown == 0 and len(ship_group) != 0:
            paused = True
            pause_bgm(paused)

        background = backgrounds[level]
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Desenho da imagem de fundo do jogo
        screen.blit(background, (0, 0))
        ship_group.update()
        explosion_group.update()
        burst_group.update()
        laser_group.update()
        invaders_group.update()
        bullets_group.update()
        mothership_group.update()
        bomb_group.update()
        ship_group.draw(screen)
        explosion_group.draw(screen)
        burst_group.draw(screen)
        laser_group.draw(screen)
        invaders_group.draw(screen)
        bullets_group.draw(screen)
        mothership_group.draw(screen)
        bomb_group.draw(screen)
        ship.rect[1] += START_SPEED if ((ship.rect[1] // 10) * 10) != screen_limit_bottom else 0

        if countdown != 0:
            counter = pygame.time.get_ticks()
            if level == 1:
                screen.blit(messages[1], LOADING)
                screen.blit(messages[7], LEVEL)
                screen.blit(numbers[10 + level], LVL_NUMBER)
                if countdown >= 3:
                    screen.blit(messages[2], GET_READY)
                elif countdown >= 2:
                    screen.blit(messages[3], INVADING)
                    start = True
                elif countdown >= 1:
                    screen.blit(messages[4], KILLEM_ALL)
            else:
                screen.blit(messages[1], LOADING)
                screen.blit(messages[7], LEVEL)
                screen.blit(numbers[10 + level], LVL_NUMBER)
                screen.blit(messages[2], GET_READY)
                if countdown >= 3:
                    screen.blit(numbers[13], SET_COUNTER)
                elif countdown >= 2:
                    screen.blit(numbers[12], SET_COUNTER)
                elif countdown >= 1:
                    screen.blit(numbers[11], SET_COUNTER)
            if counter - last_count > 1000:
                countdown -= 1
                if countdown == 0:
                    start_enemies = True
                    play_bgm(level)
                last_count = counter

        if (len(invaders_group) == 0) and (countdown == 2):
            mothership_come = create_invaders(rows, 5)
        if start and (len(invaders_group) == 0):
            level, rows = next_level()
            mothership_come = create_invaders(rows, 5)
            countdown = 4
            start_enemies = False

        if start_enemies and (len(bullets_group) <= MAX_BULLETS):
            bullet_counter = pygame.time.get_ticks()
            if bullet_counter - bullet_last_count > BULLET_TIMING:
                attacking_invader = choice(invaders_group.sprites())
                bullet = Bullets(
                    ship_group,
                    explosion_group,
                    (attacking_invader.rect.centerx, attacking_invader.rect.bottom),
                    effects[0]
                )
                bullets_group.add(bullet)
                bullet_last_count = bullet_counter
            if len(invaders_group) == mothership_come:
                mothership = Mothership(
                        effects[1],
                        (mothership_group, laser_group, burst_group)
                )
                mothership_group.add(mothership)
                mothership_come = -1

        if start_enemies and countdown == 0:
            screen.blit(messages[8], LEVEL_PLAY)
            screen.blit(numbers[level], LVL_PLAY_NUMBER)
            draw_score(screen, numbers)

        while paused:
            screen.blit(background, (0, 0))
            screen.blit(messages[9], PAUSE_GAME)
            screen.blit(messages[8], LEVEL_PLAY)
            screen.blit(numbers[level], LVL_PLAY_NUMBER)
            draw_score(screen, numbers)
            for event in pygame.event.get():
                # Evento que fecha a janela
                if event.type == QUIT:
                    close_game()
                # Evento que identifica a tecla pressionada
                if event.type == KEYDOWN:
                    # Teste para saber se a tecla é "ESCAPE"
                    if event.key == K_ESCAPE:
                        close_game()
                    # Teste para saber se a tecla é "SPACE"
                    if event.key == K_SPACE:
                        paused = False
                        pause_bgm(paused)
            pygame.display.update()

        if (len(mothership_group) > 0) and (len(bomb_group) == 0):
            shot_position = (randint(0, SCREEN_WIDTH - (mothership.get_width() // 2)) // 10) * 10
            if shot_position == (mothership.rect.x // 10) * 10:
                bomb = Bomb(
                    ship_group,
                    explosion_group,
                    (mothership.rect.centerx, mothership.rect.bottom),
                    effects[0]
                )
                bomb_group.add(bomb)

        if len(ship_group) == 0:
            gameover_cntr = pygame.time.get_ticks()
            stop_bgm(FADEOUT)
            screen.blit(messages[5], GAME_OVER)
            if gameover_cntr - gameover_lstcnt > 1000:
                gameover_cntdown -= 1
                if gameover_cntdown == 0:
                    run = False
                gameover_lstcnt = gameover_cntr

        pygame.display.update()
main()
try:
    if __name__ == "__main__":
        while True:
            main()
except SyntaxError as syntax_exception:
    print(f'Oops! Ocorreu um erro de sintaxe no código.\n\
        __class__ = {syntax_exception.__class__}\n\
        __doc__ = {syntax_exception.__doc__}\n\
        args = {syntax_exception.args}')
except (ValueError, ZeroDivisionError) as value_exception:
    print(f'Oops! Ocorreu um erro de valores.\n\
        __class__ = {value_exception.__class__}\n\
        __doc__ = {value_exception.__doc__}\n\
        args = {value_exception.args}')
except TypeError as type_exception:
    print(f'Oops! Ocorreu um erro de conversão de tipo de dados.\n\
        __class__ = {type_exception.__class__}\n\
        __doc__ = {type_exception.__doc__}\n\
        args = {type_exception.args}')
except Exception as general_exception:
    print(f'Oops! Ocorreu um erro não identificado.\n\
        __class__ = {general_exception.__class__}\n\
        __doc__ = {general_exception.__doc__}\n\
        args = {general_exception.args}')
finally:
    close_game()
