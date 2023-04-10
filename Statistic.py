from dataclasses import dataclass

from Deck import Card, Deck
import json


@dataclass
class PrimitiveStatistic:
    def __init__(self, tries=0, successes=0):
        self.tries = tries
        self.successes = successes

    def to_pair(self):
        return self.tries, self.successes


@dataclass
class CardStatistic:
    def __init__(self, card: Card):
        self.card = card
        self.stats = {}
        languages = sorted(list(card.words.keys()))
        for i in range(len(languages)):
            for j in range(len(languages)):
                if i != j:
                    pair = (languages[i], languages[j])
                    self.stats[pair] = PrimitiveStatistic()

    def try_guess(self, lang1, lang2, guessed_correctly):
        pair = (lang1, lang2)
        self.stats[pair].tries += 1
        if guessed_correctly:
            self.stats[pair].successes += 1

    @staticmethod
    def from_string(string):
        lines = string.strip().split(';')
        card = Card.from_string(lines[0])
        stats = {}
        for line in lines[1:]:
            lang1, lang2, total, correct = line.split(',')
            stats[(lang1, lang2)] = PrimitiveStatistic(int(total), int(correct))
        stat_card = CardStatistic(card)
        stat_card.stats = stats
        return stat_card

    def to_string(self):
        lines = []
        for pair in self.stats:
            lang1, lang2 = pair
            total, correct = self.stats[pair].to_pair()
            lines.append(f"{lang1},{lang2},{total},{correct}")
        return f"{str(self.card)};" + ";".join(lines)


class Statistic:
    def __init__(self):
        self.stat_cards = []

    def save_to_file(self, file_path):
        data = []
        for stat_card in self.stat_cards:
            data.append(stat_card.to_string())

        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def load_from_deck(deck: Deck):
        stat = Statistic()
        stat.stat_cards = list(map(lambda x: CardStatistic(x), deck.cards))
        return stat

    @staticmethod
    def load_from_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        stats = Statistic()

        for card_data in data:
            stats.stat_cards.append(CardStatistic.from_string(card_data))

        return stats

    def update(self, other):
        for stat_card in other.stat_cards:
            index = self.get_card_index(stat_card.card)

            if index == -1:
                self.stat_cards.append(stat_card)
            else:
                for key in stat_card.stats.keys():
                    self.stat_cards[index].stats[key].tries += stat_card.stats[key].tries
                    self.stat_cards[index].stats[key].successes += stat_card.stats[key].successes

    def load_difficult_cards(self, lang1, lang2, threshold):
        deck = Deck()
        for scard in self.stat_cards:
            stats = scard.stats[(lang1, lang2)]
            if stats is not None and stats.tries / stats.successes >= threshold:
                deck.cards.append(scard.card)

        return deck

    def update_card(self, card, lang1, lang2, success):
        index = self.get_card_index(card)
        if index != -1:
            self.stat_cards[index].try_guess(lang1, lang2, success)

    def get_card_index(self, card):
        for i, stat_card in enumerate(self.stat_cards):
            if stat_card.card == card:
                return i
        return -1


if __name__ == '__main__':
    card1 = Card(en="Cat", ru="Кот")
    card2 = Card(en="Dog", ru="Собака")
    #
    statistic = Statistic()
    statistic.stat_cards = [CardStatistic(card1), CardStatistic(card2)]

    statistic.update_card(card1, "en", "ru", True)

    statistic2 = Statistic()
    statistic2.stat_cards = [CardStatistic(card1)]
    statistic2.stat_cards.append(CardStatistic(Card(en="Ball", ru="Шар")))

    statistic2.stat_cards[0].try_guess("ru", "en", False)

    statistic.update(statistic2)

    #
    # statistic.save_to_file("stat.txt")
    # statistic = Statistic.load_from_file("stat.txt")
    print(*map(lambda x: x.to_string(), statistic.stat_cards))
