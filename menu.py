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

    def executar(self):
        opcao_selecionada = 0
        opcoes = ["Novo Jogo", "Continuar", "Configurações", "Ranking", "Sair"]
        
        while True:
            if self.__fundo:
                self.__tela.blit(self.__fundo, (0, 0))
            else:
                self.__tela.fill((0, 0, 0))
            
            titulo = self.__fonte.render("Bullet Hell", True, (255, 255, 0))
            self.__tela.blit(titulo, (self.__tela.get_width()//2 - titulo.get_width()//2, 50))
            
            for i, opcao in enumerate(opcoes):
                cor = (0, 255, 0) if i == opcao_selecionada else (255, 255, 255)
                texto = self.__fonte_pequena.render(opcao, True, cor)
                self.__tela.blit(texto, (self.__tela.get_width()//2 - texto.get_width()//2, 150 + i*50))
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair", 1
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        opcao_selecionada = (opcao_selecionada - 1) % len(opcoes)
                    if evento.key == pygame.K_DOWN:
                        opcao_selecionada = (opcao_selecionada + 1) % len(opcoes)
                    if evento.key == pygame.K_RETURN:
                        if opcoes[opcao_selecionada] == "Novo Jogo":
                            tipo_jogador = self.escolher_personagem()
                            if tipo_jogador is None: 
                                return "sair", 1
                            return "novo_jogo", tipo_jogador
                        elif opcoes[opcao_selecionada] == "Continuar":
                            return "continuar", 1
                        elif opcoes[opcao_selecionada] == "Configurações":
                            self.executar_configuracoes()
                        elif opcoes[opcao_selecionada] == "Ranking":
                            ranking_result = self.exibir_ranking()
                            if ranking_result == "sair":
                                return "sair", 1
                        elif opcoes[opcao_selecionada] == "Sair":
                            return "sair", 1

            pygame.display.flip()

    def escolher_personagem(self):
        personagem_selecionado = 0
        personagens = ["Personagem 1 (Veloz)", "Personagem 2 (Forte)"]
        
        while True:
            if self.__fundo:
                self.__tela.blit(self.__fundo, (0, 0))
            else:
                self.__tela.fill((0, 0, 0))
            
            titulo = self.__fonte.render("Selecione seu personagem", True, (255, 255, 255))
            self.__tela.blit(titulo, (self.__tela.get_width()//2 - titulo.get_width()//2, 50))
            
            for i, personagem in enumerate(personagens):
                cor = (0, 255, 0) if i == personagem_selecionado else (255, 255, 255)
                texto = self.__fonte_pequena.render(personagem, True, cor)
                self.__tela.blit(texto, (self.__tela.get_width()//2 - texto.get_width()//2, 150 + i*50))
            
            nome_texto = self.__fonte_pequena.render("Nome: " + self.__nome_jogador, True, (255, 255, 255))
            self.__tela.blit(nome_texto, (self.__tela.get_width()//2 - nome_texto.get_width()//2, 300))
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return None
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        personagem_selecionado = (personagem_selecionado - 1) % len(personagens)
                    if evento.key == pygame.K_DOWN:
                        personagem_selecionado = (personagem_selecionado + 1) % len(personagens)
                    if evento.key == pygame.K_RETURN:
                        return personagem_selecionado + 1
                    if evento.key == pygame.K_BACKSPACE:
                        self.__nome_jogador = self.__nome_jogador[:-1]
                    elif evento.key != pygame.K_RETURN:
                        if len(self.__nome_jogador) < 15:
                            self.__nome_jogador += evento.unicode

            pygame.display.flip()

    def executar_configuracoes(self):
        volume_musica = self.__som.volume_musica
        volume_efeitos = self.__som.volume_efeitos
        config_selecionada = 0
        configs = ["Volume Música", "Volume Efeitos", "Salvar e Voltar"]
        
        while True:
            if self.__fundo:
                self.__tela.blit(self.__fundo, (0, 0))
            else:
                self.__tela.fill((0, 0, 0))
            
            titulo = self.__fonte.render("Configurações", True, (255, 255, 255))
            self.__tela.blit(titulo, (self.__tela.get_width()//2 - titulo.get_width()//2, 50))
            
            for i, config in enumerate(configs):
                cor = (0, 255, 0) if i == config_selecionada else (255, 255, 255)
                texto = self.__fonte_pequena.render(config, True, cor)
                self.__tela.blit(texto, (self.__tela.get_width()//2 - 150, 150 + i*50))
                
                if i == 0:
                    pygame.draw.rect(self.__tela, (100, 100, 100), (self.__tela.get_width()//2 + 50, 150 + i*50, 200, 20))
                    pygame.draw.rect(self.__tela, (0, 255, 0), (self.__tela.get_width()//2 + 50, 150 + i*50, 200 * volume_musica, 20))
                elif i == 1:
                    pygame.draw.rect(self.__tela, (100, 100, 100), (self.__tela.get_width()//2 + 50, 150 + i*50, 200, 20))
                    pygame.draw.rect(self.__tela, (0, 0, 255), (self.__tela.get_width()//2 + 50, 150 + i*50, 200 * volume_efeitos, 20))
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_UP:
                        config_selecionada = (config_selecionada - 1) % len(configs)
                    if evento.key == pygame.K_DOWN:
                        config_selecionada = (config_selecionada + 1) % len(configs)
                    if evento.key == pygame.K_RETURN:
                        if config_selecionada == 2:
                            self.__som.volume_musica = volume_musica
                            self.__som.volume_efeitos = volume_efeitos
                            self.__som.atualizar_volumes()
                            return
                    if evento.key == pygame.K_LEFT:
                        if config_selecionada == 0:
                            volume_musica = max(0, round(volume_musica - 0.1, 1))
                        elif config_selecionada == 1:
                            volume_efeitos = max(0, round(volume_efeitos - 0.1, 1))
                    if evento.key == pygame.K_RIGHT:
                        if config_selecionada == 0:
                            volume_musica = min(1, round(volume_musica + 0.1, 1))
                        elif config_selecionada == 1:
                            volume_efeitos = min(1, round(volume_efeitos + 0.1, 1))

            pygame.display.flip()

    def exibir_ranking(self):
        while True:
            if self.__fundo:
                self.__tela.blit(self.__fundo, (0, 0))
            else:
                self.__tela.fill((0, 0, 0))
            
            titulo = self.__fonte.render("Ranking", True, (255, 255, 0))
            self.__tela.blit(titulo, (self.__tela.get_width()//2 - titulo.get_width()//2, 50))
            
            for i, entrada in enumerate(self.__ranking[:10]): 
                texto = self.__fonte_pequena.render(f"{i+1}. {entrada.get('nome', 'Desconhecido')} - {entrada.get('score', 0)}", True, (255, 255, 255))
                self.__tela.blit(texto, (self.__tela.get_width()//2 - texto.get_width()//2, 150 + i*30))
            
            voltar = self.__fonte_pequena.render("Pressione ESC para voltar", True, (255, 255, 255))
            self.__tela.blit(voltar, (self.__tela.get_width()//2 - voltar.get_width()//2, 500))
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "menu"

            pygame.display.flip()

    def exibir_game_over(self, score):
        if self.__nome_jogador and score > 0: 
            self.__ranking.append({"nome": self.__nome_jogador, "score": score})
            self.__ranking.sort(key=lambda x: x["score"], reverse=True)
            self.salvar_ranking()
        
        while True:
            if self.__fundo:
                self.__tela.blit(self.__fundo, (0, 0))
            else:
                self.__tela.fill((0, 0, 0))
            
            game_over = self.__fonte.render("GAME OVER", True, (255, 0, 0))
            self.__tela.blit(game_over, (self.__tela.get_width()//2 - game_over.get_width()//2, 150))
            
            score_text = self.__fonte_pequena.render(f"Pontuação: {score}", True, (255, 255, 255))
            self.__tela.blit(score_text, (self.__tela.get_width()//2 - score_text.get_width()//2, 250))
            
            voltar = self.__fonte_pequena.render("Pressione ENTER para voltar ao menu", True, (255, 255, 255))
            self.__tela.blit(voltar, (self.__tela.get_width()//2 - voltar.get_width()//2, 350))
            
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    return "sair"
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        return "menu"

            pygame.display.flip()

    def carregar_ranking(self):
        try:
            with open("ranking.json", "r") as f:
                self.__ranking = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self.__ranking = []

    def salvar_ranking(self) -> None:
        try:
            os.makedirs(os.path.dirname("ranking.json") or '.', exist_ok=True)
            with open("ranking.json", "w") as f:
                json.dump(self.__ranking, f, indent=4)
        except IOError as e:
            print(f"Erro de I/O ao salvar ranking: {e}")
        except Exception as e:
            print(f"Erro inesperado ao salvar ranking: {e}")
            traceback.print_exc()