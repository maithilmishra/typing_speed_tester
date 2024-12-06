#!/usr/bin/env python
# coding: utf-8

# In[7]:


import tkinter as tk
import time

# Sample passage for typing (lowercase, no punctuation)
SAMPLE_PASSAGE = (
    "life is a journey not a destination every step we take adds to our growth and learning the key "
    "to happiness lies in appreciating the small moments that make life beautiful we all face challenges "
    "but it is through these challenges that we find our strength and purpose kindness and compassion "
    "can transform the world a smile a kind word or a helping hand can make a difference in someone's life "
    "nature teaches us the beauty of simplicity the sun rises every day without fail the trees sway in the "
    "wind and the rivers flow endlessly life is a tapestry of experiences woven with threads of love hope "
    "and perseverance success is not measured by material wealth but by the positive impact we have on others "
    "believe in yourself and your ability to achieve your dreams no matter how difficult the path may seem "
    "with determination and effort anything is possible"
)

class TypingSpeedApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Typing Speed Test")
        self.root.geometry("800x600")
        self.root.configure(bg="#f4f4f4")
        
        self.start_time = None
        self.running_timer = False
        self.time_limit = 60  # Set time limit to 1 minute
        self.typed_words = []  # Store words typed by the user
        self.current_word_index = 0  # Keep track of the word to type next
        self.correct_word_count = 0

        # Split the passage into words for highlighting
        self.passage_words = SAMPLE_PASSAGE.split()

        # Title
        self.title_label = tk.Label(
            root, 
            text="Typing Speed Test", 
            font=("Arial", 20, "bold"), 
            bg="#f4f4f4", 
            fg="#333"
        )
        self.title_label.pack(pady=10)

        # Highlighted Passage
        self.passage_label = tk.Text(
            root,
            wrap="word",
            font=("Arial", 14),
            bg="#fff",
            fg="#444",
            relief="solid",
            bd=2,
            padx=10,
            pady=10,
            height=8,
            state="disabled",
        )
        self.passage_label.pack(pady=10)
        self.update_highlighted_passage()

        # Input Field for Typing
        self.input_frame = tk.Frame(root, bg="#f4f4f4")
        self.input_frame.pack(pady=10)

        self.input_label = tk.Label(
            self.input_frame,
            text="Type the highlighted word, then press Space:",
            font=("Arial", 12),
            bg="#f4f4f4",
            fg="#555"
        )
        self.input_label.pack(side="left", padx=5)

        self.input_entry = tk.Entry(self.input_frame, font=("Arial", 14), width=20, relief="solid", bd=2)
        self.input_entry.pack(side="left", padx=5)
        self.input_entry.bind("<space>", self.check_word)
        self.input_entry.bind("<FocusIn>", self.start_timer)

        # Timer
        self.timer_label = tk.Label(
            root,
            text="Time Remaining: 60 seconds",
            font=("Arial", 12, "bold"),
            bg="#f4f4f4",
            fg="#0078D7"
        )
        self.timer_label.pack(pady=10)

        # Results
        self.result_label = tk.Label(
            root,
            text="",
            font=("Arial", 14, "bold"),
            bg="#f4f4f4",
            fg="#333",
            wraplength=700,
            justify="center"
        )
        self.result_label.pack(pady=20)

        # Replay Button
        self.replay_button = tk.Button(
            root,
            text="Replay",
            font=("Arial", 14, "bold"),
            bg="#0078D7",
            fg="white",
            command=self.restart_game,
            state="disabled"
        )
        self.replay_button.pack(pady=20)

    def update_highlighted_passage(self):
        """
        Highlight the current word in the passage.
        """
        self.passage_label.config(state="normal")
        self.passage_label.delete(1.0, tk.END)

        for i, word in enumerate(self.passage_words):
            if i == self.current_word_index:
                self.passage_label.insert(tk.END, word + " ", ("highlight",))
            else:
                self.passage_label.insert(tk.END, word + " ")
        
        self.passage_label.tag_configure("highlight", foreground="blue", font=("Arial", 14, "bold"))
        self.passage_label.config(state="disabled")

    def start_timer(self, event=None):
        """
        Start the timer when the user begins typing.
        """
        if not self.running_timer:
            self.start_time = time.time()
            self.running_timer = True
            self.update_timer()

    def update_timer(self):
        """
        Update the timer and stop typing after 1 minute.
        """
        if self.running_timer:
            elapsed_time = int(time.time() - self.start_time)
            remaining_time = self.time_limit - elapsed_time

            if remaining_time > 0:
                self.timer_label.config(text=f"Time Remaining: {remaining_time} seconds")
                self.root.after(1000, self.update_timer)
            else:
                self.running_timer = False
                self.input_entry.config(state="disabled")
                self.display_results()

    def check_word(self, event):
        """
        Check if the typed word matches the corresponding word in the passage.
        """
        typed_word = self.input_entry.get().strip()
        if typed_word:  # Ignore if empty (e.g., pressing space without typing)
            self.typed_words.append(typed_word)

            # Check correctness of the word
            if self.current_word_index < len(self.passage_words):
                if typed_word == self.passage_words[self.current_word_index]:
                    self.correct_word_count += 1
            
            # Move to the next word
            self.current_word_index += 1
            self.update_highlighted_passage()

        self.input_entry.delete(0, tk.END)  # Clear the entry field

    def display_results(self):
        """
        Display the user's score, WPM, and accuracy.
        """
        elapsed_time = time.time() - self.start_time
        typed_word_count = len(self.typed_words)

        # Calculate WPM based on correct words
        words_per_minute = (self.correct_word_count / elapsed_time) * 60

        # Calculate Accuracy
        accuracy = (self.correct_word_count / max(1, typed_word_count)) * 100  # Prevent division by 0

        # Display results
        self.result_label.config(
            text=(
                f"Time's Up!\n\n"
                f"Words Typed: {typed_word_count}\n"
                f"Correct Words: {self.correct_word_count}\n"
                f"Words Per Minute (WPM): {words_per_minute:.2f}\n"
                f"Accuracy: {accuracy:.2f}%"
            ),
            fg="green"
        )

        # Enable Replay button
        self.replay_button.config(state="normal")

    def restart_game(self):
        """
        Restart the game by resetting variables and the UI.
        """
        self.start_time = None
        self.running_timer = False
        self.typed_words = []
        self.current_word_index = 0
        self.correct_word_count = 0
        self.result_label.config(text="")
        self.timer_label.config(text="Time Remaining: 60 seconds")
        self.input_entry.config(state="normal")
        self.replay_button.config(state="disabled")
        self.update_highlighted_passage()


# Run the app
root = tk.Tk()
app = TypingSpeedApp(root)
root.mainloop()


# In[ ]:




