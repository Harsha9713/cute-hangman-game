import tkinter as tk
from tkinter import messagebox
import random

# ----------------- Word List with Hints -----------------
word_list = [
    {"word": "banana", "hint1": "It's a fruit", "hint2": "Monkeys love it"},
    {"word": "butterfly", "hint1": "A flying insect", "hint2": "Emerges from a cocoon"},
    {"word": "unicorn", "hint1": "Mythical creature", "hint2": "Has a horn on its head"},
    {"word": "rainbow", "hint1": "Appears after rain", "hint2": "Has seven colors"},
    {"word": "sunshine", "hint1": "Seen during the day", "hint2": "Brings warmth and light"},
    {"word": "pineapple", "hint1": "It's a fruit", "hint2": "Has pines"},
    {"word":"school","hint1":"You visit here often","hint2":"Books"}
]

# ----------------- Game Class -----------------
class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Cute Hangman Game")
        self.root.geometry("800x600")
        self.root.configure(bg="#fffacd")

        self.score = 0
        self.wrong_guesses = 0
        self.button_refs = {}
        self.used_second_hint = False

        self.front_page()

    def front_page(self):
        self.clear_window()
        canvas = tk.Canvas(self.root, width=800, height=600, bg="#fffacd", highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        self.decorate_canvas(canvas)

        title = tk.Label(canvas, text="🢕 Cute Hangman 🢕", font=("Segoe Script", 36, "bold"), bg="#fffacd", fg="#ff69b4")
        title.place(relx=0.5, rely=0.3, anchor="center")

        start_btn = tk.Button(canvas, text="Start Game 🎮", font=("Comic Sans MS", 16, "bold"),
                              bg="#ffcccb", fg="white", activebackground="#ffb6c1", padx=20, pady=10,
                              command=self.start_game, relief="flat")
        start_btn.place(relx=0.5, rely=0.5, anchor="center")

    def start_game(self):
        self.clear_window()
        word_obj = random.choice(word_list)
        self.word = word_obj["word"]
        self.hint1 = word_obj["hint1"]
        self.hint2 = word_obj["hint2"]
        self.display = ["_" for _ in self.word]
        self.used_letters = []
        self.wrong_guesses = 0
        self.button_refs = {}
        self.used_second_hint = False

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="#fffacd", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.decorate_canvas(self.canvas)

        self.word_label = tk.Label(self.canvas, text=" ".join(self.display), font=("Arial", 28, "bold"), bg="#fffacd", fg="#ff69b4")
        self.word_label.pack(pady=10)

        self.hint1_label = tk.Label(self.canvas, text=f"Hint 1: {self.hint1}", font=("Comic Sans MS", 14), bg="#fffacd", fg="#ff69b4")
        self.hint1_label.pack()

        self.hint2_btn = tk.Button(self.canvas, text="💡 Hint", font=("Comic Sans MS", 12, "bold"), bg="#ffcccb", fg="white",
                                   activebackground="#ffb6c1", command=self.show_second_hint)
        self.hint2_btn.pack()

        self.hint2_label = tk.Label(self.canvas, text="", font=("Comic Sans MS", 14), bg="#fffacd", fg="#ff69b4")
        self.hint2_label.pack()

        self.score_label = tk.Label(self.canvas, text=f"Score: {self.score}", font=("Arial", 16), bg="#fffacd", fg="#ff69b4")
        self.score_label.pack()

        self.hangman_canvas = tk.Canvas(self.canvas, width=200, height=250, bg="#fffacd", highlightthickness=0)
        self.hangman_canvas.pack()
        self.draw_gallows()

        self.keyboard_frame = tk.Frame(self.canvas, bg="#fffacd")
        self.keyboard_frame.pack(pady=20)
        self.draw_keyboard()

    def draw_keyboard(self):
        for widget in self.keyboard_frame.winfo_children():
            widget.destroy()

        for i, letter in enumerate("abcdefghijklmnopqrstuvwxyz"):
            btn = tk.Button(self.keyboard_frame, text=letter, width=4, height=2, font=("Comic Sans MS", 12, "bold"),
                            bg="#ffe4e1", fg="#ff69b4", relief="raised",
                            command=lambda l=letter: self.guess_letter(l))
            btn.grid(row=i//9, column=i%9, padx=4, pady=4)
            self.button_refs[letter] = btn

    def guess_letter(self, letter):
        if letter in self.used_letters:
            return
        self.used_letters.append(letter)
        btn = self.button_refs.get(letter)
        if btn:
            btn.config(state="disabled")

        if letter in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.display[i] = letter
            self.word_label.config(text=" ".join(self.display))
            if btn:
                btn.config(bg="#98FB98")  # green
            if "_" not in self.display:
                self.score += 0.5 if self.used_second_hint else 1
                messagebox.showinfo("🎉 You Win!", f"Correct! The word was '{self.word}'")
                self.start_game()
        else:
            self.wrong_guesses += 1
            if btn:
                btn.config(bg="#ff6961")  # red
            self.update_hangman()
            if self.wrong_guesses >= 6:
                messagebox.showerror("😭 Game Over", f"Oops! The word was '{self.word}'")
                self.score = 0
                self.start_game()

        self.score_label.config(text=f"Score: {self.score}")

    def show_second_hint(self):
        self.used_second_hint = True
        self.hint2_label.config(text=f"Hint 2: {self.hint2}")
        self.hint2_btn.config(state="disabled")

    def draw_gallows(self):
        self.hangman_canvas.delete("all")
        self.hangman_canvas.create_line(20, 230, 180, 230, width=3)
        self.hangman_canvas.create_line(50, 230, 50, 20, width=3)
        self.hangman_canvas.create_line(50, 20, 130, 20, width=3)
        self.hangman_canvas.create_line(130, 20, 130, 50, width=3)

    def update_hangman(self):
        if self.wrong_guesses == 1:
            self.hangman_canvas.create_oval(110, 50, 150, 90, width=3)
        elif self.wrong_guesses == 2:
            self.hangman_canvas.create_line(130, 90, 130, 150, width=3)
        elif self.wrong_guesses == 3:
            self.hangman_canvas.create_line(130, 110, 110, 130, width=3)
        elif self.wrong_guesses == 4:
            self.hangman_canvas.create_line(130, 110, 150, 130, width=3)
        elif self.wrong_guesses == 5:
            self.hangman_canvas.create_line(130, 150, 110, 180, width=3)
        elif self.wrong_guesses == 6:
            self.hangman_canvas.create_line(130, 150, 150, 180, width=3)

    def decorate_canvas(self, canvas):
        # Left clouds
        canvas.create_oval(50, 50, 150, 100, fill="white", outline="")
        canvas.create_oval(120, 40, 220, 100, fill="white", outline="")
        canvas.create_oval(90, 60, 190, 110, fill="white", outline="")

        # Right clouds
        canvas.create_oval(550, 50, 650, 100, fill="white", outline="")
        canvas.create_oval(620, 40, 720, 100, fill="white", outline="")
        canvas.create_oval(590, 60, 690, 110, fill="white", outline="")

        # Ducklings
        ducklings = [(230, 300, 270, 330, 260, 285, 290, 315, 290, 300, 300, 295, 290, 290, 280, 295, 283, 298),
                     (100, 300, 140, 330, 130, 285, 160, 315, 160, 300, 170, 295, 160, 290, 150, 295, 153, 298),
                     (930, 320, 970, 350, 960, 305, 990, 335, 990, 320, 1000, 315, 990, 310, 980, 315, 983, 318),
                     (1050, 330, 1090, 360, 1080, 315, 1110, 345, 1110, 330, 1120, 325, 1110, 320, 1100, 325, 1103, 328)]
        for body_x1, body_y1, body_x2, body_y2, head_x1, head_y1, head_x2, head_y2, beak_x1, beak_y1, beak_x2, beak_y2, beak_x3, beak_y3, eye_x1, eye_y1, eye_x2, eye_y2 in ducklings:
            canvas.create_oval(body_x1, body_y1, body_x2, body_y2, fill="#ffeb3b", outline="")
            canvas.create_oval(head_x1, head_y1, head_x2, head_y2, fill="#ffeb3b", outline="")
            canvas.create_polygon(beak_x1, beak_y1, beak_x2, beak_y2, beak_x3, beak_y3, fill="orange")
            canvas.create_oval(eye_x1, eye_y1, eye_x2, eye_y2, fill="black")

        # Flowers
        for x in list(range(50, 300, 100)) + list(range(500, 700, 100)) + list(range(750, 1150, 120)):
            canvas.create_oval(x, 500, x+10, 510, fill="yellow", outline="")
            canvas.create_oval(x+10, 500, x+20, 510, fill="yellow", outline="")
            canvas.create_oval(x+5, 490, x+15, 500, fill="yellow", outline="")
            canvas.create_oval(x+5, 510, x+15, 520, fill="yellow", outline="")
            canvas.create_oval(x+7, 502, x+13, 508, fill="orange", outline="")

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# ----------------- Run Game -----------------
if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
