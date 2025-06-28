import pygame
import os
import math

class Projetil:
    def __init__(self, x: int, y: int, dono: int, vertical: bool = True):  # Adicionei parâmetro vertical
        self.__dono = dono
        self.__vertical = vertical  # Novo atributo
        
        try:
            if dono == 0:
                self.__imagem = pygame.image.load(os.path.join("assets", "bullet_inimigo.png"))
            else:
                self.__imagem = pygame.image.load(os.path.join("assets", "bullet.png"))
            self.__imagem = pygame.transform.scale(self.__imagem, (5, 10))
        except:
            self.__imagem = None
        
        speed = 3 if dono == 0 else 5
        # Sempre movimento vertical
        self.__vel_x = 0
        self.__vel_y = -speed if dono > 0 else speed  # Jogador: sobe, Inimigo: desce
        
        self.__rect = pygame.Rect(x, y, 5, 10)
        self.__gravidade = 0  # Removi gravidade para movimento puramente vertical

    @property
    def rect(self):
        return self.__rect

    def atualizar(self) -> bool:
        self.__rect.y += self.__vel_y
        
        tela = pygame.display.get_surface()
        if tela:
            if (self.__rect.bottom < 0 or 
                self.__rect.top > tela.get_height()):
                return True
        return False

    def desenhar(self, tela: pygame.Surface) -> None:
        if self.__imagem:
            tela.blit(self.__imagem, self.__rect)  # Sem rotação
        else:
            cor = (255, 0, 0) if self.__dono == 0 else (255, 255, 0)
            pygame.draw.rect(tela, cor, self.__rect)
     #não é usado
    def __eq__(self, other: 'Projetil') -> bool:
        return (self.rect.x == other.rect.x and 
                self.rect.y == other.rect.y and 
                self.__dono == other.__dono)
