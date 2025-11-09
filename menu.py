import traceback
import pygame
import os
import json

class Menu:
    def __init__(self, tela, som):
        self.__tela = tela
        self.__som = som
        self.__fonte = pygame.font.SysFont("Arial", 32)
        self.__fonte_pequena = pygame.font.SysFont("Arial", 24)
        self.__ranking = []
        self.__nome_jogador = ""
        self.__fundo = None
        self.carregar_ranking()
        
        try:
            self.__fundo = pygame.image.load(os.path.join("assets", "fundo_menu.jpg"))
            self.__fundo = pygame.transform.scale(self.__fundo, (self.__tela.get_width(), self.__tela.get_height()))
        except:
            self.__fundo = None

    @property
    def nome_jogador(self):
        return self.__nome_jogador

    @nome_jogador.setter
    def nome_jogador(self, value):
        self.__nome_jogador = value[:15]

    @property
    def ranking(self):
        return self.__ranking

    def executar(self):
