import pygame
from config import *  # Importa as configurações globais, como dimensões do ecrã e cores
from shed import shed  # Importa a função ou classe relacionada ao "shed" (galpão/abrigo)

# Classe Rounds: responsável pela lógica das rondas no jogo
class Rounds:
    def display_round_message(self, message, screen, font):
        """Exibe uma mensagem no centro do ecrã com efeito de sombra."""
        # Renderizar uma sombra para o texto com uma cor cinzenta escura
        shadow_text = font.render(message, True, (50, 50, 50))  # Cor da sombra
        shadow_rect = shadow_text.get_rect(center=(width // 2 + 2, height // 2 + 2))  # Posiciona a sombra
        screen.blit(shadow_text, shadow_rect)  # Desenha a sombra no ecrã
    
        # Renderizar o texto principal a branco e centralizado
        text = font.render(message, True, white)  # Texto principal
        text_rect = text.get_rect(center=(width // 2, height // 2))  # Posiciona o texto
        screen.blit(text, text_rect)  # Desenha o texto no ecrã

    def increase_difficulty(self, current_round, enemies):
        """Aumenta a dificuldade dos inimigos com base na ronda atual."""
        for enemy in enemies:  # Itera por todos os inimigos
            enemy.speed += current_round // 2  # Aumenta a velocidade do inimigo
            enemy.health += int(10 + current_round * 2.5)  # Aumenta a saúde do inimigo progressivamente

    def pre_round_countdown(self, screen, font, player, current_round):
        """Faz a gestão da fase de exploração e da contagem decrescente antes de começar a ronda."""
        
        shed_exploration = True  # Define que o jogador está na fase de exploração do "shed"

        # Carregar a imagem de fundo com o tema de dinossauros
        background = pygame.image.load("images/dinosaur_background.png").convert()  # Carrega a imagem de fundo
        background = pygame.transform.scale(background, (width, height))  # Ajusta o tamanho ao ecrã

        # Renderizar e posicionar a primeira linha de texto
        shed_text1 = font.render("Explore the Shed!", True, white)  # Primeira mensagem
        shed_text_rect1 = shed_text1.get_rect(center=(width // 2, height // 2 - 70))  # Posição acima do centro

        # Renderizar e posicionar a segunda linha de texto (número da ronda)
        shed_text2 = font.render(f"Press Enter to Start Round {current_round}", current_round, True, white)
        shed_text_rect2 = shed_text2.get_rect(center=(width // 2, height // 2 - 40))  # Posição intermédia

        # Renderizar e posicionar a terceira linha de texto
        shed_text3 = font.render("or P to go to the Shed", True, white)  # Mensagem adicional
        shed_text_rect3 = shed_text3.get_rect(center=(width // 2, height // 2 - 10))  # Posição logo abaixo

        # Fase de exploração do "shed"
        while shed_exploration:
            screen.blit(background, (0, 0))  # Desenha o fundo no ecrã
            screen.blit(shed_text1, shed_text_rect1)  # Exibe a primeira linha de texto
            screen.blit(shed_text2, shed_text_rect2)  # Exibe a segunda linha de texto
            screen.blit(shed_text3, shed_text_rect3)  # Exibe a terceira linha de texto
            pygame.display.flip()  # Atualiza o ecrã para mostrar os elementos

            # Processar os eventos do jogador
            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # Se o jogador fechar o jogo
                    pygame.quit()
                    return  # Sai imediatamente do programa
                elif event.type == pygame.KEYDOWN:  # Se o jogador pressionar uma tecla
                    if event.key == pygame.K_RETURN:  # Inicia a ronda
                        shed_exploration = False  # Sai da fase de exploração
                    elif event.key == pygame.K_p:  # Entra no "shed"
                        shed(player)  # Executa a lógica do "shed"

        # Fase de contagem decrescente
        for i in range(3, 0, -1):  # Contagem de 3 a 1
            screen.blit(background, (0, 0))  # Desenha o fundo novamente
            overlay = pygame.Surface((width, height))  # Cria uma camada por cima do fundo
            overlay.set_alpha(180)  # Define a transparência da camada
            overlay.fill((0, 0, 0))  # Preenche a camada com preto
            screen.blit(overlay, (0, 0))  # Aplica a camada sobre o fundo

            # Renderizar o texto da contagem decrescente
            countdown_text = font.render(f"Starting Round in {i}...", True, white)  # Texto com o número atual
            countdown_rect = countdown_text.get_rect(center=(width // 2, height // 2))  # Centraliza o texto
            screen.blit(countdown_text, countdown_rect)  # Exibe o texto

            # Criar um efeito visual com círculos concêntricos
            center = (width // 2, height // 2)  # Centro do círculo
            base_radius = 100 + i * 20  # Define o raio inicial que aumenta com a contagem
            for alpha, radius in zip(range(50, 0, -10), range(base_radius, base_radius + 50, 10)):
                # Criar uma superfície transparente para cada círculo
                smooth_circle = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(
                    smooth_circle,
                    (34, 139, 34, alpha),  # Cor verde com transparência (RGBA)
                    (radius, radius),  # Posição central do círculo
                    radius  # Raio do círculo
                )
                # Desenha o círculo suavizado no ecrã
                screen.blit(smooth_circle, (center[0] - radius, center[1] - radius))

            pygame.display.flip()  # Atualiza o ecrã para mostrar as mudanças
            pygame.time.wait(1000)  # Espera 1 segundo antes de continuar
