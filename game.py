'''
Jogo Space Invaders em Python
Utilizando a biblioteca: PyGame

Criado por: Carlos Alberto Morais Moura Filho
Versão: 1.0
Atualizado em: 20/05/2021
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
from math import ceil
import pygame
from pygame.constants import ( K_LEFT, K_RIGHT, QUIT, KEYDOWN, K_ESCAPE, K_SPACE )
# Constantes
BASE_DIR = path.dirname(__file__)    # Diretorio do jogo
SCREEN_WIDTH = 600                   # Comprimento da tela
SCREEN_HEIGHT = 860                  # Altura da tela
SPEED = 10                           # Velocidade do jogo
BULLET_SPEED = START_SPEED = 5       # Velocidade para inicio do jogo e das balas dos inimigos
FPS = 30                             # Frames por segundo
MAX_ROWS = 10                        # Número máximo de linhas na matriz de inimigos
MAX_BULLETS = 5                      # Quantidade de balas, ao mesmo tempo, na tela, do inimigo
ENEMY_ANIMATION_TIME = 300           # Tempo, em milissegundos, entre as trocas das imagens do inimigo
BULLET_ANIMATION_TIME = 200          # Tempo, em milissegundos, entre as trocas das imagens das balas
LASER_TIMING = 500                   # Tempo, em milissegundos, entre um disparo e outro
BULLET_TIMING = 2 * LASER_TIMING     # Tempo, em milissegundos, entre uma bala e outra
START_GAME = (0, 0)                  # Posição (x, y) da Splash Screen
LOADING = (440, 10)
GET_READY = (103, 525)               # Posição (x, y) da mensagem GET READY !
INVADING = (103, 525)                # Posição (x, y) da mensagem SET ENEMIES...
KILLEM_ALL = (103, 525)              # Posição (x, y) da mensagem KILL'EM ALL
GAME_OVER = (103, 525)               # Posição (x, y) da mensagem GAME OVER
SET_COUNTER = (282, 580)             # Posição (x, y) do número da contagem
HIGH_SCORE = (0, 0)                  # Posição (x, y) da mensagem HIGH SCORE
VOLUME_BGM = 0.8
FADEOUT = 1500
VOLUME_FX = 0.4

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

    def shoot(self, laser_fx):
        '''Função que representa a ação de atirar com a nave'''
        laser_fx.set_volume(VOLUME_FX)
        pygame.mixer.Sound.play(laser_fx)
        return Laser(self.rect[0] + 33, self.rect[1] - 28)

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

class Invaders(pygame.sprite.Sprite):
    '''Classe que representa os inimigos'''
    def __init__(self, alien, pos_x, pos_y, sound, invaders_group, laser_group):
        pygame.sprite.Sprite.__init__(self)
        self.enemies = (
            (
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/White-Enemy1.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/White-Enemy1_.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/White-Enemy-Burst.png').convert_alpha()
            ),
            (
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Green-Enemy2.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Green-Enemy2_.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Green-Enemy-Burst.png').convert_alpha()
            ),
            (
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Yellow-Enemy3.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Yellow-Enemy3_.png').convert_alpha(),
                pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/Yellow-Enemy-Burst.png').convert_alpha()
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
        self.laser_group = laser_group
        self.invaders_group = invaders_group
        self.explosion = sound
        self.explosion.set_volume(VOLUME_FX)

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
        if pygame.sprite.groupcollide(self.invaders_group, self.laser_group, True, True, pygame.sprite.collide_mask):
            pygame.mixer.Sound.play(self.explosion)
            self.current_image = 2

class Bullets(pygame.sprite.Sprite):
    '''Classe que representa a bala do inimigo'''
    def __init__(self, pos_x, pos_y):
        pygame.sprite.Sprite.__init__(self)
        self.images = (
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/bullet1.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/bullet2.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/bullet3.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/bullet4.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/bullet5.png').convert_alpha(),
            pygame.image.load(f'{BASE_DIR}/assets/sprites/enemies/invaders/bullet6.png').convert_alpha()
        )
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = pos_x
        self.rect[1] = pos_y
        self.last_count = pygame.time.get_ticks()
        self.speed = BULLET_SPEED

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

    def get_width(self):
        '''Função que retorna a largura da bala do inimigo'''
        return self.image.get_size()[0]

    def get_height(self):
        '''Função que retorna o comprimento da bala do inimigo'''
        return self.image.get_size()[1]

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
    bgm = (
        f'{BASE_DIR}/assets/sounds/bgm/main.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level1.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level2.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level3.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level4.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level5.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level6.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level7.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level8.mid',
        f'{BASE_DIR}/assets/sounds/bgm/level9.mid',
        f'{BASE_DIR}/assets/sounds/bgm/boss.mid'
    )
    effects = (
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/fx/{sound_type}/death.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/fx/{sound_type}/explosion.{sound_type}'),
        pygame.mixer.Sound(f'{BASE_DIR}/assets/sounds/fx/{sound_type}/shot.{sound_type}')
    )
    # Criação das mensagens do jogo
    messages = (
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/start_game.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/loading.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/get_ready.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/invading.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/kill\'em_all.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/game_over.png').convert_alpha(),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/messages/high_score.png').convert_alpha()
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
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/main.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level1.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level2.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level3.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level4.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level5.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level6.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level7.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level8.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/level9.png'),
        pygame.image.load(f'{BASE_DIR}/assets/sprites/sceneries/boss.png')
    )
    background = backgrounds[0]
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    ship_group = pygame.sprite.Group()
    ship = Spaceship()
    ship_group.add(ship)
    laser_group = pygame.sprite.Group()
    invaders_group = pygame.sprite.Group()
    def create_invaders(rows, cols):
        for row in range(rows):
            invader = randint(0, 2)
            for item in range(cols):
                enemy = Invaders(invader, 100 + item * 100, 100 + row * 50, effects[1], invaders_group, laser_group)
                invaders_group.add(enemy)
    bullets_group = pygame.sprite.Group()
    def play_bgm(track):
        if not(pygame.mixer.music.get_busy()):
            pygame.mixer.music.load(bgm[track])
            pygame.mixer.music.set_volume(VOLUME_BGM)
            pygame.mixer.music.play()
    def stop_bgm(delay):
        lstcnt = cnt = pygame.time.get_ticks()
        cntdown = 1 if (delay < 1000) else int((ceil(delay // 10) * 10) / 1000)
        pygame.mixer.music.fadeout(delay)
        if cnt - lstcnt > delay:
            cntdown -= 1
            if cntdown == 0:
                pygame.mixer.music.stop()
            lstcnt = cnt
    # Criação do controle de tempo do jogo
    clock = pygame.time.Clock()
    # Laço da tela de abertura do jogo
    ship.rect[1] -= 400
    play_bgm(0)

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
                    stop_bgm(FADEOUT)
        ship_group.update()
        ship_group.draw(screen)
        pygame.display.update()

    start_enemies = start = False
    level = 1
    countdown = 3
    last_count = laser_last_count = bullet_last_count = pygame.time.get_ticks()
    screen_limit_left = 0
    screen_limit_right = ((SCREEN_WIDTH - ship.get_width()) // 10) * 10
    screen_limit_bottom = ((SCREEN_HEIGHT - ship.get_height()) // 10) * 10

    def next_level():
        stop_bgm(FADEOUT)
        ship.reset_position()
        laser_group.empty()
        bullets_group.empty()
        if rows < MAX_ROWS:
            new_rows = rows + 1
        else:
            new_rows = MAX_ROWS
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

        background = backgrounds[level]
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        # Desenho da imagem de fundo do jogo
        screen.blit(background, (0, 0))
        ship_group.update()
        laser_group.update()
        invaders_group.update()
        bullets_group.update()
        ship_group.draw(screen)
        laser_group.draw(screen)
        invaders_group.draw(screen)
        bullets_group.draw(screen)
        ship.rect[1] += START_SPEED if ((ship.rect[1] // 10) * 10) != screen_limit_bottom else 0

        if countdown != 0:
            counter = pygame.time.get_ticks()
            if level == 1:
                screen.blit(messages[1], LOADING)
                if countdown >= 3:
                    screen.blit(messages[2], GET_READY)
                elif countdown >= 2:
                    screen.blit(messages[3], INVADING)
                    start = True
                elif countdown >= 1:
                    screen.blit(messages[4], KILLEM_ALL)
            else:
                screen.blit(messages[1], LOADING)
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
            create_invaders(rows, 5)
        if start and (len(invaders_group) == 0):
            level, rows = next_level()
            create_invaders(rows, 5)
            countdown = 3
            start_enemies = False

        if start_enemies and (len(bullets_group) <= MAX_BULLETS):
            bullet_counter = pygame.time.get_ticks()
            if bullet_counter - bullet_last_count > BULLET_TIMING:
                attacking_invader = choice(invaders_group.sprites())
                bullet = Bullets(attacking_invader.rect.centerx, attacking_invader.rect.bottom)
                bullets_group.add(bullet)
                bullet_last_count = bullet_counter

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
