import tkinter as tk
from tkinter import messagebox
import random
import time

# Function to get a random word and its hint
def get_word_and_hint(words_with_hints):
    word, hint = random.choice(list(words_with_hints.items()))
    return word, hint

# Function to format the remaining time
def format_time(seconds):
    return time.strftime("%M:%S", time.gmtime(seconds))

# Dictionary of words with hints
words_with_hints = {
    'rainbow': 'A multicolored arc in the sky',
    'computer': 'An electronic device for storing and processing data',
    'science': 'A systematic enterprise that builds and organizes knowledge',
    'programming': 'The process of writing computer programs',
    'python': 'A high-level programming language',
    'mathematics': 'The abstract science of number, quantity, and space',
    'player': 'A person taking part in a sport or game',
    'condition': 'The state of something with regard to its appearance, quality, or working order',
    'reverse': 'Move backward',
    'water': 'A transparent, tasteless, odorless, and nearly colorless chemical substance',
    'board': 'A flat, thin, rectangular piece of wood or other stiff material',
}

class WordGuessingGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Word Guessing Game")
        self.root.configure(bg='lightblue')

        self.name_label = tk.Label(root, text="Enter your name:", bg='lightblue')
        self.name_label.pack()

        self.name_entry = tk.Entry(root)
        self.name_entry.pack()

        self.start_button = tk.Button(root, text="Start Game", command=self.start_game)
        self.start_button.pack()

        self.hint_label = tk.Label(root, text="", bg='lightblue')
        self.hint_label.pack()

        self.word_label = tk.Label(root, text="", bg='lightblue')
        self.word_label.pack()

        self.guess_entry = tk.Entry(root)
        self.guess_entry.pack()

        self.guess_button = tk.Button(root, text="Guess", command=self.guess_character)
        self.guess_button.pack()

        self.time_label = tk.Label(root, text="", bg='lightblue')
        self.time_label.pack()

        self.message_label = tk.Label(root, text="", bg='lightblue')
        self.message_label.pack()

        self.turns_label = tk.Label(root, text="", bg='lightblue')
        self.turns_label.pack()

        self.points_label = tk.Label(root, text="", bg='lightblue')
        self.points_label.pack()

        self.reset_game()

    def reset_game(self):
        self.word, self.hint = get_word_and_hint(words_with_hints)
        self.guesses = ''
        self.turns = 12
        self.points = 0
        self.time_limit = 60
        self.start_time = time.time()
        self.update_word_display()
        self.hint_label.config(text=f"Hint: {self.hint}")
        self.turns_label.config(text=f"Turns left: {self.turns}")
        self.points_label.config(text=f"Points: {self.points}")
        self.message_label.config(text="")
        self.update_time()

    def start_game(self):
        self.name = self.name_entry.get()
        if not self.name:
            messagebox.showwarning("Name Required", "Please enter your name to start the game.")
            return
        self.name_entry.config(state=tk.DISABLED)
        self.start_button.config(state=tk.DISABLED)
        self.reset_game()

    def update_word_display(self):
        displayed_word = ' '.join(char if char in self.guesses else '_' for char in self.word)
        self.word_label.config(text=displayed_word)

    def update_time(self):
        elapsed_time = time.time() - self.start_time
        remaining_time = self.time_limit - elapsed_time
        if remaining_time <= 0:
            self.time_label.config(text="Time's up!")
            self.end_game(False)
        else:
            self.time_label.config(text=f"Time left: {format_time(remaining_time)}")
            self.root.after(1000, self.update_time)

    def guess_character(self):
        guess = self.guess_entry.get().lower()
        self.guess_entry.delete(0, tk.END)
        if len(guess) != 1:
            self.message_label.config(text="Please enter a single character.")
            return
        if guess in self.guesses:
            self.message_label.config(text="You already guessed that character.")
            return

        self.guesses += guess
        if guess in self.word:
            self.points += 1
        else:
            self.turns -= 1
            self.points -= 1
            self.message_label.config(text="Wrong guess!")

        self.turns_label.config(text=f"Turns left: {self.turns}")
        self.points_label.config(text=f"Points: {self.points}")
        self.update_word_display()

        if all(char in self.guesses for char in self.word):
            self.end_game(True)
        elif self.turns == 0:
            self.end_game(False)

    def end_game(self, won):
        if won:
            self.message_label.config(text=f"Congratulations, {self.name}! You guessed the word '{self.word}'. You win!")
        else:
            self.message_label.config(text=f"Sorry, {self.name}. You lose. The word was '{self.word}'.")
        self.start_button.config(state=tk.NORMAL)
        self.name_entry.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    game = WordGuessingGame(root)
    root.mainloop()
