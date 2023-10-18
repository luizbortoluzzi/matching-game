import xmlrpc.client
import tkinter as tk

server = xmlrpc.client.ServerProxy("http://localhost:8000/")
card_states = [False] * 16

def register_player():
    player_name = player_name_entry.get()
    if server.register_player(player_name):
        register_button.config(state='disabled')
        player_name_entry.config(state='disabled')
    else:
        print("Não foi possível registrar o jogador.")

def check_game_state():
    game_state = server.get_state()
    if len(game_state['matched_pairs']) == 8:  # Todos os pares foram encontrados
        winner = max(game_state['players'], key=game_state['players'].get)
        print(f"Jogo terminado! O vencedor é {winner} com {game_state['players'][winner]} pares encontrados.")
        root.quit()

def update_ui():
    game_state = server.get_state()  # Obtém as cartas que foram recentemente reveladas
    last_two_cards = game_state['last_two_cards']

    for card_index, card_value in last_two_cards:
        cards[card_index].config(text=str(card_value))
    
    if last_two_cards and len(last_two_cards) == 2:
        (index1, value1), (index2, value2) = last_two_cards
        cards[index1].config(text=str(value1))
        cards[index2].config(text=str(value2))

        # Se os valores das duas últimas cartas não são iguais, esconde-as após um pequeno intervalo
        if value1 != value2:
            root.after(1000, hide_last_two_cards, last_two_cards)

    root.after(100, update_ui)

def reveal_card(card_index, card_value):
    card_states[card_index] = True
    cards[card_index].config(text=str(card_value))

def play_card(card_index):
    if not card_states[card_index]:
        player_name = player_name_entry.get()
        card_value, last_two_cards, hide_cards = server.play_card(player_name, card_index)  # Obtendo hide_cards
        if card_value is not None:
            reveal_card(card_index, card_value)
            if hide_cards:  # Se hide_cards for True, esconda as duas últimas cartas após um breve intervalo
                root.after(1000, hide_last_two_cards, last_two_cards)

def hide_last_two_cards(last_two_cards):
    for card_index, _ in last_two_cards:
        cards[card_index].config(text=" ")  # Escondendo a carta
        card_states[card_index] = False  # Verificar o estado do jogo após um intervalo

def update_game_state():
    game_state = server.get_state()

    # Verifica se o jogo já começou
    if game_state['current_player']:
        # Mantém os pares revelados e desabilita os botões
        for pair_index in game_state['matched_pairs']:
            cards[pair_index].config(text=str(game_state['cards'][pair_index]), state=tk.DISABLED)
            card_states[pair_index] = True  # Marca o estado da carta como revelado

    root.after(1000, update_game_state)

def hide_card(card_index):
    if card_index not in server.get_state()['matched_pairs']:
        cards[card_index].config(text=" ")

def create_gui():
    global player_name_entry, register_button, cards
    cards = []

    for i in range(16):
        card_button = tk.Button(root, text=" ", width=8, height=4,
                                command=lambda i=i: play_card(i))
        card_button.grid(row=i // 4, column=i % 4)
        cards.append(card_button)

    player_name_label = tk.Label(root, text="Nome do Jogador")
    player_name_label.grid(row=4, columnspan=4)

    player_name_entry = tk.Entry(root)
    player_name_entry.grid(row=5, columnspan=4)

    register_button = tk.Button(root, text="Registrar", command=register_player)
    register_button.grid(row=6, columnspan=4)
    update_game_state()
    update_ui()

root = tk.Tk()
root.title("Jogo da Memória")
create_gui()
root.mainloop()
