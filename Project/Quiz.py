import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
import hashlib
import time
import random
from datetime import datetime

# --------------------------------------
# DATABASE SETUP
# --------------------------------------
def init_db():
    conn = sqlite3.connect('mega_quiz.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT UNIQUE,
                    password TEXT,
                    total_attempts INTEGER DEFAULT 0,
                    best_score INTEGER DEFAULT 0,
                    registration_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS scores (
                    id INTEGER PRIMARY KEY,
                    username TEXT,
                    score INTEGER,
                    total INTEGER,
                    time_taken TEXT,
                    status TEXT,
                    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )''')

    c.execute('''CREATE TABLE IF NOT EXISTS question_stats (
                    id INTEGER PRIMARY KEY,
                    question_text TEXT UNIQUE,
                    times_asked INTEGER DEFAULT 0,
                    times_correct INTEGER DEFAULT 0
                )''')

    conn.commit()
    conn.close()


# --------------------------------------
# TRANSLATIONS
# --------------------------------------
TRANSLATIONS = {
    "en": {
        "title": "🎓 PYTHON EXAM CENTER",
        "subtitle": "Advanced Testing Platform",
        "username": "👤 Username",
        "password": "🔒 Password",
        "login_btn": "🚀 Login & Start Exam",
        "register_btn": "📝 Register New Account",
        "leaderboard_btn": "🏆 View Leaderboard",
        "stats_btn": "📊 My Statistics",
        "difficulty_title": "⚙ SELECT DIFFICULTY LEVEL",
        "easy": "🟢 Easy",
        "easy_desc": "20 simple questions",
        "medium": "🟡 Medium",
        "medium_desc": "Balanced difficulty",
        "hard": "🔴 Hard",
        "hard_desc": "Expert challenge",
        "mixed": "🎲 Mixed",
        "mixed_desc": "Random difficulty",
        "back": "← Back",
        "examinee": "Examinee:",
        "difficulty": "Difficulty:",
        "timer": "⏱",
        "question": "Question",
        "answered": "Answered:",
        "skipped": "Skipped:",
        "skip_btn": "Skip",
        "submit_btn": "Submit",
        "finish_btn": "Finish",
        "language_btn": "🌐 Hindi",
        "leaderboard_title": "🏆 LEADERBOARD",
        "leaderboard_subtitle": "Top performers",
        "refresh": "Refresh"
    }
}

# ---------------------------------------------------------
# MAIN APP CLASS
# ---------------------------------------------------------
class MegaQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate Python Examination System")
        self.root.geometry("1000x750")
        self.root.configure(bg="#0a0e27")

        self.language = "en"

        # quiz states
        self.current_user = None
        self.questions = []
        self.current_q_idx = 0
        self.score = 0
        self.start_timestamp = 0
        self.total_time = 20 * 60
        self.is_quiz_active = False

        self.answered_questions = []
        self.skipped_questions = []

        self.all_questions = [
            # Easy
            {"q": "Python kisne develop ki?", "o": ["Dennis Ritchie", "Guido van Rossum", "James Gosling", "Bjarne Stroustrup"], "a": "Guido van Rossum", "d": "Easy"},
            {"q": "Python mein single line comment?", "o": ["//", "/*", "#", "--"], "a": "#", "d": "Easy"},
            {"q": "Function define karne ka keyword?", "o": ["func", "define", "def", "function"], "a": "def", "d": "Easy"},
            {"q": "Python kis type ki language hai?", "o": ["Compiled", "Interpreted", "Low-level", "Assembly"], "a": "Interpreted", "d": "Easy"},
            {"q": "String ko int mein convert kaise kare?", "o": ["str()", "int()", "float()", "parse()"], "a": "int()", "d": "Easy"},

            # Medium
            {"q": "Kaunsa datatype immutable hota hai?", "o": ["List", "Dictionary", "Set", "Tuple"], "a": "Tuple", "d": "Medium"},
            {"q": "Python dictionary ka syntax?", "o": ["[]", "()", "{}", "<>"], "a": "{}", "d": "Medium"},
            {"q": "Python keyword list check ka module?", "o": ["keyword", "os", "sys", "math"], "a": "keyword", "d": "Medium"},

            # Hard
            {"q": "Python integer division operator?", "o": ["/", "//", "%", "\\"], "a": "//", "d": "Hard"},
            {"q": "Kaunsa web framework Python ka hai?", "o": ["Pandas", "Django", "NumPy", "Matplotlib"], "a": "Django", "d": "Hard"},
        ]

        self.main_container = tk.Frame(self.root, bg="#0a0e27")
        self.main_container.pack(fill="both", expand=True)

        self.show_login_screen()

    # Utility translation
    def get_text(self, key):
        return TRANSLATIONS[self.language].get(key, key)

    def clear_screen(self):
        for w in self.main_container.winfo_children():
            w.destroy()

    # --------------------------------------------------------
    # LOGIN SCREEN
    # --------------------------------------------------------
    def show_login_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.main_container, bg="#1e293b", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text=self.get_text("title"),
                 font=("Segoe UI", 26, "bold"),
                 fg="#60a5fa", bg="#1e293b").pack(pady=10)

        tk.Label(frame, text=self.get_text("subtitle"),
                 font=("Arial", 11),
                 fg="#94a3b8", bg="#1e293b").pack(pady=5)

        # username input
        tk.Label(frame, text=self.get_text("username"), fg="white", bg="#1e293b").pack()
        self.user_ent = tk.Entry(frame, font=("Arial", 14), width=28)
        self.user_ent.pack(pady=10)

        tk.Label(frame, text=self.get_text("password"), fg="white", bg="#1e293b").pack()
        self.pass_ent = tk.Entry(frame, show="*", font=("Arial", 14), width=28)
        self.pass_ent.pack(pady=10)

        tk.Button(frame, text=self.get_text("login_btn"),
                  command=self.handle_login,
                  bg="#10b981", fg="white",
                  font=("Arial", 12, "bold"), width=28).pack(pady=8)

        tk.Button(frame, text=self.get_text("register_btn"),
                  command=self.show_register_popup,
                  bg="#6366f1", fg="white",
                  font=("Arial", 11, "bold"), width=28).pack(pady=8)

        tk.Button(frame, text=self.get_text("leaderboard_btn"),
                  command=self.show_leaderboard,
                  bg="#ec4899", fg="white",
                  font=("Arial", 11, "bold"), width=28).pack(pady=8)

    # --------------------------------------------------------
    # REGISTRATION POPUP
    # --------------------------------------------------------
    def show_register_popup(self):
        win = tk.Toplevel(self.root)
        win.title("Register")
        win.geometry("400x300")
        win.configure(bg="#1e293b")

        tk.Label(win, text="Create Account", font=("Arial", 18, "bold"),
                 fg="white", bg="#1e293b").pack(pady=10)

        tk.Label(win, text="Username:", fg="white", bg="#1e293b").pack()
        u_ent = tk.Entry(win, font=("Arial", 14))
        u_ent.pack(pady=5)

        tk.Label(win, text="Password:", fg="white", bg="#1e293b").pack()
        p_ent = tk.Entry(win, show="*", font=("Arial", 14))
        p_ent.pack(pady=5)

        def register_user():
            u = u_ent.get()
            p = p_ent.get()

            if not u or not p:
                messagebox.showerror("Error", "Fields cannot be empty!")
                return

            hp = hashlib.sha256(p.encode()).hexdigest()
            try:
                conn = sqlite3.connect("mega_quiz.db")
                c = conn.cursor()
                c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (u, hp))
                conn.commit()
                conn.close()
                messagebox.showinfo("Success", "Account created!")
                win.destroy()
            except:
                messagebox.showerror("Error", "Username already exists!")

        tk.Button(win, text="Create", command=register_user,
                  bg="#10b981", fg="white",
                  font=("Arial", 12, "bold"), width=20).pack(pady=15)

    # --------------------------------------------------------
    # WELCOME POPUP
    # --------------------------------------------------------
    def show_welcome_popup(self, username):
        popup = tk.Toplevel(self.root)
        popup.title("Welcome")
        popup.geometry("350x200")
        popup.configure(bg="#1e293b")

        tk.Label(popup, text="🎉 Welcome!", font=("Arial", 22, "bold"),
                 fg="#60a5fa", bg="#1e293b").pack(pady=15)

        tk.Label(popup, text=username, font=("Arial", 18),
                 fg="#22c55e", bg="#1e293b").pack()

        popup.after(2000, popup.destroy)

    # --------------------------------------------------------
    # DIFFICULTY SELECTION
    # --------------------------------------------------------
    def show_difficulty_screen(self):
        self.clear_screen()

        frame = tk.Frame(self.main_container, bg="#1e293b", padx=40, pady=40)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        tk.Label(frame, text=self.get_text("difficulty_title"),
                 font=("Segoe UI", 22, "bold"),
                 fg="#60a5fa", bg="#1e293b").pack(pady=20)

        diffs = [("Easy", "#22c55e"), ("Medium", "#fbbf24"), ("Hard", "#ef4444"), ("Mixed", "#8b5cf6")]

        for d, col in diffs:
            tk.Button(frame, text=d,
                      command=lambda x=d: self.start_quiz_with_difficulty(x),
                      bg=col, fg="white",
                      font=("Arial", 14, "bold"),
                      width=25).pack(pady=7)

    def start_quiz_with_difficulty(self, difficulty):
        if difficulty == "Mixed":
            self.questions = random.sample(self.all_questions, min(20, len(self.all_questions)))
        else:
            self.questions = [q for q in self.all_questions if q["d"] == difficulty][:20]

        random.shuffle(self.questions)
        self.show_quiz_screen()

    # --------------------------------------------------------
    # QUIZ SCREEN (WITH NEXT BUTTON)
    # --------------------------------------------------------
    def show_quiz_screen(self):
        self.clear_screen()

        self.current_q_idx = 0
        self.score = 0
        self.answered_questions = []
        self.skipped_questions = []
        self.is_quiz_active = True
        self.start_timestamp = time.time()

        # HEADER
        header = tk.Frame(self.main_container, bg="#1e293b", height=80)
        header.pack(fill="x")

        tk.Label(header, text=f"{self.get_text('examinee')} {self.current_user}",
                 fg="#60a5fa", bg="#1e293b", font=("Arial", 14, "bold")).place(x=20, y=20)

        self.timer_label = tk.Label(header, text="⏱ 20:00",
                                    fg="#22c55e", bg="#1e293b",
                                    font=("Courier", 24, "bold"))
        self.timer_label.place(x=800, y=20)

        # QUESTION FRAME
        q_frame = tk.Frame(self.main_container, bg="#0a0e27")
        q_frame.pack(fill="both", expand=True, pady=10)

        self.q_label = tk.Label(q_frame, text="", fg="white",
                                bg="#0a0e27", font=("Arial", 18, "bold"),
                                wraplength=800, justify="left")
        self.q_label.pack(pady=30)

        self.var = tk.StringVar()

        # OPTION BUTTONS
        self.opt_btns = []
        for _ in range(4):
            rb = tk.Radiobutton(q_frame, text="", variable=self.var, value="",
                                font=("Arial", 16), bg="#0a0e27", fg="white",
                                selectcolor="#1e293b", cursor="hand2",
                                anchor="w", padx=20, pady=10)
            rb.pack(fill="x", padx=100, pady=5)
            self.opt_btns.append(rb)

        # CONTROL BUTTONS FRAME
        btn_frame = tk.Frame(self.main_container, bg="#1e293b")
        btn_frame.pack(pady=10)

        self.submit_btn = tk.Button(btn_frame, text="Submit",
                                    command=self.process_answer,
                                    bg="#22c55e", fg="white",
                                    font=("Arial", 14, "bold"), width=14)
        self.submit_btn.pack(side="left", padx=10)

        self.skip_btn = tk.Button(btn_frame, text="Skip",
                                  command=self.skip_question,
                                  bg="#64748b", fg="white",
                                  font=("Arial", 14, "bold"), width=14)
        self.skip_btn.pack(side="left", padx=10)

        # ⭐ NEXT BUTTON ⭐ (initially hidden)
        self.next_btn = tk.Button(btn_frame, text="➡ NEXT",
                                  command=self.go_next_question,
                                  bg="#3b82f6", fg="white",
                                  font=("Arial", 14, "bold"), width=14)
        # self.next_btn.pack only AFTER answer is submitted

        self.finish_btn = tk.Button(btn_frame, text="Finish Quiz",
                                    command=self.confirm_finish,
                                    bg="#ef4444", fg="white",
                                    font=("Arial", 14, "bold"), width=14)
        self.finish_btn.pack(side="left", padx=10)

        self.load_question()
        self.update_main_timer()

    # --------------------------------------------------------
    # QUESTION LOGIC
    # --------------------------------------------------------
    def load_question(self):
        if self.current_q_idx >= len(self.questions):
            return self.end_quiz()

        self.next_btn.pack_forget()

        q = self.questions[self.current_q_idx]
        self.q_label.config(text=f"Q{self.current_q_idx+1}:  {q['q']}")

        for i, opt in enumerate(q["o"]):
            self.opt_btns[i].config(text=f"{chr(65+i)}. {opt}", value=opt)

        self.var.set(None)

    def process_answer(self):
        choice = self.var.get()
        if not choice:
            messagebox.showwarning("Warning", "Please select an answer!")
            return

        correct = self.questions[self.current_q_idx]["a"]
        if choice == correct:
            self.score += 1

        self.answered_questions.append(self.current_q_idx)

        # SHOW NEXT BUTTON
        self.next_btn.pack(side="left", padx=10)

    def skip_question(self):
        self.skipped_questions.append(self.current_q_idx)
        self.current_q_idx += 1
        self.load_question()

    def go_next_question(self):
        self.current_q_idx += 1
        self.load_question()

    # --------------------------------------------------------
    # TIMER
    # --------------------------------------------------------
    def update_main_timer(self):
        if not self.is_quiz_active:
            return

        elapsed = int(time.time() - self.start_timestamp)
        remaining = self.total_time - elapsed

        if remaining <= 0:
            self.end_quiz(timeout=True)
            return

        mins, secs = divmod(remaining, 60)
        self.timer_label.config(text=f"⏱ {mins:02d}:{secs:02d}")

        self.root.after(1000, self.update_main_timer)

    # --------------------------------------------------------
    # QUIZ FINISH
    # --------------------------------------------------------
    def confirm_finish(self):
        self.end_quiz()

    def end_quiz(self, timeout=False):
        self.is_quiz_active = False

        percentage = (self.score / len(self.questions)) * 100

        if percentage >= 80:
            grade = "A+"
        elif percentage >= 70:
            grade = "A"
        elif percentage >= 60:
            grade = "B"
        elif percentage >= 50:
            grade = "C"
        else:
            grade = "F"

        messagebox.showinfo("Result",
                            f"Score: {self.score}/{len(self.questions)}\n"
                            f"Percentage: {percentage:.1f}%\n"
                            f"Grade: {grade}")

        self.show_login_screen()

    # --------------------------------------------------------
    # LEADERBOARD
    # --------------------------------------------------------
    def show_leaderboard(self):
        win = tk.Toplevel(self.root)
        win.geometry("600x450")
        win.title("Leaderboard")

        tree = ttk.Treeview(win, columns=("User", "Score", "Time"), show="headings")
        tree.heading("User", text="Username")
        tree.heading("Score", text="Score")
        tree.heading("Time", text="Time Taken")
        tree.pack(fill="both", expand=True)

        conn = sqlite3.connect("mega_quiz.db")
        c = conn.cursor()
        c.execute("SELECT username, score, time_taken FROM scores ORDER BY score DESC")
        for row in c.fetchall():
            tree.insert("", "end", values=row)
        conn.close()

    # --------------------------------------------------------
    # LOGIN HANDLER
    # --------------------------------------------------------
    def handle_login(self):
        user = self.user_ent.get()
        passwd = self.pass_ent.get()

        hp = hashlib.sha256(passwd.encode()).hexdigest()

        conn = sqlite3.connect("mega_quiz.db")
        c = conn.cursor()
        c.execute("SELECT username FROM users WHERE username=? AND password=?", (user, hp))
        result = c.fetchone()
        conn.close()

        if result:
            self.current_user = user
            self.show_welcome_popup(user)
            self.root.after(2000, self.show_difficulty_screen)
        else:
            messagebox.showerror("Error", "Invalid username or password!")


# -------------------------------------------------------------
# MAIN PROGRAM START
# -------------------------------------------------------------
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = MegaQuizApp(root)
    root.mainloop()