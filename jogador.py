import pygame
import time
import os
import random
from projetil import Projetil

class Jogador:
    def __init__(self, x: int, y: int, tipo: int = 1):
        self.__tipo = tipo
        self.__vida = 3
        self.__projeteis = []
        self.__ultimo_poder = time.time()
        self.__tempo_recarga = 5
        self.__pulando = False
        self.__vel_y = 0
        self.__vel_x = 0
        self.__gravidade = 0.5
        self.__pulos_restantes = 2
        
        try:
            if tipo == 1:
                self.__imagem = pygame.image.load(os.path.join("assets", "jogador1.png"))
            else:
                self.__imagem = pygame.image.load(os.path.join("assets", "jogador2.png"))
            self.__imagem = pygame.transform.scale(self.__imagem, (40, 40))
        except:
            self.__imagem = pygame.Surface((40, 40))
            self.__imagem.fill((0, 255, 0) if tipo == 1 else (0, 0, 255))
        
        self.__rect = self.__imagem.get_rect(center=(x, y))
        self.__vel = 5
        self.__tela_largura = pygame.display.get_surface().get_width()

    @property
    def tipo(self):
        return self.__tipo

    @property
    def rect(self):
        return self.__rect

    @property
    def vida(self):
        return self.__vida

    @vida.setter
    def vida(self, value):
        self.__vida = max(0, value)

    @property
    def projeteis(self):
        return self.__projeteis

    @property
    def ultimo_poder(self):
        return self.__ultimo_poder

    @property
    def tempo_recarga(self):
        return self.__tempo_recarga

    @property
    def pulando(self):
        return self.__pulando

    @pulando.setter
    def pulando(self, value):
        self.__pulando = value

    @property
    def vel_y(self):
        return self.__vel_y

    @vel_y.setter
    def vel_y(self, value):
        self.__vel_y = value

    @property
    def vel_x(self):
        return self.__vel_x

    @vel_x.setter
    def vel_x(self, value):
        self.__vel_x = value

    @property
    def pulos_restantes(self):
        return self.__pulos_restantes

    @pulos_restantes.setter
    def pulos_restantes(self, value):
        self.__pulos_restantes = max(0, value)

    def mover(self, teclas: list) -> None:
        self.__vel_x = 0
        vento = random.uniform(-0.5, 0.5)

        if teclas[pygame.K_UP] and not self.__pulando and self.__pulos_restantes > 0:
            self.__vel_y = -12
            self.__pulando = True
            self.__pulos_restantes -= 1
        
        if teclas[pygame.K_LEFT]: 
            self.__vel_x = -(self.__vel + vento)
        if teclas[pygame.K_RIGHT]: 
            self.__vel_x = (self.__vel - vento)

        self.__rect.x += self.__vel_x
        self.__rect.x = max(0, min(self.__tela_largura - self.__rect.width, self.__rect.x))

        self.__vel_y += self.__gravidade
        self.__rect.y += self.__vel_y
        
        if self.__rect.bottom > 500:
            self.__rect.bottom = 500
            self.__vel_y = 0
            self.__pulando = False
            self.__pulos_restantes = 2

    def atirar(self) -> None:
        if self.__tipo == 1:
            self.__projeteis.append(Projetil(self.__rect.centerx, self.__rect.top, self.__tipo))
        else:
            self.__projeteis.append(Projetil(self.__rect.centerx - 15, self.__rect.top, self.__tipo, vertical=True))
            self.__projeteis.append(Projetil(self.__rect.centerx + 15, self.__rect.top, self.__tipo, vertical=True))

    def poder_especial(self, inimigos) -> None:
        agora = time.time()
        if agora - self.__ultimo_poder >= self.__tempo_recarga:
            if self.__tipo == 1:
                for angle in range(-30, 31, 15):
                    self.__projeteis.append(Projetil(self.__rect.centerx, self.__rect.top, self.__tipo, 90 + angle))
            else:
                for inimigo in inimigos:
                    inimigo.eliminado = True
            self.__ultimo_poder = agora

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.blit(self.__imagem, self.__rect)
        for p in self.__projeteis:
            p.desenhar(tela)