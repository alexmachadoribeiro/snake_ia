import pygame
import time
import random

# Inicializa o Pygame
pygame.init()

# Define as cores (RGB)
white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

# Define as dimensões da tela
dis_width = 800
dis_height = 600

# Cria a tela do jogo
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption('Jogo da Cobrinha by Gemini')

# Define o relógio para controlar a velocidade do jogo
clock = pygame.time.Clock()

# Define o tamanho do bloco da cobra e a velocidade
snake_block = 20 # Tamanho de cada segmento da cobra e da maçã
snake_speed = 15 # Velocidade inicial da cobra

# Define a fonte para exibir mensagens
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def exibir_pontuacao(score):
    """Exibe a pontuação atual na tela."""
    value = score_font.render("Sua Pontuação: " + str(score), True, yellow)
    dis.blit(value, [0, 0])

def desenhar_cobra(snake_block, snake_list):
    """Desenha a cobra na tela."""
    # snake_list contém as coordenadas [x,y] de cada bloco da cobra
    for i, x_y in enumerate(snake_list):
        # Define a cor da cabeça diferente do corpo
        color = green
        if i == len(snake_list) - 1: # Último elemento é a cabeça
            color = (0, 150, 0) # Verde mais escuro para a cabeça
        pygame.draw.rect(dis, color, [x_y[0], x_y[1], snake_block, snake_block])
        pygame.draw.rect(dis, black, [x_y[0], x_y[1], snake_block, snake_block], 1) # Borda preta

def exibir_mensagem(msg, color, y_displace=0, font=font_style):
    """Exibe uma mensagem na tela."""
    mesg = font.render(msg, True, color)
    # Centraliza a mensagem
    text_rect = mesg.get_rect(center=(dis_width / 2, dis_height / 2 + y_displace))
    dis.blit(mesg, text_rect)

def gameLoop():
    """Função principal do jogo."""
    game_over = False
    game_close = False

    # Posição inicial da cobra (centro da tela)
    x1 = dis_width / 2
    y1 = dis_height / 2

    # Mudança inicial na posição (cobra parada)
    x1_change = 0
    y1_change = 0

    # Lista para armazenar os blocos da cobra
    snake_List = []
    Length_of_snake = 1 # Comprimento inicial da cobra

    # Gera a posição aleatória da primeira maçã
    # Garante que a maçã apareça em uma posição múltipla do snake_block
    foodx = round(random.randrange(0, dis_width - snake_block) / float(snake_block)) * snake_block
    foody = round(random.randrange(0, dis_height - snake_block) / float(snake_block)) * snake_block

    current_snake_speed = snake_speed

    while not game_over:

        while game_close == True:
            dis.fill(blue)
            exibir_mensagem("Você Perdeu! Pressione C para Jogar Novamente ou Q para Sair", red, -50)
            exibir_pontuacao(Length_of_snake - 1)
            pygame.display.update()

            # Verifica eventos na tela de game over
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q: # Tecla Q para sair
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_c: # Tecla C para jogar novamente
                        gameLoop() # Reinicia o jogo

        # Processamento de eventos (teclado, mouse, etc.)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Evento de fechar a janela
                game_over = True
            if event.type == pygame.KEYDOWN: # Evento de pressionar uma tecla
                if event.key == pygame.K_LEFT:
                    if x1_change == snake_block: # Evita que a cobra se mova para trás instantaneamente
                        continue
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    if x1_change == -snake_block:
                        continue
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    if y1_change == snake_block:
                        continue
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    if y1_change == -snake_block:
                        continue
                    y1_change = snake_block
                    x1_change = 0
                elif event.key == pygame.K_ESCAPE: # Tecla ESC para sair
                    game_over = True


        # Verifica se a cobra atingiu as bordas da tela
        if x1 >= dis_width or x1 < 0 or y1 >= dis_height or y1 < 0:
            game_close = True

        # Atualiza a posição da cabeça da cobra
        x1 += x1_change
        y1 += y1_change

        # Preenche o fundo da tela
        dis.fill(black) # Mudei para preto para melhor contraste

        # Desenha a maçã
        pygame.draw.rect(dis, red, [foodx, foody, snake_block, snake_block])
        pygame.draw.rect(dis, white, [foodx, foody, snake_block, snake_block],1) # Borda branca na maçã

        # Adiciona a nova posição da cabeça à lista da cobra
        snake_Head = []
        snake_Head.append(x1)
        snake_Head.append(y1)
        snake_List.append(snake_Head)

        # Mantém o tamanho da cobra
        if len(snake_List) > Length_of_snake:
            del snake_List[0] # Remove o bloco mais antigo (cauda)

        # Verifica se a cobra colidiu com ela mesma
        for x in snake_List[:-1]: # Verifica todos os blocos exceto a cabeça
            if x == snake_Head:
                game_close = True

        # Desenha a cobra
        desenhar_cobra(snake_block, snake_List)
        # Exibe a pontuação
        exibir_pontuacao(Length_of_snake - 1)

        # Atualiza a tela
        pygame.display.update()

        # Verifica se a cobra comeu a maçã
        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, dis_width - snake_block) / float(snake_block)) * snake_block
            foody = round(random.randrange(0, dis_height - snake_block) / float(snake_block)) * snake_block
            Length_of_snake += 1
            # Aumenta a velocidade um pouco a cada 5 maçãs comidas
            if (Length_of_snake -1) % 5 == 0:
                current_snake_speed +=1


        # Controla a velocidade do jogo
        clock.tick(current_snake_speed)

    # Finaliza o Pygame
    pygame.quit()
    quit() # Termina o script Python

# Inicia o loop do jogo
gameLoop()
