import os
import random
from getch import getch # Biblioteca auxiliar multiplataforma para retornar um caractere imediatamente após pressionar

# Para imprimir comandos do teclado que foram pressionados (desenha no meio da tela)
DEBUG = False

# Combinações vencedoras em binário para comparação bitwise
win_combos = [
    448,  # 0b 111000000
    56,   # 0b 000111000
    7,    # 0b 000000111
    292,  # 0b 100100100
    146,  # 0b 010010010
    73,   # 0b 001001001
    273,  # 0b 100010001
    84    # 0b 001010100
]

# Funções ANSI Escape para cursor de texto
# Move cursor para determinada linha e coluna
def move_cursor(line, column):
    print(f"\x1B[{line};{column}H", end='')

# Move o cursor determinados passos à direita
def move_right(number):
    print(f"\x1B[{number}C", end='')

# "Apaga" o exato lugar que o cursor está preenchendo com um caractere de espaço
def erase_cursor():
    print(' ', end='')

# Apaga linha
def erase_line():
    print("        ", end='')
    print("\x1B[K")

# Desenha o ícone colorido de um dos jogadores
def draw_play(line, column, player):
    move_cursor(line, column)
    if (player == 'X'):
        print(f"\x1b[34mX\x1b[0m")
    else:
        print(f"\x1b[31mO\x1b[0m")
    move_cursor(20,0)

# Apaga o cursor de seleção do jogador e desenha outro
def erase_and_draw_cursor(current_cursor_position, line, column):
    move_cursor(current_cursor_position[0],current_cursor_position[1])
    erase_cursor()
    move_right(1)
    erase_cursor()
    move_cursor(line, column)
    print('[', end = '')
    move_right(1)
    print(']')
    move_cursor(20,0)
    return [line, column]

# Limpa a tela completamente, inclusive o texto do diretório
def clear_screen():
    print("\x1B[2J", end='')

# Esconde o ícone do cursor
def hide_cursor():
    print("\x1B[?25l", end='')

def show_cursor():
    print("\x1B[?25h", end='')

# Função main
def main():
    # limpa a tela pelo sistema operacional antes de tudo
    os.system('cls||clear')

    # Cria o tabuleiro, jogadas possíveis e localização do cursor do jogador
    board = [0] * 9
    possible_plays = [0,1,2,3,4,5,6,7,8]
    cursor_index = 0

    # Flags auxiliares para lógica de jogo
    x_played = False
    o_played = False
    game_end = False
    winner = False

    # Player será 1 (X) ou -1 (O), dependendo do estado do jogo
    player = 0

    # Estado do jogo atual
    actual_state = 0

    # Esconde o cursor e limpa a tela
    hide_cursor()
    clear_screen()

    # Move o cursor para o início e desenha tabuleiro e background do jogo
    move_cursor(0, 0)
    print("Jogo da Velha no terminal\n\n")
    print("\
     #     #\n\
     #     #\n\
     #     #\n\
#################\n\
     #     #\n\
     #     #\n\
     #     #\n\
#################\n\
     #     #\n\
     #     #\n\
     #     #\n")

    print("\nPressione as SETAS para mover e ENTER para realizar uma jogada com o X\nPressione Q para sair")

    # Imprime as informações de estado ao lado
    move_cursor(8,25)
    print("Estado Atual:")

    move_cursor(8,39)
    print("TEM JOGO              ")

    cursor_position = [5,2]

    # Desenha o cursor na posição de índice zero (canto superior esquerdo do tabuleiro)
    move_cursor(cursor_position[0], cursor_position[1])
    print('[', end = '')
    move_right(1)
    print(']')

    # Variável de tecla pressionada
    key = ''

    # Loop de lógica do jogo. Q quebra o loop e sai do jogo.
    while(key != 'q'):
        key = getch() # Chama função getch para receber qualquer tecla pressionada

        # Se é a vez do O (bot), seleciona aleatoriamente um espaço para jogar
        if (x_played and not o_played):
            bot_choice = random.choice(possible_plays)
            possible_plays.remove(bot_choice)
            board[bot_choice] = -1
            match bot_choice:
                case 0:
                    draw_play(5, 3, 'O')
                case 1:
                    draw_play(5, 9, 'O')
                case 2:
                    draw_play(5, 15, 'O')
                case 3:
                    draw_play(9, 3, 'O')
                case 4:
                    draw_play(9, 9, 'O')
                case 5:
                    draw_play(9, 15, 'O')
                case 6:
                    draw_play(13, 3, 'O')
                case 7:
                    draw_play(13, 9, 'O')
                case 8:
                    draw_play(13, 15, 'O')
            player = -1
            o_played = True

        # Se é a vez do X (jogador), verifica se a tecla pressionada é válida
        if (not x_played):
            if (key == "\r"): # Tecla Enter
                if DEBUG:
                    print("Pressed Enter")
                if (cursor_index in possible_plays): # Verifica se é possível preencher o espaço
                    possible_plays.remove(cursor_index)
                    board[cursor_index] = 1

                    # Caso esteja livre, desenha na tela
                    match cursor_index:
                        case 0:
                            draw_play(5, 3, 'X')
                        case 1:
                            draw_play(5, 9, 'X')
                        case 2:
                            draw_play(5, 15, 'X')
                        case 3:
                            draw_play(9, 3, 'X')
                        case 4:
                            draw_play(9, 9, 'X')
                        case 5:
                            draw_play(9, 15, 'X')
                        case 6:
                            draw_play(13, 3, 'X')
                        case 7:
                            draw_play(13, 9, 'X')
                        case 8:
                            draw_play(13, 15, 'X')
                    
                    # Identifica quem jogou e liga o flag que X jogou
                    player = 1
                    x_played = True

            # Se é Windows, a decodificação necessita ser na biblioteca getch,
            # então só avalia o final do ANSI code das setas (H,P,M,K)
            if (os.name == 'nt'):
                match key:
                    case 'H': # Seta de cima
                        cursor_index -= 3 # Desce 3 no tabuleiro
                        if DEBUG:
                            print("Pressed UP")
                        if (cursor_index < 0): # Caso passe, ajusta
                            cursor_index += 9
                    case 'P': # Seta de baixo
                        cursor_index += 3
                        if DEBUG:
                            print("Pressed DOWN")
                        if (cursor_index > 8):
                            cursor_index -= 9
                    case 'M': # Seta da direita
                        cursor_index += 1
                        if DEBUG:
                            print("Pressed RIGHT")
                        if (cursor_index > 8):
                            cursor_index = 0
                    case 'K':  # Seta da esquerda
                        cursor_index -= 1
                        if DEBUG:
                            print("Pressed LEFT")
                        if (cursor_index < 0):
                            cursor_index = 8

            # Se é POSIX, procura pelo ANSI que começa com ESC, que pode ser uma das setas
            elif (key == "\x1B"):
                getch() # Descarta [ que vem do código ANSI
                key = getch() # Recebe o resto

                match key:
                    case 'A': # Seta de cima
                        cursor_index -= 3 # Desce 3 no tabuleiro
                        if DEBUG:
                            print("Pressed UP")
                        if (cursor_index < 0): # Caso passe, ajusta
                            cursor_index += 9
                    case 'B': # Seta de baixo
                        cursor_index += 3
                        if DEBUG:
                            print("Pressed DOWN")
                        if (cursor_index > 8):
                            cursor_index -= 9
                    case 'C': # Seta da direita
                        cursor_index += 1
                        if DEBUG:
                            print("Pressed RIGHT")
                        if (cursor_index > 8):
                            cursor_index = 0
                    case 'D':  # Seta da esquerda
                        cursor_index -= 1
                        if DEBUG:
                            print("Pressed LEFT")
                        if (cursor_index < 0):
                            cursor_index = 8

                if DEBUG:
                    print(f"Cursor index: {cursor_index}")
            
            # Ajusta a posição do cursor de seleção para cada movimento
            match cursor_index:
                case 0:
                    cursor_position = erase_and_draw_cursor(cursor_position, 5, 2)
                case 1:
                    cursor_position = erase_and_draw_cursor(cursor_position, 5, 8)
                case 2:
                    cursor_position = erase_and_draw_cursor(cursor_position, 5, 14)
                case 3:
                    cursor_position = erase_and_draw_cursor(cursor_position, 9, 2)
                case 4:
                    cursor_position = erase_and_draw_cursor(cursor_position, 9, 8)
                case 5:
                    cursor_position = erase_and_draw_cursor(cursor_position, 9, 14)
                case 6:
                    cursor_position = erase_and_draw_cursor(cursor_position, 13, 2)
                case 7:
                    cursor_position = erase_and_draw_cursor(cursor_position, 13, 8)
                case 8:
                    cursor_position = erase_and_draw_cursor(cursor_position, 13, 14)
        
        # Move cursor para baixo e apaga a linha para evitar caracteres indesejados em cima do tabuleiro
        move_cursor(20,0)
        erase_line()

        # Estado atual por lógica de jogo também
        move_cursor(8,39)

        # Verifica se alguém venceu
        plays = abs(sum(map(lambda x: x[1] << x[0] if (x[1] == player) else 0, enumerate(board))))
        # Faz a comparação com as combinações vencedoras possíveis
        for win_combo in win_combos:
            if (plays & win_combo ^ win_combo == 0):
                if (player == -1):
                    print("O VENCE               ")
                    actual_state = 3
                else:
                    print("X VENCE               ")
                    actual_state = 4
                game_end = True
                winner = True

        # Se o tabuleiro está todo preenchido e não existem vencedores, é empate
        if (len(possible_plays) <= 0 and not winner):
            print("EMPATE                ")
            actual_state = 2
            game_end = True
        
        # Se não houve vencedores ou empate, Procura uma próxima jogada que pode ser vencedora
        if (not game_end and not winner):
            possible_win = False
            for play in possible_plays:
                possible_next_board = board.copy()

                # Como o O não joga por último, não pode vencer
                if (len(possible_plays) > 1):
                    # Teste de uma possível vitória de O
                    possible_next_board[play] = -1
                    plays = abs(sum(map(lambda x: x[1] << x[0] if (x[1] == -1) else 0, enumerate(possible_next_board))))            
                    for win_combo in win_combos:
                        if (plays & win_combo ^ win_combo == 0):
                            possible_win = True

                # Teste de uma possível vitória de X
                possible_next_board[play] = 1
                plays = abs(sum(map(lambda x: x[1] << x[0] if (x[1] == 1) else 0, enumerate(possible_next_board))))
                for win_combo in win_combos:
                    if (plays & win_combo ^ win_combo == 0):
                        possible_win = True

            if (possible_win):
                print("POSSIBILIDADE FIM JOGO")
                actual_state = 1
            # Caso não possa haver vencedores neste momento, é, ou voltar a ser, a classe Tem Jogo
            else:
                print("TEM JOGO              ")
                actual_state = 0

        # Se os dois jogaram, reseta
        if (x_played and o_played):
            x_played = False
            o_played = False
        
        # Mais uma vez, move cursor para baixo e apaga a linha para evitar caracteres indesejados em cima do tabuleiro
        move_cursor(20,0)
        erase_line()
        
        # Quebra o loop se o jogo terminou
        if (game_end):
            # Remove o cursor de seleção
            move_cursor(cursor_position[0],cursor_position[1])
            erase_cursor()
            move_right(1)
            erase_cursor()
            move_cursor(20,0)
            break
    
    # Possivelmente desnecessário, mas deixa de esconder o cursor
    show_cursor()

# Se está chamando deste arquivo, é o main, então executa função main
if __name__ == "__main__":
    main()
