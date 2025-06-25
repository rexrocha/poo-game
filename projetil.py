import pygame
import os
import math

class Projetil:
    def __init__(self, x: int, y: int, dono: int, angulo: float = 90, vertical: bool = False):
        self.__dono = dono
        self.__vertical = vertical
        self.__angulo = math.radians(angulo)
        
        try:
            if dono == 0:
                self.__imagem = pygame.image.load(os.path.join("assets", "bullet_inimigo.png"))
            else:
                self.__imagem = pygame.image.load(os.path.join("assets", "bullet.png"))
            self.__imagem = pygame.transform.scale(self.__imagem, (5, 10))
        except:
            self.__imagem = None
        
        speed = 3 if dono == 0 else 5
        if vertical:
            self.__vel_x = 0
            self.__vel_y = -speed
        else:
            self.__vel_x = speed * math.cos(self.__angulo)
            self.__vel_y = -speed * math.sin(self.__angulo)

        self.__rect = pygame.Rect(x, y, 5, 10)
        self.__gravidade = 0.1 if dono == 0 else 0

    @property
    def rect(self):
        return self.__rect

    def atualizar(self) -> bool:
        self.__rect.x += self.__vel_x
        self.__rect.y += self.__vel_y
        self.__vel_y += self.__gravidade
        
        tela = pygame.display.get_surface()
        if tela:
            if (self.__rect.bottom < 0 or 
                self.__rect.top > tela.get_height() or
                self.__rect.right < 0 or 
                self.__rect.left > tela.get_width()):
                return True
        return False

    def desenhar(self, tela: pygame.Surface) -> None:
        if self.__imagem:
            if not self.__vertical:
                img_rot = pygame.transform.rotate(self.__imagem, -math.degrees(self.__angulo))
                new_rect = img_rot.get_rect(center=self.__rect.center)
                tela.blit(img_rot, new_rect)
            else:
                tela.blit(self.__imagem, self.__rect)
        else:
            cor = (255, 0, 0) if self.__dono == 0 else (255, 255, 0)
            pygame.draw.rect(tela, cor, self.__rect)