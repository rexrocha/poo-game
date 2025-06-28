import pygame
import os

class Som:
    def __init__(self):
        pygame.mixer.init()
        self.__fonte = pygame.font.SysFont("Arial", 24)
        self.__volume_musica = 0.5
        self.__volume_efeitos = 0.7
        self.__efeitos = {}
        self.__musica_fundo = None
        self.__musica_tocando = False
        
        try:
            self.__musica_fundo = pygame.mixer.Sound(os.path.join("assets", "musica.wav"))
            self.__musica_fundo.set_volume(self.__volume_musica)
            
            self.carregar_efeito("tiro", "tiro.wav")
            self.carregar_efeito("explosao", "explosao.wav")
            self.carregar_efeito("dano", "dano.wav")
            self.carregar_efeito("poder", "poder.wav")
        except Exception as e:
            print(f"Erro ao carregar sons: {e}")

    @property
    def fonte(self):
        return self.__fonte

    @property
    def volume_musica(self):
        return self.__volume_musica

    @volume_musica.setter
    def volume_musica(self, value):
        self.__volume_musica = max(0, min(1, value))

    @property
    def volume_efeitos(self):
        return self.__volume_efeitos

    @volume_efeitos.setter
    def volume_efeitos(self, value):
        self.__volume_efeitos = max(0, min(1, value))

    def carregar_efeito(self, nome, arquivo):
        try:
            som = pygame.mixer.Sound(os.path.join("assets", arquivo))
            som.set_volume(self.__volume_efeitos)
            self.__efeitos[nome] = som
        except Exception as e:
            print(f"Erro ao carregar efeito {nome}: {e}")
            self.__efeitos[nome] = None

    def tocar_musica(self):
        if self.__musica_fundo and not self.__musica_tocando:
            self.__musica_fundo.play(-1)  # Toca em loop
            self.__musica_tocando = True

    def parar_musica(self):
        if self.__musica_fundo and self.__musica_tocando:
            self.__musica_fundo.stop()
            self.__musica_tocando = False

    def tocar_efeito(self, nome):
        if nome in self.__efeitos and self.__efeitos[nome]:
            self.__efeitos[nome].play()

    def atualizar_volumes(self):
        if self.__musica_fundo:
            self.__musica_fundo.set_volume(self.__volume_musica)
        for efeito in self.__efeitos.values():
            if efeito:
                efeito.set_volume(self.__volume_efeitos)