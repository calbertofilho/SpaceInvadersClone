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
SCREEN_HEIGHT = 800                  # Altura da tela
FPS = 30                             # Frames por segundo

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
    # Criação do controle de tempo do jogo
    clock = pygame.time.Clock()
