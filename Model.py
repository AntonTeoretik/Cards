import Deck
from Deck import *
from Statistic import Statistic


class GameState:
    def __init__(self, deck: Deck):
        self.current_round = 0
        self.remaining_words = len(deck.cards)


class Model:
    def __init__(self):
        self.cycle_ended = True

        self.unknown_lan = None
        self.known_lan = None
        self.game_started = False

        self.deck = None
        self.remaining_cards = None
        self.guessed_cards = None
        self.unguessed_cards = None

        self.local_statistic = None

        self.game_state = None

        self.active_card = None
        self.last_card_guessed = None

    def load_deck(self, filename):
        self.deck = Deck()
        self.deck.from_csv(filename, [self.known_lan, self.unknown_lan])
        self.unguessed_cards = self.deck.copy()

    def set_mode(self, known_lang, unknown_lang):
        self.known_lan = known_lang
        self.unknown_lan = unknown_lang
        print("Languages set: " + known_lang + " " + unknown_lang)

    def able_to_start(self) -> bool:
        return self.deck is not None

    def prepare_game(self):
        self.game_state = GameState(self.deck)
        self.local_statistic = Statistic.load_from_deck(self.deck)
        self.remaining_cards = self.deck.copy()
        self.guessed_cards = Deck()
        self.unguessed_cards = Deck()

    def start_game(self):
        if self.able_to_start():
            self.prepare_game()
            self.game_started = True

    def take_card(self):
        if self.deck_is_not_empty():
            self.active_card = self.remaining_cards.cards.pop()
            self.game_state.remaining_cards -= 1

    def return_card_back(self):
        self.game_state.remaining_cards += 1
        self.remaining_cards.cards.append(self.active_card)
        self.active_card = None

    def guess_card(self, card_guessed):
        self.last_card_guessed = card_guessed
        self.end_cycle_check()

    def end_round(self):
        self.distribute_card()
        self.local_statistic.update_card(self.active_card, self.known_lan, self.unknown_lan, self.last_card_guessed)
        self.active_card = None
        self.last_card_guessed = None

        if self.cycle_ended:
            print("End of cycle")
            self.end_cycle()

    def start_cycle(self):
        print("START CYCLE")
        self.cycle_ended = False
        self.remaining_cards.shuffle()
        self.game_state.current_round += 1
        self.game_state.remaining_cards = len(self.deck.cards)

    def end_cycle_check(self):
        if not self.deck_is_not_empty():
            self.cycle_ended = True
        if self.cycle_ended and len(self.unguessed_cards.cards) == 0:
            self.game_started = False

    def finish_game(self):
        self.remaining_cards = None
        self.unguessed_cards = None
        self.guessed_cards = None
        print("End game")

    def end_cycle(self):
        if not self.cycle_ended:
            raise Exception("Invalid state")

        if not self.game_started:
            self.finish_game()
            return

        self.remaining_cards = self.unguessed_cards
        self.unguessed_cards = Deck()
        self.guessed_cards = Deck()

    def distribute_card(self):
        if self.active_card is None:
            return

        if self.last_card_guessed is True:
            self.guessed_cards.cards.append(self.active_card)
        elif self.last_card_guessed is False:
            self.unguessed_cards.cards.append(self.active_card)

    def deck_is_not_empty(self):
        return len(self.remaining_cards.cards) != 0
