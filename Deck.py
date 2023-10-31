import csv
import random
import json
from dataclasses import dataclass

from tabulate import tabulate


class Deck:
    def __init__(self):
        self.cards = []

    def add_card(self, card):
        self.cards.append(card)

    def remove_card(self, card):
        self.cards.remove(card)

    def shuffle(self):
        random.shuffle(self.cards)

    def get_card(self, index):
        return self.cards[index]

    def size(self):
        return len(self.cards)

    def to_csv(self, filename):
        # Get all the unique language codes in the deck
        language_codes = set()
        for card in self.cards:
            for language_code in card.words.keys():
                language_codes.add(language_code)

        # Create a dictionary mapping language codes to column indices
        language_indices = {}
        for i, language_code in enumerate(sorted(language_codes)):
            language_indices[language_code] = i

        # Write the deck to a CSV file
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile, delimiter=";")
            # Write the header row with the language codes
            header_row = [''] * len(language_indices)
            for language_code, index in language_indices.items():
                header_row[index] = language_code
            writer.writerow(header_row)
            # Write the data rows with the card words
            for card in self.cards:
                data_row = [''] * len(language_indices)
                for language_code, word in card.words.items():
                    index = language_indices[language_code]
                    data_row[index] = word
                writer.writerow(data_row)

    def from_csv(self, filename, languages):
        self.cards = []
        with open(filename, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile, delimiter=";")
            header_row = next(reader)
            language_indices = {}
            for i, language_code in enumerate(header_row):
                language_indices[language_code] = i
            for row in reader:
                if not row:
                    continue
                if row[0].lstrip().startswith('#'):
                    continue  # Skip this iteration if row starts with '#' after removing leading whitespace
                words = {}
                for language_code, index in language_indices.items():
                    if index < len(row) and language_code in languages:
                        words[language_code] = row[index]

                if all(isinstance(val, str) and val != '' for val in words.values()):
                    self.cards.append(Card(**words))

    def copy(self):
        new_deck = Deck()
        new_deck.cards = self.cards.copy()
        return new_deck

    def __str__(self):
        table = []
        headers = self.get_keys()
        for card in self.cards:
            row = [card.words.get(h, '') for h in headers]
            table.append(row)
        str = tabulate(table, headers, showindex=True)
        print(str)
        return str

    def get_keys(self):
        language_codes = set()
        for card in self.cards:
            for language_code in card.words.keys():
                language_codes.add(language_code)
        return list(language_codes)


@dataclass
class Card:
    def __init__(self, **kwargs):
        self.words = kwargs

    def __getitem__(self, key):
        return self.words[key]

    def __setitem__(self, key, value):
        self.words[key] = value

    def __str__(self):
        return json.dumps(self.words)

    def __eq__(self, other):
        return self.words == other.words

    @staticmethod
    def from_string(string):
        return Card(**json.loads(string))


if __name__ == '__main__':
    print(str(Card.from_string('{"en":"AAA"}')))
