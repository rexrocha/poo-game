import pygame
import sys
import os
from menu import Menu
from gerenciador import Gerenciador
from som import Som
from salvar_carregar import SalvarCarregar

def main():
    pygame.init()
    largura, altura = 800, 600
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("Bullet Hell - Projeto POO")

    try:
        icon = pygame.image.load(os.path.join("assets", "icon.png"))
        pygame.display.set_icon(icon)
    except:
        pass

    clock = pygame.time.Clock()
    fps = 60

    som = Som()
    menu = Menu(tela, som)
    salvar = SalvarCarregar()
    gerenciador = None

    estado = "menu"
    tipo_jogador = 1

    while True:
        if estado == "menu":
            som.tocar_musica()  
            resultado = menu.executar()
            if resultado is None:
                estado = "sair"
            else:
                estado, tipo_jogador = resultado
        elif estado == "novo_jogo":
            gerenciador = Gerenciador(tela, som, salvar, tipo_jogador)
            estado = "jogo"
        elif estado == "continuar":
            dados = salvar.carregar()
            gerenciador = Gerenciador(tela, som, salvar, dados.get("tipo_jogador", 1)) 
            gerenciador.jogador.vida = dados.get("vida", 3)
            gerenciador.jogador.rect.x = dados.get("pos_x", 400)
            gerenciador.jogador.rect.y = dados.get("pos_y", 500)
            gerenciador.score = dados.get("score", 0)
            estado = "jogo"
        elif estado == "jogo":
            resultado = gerenciador.executar()
            if resultado == "game_over":
                estado = "game_over"
            elif resultado == "menu":
                estado = "menu"
        elif estado == "game_over":
            estado = menu.exibir_game_over(gerenciador.score)
        elif estado == "sair":
            pygame.quit()
            sys.exit()

        clock.tick(fps)

if __name__ == '__main__':
    main()