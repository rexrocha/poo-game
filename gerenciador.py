import pygame
import os
import random
import time
from jogador import Jogador
from inimigo import Inimigo
from obstaculo import ObstaculoFixo, ObstaculoMovel

class Gerenciador:
    def __init__(self, tela, som, salvar, tipo_jogador: int = 1):
        self.__tela = tela
        self.__som = som
        self.__salvar = salvar
        self.__jogador = Jogador(400, 500, tipo_jogador)
        self.__inimigos = []
        self.__obstaculos = []
        self.__score = 0
        self.__tempo_inicio = pygame.time.get_ticks()
        self.__fundo = None
        
        self.gerar_obstaculos()
        self.gerar_inimigos()
        
        try:
            self.__fundo = pygame.image.load(os.path.join("assets", "fundo_jogo.jpg"))
            self.__fundo = pygame.transform.scale(self.__fundo, (self.__tela.get_width(), self.__tela.get_height()))
        except Exception as e:
            print(f"Erro ao carregar fundo: {e}")

    @property
    def score(self):
        return self.__score

    @score.setter
    def score(self, value):
        self.__score = max(0, value)
        
    @property
    def jogador(self):
        return self.__jogador

    def executar(self):
        while True:
            tempo_decorrido = (pygame.time.get_ticks() - self.__tempo_inicio) // 1000
            self.score = tempo_decorrido * 10
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.salvar_jogo()
                    return "sair"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        self.salvar_jogo()
                        return "menu"
                    if evento.key == pygame.K_z:
                        self.__jogador.atirar()
                        self.__som.tocar_efeito("tiro")
                    if evento.key == pygame.K_x:
                        self.__jogador.poder_especial(self.__inimigos)
                        self.__som.tocar_efeito("poder")
                if evento.type == pygame.USEREVENT + 1:
                    self.gerar_inimigos()
            
            teclas = pygame.key.get_pressed()
            self.__jogador.mover(teclas)
            
            self.atualizar_projeteis()
            resultado_colisao = self.processar_colisoes()
            if resultado_colisao == "game_over":
                return "game_over"
            self.atualizar_obstaculos()
            self.renderizar()

            pygame.display.flip()
            pygame.time.delay(30)

    def atualizar_projeteis(self):
        for p in self.__jogador.projeteis[:]:
            if p.atualizar():
                self.__jogador.projeteis.remove(p)
        
        for inimigo in self.__inimigos:
            for p in inimigo.projeteis[:]:
                if p.atualizar():
                    inimigo.projeteis.remove(p)

    def processar_colisoes(self):
        inimigos_para_remover = []
        
        for inimigo in self.__inimigos[:]:
            if inimigo.eliminado:
                inimigos_para_remover.append(inimigo)
                self.score += 100
                continue
                
            inimigo.mover(self.__jogador)
            
            for p in inimigo.projeteis[:]:
                if p.rect.colliderect(self.__jogador.rect):
                    self.__jogador.vida -= 1
                    inimigo.projeteis.remove(p)
                    self.__som.tocar_efeito("dano")
                    if self.__jogador.vida <= 0:
                        return "game_over"
                elif p.rect.top > self.__tela.get_height() or p.rect.bottom < 0:
                    inimigo.projeteis.remove(p)
            
            for p in self.__jogador.projeteis[:]:
                if p.rect.colliderect(inimigo.rect):
                    inimigo.vida -= 1
                    self.__jogador.projeteis.remove(p)
                    self.__som.tocar_efeito("explosao")
                    if inimigo.vida <= 0:
                        inimigos_para_remover.append(inimigo)
                        self.score += 100
                        break
            
            if inimigo.rect.colliderect(self.__jogador.rect):
                self.__jogador.vida -= 1
                if inimigo not in inimigos_para_remover:
                    inimigos_para_remover.append(inimigo)
                self.__som.tocar_efeito("dano")
                if self.__jogador.vida <= 0:
                    return "game_over"
            
            if inimigo.rect.top > self.__tela.get_height():
                if inimigo not in inimigos_para_remover:
                    inimigos_para_remover.append(inimigo)
        
        for inimigo in inimigos_para_remover:
            if inimigo in self.__inimigos:
                self.__inimigos.remove(inimigo)
        
        for obstaculo in self.__obstaculos:
            if self.__jogador.rect.colliderect(obstaculo.rect):
                if self.__jogador.vel_y > 0 and self.__jogador.rect.bottom > obstaculo.rect.top and self.__jogador.rect.top < obstaculo.rect.top:
                    self.__jogador.rect.bottom = obstaculo.rect.top
                    self.__jogador.vel_y = 0
                    self.__jogador.pulando = False
                    self.__jogador.pulos_restantes = 2
                elif self.__jogador.rect.right > obstaculo.rect.left and self.__jogador.rect.left < obstaculo.rect.left and self.__jogador.vel_x > 0:
                    self.__jogador.rect.right = obstaculo.rect.left
                elif self.__jogador.rect.left < obstaculo.rect.right and self.__jogador.rect.right > obstaculo.rect.right and self.__jogador.vel_x < 0:
                    self.__jogador.rect.left = obstaculo.rect.right
                elif self.__jogador.vel_y < 0 and self.__jogador.rect.top < obstaculo.rect.bottom and self.__jogador.rect.bottom > obstaculo.rect.bottom:
                    self.__jogador.rect.top = obstaculo.rect.bottom
                    self.__jogador.vel_y = 0

    def atualizar_obstaculos(self):
        for obstaculo in self.__obstaculos:
            obstaculo.atualizar()

    def renderizar(self):
        if self.__fundo:
            self.__tela.blit(self.__fundo, (0, 0))
        else:
            self.__tela.fill((30, 30, 30))
            
        for obstaculo in self.__obstaculos:
            obstaculo.desenhar(self.__tela)
            
        self.__jogador.desenhar(self.__tela)
        for inimigo in self.__inimigos:
            inimigo.desenhar(self.__tela)
        
        vida_text = self.__som.fonte.render(f"Vida: {self.__jogador.vida}", True, (255, 255, 255))
        score_text = self.__som.fonte.render(f"Pontuação: {self.score}", True, (255, 255, 255))
        self.__tela.blit(vida_text, (10, 10))
        self.__tela.blit(score_text, (10, 50))
        
        tempo_recarga = max(0, self.__jogador.tempo_recarga - (time.time() - self.__jogador.ultimo_poder))
        if tempo_recarga > 0:
            recarga_text = self.__som.fonte.render(f"Poder: {tempo_recarga:.1f}s", True, (255, 255, 0))
            self.__tela.blit(recarga_text, (10, 90))

    def gerar_inimigos(self):
        if len(self.__inimigos) < 10:
            x = random.randint(50, self.__tela.get_width() - 50)
            tipo = random.choices([1, 2], weights=[0.7, 0.3])[0]
            self.__inimigos.append(Inimigo(x, -50, tipo))
        
        pygame.time.set_timer(pygame.USEREVENT + 1, random.randint(1000, 3000))

    def gerar_obstaculos(self):
        self.__obstaculos.append(ObstaculoFixo(100, 400, 200, 20))
        self.__obstaculos.append(ObstaculoFixo(500, 350, 150, 20))
        self.__obstaculos.append(ObstaculoFixo(300, 300, 100, 20))
        self.__obstaculos.append(ObstaculoMovel(200, 200, 80, 20))

    def salvar_jogo(self):
        dados = {
            "score": self.score,
            "vida": self.__jogador.vida,
            "pos_x": self.__jogador.rect.x,
            "pos_y": self.__jogador.rect.y,
            "tipo_jogador": self.__jogador.tipo
        }
        self.__salvar.salvar(dados)