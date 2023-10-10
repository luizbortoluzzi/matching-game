from xmlrpc.server import SimpleXMLRPCServer
import random
import threading

class MemoryGameServer:
    def __init__(self):
        self.cards = list(range(1, 9)) * 2
        random.shuffle(self.cards)
        self.players = {}
        self.matched_pairs = []
        self.current_player = None
        self.player_list = []  # Lista de jogadores registrados
        self.last_two_cards = []  # Armazena os índices das duas últimas cartas selecionadas

    def register_player(self, player_name):
        if len(self.players) < 2:
            self.players[player_name] = 0
            self.player_list.append(player_name)

            if len(self.player_list) == 2:
                # Inicialize as cartas e defina o primeiro jogador quando ambos os jogadores estiverem registrados
                self.cards = list(range(1, 9)) * 2
                random.shuffle(self.cards)
                self.current_player = self.player_list[0]
            return True
        return False

    def get_current_player(self):
        return self.current_player

    # def play_card(self, player_name, card_index):
    #     if player_name == self.current_player and card_index not in [index for index, _ in self.last_two_cards]:
    #         card_value = self.cards[card_index]

    #         self.last_two_cards.append((card_index, card_value))

    #         if len(self.last_two_cards) == 2:
    #             index1, value1 = self.last_two_cards[0]
    #             index2, value2 = self.last_two_cards[1]

    #             if value1 == value2:
    #                 self.players[player_name] += 1
    #                 self.matched_pairs.extend([value1, value2])

    #             # Limpando a lista das duas últimas cartas reveladas
    #             self.last_two_cards.clear()

    #             # Alternando o jogador
    #             current_index = self.player_list.index(self.current_player)
    #             next_index = (current_index + 1) % len(self.player_list)
    #             self.current_player = self.player_list[next_index]

    #         return card_value
    #     return None

    def play_card(self, player_name, card_index):
        if player_name == self.current_player and card_index not in [index for index, _ in self.last_two_cards]:
            card_value = self.cards[card_index]
            self.last_two_cards.append((card_index, card_value))

            hide_cards = False  # Inicializando a flag

            if len(self.last_two_cards) == 2:
                index1, value1 = self.last_two_cards[0]
                index2, value2 = self.last_two_cards[1]

                if value1 == value2:
                    self.players[player_name] += 1
                    self.matched_pairs.extend([index1, index2])
                else:
                    hide_cards = True  # Definindo a flag como True se as cartas não formarem um par

                    # Alternando o jogador (só alternar se as cartas não formarem um par)
                    current_index = self.player_list.index(self.current_player)
                    next_index = (current_index + 1) % len(self.player_list)
                    self.current_player = self.player_list[next_index]

                # Limpando a lista das duas últimas cartas reveladas após um intervalo, permitindo que os jogadores as vejam
                timer = threading.Timer(1.0, self.clear_last_two_cards)  # Cria um timer de 1 segundo
                timer.start()  # Inicia o timer

            return card_value, self.last_two_cards, hide_cards  # Retornando a flag junto com os outros valores
        return None, None, None

    def clear_last_two_cards(self):
        self.last_two_cards.clear()

    def get_state(self):
        return {
            'cards': self.cards,
            'players': self.players,
            'matched_pairs': self.matched_pairs,
            'current_player': self.current_player
        }

def main():
    server = SimpleXMLRPCServer(('localhost', 8000), allow_none=True)
    game_server = MemoryGameServer()
    server.register_instance(game_server)
    print("O servidor do jogo da memória está rodando na porta 8000...")
    server.serve_forever()

if __name__ == "__main__":
    main()
