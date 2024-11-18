from tkinter import *
import random

# A unique class to hold jokes and related content
class UniqueWords:
    def __init__(self, joke, punchline):
        self.joke = joke
        self.punchline = punchline

    def get_joke(self):
        return self.joke

    def get_punchline(self):
        return self.punchline

class JokeTeller:
    def __init__(self, master):
        self.master = master
        self.master.title("Joke Teller")  # "Title? That's lit!"
        self.master.geometry('500x500')  # Size to fit the vibes
        self.master.configure(bg="#fcba03")  # Background color vibes
        self.jokes = self.load_jokes()  # Load the jokes like it's a playlist
        self.current_label = None
        self.show_welcome_screen()

    def load_jokes(self):
        jokes_list = []
        # Load jokes from a file, keep it 100
        with open(r"C:\Users\bauti\Downloads\Tkinter program Python ASSESMENTS\randomjokes.txt") as file:
            for line in file:
                if '?' in line:
                    parts = line.strip().split('?')
                    # Create an instance of UniqueWords for each joke
                    jokes_list.append(UniqueWords(parts[0].strip(), parts[1].strip()))
        return jokes_list

    def tell_joke(self):
        current_joke = random.choice(self.jokes)  # Pick a joke like a snack
        self.clear_frame()
        self.display_joke(current_joke.get_joke())  # Joke time
        Button(self.master, text="Show Punchline", font=("Poppins", 12), bg="white", 
               command=lambda: self.show_punchline(current_joke.get_punchline())).pack(pady=10)

    def show_punchline(self, punchline):
        self.clear_frame()
        self.display_joke(punchline)  # Show that punchline glow-up
        Button(self.master, text="Tell another Joke", font=("Poppins", 12), bg="white", 
               command=self.tell_joke).pack(pady=10)

    def show_welcome_screen(self):
        self.clear_frame()
        welcome_frame = Frame(self.master, bg="#fcba03")  # Keeping it fresh
        welcome_frame.pack(pady=20)
        Label(welcome_frame, text="Welcome to the Joke Teller!", font=("Poppins", 16, "bold"), 
              bg="#fcba03").grid(row=0, column=0, columnspan=2, pady=10)
        Button(welcome_frame, text="Tell me a Joke", font=("Poppins", 12), bg="white", 
               command=self.tell_joke).grid(row=2, column=0, pady=10)
        Button(welcome_frame, text="Exit", font=("Poppins", 12), bg="white", 
               command=self.master.quit).grid(row=2, column=1, pady=10)

    def display_joke(self, text):
        # Create a label for the text
        self.current_label = Label(self.master, text=text, font=("Poppins", 14), bg="#fcba03")
        self.current_label.pack(pady=20)

    def clear_frame(self):
        for widget in self.master.winfo_children():
            widget.destroy()  # Clear the space like a fresh slate

if __name__ == "__main__":
    root = Tk()
    app = JokeTeller(root)
    root.mainloop()
