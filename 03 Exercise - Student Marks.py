from tkinter import *
from tkinter import font, ttk
import csv

# 🍎 Class representing a Student object with properties and methods to calculate grade and provide summary
class Student:
    def __init__(self, student_id, name, coursework_marks, exam_mark):
        self.student_id = student_id
        self.name = name
        self.coursework_marks = coursework_marks
        self.exam_mark = exam_mark
        # 🧮 Adding coursework marks to get that cumulative score
        self.total_coursework = sum(coursework_marks)
        # 🎯 Calculating total score (coursework + exam)
        self.total_score = self.total_coursework + exam_mark
        # 🎓 Find percentage based on total possible score (160)
        self.percentage = (self.total_score / 160) * 100
        # 🌟 Assign grade based on calculated percentage
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        # 🤓 Grade calculation logic, no cap
        if self.percentage >= 70:
            return 'A'
        elif self.percentage >= 60:
            return 'B'
        elif self.percentage >= 50:
            return 'C'
        elif self.percentage >= 40:
            return 'D'
        else:
            return 'F'

    def summary(self):
        # 📄 Generating a detailed summary for each student
        return (f"Name: {self.name}\nID: {self.student_id}\n"
                f"Total Coursework Mark: {self.total_coursework}\n"
                f"Exam Mark: {self.exam_mark}\nOverall Percentage: {self.percentage:.2f}%\n"
                f"Grade: {self.grade}\n")

# 🖥️ GUI class to manage student records using tkinter
class StudentManagerGUI:
    def __init__(self, master):
        # 🎨 Set up main window
        self.master = master
        self.master.title("Student Manager")
        self.master.geometry("700x500")
        self.master.configure(bg="#fcba03")  # 🔆 Setting background color to pop yellow
        
        # 🚀 Auto-loading student data from file on startup
        self.students = self.load_data(r"C:\Users\bauti\Downloads\Tkinter program Python ASSESMENTS\studentMarks.txt")
        self.student_names = [student.name for student in self.students]
        
        # 🏷️ Title setup
        title_font = font.Font(family="Poppins", size=16, weight="bold")
        Label(master, text="Student Manager", font=title_font, bg="#fcba03").pack(pady=10)
        
        # ⬇️ Section for main action buttons (view all, highest, lowest)
        button_frame = Frame(master, bg="#fcba03")
        button_font = font.Font(family="Poppins", size=10)
        
        # 👀 Button to view all student records
        view_all_button = Button(button_frame, text="View All Student Records", font=button_font, width=20, command=self.view_all_records)
        view_all_button.grid(row=0, column=0, padx=5, pady=10)
        
        # 🔝 Button to show the highest scoring student
        highest_score_button = Button(button_frame, text="Show Highest Score", font=button_font, width=20, command=self.show_highest_score)
        highest_score_button.grid(row=0, column=1, padx=5, pady=10)
        
        # 📉 Button to show the lowest scoring student
        lowest_score_button = Button(button_frame, text="Show Lowest Score", font=button_font, width=20, command=self.show_lowest_score)
        lowest_score_button.grid(row=0, column=2, padx=5, pady=10)
        
        button_frame.pack(pady=10)
        
        # 🎯 Section title for individual student records
        individual_label_font = font.Font(family="Poppins", size=12, weight="bold")
        Label(master, text="View Individual Student Record", font=individual_label_font, bg="#fcba03").pack(pady=10)
        
        # 🧩 Frame to hold dropdown and record view button
        individual_frame = Frame(master, bg="#fcba03")
        
        # 📝 Dropdown to select student
        self.selected_student = StringVar()
        self.selected_student.set("Select Student")
        
        student_dropdown = ttk.Combobox(individual_frame, textvariable=self.selected_student, values=self.student_names, font=button_font, width=20)
        student_dropdown.grid(row=0, column=0, padx=5)
        
        # 🔍 Button to view the selected student's record
        view_record_button = Button(individual_frame, text="View Record", font=button_font, command=self.view_individual_record)
        view_record_button.grid(row=0, column=1, padx=5)
        
        individual_frame.pack(pady=10)
        
        # 📝 Text box with scroll bar to display student records
        text_frame = Frame(master, bg="#fcba03")
        text_frame.pack(pady=10)
        
        self.record_text = Text(text_frame, height=12, width=80, font=("Poppins", 10), bg="white", wrap=WORD)
        self.record_text.grid(row=0, column=0)
        self.record_text.config(state=DISABLED)
        
        # 📜 Scroll bar to navigate through records if too long
        scrollbar = Scrollbar(text_frame, command=self.record_text.yview)
        scrollbar.grid(row=0, column=1, sticky='ns')
        self.record_text['yscrollcommand'] = scrollbar.set

    def load_data(self, filename):
        # 📂 Load student data from .txt file
        students = []
        try:
            with open(filename, newline='') as file:
                reader = csv.reader(file)
                next(reader)  # 🧹 Skipping header line
                for row in reader:
                    student_id = int(row[0])
                    name = row[1]
                    coursework_marks = list(map(int, row[2:5]))
                    exam_mark = int(row[5])
                    # 🎒 Creating Student object and adding to list
                    students.append(Student(student_id, name, coursework_marks, exam_mark))
        except FileNotFoundError:
            print("File not found. Make sure studentMarks.txt is in the specified location.")
        except Exception as e:
            print(f"An error occurred: {e}")
        return students

    def view_all_records(self):
        # 🔍 Displaying all records in text box
        self.record_text.config(state=NORMAL)
        self.record_text.delete(1.0, END)
        records = "\n\n".join(student.summary() for student in self.students)
        # 📊 Calculating total and average percentage for all students
        total_percentage = sum(student.percentage for student in self.students)
        avg_percentage = total_percentage / len(self.students) if self.students else 0
        records += f"\n\nAverage Percentage: {avg_percentage:.2f}%\nTotal Students: {len(self.students)}"
        self.record_text.insert(END, records)
        self.record_text.config(state=DISABLED)

    def show_highest_score(self):
        # 🎖 Display student with the highest score
        self.record_text.config(state=NORMAL)
        self.record_text.delete(1.0, END)
        if self.students:
            highest_student = max(self.students, key=lambda s: s.total_score)
            self.record_text.insert(END, "Student with the Highest Score:\n" + highest_student.summary())
        else:
            self.record_text.insert(END, "No student records available.")
        self.record_text.config(state=DISABLED)

    def show_lowest_score(self):
        # 👇 Display student with the lowest score
        self.record_text.config(state=NORMAL)
        self.record_text.delete(1.0, END)
        if self.students:
            lowest_student = min(self.students, key=lambda s: s.total_score)
            self.record_text.insert(END, "Student with the Lowest Score:\n" + lowest_student.summary())
        else:
            self.record_text.insert(END, "No student records available.")
        self.record_text.config(state=DISABLED)

    def view_individual_record(self):
        # 🔎 Fetch and display individual student record
        selected_name = self.selected_student.get()
        self.record_text.config(state=NORMAL)
        self.record_text.delete(1.0, END)
        found_student = next((student for student in self.students if student.name == selected_name), None)
        if found_student:
            self.record_text.insert(END, f"Record for {selected_name}:\n" + found_student.summary())
        else:
            self.record_text.insert(END, "Student not found.")
        self.record_text.config(state=DISABLED)

# 🌟 Initialize and start GUI application
root = Tk()
app = StudentManagerGUI(root)
root.mainloop()
