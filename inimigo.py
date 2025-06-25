import pygame
import random
import os
import math
import time
from projetil import Projetil

class Inimigo:
    def __init__(self, x: int, y: int, tipo: int = 1):
        self.__tipo = tipo
        self.__eliminado = False
        
        try:
            if tipo == 1:
                self.__imagem = pygame.image.load(os.path.join("assets", "inimigo1.png"))
            else:
                self.__imagem = pygame.image.load(os.path.join("assets", "inimigo2.png"))
            self.__imagem = pygame.transform.scale(self.__imagem, (40, 40))
        except:
            self.__imagem = pygame.Surface((40, 40))
            self.__imagem.fill((255, 0, 0) if tipo == 1 else (255, 165, 0))
        
        self.__rect = self.__imagem.get_rect(topleft=(x, y))
        self.__vel = 2 if tipo == 2 else random.randint(1, 3)
        self.__vida = 2 if tipo == 2 else 1
        self.__ultimo_tiro = time.time()
        self.__tempo_entre_tiros = random.uniform(1.0, 3.0)
        self.__projeteis = []

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
    def eliminado(self):
        return self.__eliminado

    @eliminado.setter
    def eliminado(self, value):
        self.__eliminado = value

    @property
    def projeteis(self):
        return self.__projeteis

    def mover(self, jogador) -> None:
        if self.__tipo == 2:
            dx = jogador.rect.centerx - self.__rect.centerx
            dy = jogador.rect.centery - self.__rect.centery
            dist = max(1, math.sqrt(dx*dx + dy*dy))
            
            self.__rect.x += (dx / dist) * self.__vel
            self.__rect.y += (dy / dist) * self.__vel
            
            agora = time.time()
            if agora - self.__ultimo_tiro > self.__tempo_entre_tiros / 2:
                self.atirar()
                self.__ultimo_tiro = agora
        else:
            self.__rect.y += self.__vel
            self.__rect.x += random.choice([-1, 0, 1])
            
            if random.random() < 0.01:
                self.atirar()

    def atirar(self) -> None:
        self.__projeteis.append(Projetil(self.__rect.centerx, self.__rect.bottom, 0))

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.blit(self.__imagem, self.__rect)
        for p in self.__projeteis:
            p.desenhar(tela)