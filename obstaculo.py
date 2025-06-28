import pygame
import os
from abc import ABC, abstractmethod

class Obstaculo(ABC):
    def __init__(self, x: int, y: int, largura: int, altura: int):
        try:
            self.__imagem = pygame.image.load(os.path.join("assets", "plataforma.png"))
            self.__imagem = pygame.transform.scale(self.__imagem, (largura, altura))
        except:
            self.__imagem = pygame.Surface((largura, altura))
            self.__imagem.fill((150, 75, 0))
        self.__rect = self.__imagem.get_rect(topleft=(x, y))

    @property
    def rect(self):
        return self.__rect

    @abstractmethod
    def atualizar(self):
        pass

    def desenhar(self, tela: pygame.Surface) -> None:
        tela.blit(self.__imagem, self.__rect)

class ObstaculoFixo(Obstaculo):
    def atualizar(self):
        pass

class ObstaculoMovel(Obstaculo):
    def __init__(self, x: int, y: int, largura: int, altura: int):
        super().__init__(x, y, largura, altura)
        self.__vel = 2
        self.__direcao = 1
        self.__x_original = x

    def atualizar(self) -> None:
        self.rect.x += self.__vel * self.__direcao
        if abs(self.rect.x - self.__x_original) > 100:
            self.__direcao *= -1