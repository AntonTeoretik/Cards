import tkinter as tk
from tkinter import filedialog, Toplevel
import os

import Model
import View

FROM_UNKNOWN_TO_KNOWN_MODE = "from"
FROM_KNOWN_TO_UNKNOWN_MODE = "to"

RUSSIAN = "ru"
ENGLISH = "en"
DEUTSCH = "de"


class Application:
    cards_window: Toplevel or None

    def __init__(self, known_lang=None, unknown_lang=None):
        # window creation
        root = self.create_window()
        self.cards_window = None
        self.model = Model.Model()

        self.root = root

        self.choose_language_view = View.ChooseLanguageView(root, self.choose_language)
        self.load_deck_view = View.LoadDeckView(self.root, self.browse_file, self.start_game)
        self.game_view = View.CardsView(None)

        self.known_lang = known_lang
        self.unknown_lang = unknown_lang

        if known_lang and unknown_lang:
            self.load_deck_view.update_languages(known_lang, unknown_lang)
            self.load_deck_view.pack()
        else:
            self.known_lang = RUSSIAN
            self.choose_language_view.pack()

        self.root = root
        self.start_app()

    def choose_language(self, lang):
        self.unknown_lang = lang
        self.choose_language_view.destroy()
        self.model.set_mode(known_lang=self.known_lang, unknown_lang=self.unknown_lang)
        self.load_deck_view.update_languages(self.known_lang, self.unknown_lang)
        self.load_deck_view.pack()

    # Create a function for browsing for a file
    def browse_file(self, event=None):
        filename = filedialog.askopenfilename(
            initialdir=os.path.abspath(__file__),
            title="Choose a CSV file",
            filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
        )
        if filename:
            self.load_deck(filename)
            self.update_text()
            self.activate_next_buttons()

    def load_deck(self, filename):
        # Load the deck from the CSV file
        self.model.load_deck(filename)

    def activate_next_buttons(self):
        self.load_deck_view.next_button_to.configure(state="normal")
        self.load_deck_view.next_button_from.configure(state="normal")

    def update_text(self):
        self.load_deck_view.deck_text.configure(state="normal")

        s = self.model.deck.__str__()
        self.load_deck_view.deck_text.delete(1.0, tk.END)
        self.load_deck_view.deck_text.insert(tk.END, s)

        # Set the text widget to read-only mode
        self.load_deck_view.deck_text.configure(state="disabled")

    def start_game(self, mode):
        if mode == FROM_KNOWN_TO_UNKNOWN_MODE:
            self.model.set_mode(self.known_lang, self.unknown_lang)
        elif mode == FROM_UNKNOWN_TO_KNOWN_MODE:
            self.model.set_mode(self.unknown_lang, self.known_lang)

        if not self.model.able_to_start():
            return

        self.load_deck_view.continue_button.configure(state="normal", command=self.continue_game)
        self.model.start_game()

        self._set_game_window()
        self.start_cycle()
        self.cards_window.wait_window()

    def continue_game(self):
        if self.model.game_started:
            self._set_game_window()
            self.prepare_for_next_round()

    def update_game_view_statistic(self):
        self.game_view.cycle_number_label.configure(text="Cycle " + str(self.model.game_state.current_round))

        if self.model.game_started:
            self.game_view.remaining_cards_number.configure(text=str(len(self.model.remaining_cards.cards)))
            self.game_view.guessed_cards_number.configure(text=str(len(self.model.guessed_cards.cards)))
            self.game_view.left_cards_number.configure(text=str(len(self.model.unguessed_cards.cards)))
        else:
            self.game_view.remaining_cards_number.configure(text="")
            self.game_view.guessed_cards_number.configure(text="")
            self.game_view.left_cards_number.configure(text="")

    def clear_card_labels(self):
        self.game_view.card_known.configure(text="")
        self.game_view.card_unknown.configure(text="")
        self.game_view.card_known.reset_font_size()
        self.game_view.card_unknown.reset_font_size()
        self.cards_window.update()

    def start_cycle(self):
        print("Start cycle")

        self.model.start_cycle()
        self.update_game_view_statistic()
        self.game_view.pick_button.configure(text="Pick!", command=self.take_card)
        self.cards_window.bind('<Return>', lambda x: self.take_card())

    def finish_the_game(self):
        self.load_deck_view.continue_button.configure(state="disabled", command=self.continue_game)
        self.cards_window.destroy()

    def take_card(self):
        print("Take card")
        self.model.take_card()
        self.update_game_view_statistic()

        self.game_view.card_known.configure(text=self.model.active_card[self.model.known_lan])

        self.game_view.card_known.adjust_font_size()

        self.game_view.pick_button.configure(text="Show translation", command=self.show_translation)
        self.cards_window.bind('<Return>', lambda x: self.show_translation())

    def show_translation(self):
        self.game_view.card_unknown.configure(text=self.model.active_card[self.model.unknown_lan])
        self.game_view.no_button.configure(state="normal", command=self.card_unguessed)
        self.game_view.got_it.configure(state="normal", command=self.card_guessed)
        self.cards_window.bind('<Return>', lambda x: self.card_guessed())
        self.cards_window.bind("'", lambda x: self.card_unguessed())
        self.game_view.pick_button.configure(text="Pick!", state="disabled")

        self.game_view.card_unknown.adjust_font_size()

    def card_unguessed(self):
        print("No :-(")
        self.model.distribute_card(False)
        self.prepare_for_next_round()

    def card_guessed(self):
        print("Yeees!")
        self.model.distribute_card(True)
        self.prepare_for_next_round()

    def prepare_for_next_round(self):
        print("Prepare for next round")

        self.cards_window.unbind("'")

        self.clear_card_labels()
        self.update_game_view_statistic()
        self.game_view.no_button.configure(state="disabled")
        self.game_view.got_it.configure(state="disabled")
        self.game_view.pick_button.configure(state="normal", command=self.take_card)

        self.cards_window.bind('<Return>', lambda x: self.take_card())
        if self.model.game_started and self.model.cycle_ended:
            self.cards_window.bind('<Return>', lambda x: self.start_cycle())
            self.game_view.pick_button.configure(text="Start next cycle", command=self.start_cycle)

        elif not self.model.game_started:
            self.cards_window.bind('<Return>', lambda x: self.finish_the_game())
            self.game_view.pick_button.configure(text="Finish the game", command=self.finish_the_game)

    @staticmethod
    def create_window():
        root = tk.Tk()

        # Set the window size to 800x600
        width = 800
        height = 600

        # Get the screen width and height
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()

        # Calculate the x and y coordinates to center the window on the screen
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        # Set the window size and position
        root.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        root.title("German Word Learning Game")

        return root

    def start_app(self):
        self.root.mainloop()

    def _set_game_window(self):
        cards_window = tk.Toplevel(self.root)

        # Set the window size to 800x600
        width = 700
        height = 400

        # Get the screen width and height
        screen_width = cards_window.winfo_screenwidth()
        screen_height = cards_window.winfo_screenheight()

        # Calculate the x and y coordinates to center the window on the screen
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        cards_window.title("Cards")
        cards_window.grab_set()

        cards_window.geometry('{}x{}+{}+{}'.format(width, height, x, y))

        self.game_view = View.CardsView(cards_window)
        self.game_view.pack()
        self.cards_window = cards_window
        self.cards_window.focus_set()