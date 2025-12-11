import random
import tkinter as tk
from tkinter import PhotoImage, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime

# ------------------ Log Page ------------------
class LogPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#EEEEEE")
        self.master = master
        self.exercise_log = []

        frame = tk.Frame(self,bg="#3838D5")
        frame.pack(side="top",fill="x")
        tk.Label(frame,text="Log",font=("Comic Sans MS",30,"bold"),bg="#3838D5",fg="black").pack(padx=10)

        self.activity_options = [
            "None", "Running", "Walking", "Cycling", "Swimming",
            "Weightlifting", "Yoga", "HIIT",
            "Arm", "Abs", "Leg", "Chest", "Back"
        ]
        self.log_tab(self)
        self.load_saved_logs()

    def log_tab(self, frames):
        #Frame container
        self.report_frame = tk.Frame(frames, bg="#EEEEEE")
        self.report_frame.pack(fill="both", expand=True, padx=10, pady=10)

        #-----Activity Type-----
        activity_frame = tk.Frame(self.report_frame, bg="#EEEEEE")
        activity_frame.pack(fill="x", pady=5)

        tk.Label(
            activity_frame, text="Activity Type:", bg="#EEEEEE", 
            font=("Consolas", 14, "bold"), width=15, anchor="w"
        ).pack(side="left")

        self.activity_options = [
            "None", "Running", "Walking", "Cycling", "Swimming",
            "Weightlifting", "Yoga", "HIIT",
            "Arm", "Abs", "Leg", "Chest", "Back"
        ]

        self.selected_activity = ttk.Combobox(
            activity_frame, values=self.activity_options, state="readonly", 
            width=20, font=("Arial", 13)
        )
        self.selected_activity.set("None")
        self.selected_activity.pack(side="left", padx=5)

        #-----Duration-----
        duration_frame = tk.Frame(self.report_frame, bg="#EEEEEE")
        duration_frame.pack(fill="x", pady=5)

        tk.Label(
            duration_frame, text="Duration     :", bg="#EEEEEE", 
            font=("Consolas", 14, "bold"), width=15, anchor="w"
        ).pack(side="left")

        self.hour_combo = ttk.Combobox(
            duration_frame, values=[f"{i:02d}" for i in range(24)],
            width=3, state="disabled", font=("Arial", 13)
        )
        self.hour_combo.set("00")
        self.hour_combo.pack(side="left", padx=(0,2))
        tk.Label(duration_frame, text="H", bg="#EEEEEE", font=("Arial", 13)).pack(side="left")

        self.minute_combo = ttk.Combobox(
            duration_frame, values=[f"{i:02d}" for i in range(1,60)],
            width=3, state="disabled", font=("Arial", 13)
        )
        self.minute_combo.set("01")
        self.minute_combo.pack(side="left", padx=(5,2))
        tk.Label(duration_frame, text="M", bg="#EEEEEE", font=("Arial", 13)).pack(side="left")

        #-----Intensity-----
        intensity_frame = tk.Frame(self.report_frame, bg="#EEEEEE")
        intensity_frame.pack(fill="x", pady=5)

        tk.Label(
            intensity_frame, text="Intensity    :", bg="#EEEEEE", 
            font=("Consolas", 14, "bold"), width=15, anchor="w"
        ).pack(side="left")

        self.standard_intensity = ["Low", "Medium", "High"]
        self.bodypart_intensity = ["Beginner", "Intermediate", "Advanced"]

        self.selected_intensity = ttk.Combobox(
            intensity_frame, values=[], state="disabled", width=20, font=("Arial", 13)
        )
        self.selected_intensity.pack(side="left", padx=5)

        #-----Record Button-----
        self.record_btn = ctk.CTkButton(
            self.report_frame, text="Record",hover_color="#6767FF", fg_color="#3838D5", text_color="#FFFFFF", 
            command=self.record_exercise, state="disabled", font=("Consolas", 20, "bold")
        )
        self.record_btn.pack(pady=10)

        #-----Log Display-----
        self.report_display = tk.Text(self.report_frame, width=40, height=15, font=("Arial", 12))
        self.report_display.pack(side="left", fill="both", expand=True, pady=10, padx=5)

        scrollbar = tk.Scrollbar(self.report_frame, command=self.report_display.yview)
        scrollbar.pack(side="right", fill="y")
        self.report_display.config(yscrollcommand=scrollbar.set)

        #Storage
        self.exercise_log = []

        #-----Functions for enabling/disabling inputs-----
        def update_intensity_options():
            act = self.selected_activity.get()
            if act in ["Arm", "Abs", "Leg", "Chest", "Back"]:
                self.selected_intensity.config(values=self.bodypart_intensity, state="readonly")
                self.selected_intensity.set(self.bodypart_intensity[0])
            elif act == "None":
                self.selected_intensity.set("")
                self.selected_intensity.config(values=[], state="disabled")
            else:
                self.selected_intensity.config(values=self.standard_intensity, state="readonly")
                self.selected_intensity.set(self.standard_intensity[0])

        def update_duration_state():
            if self.selected_activity.get() == "None":
                self.hour_combo.config(state="disabled")
                self.minute_combo.config(state="disabled")
            else:
                self.hour_combo.config(state="readonly")
                self.minute_combo.config(state="readonly")

        def update_record_button():
            if self.selected_activity.get() == "None":
                self.record_btn.configure(state="disabled")
            else:
                self.record_btn.configure(state="normal")

        #Bind activity change
        self.selected_activity.bind(
            "<<ComboboxSelected>>", 
            lambda e: [
                update_intensity_options(),
                update_record_button(),
                update_duration_state()
            ]
        )

    def record_exercise(self):
            # Get selected activity and intensity
            activity = self.selected_activity.get()
            intensity = self.selected_intensity.get().lower()

            # Get hours and minutes
            hours = int(self.hour_combo.get())
            minutes = int(self.minute_combo.get())

            # Get time now
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Save record in memory
            record = {
                "activity": activity,
                "hours": hours,
                "minutes": minutes,
                "intensity": intensity.title(),
                "date": timestamp  
            }
            self.exercise_log.append(record)

            #---- Write to text file WITH USERNAME + DATE/TIME ----
            current_user = self.master.current_user
            
            try:
                with open("workout_records.txt", "a", encoding="utf-8") as f:
                    # Format: USERNAME \t DATETIME \t ACTIVITY \t DURATION \t INTENSITY
                    f.write(
                        f"{current_user}\t{timestamp}\t{activity}\t{hours:02d}H {minutes:02d}M\t{intensity.title()}\n"
                    )
            except Exception as e:
                print("Error writing workout log:", e)

            # Update report on screen
            self.update_report_display()

    def update_report_display(self):
        self.report_display.config(state="normal")
        self.report_display.delete("1.0", "end")

        #Change font of all log records (Consolas, size -2)
        self.report_display.configure(font=("Consolas", 11))

        #Title
        title = "Workout Records"
        self.report_display.insert("end", f"{title:^35}", "title")
        self.report_display.insert("end", "_" * 40 + "\n")

        #Icons
        activity_icons = {
            "running": "🏃‍♂️",
            "walking": "🚶‍♂️",
            "cycling": "🚴‍♂️",
            "swimming": "🏊‍♂️",
            "weightlifting": "🏋️‍♂️",
            "yoga": "🧘‍♂️",
            "hiit": "💪",
            "arm": "💪",
            "abs": "💥",
            "leg": "🦵",
            "chest": "🏋️",
            "back": "🛡️"
        }

        #Format logs in aligned columns
        for i, item in enumerate(self.exercise_log, start=1):
            icon = activity_icons.get(item['activity'].lower(), "⚡")
            line = (f"{i:>3}. " f"{item['activity']:<13}  " f"{item['hours']:02d}H {item['minutes']:02d}M  " f"{item['intensity']:<12}\n")
            self.report_display.insert("end", line)

        #Styling
        self.report_display.tag_config(
            "title",
            font=("Consolas", 15, "bold")
        )

        self.report_display.config(state="disabled")

    def load_saved_logs(self):
            self.exercise_log = [] # Clear existing logs in memory first
            current_user = self.master.current_user

            try:
                with open("workout_records.txt", "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line:
                            continue

                        # File format: Username \t Date \t Activity \t Duration \t Intensity
                        parts = [x.strip() for x in line.split("\t")]

                        # Only load if the Username (part[0]) matches the current user
                        if len(parts) >= 5 and parts[0] == current_user:
                            # parts[1] is datetime (Now we capture it for Report filtering)
                            date_str = parts[1] 
                            activity = parts[2]
                            duration = parts[3]
                            intensity = parts[4]

                            try:
                                # Parse "01H 30M"
                                hours = int(duration.split("H")[0])
                                minutes = int(duration.split("H")[1].replace("M", "").strip())
                                
                                self.exercise_log.append({
                                    "activity": activity, 
                                    "hours": hours, 
                                    "minutes": minutes, 
                                    "intensity": intensity,
                                    "date": date_str  # Store the date in memory
                                })
                            except:
                                pass # Skip badly formatted lines

                # Update the on-screen display after loading
                self.update_report_display()

            except FileNotFoundError:
                pass

