import Application
from Widgets import *


class View:
    def __init__(self, root):
        self.root = root
        self.frame = tk.Frame(root)
        self.frame.configure(bg=DesignSettings.BG_COLOR)

    def pack(self):
        self.frame.pack(fill="both", expand=True)

    def destroy(self):
        self.frame.destroy()


class ChooseLanguageView(View):
    def __init__(self, root, select_language_callback):
        super().__init__(root)

        self.welcome_label = Label(self.frame, "Welcome to the Word Learning Game!")
        self.welcome_label = tk.Label(self.frame,
                                      text="Welcome to the Word Learning Game!",
                                      bg=DesignSettings.BG_COLOR,
                                      fg=DesignSettings.FG_COLOR,
                                      font=DesignSettings.FONT)

        self.welcome_label.pack(side="top", pady=20, padx=10)

        self.eng_ru_button = Button(self.frame, "English", lambda: select_language_callback(Application.ENGLISH))
        self.eng_ru_button.pack(side="top", pady=5)

        self.de_ru_button = Button(self.frame, "German", lambda: select_language_callback(Application.DEUTSCH))
        self.de_ru_button.pack(side="top", pady=5)


class LoadDeckView(View):
    def __init__(self, root, select_file_callback, start_callback, known_lang="russian", unknown_lang="english"):
        super().__init__(root)

        # Add welcome message
        self.welcome_label = Label(self.frame, "Welcome to the Word Learning Game!")

        self.welcome_label.pack(side="top", pady=20, padx=10)

        # Add select file button
        self.select_file_button = Button(self.frame, "Select File", select_file_callback)
        self.select_file_button.pack(side="top", pady=5)

        # Add label for displaying deck content
        self.deck_text = DeckText(self.frame, height=0)
        self.deck_text.pack(pady=10, padx=10, fill='both', expand=True)

        # Add next button
        self.next_button_from = Button(self.frame, "Start from " + known_lang + " to " + unknown_lang,
                                       lambda: start_callback(Application.FROM_KNOWN_TO_UNKNOWN_MODE),
                                       state="disabled",
                                       width=40)
        self.next_button_from.pack(side="top", pady=10)

        self.next_button_to = Button(self.frame, "Start from " + unknown_lang + " to " + known_lang,
                                     lambda: start_callback(Application.FROM_UNKNOWN_TO_KNOWN_MODE),
                                     state="disabled",
                                     width=40)
        self.next_button_to.pack(side="top", pady=0)

        self.continue_button = Button(self.frame, "Continue",
                                      state="disabled",
                                      command="None",
                                      width=40)
        self.continue_button.pack(side="top", pady=10)

    def enable_next_buttons(self):
        self.next_button_to.config(state="normal")
        self.next_button_from.config(state="normal")

    def update_languages(self, known, unknown):
        self.next_button_to.config(text="Start from " + unknown + " to " + known)
        self.next_button_from.config(text="Start from " + known + " to " + unknown)
        self.frame.update()


class CardsView(View):
    def __init__(self, root):
        super().__init__(root)
        self.cycle_number_label = Label(self.frame, "Cycle 3")
        self.cycle_number_label.pack(side="top", pady=15, padx=10, fill="x")

        # Statistic
        self.statistic_frame = tk.Frame(self.frame, bg=DesignSettings.BG_COLOR, height=40, width=400)

        self.remaining_cards_label = Label(self.statistic_frame, "Remaining cards:")
        self.remaining_cards_label.configure(font=DesignSettings.SMALL_FONT)
        self.remaining_cards_number = Label(self.statistic_frame, "21")

        self.guessed_cards_label = Label(self.statistic_frame, "Guessed cards:")
        self.guessed_cards_label.configure(font=DesignSettings.SMALL_FONT)
        self.guessed_cards_number = Label(self.statistic_frame, "7")

        self.left_cards_label = Label(self.statistic_frame, "Left to next cycle:")
        self.left_cards_label.configure(font=DesignSettings.SMALL_FONT)
        self.left_cards_number = Label(self.statistic_frame, "53")

        self.remaining_cards_label.grid(row=0, column=0, sticky="w")
        self.remaining_cards_number.grid(row=0, column=1, sticky="we")
        self.guessed_cards_label.grid(row=1, column=0, sticky="w")
        self.guessed_cards_number.grid(row=1, column=1, sticky="we")
        self.left_cards_label.grid(row=2, column=0, sticky="w")
        self.left_cards_number.grid(row=2, column=1, sticky="we")

        self.statistic_frame.pack(side="top", pady=10, padx=10)

        # Cards
        self.cards_frame = tk.Frame(self.frame, bg=DesignSettings.BG_COLOR)
        self.cards_frame.rowconfigure(0, weight=1)
        self.cards_frame.columnconfigure(0, weight=1)
        self.cards_frame.columnconfigure(1, weight=1)

        self.card_known = Label(self.cards_frame, text="", width=20)
        self.card_unknown = Label(self.cards_frame, text="", width=20)

        self.card_known.configure(bg=DesignSettings.BG_COLOR_CARDS)
        self.card_unknown.configure(bg=DesignSettings.BG_COLOR_CARDS)

        self.card_known.grid(row=0, column=0, padx=5, sticky="nwse")
        self.card_unknown.grid(row=0, column=1, padx=5, sticky="nwse")
        self.cards_frame.pack(side="top", pady=15, padx=10, expand=True, fill="both")

        # Buttons
        self.buttons_frame = tk.Frame(self.frame, bg=DesignSettings.BG_COLOR)
        self.buttons_frame.rowconfigure(0, weight=1)
        self.buttons_frame.rowconfigure(1, weight=1)
        self.buttons_frame.columnconfigure(0, weight=1)
        self.buttons_frame.columnconfigure(1, weight=1)

        self.pick_button = Button(self.buttons_frame, "Pick", "null")
        self.pick_button.grid(row=0, column=0, columnspan=2, padx=1, pady=1, sticky="nwse")

        self.got_it = Button(self.buttons_frame, "Got it!", "null", state="disabled")
        self.got_it.grid(row=1, column=1, padx=1, sticky="nwse")

        self.no_button = Button(self.buttons_frame, "No :-(", "null", state="disabled")
        self.no_button.grid(row=1, column=0, padx=1, sticky="nwse")

        self.buttons_frame.pack(pady=20)
