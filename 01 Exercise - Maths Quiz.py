from tkinter import *
import random

class AZPENMathQuiz:
    def __init__(self, master):
        self.master = master
        self.master.title("AZPEN Math Quiz")
        self.master.geometry('500x500')
        self.master.configure(bg="#fcba03")  # Keeping your original yellow theme

        self.player_name = ""
        self.player_score = 0
        self.current_q_index = 0
        self.selected_level = "Easy"
        self.max_attempts = 3
        self.remaining_time = 0
        self.timer_id = None

        # Difficulty settings: (min value, max value, number of questions, timer duration)
        self.difficulty_settings = {
            "Easy": (1, 9, 20, 15),
            "Moderate": (10, 99, 15, 12),
            "Advanced": (1000, 9999, 10, 10)
        }

        # Fun Gen Z-inspired comments for feedback
        self.correct_comments = [
            "Slayed it! 🥳", 
            "You're lowkey a math wizard! 🔮", 
            "Big brain energy! 💡", 
            "Yasss! Nailed it! 🙌", 
            "Legend behavior, no cap. 🤯", 
            "Certified genius moment 🧠"
        ]
        self.incorrect_comments = [
            "Oof, not quite. 😬", 
            "That’s a flop... Try again! 🚫", 
            "You’re close, fam! 👀", 
            "Don’t stress, even legends make mistakes. 😅", 
            "Keep going, you got this! ✨", 
            "Take the L and learn from it! 🧠"
        ]
        self.timeout_comments = [
            "Oops, you ran outta time! ⏰", 
            "Time really flew there! ⏳", 
            "It’s okay, time’s tricky like that! 💨", 
            "Missed it! But you're still fire. 🔥"
        ]

        # Start with the welcome screen
        self.show_welcome_screen()

    # Display welcome screen with original yellow background
    def show_welcome_screen(self):
        self.clear_frame()
        
        welcome_frame = Frame(self.master, bg="#fcba03")
        welcome_frame.pack(pady=20)

        Label(welcome_frame, text="Welcome to AZPEN Math!", font=("Poppins", 16, "bold"), bg="#fcba03").grid(row=0, column=0, columnspan=2, pady=10)
        Label(welcome_frame, text="Ready to flex those brain muscles?", font=("Poppins", 14), bg="#fcba03").grid(row=1, column=0, columnspan=2, pady=5)

        Button(welcome_frame, text="Let's Go!", font=("Poppins", 12), bg="white", command=self.get_player_name).grid(row=2, column=0, pady=10)
        Button(welcome_frame, text="Exit", font=("Poppins", 12), bg="white", command=self.master.destroy).grid(row=2, column=1, pady=10)

    # Get the player's name with an animation trigger on submit
    def get_player_name(self):
        self.clear_frame()
        Label(self.master, text="What's your name, mathlete?", font=("Poppins", 12), bg="#fcba03").pack(pady=10)
        self.name_input = Entry(self.master, font=("Poppins", 12))
        self.name_input.pack(pady=10)
        Button(self.master, text="Submit", font=("Poppins", 12), bg="white", command=self.set_name).pack(pady=10)

    # Set the player's name and move to difficulty selection
    def set_name(self):
        self.player_name = self.name_input.get()
        if self.player_name.strip():
            self.show_difficulty_selection()
        else:
            self.display_feedback("Please enter a valid name. It’s a must!")

    # Show difficulty level selection with original yellow theme
    def show_difficulty_selection(self):
        self.clear_frame()
        Label(self.master, text="Choose Your Challenge Level", font=("Poppins", 16, "bold"), bg="#fcba03").pack(pady=10)

        for level in self.difficulty_settings.keys():
            Button(self.master, text=level, font=("Poppins", 12), width=20, bg="white", command=lambda lvl=level: self.start_quiz(lvl)).pack(pady=10)

    # Start the quiz for the selected difficulty level
    def start_quiz(self, level):
        self.selected_level = level
        self.player_score = 0
        self.current_q_index = 0
        self.reset_attempts()
        self.ask_next_question()

    # Reset the attempt counter
    def reset_attempts(self):
        self.max_attempts = 3

    # Generate a random integer
    def generate_random_int(self, min_val, max_val):
        return random.randint(min_val, max_val)

    # Randomly decide on addition or subtraction
    def pick_operation(self):
        return random.choice(['+', '-'])

    # Set up and display the current math problem
    def setup_problem(self):
        self.clear_frame()
        min_val, max_val = self.difficulty_settings[self.selected_level][:2]
        
        self.first_num = self.generate_random_int(min_val, max_val)
        self.second_num = self.generate_random_int(min_val, max_val)
        self.operation = self.pick_operation()

        if self.operation == '-' and self.first_num < self.second_num:
            self.first_num, self.second_num = self.second_num, self.first_num

        self.correct_answer = self.first_num + self.second_num if self.operation == '+' else self.first_num - self.second_num
        problem_text = f"{self.first_num} {self.operation} {self.second_num} = ?"

        Label(self.master, text=problem_text, font=("Poppins", 14), bg="#fcba03").pack(pady=10)

        self.answer_input = Entry(self.master, font=("Poppins", 12))
        self.answer_input.pack(pady=10)
        self.answer_input.focus()

        Button(self.master, text="Check Answer", font=("Poppins", 12), bg="white", command=self.verify_answer).pack(pady=5)
        Label(self.master, text=f"Score: {self.player_score}", font=("Poppins", 12), bg="#fcba03").pack(pady=5)
        Label(self.master, text=f"Remaining Attempts: {self.max_attempts}", font=("Poppins", 12), bg="#fcba03").pack(pady=5)

        self.remaining_time = self.difficulty_settings[self.selected_level][3]
        self.timer_label = Label(self.master, text=f"Time left: {self.remaining_time} s", font=("Poppins", 12), bg="#fcba03")
        self.timer_label.pack(pady=5)
        self.start_timer()

    # Timer for the question
    def start_timer(self):
        if self.remaining_time > 0:
            self.remaining_time -= 1
            self.timer_label.config(text=f"Time left: {self.remaining_time} s")
            self.timer_id = self.master.after(1000, self.start_timer)
        else:
            self.master.after_cancel(self.timer_id)
            self.max_attempts -= 1
            if self.max_attempts <= 0:
                self.finish_quiz("Time's up! You ran out of attempts!")
            else:
                self.display_feedback(random.choice(self.timeout_comments), next_question=True)

    # Verify the player's answer
    def verify_answer(self):
        if self.timer_id:
            self.master.after_cancel(self.timer_id)
        
        try:
            user_answer = int(self.answer_input.get())
        except ValueError:
            self.display_feedback("Uh oh, that's not even a number! 📉 Try again.")
            return
        
        if user_answer == self.correct_answer:
            self.player_score += 10
            self.display_feedback(random.choice(self.correct_comments), next_question=True)
        else:
            self.max_attempts -= 1
            if self.max_attempts <= 0:
                self.finish_quiz("Incorrect. All attempts are gone!")
            else:
                self.display_feedback(random.choice(self.incorrect_comments))

    # Ask the next question or finish the quiz
    def ask_next_question(self):
        self.current_q_index += 1
        if self.current_q_index < self.difficulty_settings[self.selected_level][2]:
            self.setup_problem()
        else:
            self.finish_quiz("Great job! You finished all the questions!")

    # Provide feedback to the player
    def display_feedback(self, msg, next_question=False):
        self.clear_frame()
        Label(self.master, text=msg, font=("Poppins", 14), bg="#fcba03").pack(pady=10)

        if next_question:
            Button(self.master, text="Next Question", font=("Poppins", 12), bg="white", command=self.ask_next_question).pack(pady=10)
        else:
            Button(self.master, text="Try Again", font=("Poppins", 12), bg="white", command=self.setup_problem).pack(pady=5)

    # End the quiz and show results
    def finish_quiz(self, msg):
        self.clear_frame()
        final_grade = self.calculate_grade()
        Label(self.master, text=msg, font=("Poppins", 16, "bold"), bg="#fcba03").pack(pady=10)
        Label(self.master, text=f"{self.player_name}'s Final Score: {self.player_score}", font=("Poppins", 14), bg="#fcba03").pack(pady=5)
        Label(self.master, text=f"Grade: {final_grade}", font=("Poppins", 14), bg="#fcba03").pack(pady=5)

        Button(self.master, text="Play Again", font=("Poppins", 12), bg="white", command=self.show_difficulty_selection).pack(pady=10)
        Button(self.master, text="Exit", font=("Poppins", 12), bg="white", command=self.master.destroy).pack(pady=5)

    # Calculate the player's grade based on their score
    def calculate_grade(self):
        if self.player_score >= 90:
            return "A+ 🎉 You're a genius!"
        elif self.player_score >= 75:
            return "A 😄 Amazing job!"
        elif self.player_score >= 60:
            return "B 👍 Good effort!"
        elif self.player_score >= 50:
            return "C 🙂 Keep practicing!"
        else:
            return "D 😅 Don't give up!"

    # Clear the frame for new content
    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()

# Initialize the GUI application
root = Tk()
app = AZPENMathQuiz(root)
root.mainloop()
