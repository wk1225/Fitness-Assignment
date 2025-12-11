import random
import tkinter as tk
from tkinter import PhotoImage, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime

# ------------------ Plan Page ------------------
class PlanPage(tk.Frame):
    def __init__(self, master, selected_exercises,all_frames,selected_date):
        super().__init__(master, bg="#EEEEEE")
        self.master = master
        self.selected_exercises = selected_exercises
        self.selected_date = selected_date
        self.all_frames = all_frames
        self.other_photo=[] #used for storing png
        self.buttons = {}
        self.confirm_exercise =[]

        self.quotes =["No workout is wasted.",
            "Push yourself.",
            "Stay consistent.",
            "Stronger every day.",
            "Future you will smile.",
            "Progress is progress.",
            "Challenge brings change.",
            "One day at a time. ",
            "Be consistent, not extreme.",
            "Sweat it out.",
            "Make yourself proud.",
            "Finish what you start.",
            "Health is wealth.",
            "Discipline wins.",
            "Progress, not perfection.",
            "No excuses.",
            "Get off the couch.",
            "Train with purpose.",
            "You only need 1 hour.",
            "Believe, then achieve.",
            ]


        self.all_exercises = [
            "Arm Beginner","Arm Intermediate","Arm Advanced",
            "Abs Beginner","Belly Fat burner HIIT Beginner","Abs Intermediate","Abs Advanced",
            "Leg Beginner","Get Rid of Man Boobs HIIT","Leg Intermediate","Leg Advanced",
            "Chest Beginner","Chest Intermediate","Chest Advanced","Back Beginner","Back Intermediate"
            ,"Back Advanced","Fat Burning HIIT"
            ,"Killer Core HIIT Beginner","Lose Fat(No Jumping!)"
        ]
        self.day = [
            "Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday",
        ]

        #other page 里面的exercise
        self.other = ["Fat Burning HIIT","Killer Core HIIT Beginner","Get Rid of Man Boobs HIIT"
                      ,"Belly Fat burner HIIT Beginner","Lose Fat(No Jumping!)"]

        #other page exercise 的png
        self.imgOther = ["image/other_1.png","image/other_2.png","image/other_3.png",
             "image/other_4.png","image/other_5.png"]
        
        self.armImg =["Arm Beginner","Arm Intermediate","Arm Advanced"]
        self.arm_img =["image/arm1.png","image/arm2.png","image/arm3.png"]

        self.absImg =["Abs Beginner","Abs Intermediate","Abs Advanced"]
        self.abs_img =["image/abs1.png","image/abs2.png","image/abs3.png"]

        self.legImg =["Leg Beginner","Leg Intermediate","Leg Advanced"]
        self.leg_img =["image/leg1.png","image/leg2.png","image/leg3.png"]

        self.chestImg =["Chest Beginner","Chest Intermediate","Chest Advanced"]
        self.chest_img =["image/chest1.png","image/chest2.png","image/chest3.png"]

        self.backImg =["Back Beginner","Back Intermediate","Back Advanced"]
        self.back_img =["image/back1.png","image/back2.png","image/back3.png"]

        self.img_other =["image/other_0.png","image/record_0.png"]
        self.other_fun =[self.other_exercise,self.daily_plan]


        frame = tk.Frame(self,bg="#3838D5")
        frame.pack(side="top",fill="x")
        label2 = tk.Label(frame,text="Plan",font=("Comic Sans MS",30,"bold"),bg="#3838D5",fg="black")
        label2.pack(padx=10)
        self.create_top_buttons()
        self.image_frame = tk.Frame(self, bg="#EEEEEE")
        self.image_frame.pack(pady=10, padx=10)

        self.show_content("Arm")

    def create_top_buttons(self):
        self.subpage1 = tk.Frame(self, bg="#EEEEEE")
        self.subpage1.pack(fill="x", side="top")

        for name in ["Arm","Abs","Leg","Chest","Back"]:
            plan_but = ctk.CTkButton(self.subpage1,text=name,fg_color="#DDDDDD",text_color="#6767FF",hover_color="#6767FF",font=("Times New Roman",14,"bold"),corner_radius=50,width=60, height=35,command=lambda n=name:self.show_content(n))
            plan_but.pack(pady=10,side="left",padx=8,anchor="center",expand=True)
            self.buttons[name]=plan_but

    def show_content(self, name):
        for btn_name, btn in self.buttons.items():
            if btn_name == name:
                btn.configure(fg_color="#3838D5", text_color="#FFFFFF")
            else:
                btn.configure(fg_color="#CCCCCC", text_color="#181818",command=lambda n=btn_name: self.show_content(n))

        # Clear previous images
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        if name == "Arm":
            self.arm_image_d()
        elif name == "Abs":
            self.abs_image_d()
        elif name == "Leg":
            self.leg_image_d()
        elif name == "Chest":
            self.chest_image_d()
        elif name == "Back":
            self.back_image_d()

    def arm_image_d(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()
        
        for i,exer in enumerate(self.arm_img):
            img = Image.open(exer).resize((410,120))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.image_frame, image=other_img,bg="#FFFFFF")
            label.pack(pady=5)
            label.pack_propagate(False)

            button = ctk.CTkButton(label, fg_color="#3838D5",hover_color="#6767FF",text_color="#FBFBFB",corner_radius=60,text="Select",width=80,height=40)
            button.pack(side="bottom",anchor="se",pady=5,padx=10)

            button.bind("<Button-1>", lambda e, name=self.armImg[i]: self.ask_for_date(name))

        self.frame_bott = tk.Frame(self.image_frame,bg="#EEEEEE",height=300)
        self.frame_bott.pack(side="bottom",fill="both")

        for i,exer in enumerate(self.img_other):
            img = Image.open(exer).resize((200,100))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.frame_bott, image=other_img,)
            label.pack(pady=5,side="left")
            label.pack_propagate(False)
            label.bind("<Button-1>", lambda e, func=self.other_fun[i]: func())
        
    def abs_image_d(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        for i,exer in enumerate(self.abs_img):
            img = Image.open(exer).resize((410,120))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.image_frame, image=other_img,bg="#FFFFFF")
            label.pack(pady=5)
            label.pack_propagate(False)

            button = ctk.CTkButton(label, fg_color="#3838D5",hover_color="#6767FF",text_color="#FBFBFB",corner_radius=60,text="Select",width=80,height=40)
            button.pack(side="bottom",anchor="se",pady=5,padx=10)

            button.bind("<Button-1>", lambda e, name=self.absImg[i]: self.ask_for_date(name))

        self.frame_bott = tk.Frame(self.image_frame,bg="#EEEEEE",height=300)
        self.frame_bott.pack(side="bottom",fill="both")
        for i,exer in enumerate(self.img_other):
            img = Image.open(exer).resize((200,100))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.frame_bott, image=other_img,)
            label.pack(pady=5,side="left")
            label.pack_propagate(False)
            label.bind("<Button-1>", lambda e, func=self.other_fun[i]: func())

    def leg_image_d(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        for i,exer in enumerate(self.leg_img):
            img = Image.open(exer).resize((410,120))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.image_frame, image=other_img,bg="#FFFFFF")
            label.pack(pady=5)
            label.pack_propagate(False)

            button = ctk.CTkButton(label, fg_color="#3838D5",hover_color="#6767FF",text_color="#FBFBFB",corner_radius=60,text="Select",width=80,height=40)
            button.pack(side="bottom",anchor="se",pady=5,padx=10)

            button.bind("<Button-1>", lambda e, name=self.legImg[i]: self.ask_for_date(name))

        self.frame_bott = tk.Frame(self.image_frame,bg="#EEEEEE",height=300)
        self.frame_bott.pack(side="bottom",fill="both")
        for i,exer in enumerate(self.img_other):
            img = Image.open(exer).resize((200,100))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.frame_bott, image=other_img,)
            label.pack(pady=5,side="left")
            label.pack_propagate(False)
            label.bind("<Button-1>", lambda e, func=self.other_fun[i]: func())

    def chest_image_d(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        for i,exer in enumerate(self.chest_img):
            img = Image.open(exer).resize((410,120))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.image_frame, image=other_img,bg="#FFFFFF")
            label.pack(pady=5)
            label.pack_propagate(False)

            button = ctk.CTkButton(label, fg_color="#3838D5",hover_color="#6767FF",text_color="#FBFBFB",corner_radius=60,text="Select",width=80,height=40)
            button.pack(side="bottom",anchor="se",pady=5,padx=10)

            button.bind("<Button-1>", lambda e, name=self.chestImg[i]: self.ask_for_date(name))

        self.frame_bott = tk.Frame(self.image_frame,bg="#EEEEEE",height=300)
        self.frame_bott.pack(side="bottom",fill="both")
        for i,exer in enumerate(self.img_other):
            img = Image.open(exer).resize((200,100))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.frame_bott, image=other_img,)
            label.pack(pady=5,side="left")
            label.pack_propagate(False)
            label.bind("<Button-1>", lambda e, func=self.other_fun[i]: func())

    def back_image_d(self):
        for widget in self.image_frame.winfo_children():
            widget.destroy()

        for i,exer in enumerate(self.back_img):
            img = Image.open(exer).resize((410,120))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.image_frame, image=other_img,bg="#FFFFFF")
            label.pack(pady=5)
            label.pack_propagate(False)

            button = ctk.CTkButton(label, fg_color="#3838D5",hover_color="#6767FF",text_color="#FBFBFB",corner_radius=60,text="Select",width=80,height=40)
            button.pack(side="bottom",anchor="se",pady=5,padx=10)

            button.bind("<Button-1>", lambda e, name=self.backImg[i]: self.ask_for_date(name))

        self.frame_bott = tk.Frame(self.image_frame,bg="#EEEEEE",height=300)
        self.frame_bott.pack(side="bottom",fill="both")
        for i,exer in enumerate(self.img_other):
            img = Image.open(exer).resize((200,100))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.frame_bott, image=other_img,)
            label.pack(pady=5,side="left")
            label.pack_propagate(False)
            label.bind("<Button-1>", lambda e, func=self.other_fun[i]: func())

    def ask_for_date(self,name):
        ask_date = tk.Toplevel(self)
        ask_date.title("Message")
        ask_date.resizable(False, False)
        ask_date.config(bg="#FFFFFF")

        width, height = 250, 150 

        def update_position():
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()

            x = root_x + (root_width - width) // 2
            y = root_y + (root_height - height) // 2
            ask_date.geometry(f"{width}x{height}+{x}+{y}")

            if ask_date.winfo_exists():
                ask_date.after(1, update_position)

        update_position() 

        tk.Label(ask_date, text="Day : ",bg="#FFFFFF", fg="#3838D5", font=("Arial", 15,"bold")).pack(pady=10)
        self.selected_days = ttk.Combobox(ask_date, values=self.day, state="readonly", width=20, font=("Arial", 13))
        self.selected_days.set("None")
        self.selected_days.pack(side="top")

        def confirm_date():
            date = self.selected_days.get()
            if date == "None":
                self.error_msg("Cannot be \'None\'")
                return
            ask_date.destroy()
            self.select_exercise(name, date)
            
            
        select_but = ctk.CTkButton(ask_date, text="Select",hover_color="#6767FF", fg_color="#3838D5",command=confirm_date, text_color="#FFFFFF", width=90, height=40, corner_radius=60)
        select_but.pack(pady=15,side="bottom")

        ask_date.grab_set()
        ask_date.focus_set()
        ask_date.transient(self)
    
    def show_center_msg(self, msg):
        popup = tk.Toplevel(self)
        popup.title("Message")
        popup.resizable(False, False)

        width, height = 300, 150

        def update_position():
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()

            x = root_x + (root_width - width) // 2
            y = root_y + (root_height - height) // 2
            popup.geometry(f"{width}x{height}+{x}+{y}")
            if popup.winfo_exists():
                popup.after(1, update_position)

        update_position() 

        tk.Label(popup, text=msg, fg="#3838D5", font=("Arial", 15,"bold"),wraplength=250).pack(pady=10)
        ctk.CTkButton(popup, text="OK",hover_color="#6767FF", fg_color="#3838D5", text_color="#FFFFFF", command=popup.destroy, width=120,height=40,corner_radius=50).pack(pady=15)

        popup.grab_set()
        popup.focus_set()
        popup.transient(self)

    def error_msg(self, msg):
        popup = tk.Toplevel(self)
        popup.title("Error!!")
        popup.resizable(False, False)

        width, height = 300, 150 

        def update_position():
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()

            x = root_x + (root_width - width) // 2
            y = root_y + (root_height - height) // 2
            popup.geometry(f"{width}x{height}+{x}+{y}")

            if popup.winfo_exists():
                popup.after(1, update_position)

        update_position() 

        tk.Label(popup, text=msg, fg="#FF0000", font=("Arial", 15), wraplength=270).pack(pady=15)
        ctk.CTkButton(popup, text="OK",hover_color="#6767FF", fg_color="#3838D5", text_color="#FFFFFF", command=popup.destroy, width=120,height=40,corner_radius=50).pack(pady=20)

        popup.grab_set()
        popup.focus_set()
        popup.transient(self)

    def other_exercise(self):
    #display other exercise 的 function

        for widget in self.winfo_children():
            widget.destroy()
        self.master.nav_bar.pack_forget()

        self.frame_0 = tk.Frame(self,bg="#ADB0AD",height=130)
        self.frame_0.pack(fill="x",side="top")
        self.frame_0.pack_propagate(False)
        img = Image.open("image/other_6.png").resize((410,150))
        arm1 = ImageTk.PhotoImage(img)
        self.top_label = tk.Label(self.frame_0,image=arm1)
        self.top_label.image = arm1
        self.top_label.pack(side="top")
        self.back_but = ctk.CTkButton(self.top_label,text="<",text_color="#000000",fg_color="#AEB1AE",corner_radius=0,width=40,height=40,hover_color="#AEB1AE",font=("Consolas", 30, "bold"),cursor="hand2",command=self.go_back_to_plan)
        self.back_but.place(x=10,y=10)

        self.frame_1 = tk.Label(self,bg="#EEEEEE")
        self.frame_1.pack(fill="x",side="top")

        for i, exer in enumerate(self.imgOther):
            img = Image.open(exer).resize((380,100))
            other_img = ImageTk.PhotoImage(img)
            self.other_photo.append(other_img)

            label = tk.Label(self.frame_1, image=other_img,bg="#FFFFFF")
            label.pack(pady=5)
            label.pack_propagate(False)

            button = ctk.CTkButton(label, fg_color="#3838D5",hover_color="#6767FF",text_color="#FBFBFB",corner_radius=50,text="Select",width=70,height=30)
            button.pack(side="bottom",anchor="se",pady=5,padx=10)

            button.bind("<Button-1>", lambda e, name=self.other[i]: self.ask_for_date(name))

        self.frame_2 = tk.Frame(self,bg="#FBFBFB")
        self.frame_2.pack(side="top",fill="both")

    def select_exercise(self, name, date):
    #选exercise 的function
        exer_name = f"{date} - {name}"
        if len(self.confirm_exercise) >=10:
            self.error_msg("Maximum 10 exercises")
            return  
        elif exer_name in self.confirm_exercise:
            self.error_msg("Exercise already selected, cannot select again")
        else:
            self.confirm_exercise.append(exer_name)
            self.show_center_msg("Exercise have been saved in Training Plan!!") 

    def daily_plan(self):
    #被select的会在这边出现
        for widget in self.winfo_children():
            widget.destroy()
        self.master.nav_bar.pack_forget()

        self.frame_0 = tk.Frame(self,bg="#3838D5",height=75)
        self.frame_0.pack(fill="x",side="top")
        self.frame_0.pack_propagate(False)
        self.label_record = tk.Label(self.frame_0,bg="#3838D5",fg="#000000",text="Daily Plan",font=("Comic Sans MS",30))
        self.label_record.pack(pady=10)
        self.back_but = ctk.CTkButton(self.frame_0,corner_radius=20,text="<",hover_color="#3838D5",width=40,height=40,text_color="#000000",fg_color="#3838D5",font=("Consolas", 40, "bold"),cursor="hand2",command=self.go_back_to_plan)
        self.back_but.place(x=40,y=37,anchor="center")

        self.daily_plan_frame = tk.Frame(self,bg="#FFFFFF")
        self.daily_plan_frame.pack(fill="x")

        for widget in self.daily_plan_frame.winfo_children():
            widget.destroy()

        quote_label = tk.Label(self.daily_plan_frame,bg="#FFFFFF",fg="#3838D5",text=f"*{random.choice(self.quotes)}*", font=("Comic Sans MS",20,"bold"))
        quote_label.pack(anchor="center",pady=30)
        
        text_container = tk.Frame(self.daily_plan_frame, bg="#FFFFFF", width=380, height=350) 
        text_container.pack(fill="both", expand=True, pady=5)

        text_container.pack_propagate(False) 

        self.daily_plan_display = tk.Text(text_container, width=40, font=("Microsoft HaYei", 14,"bold"),fg="#000000",wrap=tk.WORD) 
        self.daily_plan_display.pack(side="left", fill="both", expand=True, pady=15, padx=5)

        scrollbar = tk.Scrollbar(text_container, command=self.daily_plan_display.yview)
        scrollbar.pack(side="right", fill="y", padx=(0, 5))
        self.daily_plan_display.config(yscrollcommand=scrollbar.set)
        self.daily_plan_display.delete("1.0", tk.END)
    
        if self.confirm_exercise:
            for ex in self.confirm_exercise:
                self.daily_plan_display.insert(tk.END, f"{ex}\n")
        else:
            self.daily_plan_display.insert(tk.END, "No exercise selected\n")

        self.daily_plan_display.config(state=tk.DISABLED)
            

        self.frame_2 = tk.Frame(self,bg="#FFFFFF",height=100)
        self.frame_2.pack(fill="both",side="bottom",expand=True)
        self.frame_2.pack_propagate(False)
        self.but_edit = ctk.CTkButton(self.frame_2,fg_color="#3838D5",hover_color="#6767FF",text_color="#FBFBFB",text="Edit",font=("Comic Sans MS",20,"bold"),corner_radius=60,width=120,height=60)
        self.but_edit.pack(side="bottom",pady=35)
        self.but_edit.bind("<Button-1>",lambda e:self.edit_exr())
        
    def edit_exr(self):
    #用户可以edit，delete, add

        self.frame_0.pack_forget()
        self.daily_plan_frame.pack_forget()
        self.frame_2.pack_forget()

        self.manage_frame = tk.Frame(self, bg="#FFFFFF")
        self.manage_frame.pack(fill="both", expand=True)

        self.top_bar = tk.Frame(self.manage_frame,bg="#3838D5",height=75)
        self.top_bar.pack(fill="x")
        self.top_bar.pack_propagate(False)
        self.back_but = ctk.CTkButton(self.top_bar,corner_radius=20,text="<",hover_color="#3838D5",width=40,height=40,text_color="#000000",fg_color="#3838D5",font=("Consolas", 40, "bold"),cursor="hand2",command=self.back_to_plan)
        self.back_but.place(x=40,y=37,anchor="center")
        self.top_label = tk.Label(self.top_bar,bg="#3838D5",fg="#000000",font=("Comic Sans MS",30),text="Daily Plan")
        self.top_label.pack(pady=10)
        self.exercise_frame = tk.Frame(self.manage_frame, bg="#FFFFFF",height=100)
        self.exercise_frame.pack(fill="x", pady=5,side="top")

        self.daylabel = tk.Label(self.exercise_frame, text="Day : ", font=("Arial", 13,"bold"), bg="#FFFFFF")
        self.daylabel.place(x=60,y=20)
        self.selected_days = ttk.Combobox(
            self.exercise_frame, values=self.day, state="readonly", 
            width=20, font=("Arial", 13)
        )
        self.selected_days.set("None")
        self.selected_days.place(x=110,y=20)

        self.daylabel = tk.Label(self.exercise_frame, text="Exercise : ", font=("Arial", 13,"bold"), bg="#FFFFFF")
        self.daylabel.place(x=20,y=60)
        self.selected_exercise = ttk.Combobox(
            self.exercise_frame, values=self.all_exercises, state="readonly", 
            width=20, font=("Arial", 13)
        )
        self.selected_exercise.set("None")
        self.selected_exercise.place(x=110,y=60)

        self.add_exr = ctk.CTkButton(self.exercise_frame,text="Add",font=("Microsoft Hayei",15,"bold"),hover_color="#6767FF",fg_color="#3838D5",text_color="#FFFFFF",width=80,height=60,corner_radius=20,command=self.add_exercise)
        self.add_exr.place(x=320,y=20)
        self.selected_label = tk.Label(self.manage_frame,bg="#FFFFFF",text="Selected Exercise : ",font=("Microsoft Hayei",20,"bold"),fg="#3838D5")
        self.selected_label.pack(side="top")
        self.selected_label = tk.Frame(self.manage_frame,bg="#3838D5",height=2)
        self.selected_label.pack(side="top",fill="x")
        self.frame_entries = tk.Frame(self.manage_frame, bg="#FFFFFF")
        self.frame_entries.pack()

        self.exercise_entries = {}

        self.refresh_manage_entries()

        add_frame = tk.Frame(self.manage_frame, bg="#FFFFFF")
        add_frame.pack(pady=10)

    def refresh_manage_entries(self):

        for widget in self.frame_entries.winfo_children():
            widget.destroy()
        self.exercise_entries.clear()

        for ex in self.confirm_exercise:
            row = tk.Frame(self.frame_entries, bg="#FFFFFF")
            row.pack(fill="x", pady=5, anchor="w")

            var = tk.StringVar(value=ex)

            label = tk.Label(row, textvariable=var, font=("Verdana",12,"bold"), width=30,bg="#FFFFFF",wraplength=350)
            label.pack(side="left")

            spacer = tk.Frame(row, bg="#FFFFFF")
            spacer.pack(side="left", expand=True, fill="x")

            del_btn = ctk.CTkButton(row, text="X",fg_color="#FF0000",font=("Verdana", 12, "bold"),text_color="#DDDDDD",width=20,height=20, command=lambda e=ex: self.delete_exercise(e))
            del_btn.pack(side="right")
            self.exercise_entries[ex] = var

    def delete_exercise(self, name):
        if name in self.confirm_exercise:
            self.confirm_exercise.remove(name)
        self.refresh_manage_entries()

    def add_exercise(self):
        day = self.selected_days.get()
        exercise = self.selected_exercise.get()

        if day == "None" or exercise == "None":
            self.error_msg("Day / Exercise can't be \'None\'")
            return
        
        name = f"{day} - {exercise}" 
        if name in self.confirm_exercise:
            self.error_msg("Invalid, 1 exercise can only be selected \'once\' in same day")
        elif len(self.confirm_exercise) >= 10: 
            self.error_msg("Maximum 10 exercises!")
        else:
            self.confirm_exercise.append(name)
        self.refresh_manage_entries()

    def go_back_to_plan(self):
    #used for jump back to Plan page

        for widget in self.winfo_children():
            widget.destroy()
        
        self.master.create_navbar()
        self.master.show_pages("Plan")
        frame = tk.Frame(self,bg="#3838D5")
        frame.pack(side="top",fill="x")
        label2 = tk.Label(frame,text="Plan",font=("Comic Sans MS",30,"bold"),bg="#3838D5",fg="black")
        label2.pack(padx=10)
        self.create_top_buttons()
        self.image_frame = tk.Frame(self, bg="#EEEEEE")
        self.image_frame.pack(pady=10, padx=10)

        self.show_content("Arm")

    def back_to_plan(self):
    #used for jump back to Plan page(For edit page only)

        self.manage_frame.pack_forget()

        self.daily_plan()
