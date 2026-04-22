import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
import threading
import winsound
import random

class AlarmClock:
    def __init__(self, root):
        self.root = root
        self.root.title("Smart Alarm Clock")
        self.root.geometry("500x750")
        
        # RESIZABLE ENABLED
        self.root.resizable(True, True)
        
        self.root.configure(bg="#1a1a2e")
        
        self.alarms = []
        self.alarm_missions = {}
        self.alarm_sounds = {}
        self.running = True
        self.stop_alarm = False
        
        self.setup_ui()
        self.update_time()
        
    def setup_ui(self):
        # Title
        title_label = tk.Label(
            self.root,
            text="⏰ SMART ALARM",
            font=("Helvetica", 24, "bold"),
            bg="#1a1a2e",
            fg="#00d9ff"
        )
        title_label.pack(pady=15)
        
        # Current time display - LARGER
        self.time_frame = tk.Frame(self.root, bg="#16213e", bd=0)
        self.time_frame.pack(pady=10, padx=20, fill="x")
        
        self.time_label = tk.Label(
            self.time_frame,
            text="00:00:00",
            font=("Digital-7", 56, "bold"),
            bg="#16213e",
            fg="#00ff88"
        )
        self.time_label.pack(pady=15)
        
        self.date_label = tk.Label(
            self.time_frame,
            text="",
            font=("Helvetica", 13),
            bg="#16213e",
            fg="#aaaaaa"
        )
        self.date_label.pack(pady=(0, 15))
        
        # Set alarm section
        alarm_frame = tk.Frame(self.root, bg="#16213e", bd=0)
        alarm_frame.pack(pady=15, padx=20, fill="x")
        
        tk.Label(
            alarm_frame,
            text="Set New Alarm",
            font=("Helvetica", 15, "bold"),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=(10, 10))
        
        # Time input frame
        input_frame = tk.Frame(alarm_frame, bg="#16213e")
        input_frame.pack(pady=10)
        
        # Hour
        tk.Label(input_frame, text="Hour", font=("Helvetica", 11), bg="#16213e", fg="#aaaaaa").grid(row=0, column=0, padx=5)
        self.hour_var = tk.StringVar(value="00")
        self.hour_spin = tk.Spinbox(
            input_frame,
            from_=0,
            to=23,
            textvariable=self.hour_var,
            width=5,
            font=("Helvetica", 16, "bold"),
            format="%02.0f",
            bg="#0f3460",
            fg="#ffffff",
            buttonbackground="#16213e",
            relief="flat"
        )
        self.hour_spin.grid(row=1, column=0, padx=5)
        
        # Minute
        tk.Label(input_frame, text="Minute", font=("Helvetica", 11), bg="#16213e", fg="#aaaaaa").grid(row=0, column=1, padx=5)
        self.minute_var = tk.StringVar(value="00")
        self.minute_spin = tk.Spinbox(
            input_frame,
            from_=0,
            to=59,
            textvariable=self.minute_var,
            width=5,
            font=("Helvetica", 16, "bold"),
            format="%02.0f",
            bg="#0f3460",
            fg="#ffffff",
            buttonbackground="#16213e",
            relief="flat"
        )
        self.minute_spin.grid(row=1, column=1, padx=5)
        
        # Second
        tk.Label(input_frame, text="Second", font=("Helvetica", 11), bg="#16213e", fg="#aaaaaa").grid(row=0, column=2, padx=5)
        self.second_var = tk.StringVar(value="00")
        self.second_spin = tk.Spinbox(
            input_frame,
            from_=0,
           to=59,
            textvariable=self.second_var,
            width=5,
            font=("Helvetica", 16, "bold"),
            format="%02.0f",
            bg="#0f3460",
            fg="#ffffff",
            buttonbackground="#16213e",
            relief="flat"
        )
        self.second_spin.grid(row=1, column=2, padx=5)
        
        # Alarm Sound Selection
        tk.Label(
            alarm_frame,
            text="🎵 Alarm Sound",
            font=("Helvetica", 12, "bold"),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=(15, 5))
        
        self.sound_var = tk.StringVar(value="Default Beep")
        
        sound_frame = tk.Frame(alarm_frame, bg="#16213e")
        sound_frame.pack(pady=5)
        
        sounds = [
            ("Default Beep", "🔔"),
            ("Gentle Melody", "🎵"),
            ("Loud Siren", "🚨"),
            ("Nature Sounds", "🌿"),
            ("Custom Music", "🎧")
        ]
        
        for i, (sound, emoji) in enumerate(sounds):
            sound_btn = tk.Button(
                sound_frame,
                text=f"{emoji} {sound}",
                command=lambda s=sound: self.sound_var.set(s),
                font=("Helvetica", 9),
                bg="#0f3460",
                fg="#ffffff",
                activebackground="#00d9ff",
                activeforeground="#1a1a2e",
                relief="flat",
                cursor="hand2",
                width=14,
                pady=5
            )
            sound_btn.grid(row=i//2, column=i%2, padx=5, pady=3)
        
        self.selected_sound_label = tk.Label(
            alarm_frame,
            text="Selected: Default Beep",
            font=("Helvetica", 9, "italic"),
            bg="#16213e",
            fg="#aaaaaa"
        )
        self.selected_sound_label.pack(pady=5)
        
        # Update selected sound display
        def update_sound_display(*args):
            self.selected_sound_label.config(text=f"Selected: {self.sound_var.get()}")
        
        self.sound_var.trace('w', update_sound_display)
        
        # Mission selection
        tk.Label(
            alarm_frame,
            text="Wake-up Mission",
            font=("Helvetica", 12, "bold"),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=(15, 5))
        
        self.mission_var = tk.StringVar(value="Math Problem")
        missions = ["Math Problem", "Typing Challenge", "Memory Puzzle", "Simple Question"]
        
        mission_frame = tk.Frame(alarm_frame, bg="#16213e")
        mission_frame.pack(pady=5)
        
        for mission in missions:
            rb = tk.Radiobutton(
                mission_frame,
                text=mission,
                variable=self.mission_var,
                value=mission,
                font=("Helvetica", 10),
                bg="#16213e",
                fg="#ffffff",
                selectcolor="#0f3460",
                activebackground="#16213e",
                activeforeground="#00d9ff"
            )
            rb.pack(anchor="w", padx=20, pady=2)
        
        # Add alarm button
        add_btn = tk.Button(
            alarm_frame,
            text="➕ Add Alarm with Mission",
            command=self.add_alarm,
            font=("Helvetica", 13, "bold"),
            bg="#00d9ff",
            fg="#1a1a2e",
            activebackground="#00b8d4",
            relief="flat",
            cursor="hand2",
            padx=20,
            pady=10
        )
        add_btn.pack(pady=15)
        
        # Alarms list
        list_frame = tk.Frame(self.root, bg="#16213e", bd=0)
        list_frame.pack(pady=10, padx=20, fill="both", expand=True)
        
        tk.Label(
            list_frame,
            text="Active Alarms",
            font=("Helvetica", 13, "bold"),
            bg="#16213e",
            fg="#ffffff"
        ).pack(pady=(10, 5))
        
        # Scrollable alarm list
        canvas_frame = tk.Frame(list_frame, bg="#16213e")
        canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.alarm_listbox = tk.Listbox(
            canvas_frame,
            font=("Helvetica", 11),
            bg="#0f3460",
            fg="#ffffff",
            selectbackground="#00d9ff",
            selectforeground="#1a1a2e",
            relief="flat",
            height=5
        )
        self.alarm_listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = tk.Scrollbar(canvas_frame, command=self.alarm_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.alarm_listbox.config(yscrollcommand=scrollbar.set)
        
        # Delete button
        delete_btn = tk.Button(
            list_frame,
            text="🗑️ Delete Selected",
            command=self.delete_alarm,
            font=("Helvetica", 11),
            bg="#e94560",
            fg="#ffffff",
            activebackground="#d63447",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8
        )
        delete_btn.pack(pady=(5, 10))
        
    def update_time(self):
        if self.running:
            now = datetime.now()
            time_string = now.strftime("%H:%M:%S")
            date_string = now.strftime("%A, %B %d, %Y")
            
            self.time_label.config(text=time_string)
            self.date_label.config(text=date_string)
            
            self.check_alarms(time_string)
            
            self.root.after(1000, self.update_time)
    
    def add_alarm(self):
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            second = int(self.second_var.get())
            
            alarm_time = f"{hour:02d}:{minute:02d}:{second:02d}"
            mission = self.mission_var.get()
            sound = self.sound_var.get()
            
            if alarm_time in self.alarms:
                messagebox.showwarning("Duplicate", "This alarm already exists!")
                return
            self.alarms.append(alarm_time)
            self.alarm_missions[alarm_time] = mission
            self.alarm_sounds[alarm_time] = sound
            self.alarm_listbox.insert(tk.END, f"  ⏰ {alarm_time} | {mission} | {sound}")
            messagebox.showinfo("Success", f"Alarm set for {alarm_time}\nMission: {mission}\nSound: {sound}")
            
        except ValueError:
            messagebox.showerror("Error", "Please enter valid time values!")
    
    def delete_alarm(self):
        try:
            selected = self.alarm_listbox.curselection()
            if selected:
                index = selected[0]
                alarm_time = self.alarms[index]
                self.alarms.pop(index)
                del self.alarm_missions[alarm_time]
                del self.alarm_sounds[alarm_time]
                self.alarm_listbox.delete(index)
                messagebox.showinfo("Deleted", f"Alarm {alarm_time} deleted!")
            else:
                messagebox.showwarning("No Selection", "Please select an alarm to delete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def check_alarms(self, current_time):
        if current_time in self.alarms:
            mission = self.alarm_missions[current_time]
            sound = self.alarm_sounds[current_time]
            self.trigger_alarm(current_time, mission, sound)
    
    def trigger_alarm(self, alarm_time, mission, sound):
        # Remove the triggered alarm
        if alarm_time in self.alarms:
            index = self.alarms.index(alarm_time)
            self.alarms.pop(index)
            del self.alarm_missions[alarm_time]
            del self.alarm_sounds[alarm_time]
            self.alarm_listbox.delete(index)
        
        # Show mission window
        self.show_mission_window(alarm_time, mission, sound)
    
    def show_mission_window(self, alarm_time, mission, sound):
        # Create popup window
        self.alarm_window = tk.Toplevel(self.root)
        self.alarm_window.title("⏰ WAKE UP!")
        self.alarm_window.geometry("450x400")
        
        # RESIZABLE WINDOW ENABLED
        self.alarm_window.resizable(True, True)
        
        self.alarm_window.configure(bg="#e94560")
        self.alarm_window.resizable(True, True)
        self.alarm_window.attributes('-topmost', True)
        
        # Start sound based on selection
        self.stop_alarm = False
        self.current_sound = sound
        sound_thread = threading.Thread(target=self.play_alarm_sound, daemon=True)
        sound_thread.start()
        
        # Header
        tk.Label(
            self.alarm_window,
            text="⏰ ALARM!",
            font=("Helvetica", 32, "bold"),
            bg="#e94560",
            fg="#ffffff"
        ).pack(pady=20)
        
        tk.Label(
            self.alarm_window,
            text=f"Time: {alarm_time}",
            font=("Helvetica", 14),
            bg="#e94560",
            fg="#ffffff"
        ).pack(pady=5)
        
        # Mission content frame
        mission_frame = tk.Frame(self.alarm_window, bg="#ffffff", bd=0)
        mission_frame.pack(pady=20, padx=30, fill="both", expand=True)
        
        if mission == "Math Problem":
            self.show_math_mission(mission_frame)
        elif mission == "Typing Challenge":
            self.show_typing_mission(mission_frame)
        elif mission == "Memory Puzzle":
            self.show_memory_mission(mission_frame)
        elif mission == "Simple Question":
            self.show_question_mission(mission_frame)
        
        # Flash effect
        self.flash_window(self.alarm_window)
    
    def show_math_mission(self, frame):
        num1 = random.randint(10, 50)
        num2 = random.randint(10, 50)
        operation = random.choice(['+', '-', '*'])
        
        if operation == '+':
            self.correct_answer = num1 + num2
        elif operation == '-':
            self.correct_answer = num1 - num2
        else:
            self.correct_answer = num1 * num2
        
        tk.Label(
            frame,
            text="Solve to Stop Alarm:",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=15)
        
        tk.Label(
            frame,
            text=f"{num1} {operation} {num2} = ?",
            font=("Helvetica", 28, "bold"),
            bg="#ffffff",
            fg="#e94560"
        ).pack(pady=20)
        
        self.answer_entry = tk.Entry(
            frame,
            font=("Helvetica", 20),
            justify="center",
            bg="#f0f0f0",
            fg="#333333",
            relief="flat",
            width=10
        )
        self.answer_entry.pack(pady=15)
        self.answer_entry.focus()
        
        submit_btn = tk.Button(
            frame,
            text="Submit Answer",
            command=lambda: self.check_math_answer(),
            font=("Helvetica", 12, "bold"),
            bg="#00d9ff",
            fg="#ffffff",
            activebackground="#00b8d4",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10
        )
        submit_btn.pack(pady=10)
        
        self.answer_entry.bind('<Return>', lambda e: self.check_math_answer())
    
    def show_typing_mission(self, frame):
        sentences = [
            "The quick brown fox jumps over the lazy dog",
            "Practice makes perfect every single day",
            "Wake up and seize the wonderful day ahead",
            "Early bird catches the worm always"
        ]
        self.target_text = random.choice(sentences)
        
        tk.Label(
            frame,
            text="Type this exactly:",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=15)
        
        tk.Label(
            frame,
            text=self.target_text,
            font=("Helvetica", 14),
            bg="#f0f0f0",
            fg="#e94560",
            wraplength=350,
            padx=10,
            pady=10
        ).pack(pady=15)
        
        self.answer_entry = tk.Entry(
            frame,
            font=("Helvetica", 12),
            bg="#f0f0f0",
            fg="#333333",
            relief="flat",
            width=35
        )
        self.answer_entry.pack(pady=15, padx=10)
        self.answer_entry.focus()
        
        submit_btn = tk.Button(
            frame,
            text="Submit",
            command=lambda: self.check_typing_answer(),
            font=("Helvetica", 12, "bold"),
            bg="#00d9ff",
            fg="#ffffff",
            activebackground="#00b8d4",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10
        )
        submit_btn.pack(pady=10)
        
        self.answer_entry.bind('<Return>', lambda e: self.check_typing_answer())
    
    def show_memory_mission(self, frame):
        self.memory_sequence = [random.randint(1, 9) for _ in range(5)]
        sequence_str = " ".join(map(str, self.memory_sequence))
        
        tk.Label(
            frame,
            text="Memorize these numbers:",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=15)
        
        number_label = tk.Label(
            frame,
            text=sequence_str,
            font=("Helvetica", 32, "bold"),
            bg="#ffffff",
            fg="#e94560"
        )
        number_label.pack(pady=20)
        
        # Hide after 3 seconds
        def hide_numbers():
            number_label.config(text="???")
            self.answer_entry.config(state="normal")
            self.answer_entry.focus()
        
        self.alarm_window.after(3000, hide_numbers)
        
        tk.Label(
            frame,
            text="Enter the numbers:",
            font=("Helvetica", 12),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=10)
        
        self.answer_entry = tk.Entry(
            frame,
            font=("Helvetica", 18),
            justify="center",
            bg="#f0f0f0",
            fg="#333333",
            relief="flat",
            width=15,
            state="disabled"
        )
        self.answer_entry.pack(pady=10)
        
        submit_btn = tk.Button(
            frame,
            text="Submit",
            command=lambda: self.check_memory_answer(),
            font=("Helvetica", 12, "bold"),
            bg="#00d9ff",
            fg="#ffffff",
            activebackground="#00b8d4",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10
        )
        submit_btn.pack(pady=10)
        
        self.answer_entry.bind('<Return>', lambda e: self.check_memory_answer())
    
    def show_question_mission(self, frame):
        questions = [
            ("What is the capital of France?", "paris"),
            ("How many continents are there?", "7"),
            ("What color do you get mixing blue and yellow?", "green"),
            ("How many days in a week?", "7"),
            ("What is 10 x 10?", "100")
        ]
        
        self.current_question = random.choice(questions)
        
        tk.Label(
            frame,
            text="Answer this question:",
            font=("Helvetica", 14, "bold"),
            bg="#ffffff",
            fg="#333333"
        ).pack(pady=15)
        
        tk.Label(
            frame,
            text=self.current_question[0],
            font=("Helvetica", 16),
            bg="#ffffff",
            fg="#e70027",
            wraplength=350
        ).pack(pady=20)
        
        self.answer_entry = tk.Entry(
            frame,
            font=("Helvetica", 16),
            justify="center",
            bg="#f0f0f0",
            fg="#333333",
            relief="flat",
            width=20
        )
        self.answer_entry.pack(pady=15)
        self.answer_entry.focus()
        
        submit_btn = tk.Button(
            frame,
            text="Submit Answer",
            command=lambda: self.check_question_answer(),
            font=("Helvetica", 12, "bold"),
            bg="#00d9ff",
            fg="#ffffff",
            activebackground="#00b8d4",
            relief="flat",
            cursor="hand2",
            padx=30,
            pady=10
        )
        submit_btn.pack(pady=10)
        
        self.answer_entry.bind('<Return>', lambda e: self.check_question_answer())
    
    def check_math_answer(self):
        try:
            user_answer = int(self.answer_entry.get())
            if user_answer == self.correct_answer:
                self.stop_alarm = True
                self.alarm_window.destroy()
                messagebox.showinfo("Success!", "Correct! Alarm stopped.")
            else:
                messagebox.showerror("Wrong!", "Try again!")
                self.answer_entry.delete(0, tk.END)
        except:
            messagebox.showerror("Invalid", "Enter a valid number!")
    
    def check_typing_answer(self):
        user_text = self.answer_entry.get()
        if user_text == self.target_text:
            self.stop_alarm = True
            self.alarm_window.destroy()
            messagebox.showinfo("Success!", "Perfect! Alarm stopped.")
        else:
            messagebox.showerror("Wrong!", "Type it exactly as shown!")
            self.answer_entry.delete(0, tk.END)
    
    def check_memory_answer(self):
        user_answer = self.answer_entry.get().replace(" ", "")
        correct_answer = "".join(map(str, self.memory_sequence))
        if user_answer == correct_answer:
            self.stop_alarm = True
            self.alarm_window.destroy()
            messagebox.showinfo("Success!", "Correct! Alarm stopped.")
        else:
            messagebox.showerror("Wrong!", "Try to remember again!")
            self.answer_entry.delete(0, tk.END)
    
    def check_question_answer(self):
        user_answer = self.answer_entry.get().strip().lower()
        correct_answer = self.current_question[1].lower()
        if user_answer == correct_answer:
            self.stop_alarm = True
            self.alarm_window.destroy()
            messagebox.showinfo("Success!", "Correct! Alarm stopped.")
        else:
            messagebox.showerror("Wrong!", "Try again!")
            self.answer_entry.delete(0, tk.END)
    
    def flash_window(self, window):
        try:
            current_color = window.cget("bg")
            new_color = "#ffffff" if current_color == "#e94560" else "#e94560"
            window.configure(bg=new_color)
            if not self.stop_alarm and window.winfo_exists():
                window.after(500, lambda: self.flash_window(window))
        except:
            pass
    
    def play_alarm_sound(self):
        try:
            sound_type = self.current_sound
            
            if sound_type == "Default Beep":
                # Original alternating beep
                while not self.stop_alarm:
                    winsound.Beep(1000, 400)
                    time.sleep(0.1)
                    if self.stop_alarm:
                        break
                    winsound.Beep(1200, 400)
                    time.sleep(0.1)
                    
            elif sound_type == "Gentle Melody":
                # Softer musical notes
                notes = [523, 587, 659, 698, 784]  # C, D, E, F, G
                while not self.stop_alarm:
                    for note in notes:
                        if self.stop_alarm:
                            break
                        winsound.Beep(note, 300)
                        time.sleep(0.1)
                        
            elif sound_type == "Loud Siren":
                # Loud alternating siren
                while not self.stop_alarm:
                    winsound.Beep(800, 300)
                    if self.stop_alarm:
                        break
                    winsound.Beep(1400, 300)
                    
            elif sound_type == "Nature Sounds":
                # Bird chirp simulation
                while not self.stop_alarm:
                    winsound.Beep(2000, 150)
                    time.sleep(0.1)
                    winsound.Beep(2500, 150)
                    time.sleep(0.5)
                    if self.stop_alarm:
                        break
                    winsound.Beep(2200, 150)
                    time.sleep(0.3)
                    
            elif sound_type == "Custom Music":
                # Continuous melodic pattern
                melody = [262, 294, 330, 349, 392, 440, 494, 523]
                while not self.stop_alarm:
                    for freq in melody:
                        if self.stop_alarm:
                            break
                        winsound.Beep(freq, 200)
                        time.sleep(0.05)
                    time.sleep(0.2)
                    
        except Exception as e:
            # Fallback for non-Windows or if winsound fails
            try:
                while not self.stop_alarm:
                    print('\a')  # System bell
                    time.sleep(0.5)
            except:
                pass
    
    def on_closing(self):
        self.running = False
        self.stop_alarm = True
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmClock(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()