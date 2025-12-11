import random
import tkinter as tk
from tkinter import PhotoImage, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from PlanPage import *
from ReportPage import *
from LogPage import *
from ProfilePage import *

# ------------------ Main App ------------------
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Anytime Fitness")
        icon_image_pil = Image.open("image/AF_tk.png").resize((25,15))
        self._icon = ImageTk.PhotoImage(icon_image_pil) 
        self.iconphoto(True, self._icon)
        self.geometry("410x700")
        self.resizable(False, False)
        frame = tk.Frame(self,width=410,height=700, bg="#3838D5")
        frame.pack(fill="both")
        frame.pack_propagate(False)

        img = Image.open("image/AF_loading.png")
        logo = ImageTk.PhotoImage(img)
        logo_name = tk.Label(frame,image=logo,bg="#3838D5")
        logo_name.image = logo
        logo_name.pack(pady=250,anchor="center")
        frame.after(2000, frame.pack_forget)

        # navigator bar 的字
        self.tabs = ["Plan","Report","Log","Profile"]
        self.selected_exercises = []#用来store selected exercise
        self.selected_date = []
        
        self.all_frames = {}
        self.top_label = {}
        self.current_user = " "
        self.USER_FILE = "user_info.txt"

        for tab in self.tabs:
            if tab == "Plan":
                frame = PlanPage(self, self.selected_exercises,self.all_frames,self.selected_date)
            elif tab == "Report":
                frame = ReportPage(self)
            elif tab == "Log":
                frame = LogPage(self)
            elif tab == "Profile":
                frame = ProfilePage(self, self.all_frames)
            self.all_frames[tab] = frame
            frame.pack(fill="both", expand=True)
            frame.pack_forget()

        if "Report" in self.all_frames and "Log" in self.all_frames:
            self.all_frames["Report"].set_log_page(self.all_frames["Log"])

        self.main_page()

    def create_navbar(self):
    #navigate bar 的display function
        self.nav_tabs = {}
        self.nav_bar = tk.Frame(self, bg="#67DDFF", height=50)
        self.nav_bar.pack(side="bottom", fill="x")
        self.nav_bar.pack_propagate(False)

        for tab in self.tabs:
            label = tk.Label(self.nav_bar,bg="#67DDFF",fg="black",font=("Tahoma", 14, "bold"),cursor="hand2",text=tab)
            label.pack(side="left", expand=True)
            label.bind("<Button-1>", lambda e, t=tab: self.show_pages(t))
            self.nav_tabs[tab] = label
            
    def show_pages(self,tab_name):
    #display page 的function

        for frames in self.all_frames.values():
            frames.pack_forget()

        self.all_frames[tab_name].pack(fill="both", expand=True)

        for tab, lbl in self.nav_tabs.items():
            if tab == tab_name:
                lbl.config(fg="#3838D5")
            else:
                lbl.config(fg="#000000")

        for tab, lbl in self.top_label.items():
            if tab == tab_name:
                lbl.config(text=tab)

    def save_user(self, username, password):
            # Format: Username \t Password \t Age \t Gender \t Description
            # We set default values for new users
            default_age = "-"
            default_gender = "-"
            default_desc = "No Description"
            
            with open(self.USER_FILE, "a") as f:
                f.write(f"{username}\t{password}\t{default_age}\t{default_gender}\t{default_desc}\n")

    def load_users(self):
        # Returns a dictionary: { "username": ["password", "age", "gender", "desc"] }
        users = {}
        try:
            with open(self.USER_FILE, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        parts = line.split("\t")
                        if len(parts) >= 2:
                            u = parts[0]
                            p = parts[1]
                            # specific handling if older data didn't have profile info
                            age = parts[2] if len(parts) > 2 else "-"
                            gender = parts[3] if len(parts) > 3 else "-"
                            desc = parts[4] if len(parts) > 4 else "No Description"
                            
                            users[u] = [p, age, gender, desc]
        except FileNotFoundError:
            pass
        return users

    def main_page(self):

        self.block = tk.Frame(self,bg="#3838D5",height=75)
        self.block.pack(side="top",fill="both")
        self.block.pack_propagate(False)

        signup_label = tk.Label(self.block, text="Sign Up", font=("Arial", 30, "bold"), bg="#3838D5")
        signup_label.pack(side="top",pady=15)
        
        self.block2 = tk.Frame(self,bg="#67DDFF",height=75)
        self.block2.pack(side="top",fill="both")
        self.block2.pack_propagate(False)

        self.main_frame = tk.Frame(self,bg="#67DDFF",height=550)
        self.main_frame.pack(fill="x",side="top")
        self.main_frame.pack_propagate(False)

        tk.Label(self.main_frame, text="Welcome to Anytime Fitness", font=("Arial", 18, "bold"),bg="#67DDFF").pack(pady=20)
        self.signup_frame = ctk.CTkFrame(self.main_frame,fg_color="#FBFBFB",corner_radius=30,border_width=2)
        self.signup_frame.pack(fill="both",side="top",pady=5,padx=10)
        tk.Label(self.signup_frame,bg="#FBFBFB", text="Username:",font=("Arial",12)).place(x=80,y=30)
        self.signup_username = tk.Entry(self.signup_frame,width=30)
        self.signup_username.place(x=170,y=30)


        tk.Label(self.signup_frame,bg="#FBFBFB", text="Password:",font=("Arial",12)).place(x=80,y=70)
        self.signup_password = tk.Entry(self.signup_frame, show="*",width=30)
        self.signup_password.place(x=170,y=70)

        tk.Label(self.signup_frame,bg="#FBFBFB", text="Confirm Password:",font=("Arial",12)).place(x=20,y=110)
        self.signup_confirm = tk.Entry(self.signup_frame, show="*",width=30)
        self.signup_confirm.place(x=170,y=110)
        self.signup_confirm.bind("<Return>", lambda event: self.sign_up())

        ctk.CTkButton(self.signup_frame, text="Sign Up", width=200, height=50,font=("Comic Sans MS",20),
                  fg_color="#3838D5",hover_color="#6767FF", text_color="#FFFFFF", corner_radius=60,command=self.sign_up).place(x=100,y=140)

        self.login_label = tk.Label(self.main_frame,text="If you have an account, ",fg="#000000",bg="#67DDFF",font=("Arial",12))
        self.login_label.place(x=100,y=300)
        self.label = tk.Label(self.main_frame, text="log in", bg="#67DDFF", fg="#3838D5",font=("Arial",12,"underline","bold"))
        self.label.place(x=260,y=300)
        self.label.bind("<Button-1>",lambda e:self.login_page())

    def login_page(self):
        self.block.pack_forget()
        self.block2.pack_forget()
        self.block = tk.Frame(self,bg="#3838D5",height=75)
        self.block.pack(side="top",fill="both")
        self.block.pack_propagate(False)


        self.main_frame.pack_forget()
        self.block2 = tk.Frame(self,bg="#67DDFF",height=150)
        self.block2.pack(side="top",fill="x")
        self.block2.pack_propagate(False)
        self.login_main = tk.Frame(self,bg="#67DDFF")
        self.login_main.pack(side="top",fill="x")

        self.back_but = ctk.CTkButton(self.block,corner_radius=20,text="<",width=40,height=40,hover_color="#3838D5",text_color="#000000",fg_color="#3838D5",font=("Consolas", 40, "bold"),cursor="hand2",command=self.back_to_main)
        self.back_but.place(x=40,y=35,anchor="center")
        tk.Label(self.block, text="Log In", font=("Arial", 30, "bold"), bg="#3838D5").pack(pady=10)

        self.login_frame = ctk.CTkFrame(self.login_main,fg_color="#FBFBFB",corner_radius=30,border_width=2)
        self.login_frame.pack(fill="both",side="top",pady=10,padx=10)

        tk.Label(self.login_frame, text="Username:", bg="#FBFBFB",font=("Arial",12)).place(x=50,y=30)
        self.login_username = tk.Entry(self.login_frame,width=30)
        self.login_username.place(x=140,y=30)

        tk.Label(self.login_frame, text="Password:", bg="#FBFBFB",font=("Arial",12)).place(x=50,y=70)
        self.login_password = tk.Entry(self.login_frame, show="*",width=30)
        self.login_password.place(x=140,y=70)
        
        self.login_password.bind("<Return>", lambda event: self.log_in())

        ctk.CTkButton(self.login_frame, text="Log In", width=200,hover_color="#6767FF", height=50,corner_radius=60,fg_color="#3838D5", text_color="#FFFFFF",font=("Comic Sans MS",20), command=self.log_in).place(x=100,y=120)
        self.login_main1 = tk.Frame(self,bg="#67DDFF",height=270)
        self.login_main1.pack(side="bottom",fill="x")
        self.login_main1.pack_propagate(False)

    def log_in(self):
            username = self.login_username.get()
            password = self.login_password.get()

            users = self.load_users()

            # Check if user exists and password matches (index 0 of the list is password)
            if (username == "admin" and password == "1234") or \
                    (username in users and users[username][0] == password):
                
                self.current_user = username
                self.show_center_msg(f"Welcome, {username}")
                self.login_main.destroy()
                self.block.destroy()
                self.login_main1.destroy()
                self.block2.destroy()

                # LOAD PROFILE DATA INTO PROFILE PAGE
                profile_frame = self.all_frames["Profile"]
                
                # Get data from file (or defaults if admin)
                if username in users:
                    user_data = users[username] # [pass, age, gender, desc]
                    profile_frame.profile_data = [username, user_data[1], user_data[2], user_data[3]]
                else:
                    profile_frame.profile_data = ["admin", "-", "-", "Admin Account"]

                profile_frame.profile_display()
                
                # LOAD LOGS FOR THIS USER SPECIFICALLY
                self.all_frames["Log"].load_saved_logs()
                
                self.create_navbar()
                self.show_pages("Profile")
            else:
                self.error_msg("Wrong username or password!")

    def show_center_msg(self, msg):
        popup = tk.Toplevel(self)
        popup.title("Successful")
        popup.resizable(False, False)

        width, height = 250, 120  # 弹窗大小

        def update_position():
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()
            # 计算居中位置
            x = root_x + (root_width - width) // 2
            y = root_y + (root_height - height) // 2
            popup.geometry(f"{width}x{height}+{x}+{y}")
            # 如果弹窗还存在，50毫秒后再次更新
            if popup.winfo_exists():
                popup.after(1, update_position)

        update_position() 

        tk.Label(popup, text=msg, fg="#000000", font=("Arial", 15,"bold")).pack(pady=10)
        ctk.CTkButton(popup, text="OK", fg_color="#3838D5",hover_color="#6767FF", text_color="#FFFFFF", command=popup.destroy, width=120,height=40,corner_radius=50).pack(pady=5)
        "#3838D5"

        popup.grab_set()
        popup.focus_set()
        popup.transient(self)

    def error_msg(self, msg):
        popup = tk.Toplevel(self)
        popup.title("Error")
        popup.resizable(False, False)

        width, height = 250, 150  # 弹窗大小

        def update_position():
            root_x = self.winfo_rootx()
            root_y = self.winfo_rooty()
            root_width = self.winfo_width()
            root_height = self.winfo_height()
            # 计算居中位置
            x = root_x + (root_width - width) // 2
            y = root_y + (root_height - height) // 2
            popup.geometry(f"{width}x{height}+{x}+{y}")
            # 如果弹窗还存在，50毫秒后再次更新
            if popup.winfo_exists():
                popup.after(1, update_position)

        update_position() 

        tk.Label(popup, text=msg, fg="#FF0000", font=("Arial", 15,"bold"),wraplength=200).pack(pady=10)
        ctk.CTkButton(popup, text="OK", fg_color="#3838D5",hover_color="#6767FF", text_color="#FFFFFF", command=popup.destroy, width=120,height=30,corner_radius=50).pack(pady=15)

        popup.grab_set()
        popup.focus_set()
        popup.transient(self)

    def back_to_main(self):
        self.login_frame.pack_forget()
        self.login_main.pack_forget()
        self.login_main1.pack_forget()
        self.block.pack_forget()
        self.block2.pack_forget()
        self.main_page()

    def sign_up(self):

        username = self.signup_username.get()
        password = self.signup_password.get()
        confirm = self.signup_confirm.get()

        if username == "" or password == "" or confirm == "":
            self.error_msg("Fields cannot be empty!")
            return

        if password != confirm:
            self.error_msg("Passwords do not match!")
            return

        users = self.load_users()

        if username in users:
            self.error_msg("Username already exists!")
            return

        self.save_user(username, password)
        self.show_center_msg("Sign Up Successfully!")

        self.main_frame.destroy()
        self.login_page()

App().mainloop()