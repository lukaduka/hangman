import tkinter as tk
from tkinter import messagebox
import random
from PIL import Image, ImageTk

# List of words for the Hangman game
WORDS = ["complicated", "philosophy", "architecture", "determination", "psychology", "exaggerate", "vocabulary", "literature", "algorithm", "synchronize", "parallel", "mathematics", "biology", "astronomy", "experiment", "elephant", "giraffe", "butterfly", "penguin", "rainbow"]

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")

        # Center the window
        self.root.geometry("600x600")
        self.root.resizable(False, False)

        self.word_to_guess = random.choice(WORDS).upper()
        self.guessed_word = ["_" for _ in self.word_to_guess]
        self.remaining_attempts = 6
        self.guessed_letters = set()

        # Load and resize hangman images
        self.hangman_images = [
            ImageTk.PhotoImage(Image.open(f"hangman-pictures/hangman{i}.png").resize((2024, 738)))
            for i in range(7)
        ]

        # Create a frame to center all elements with padding at the top
        self.frame = tk.Frame(root)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")
        self.frame.pack(pady=20)

        # Create UI elements
        self.canvas = tk.Canvas(self.frame, width=300, height=300)
        self.canvas.grid(row=0, column=0, columnspan=2, pady=10)
        self.image_on_canvas = self.canvas.create_image(150, 150, image=self.hangman_images[0])

        self.label_word = tk.Label(self.frame, text=" ".join(self.guessed_word), font=("Arial", 24))
        self.label_word.grid(row=1, column=0, columnspan=2, pady=10)

        self.label_message = tk.Label(self.frame, text="Guess a letter!", font=("Arial", 16))
        self.label_message.grid(row=2, column=0, columnspan=2, pady=10)

        self.entry_letter = tk.Entry(self.frame, font=("Arial", 16), justify="center")
        self.entry_letter.grid(row=3, column=0, columnspan=2, pady=10)
        self.entry_letter.bind("<Return>", self.guess_letter)

        self.button_guess = tk.Button(self.frame, text="Guess", command=self.guess_letter, font=("Arial", 16))
        self.button_guess.grid(row=4, column=0, pady=10)

        self.label_attempts = tk.Label(self.frame, text=f"Remaining attempts: {self.remaining_attempts}", font=("Arial", 16))
        self.label_attempts.grid(row=4, column=1, pady=10)

        self.reset_button = tk.Button(self.frame, text="Restart Game", command=self.reset_game, font=("Arial", 16))
        self.reset_button.grid(row=5, column=0, columnspan=2, pady=20)

        # Set focus to the input box when the game starts
        self.entry_letter.focus_set()

    def guess_letter(self, event=None):
        letter = self.entry_letter.get().strip().upper()
        self.entry_letter.delete(0, tk.END)

        if not letter or len(letter) != 1 or not letter.isalpha():
            self.label_message.config(text="Enter a valid single letter.")
            return

        if letter in self.guessed_letters:
            self.label_message.config(text=f"You already guessed '{letter}'.")
            return

        self.guessed_letters.add(letter)

        if letter in self.word_to_guess:
            for i, char in enumerate(self.word_to_guess):
                if char == letter:
                    self.guessed_word[i] = letter
            self.label_message.config(text=f"Good job! '{letter}' is correct.")
        else:
            self.remaining_attempts -= 1
            self.label_message.config(text=f"Sorry, '{letter}' is not in the word.")

        self.update_ui()
        self.check_game_over()

    def update_ui(self):
        self.label_word.config(text=" ".join(self.guessed_word))
        self.label_attempts.config(text=f"Remaining attempts: {self.remaining_attempts}")
        self.canvas.itemconfig(self.image_on_canvas, image=self.hangman_images[6 - self.remaining_attempts])

    def check_game_over(self):
        if "_" not in self.guessed_word:
            messagebox.showinfo("Game Over", "Congratulations! You guessed the word!")
            self.reset_game()
        elif self.remaining_attempts == 0:
            messagebox.showinfo("Game Over", f"You lost! The word was: {self.word_to_guess}")
            self.reset_game()

    def reset_game(self):
        self.word_to_guess = random.choice(WORDS).upper()
        self.guessed_word = ["_" for _ in self.word_to_guess]
        self.remaining_attempts = 6
        self.guessed_letters = set()
        self.update_ui()
        self.label_message.config(text="Guess a letter!")
        self.entry_letter.focus_set()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
