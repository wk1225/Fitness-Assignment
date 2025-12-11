import random
import tkinter as tk
from tkinter import PhotoImage, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime
import os
import sys
import subprocess


# ------------------ Profile Page ------------------
class ProfilePage(tk.Frame):
    def __init__(self, master, all_frames):
        super().__init__(master, bg="#FFFFFF")
        self.master = master
        self.profile_data = ["?", "-", "unknown", "No Description"] #Profile initial value
        self.all_frames = all_frames
        
        self.profile_main_area = tk.Frame(self, bg="#FFFFFF")
        self.profile_main_area.pack(fill="both", expand=True)
        self.profile_display()

    def profile_display(self):
    #Display profile page

        self.profile_data[0]=self.master.current_user
        name, age, gender, desc = self.profile_data

        # Create/reset internal content frame
        if hasattr(self, "profile_content_frame"):
            for w in self.profile_content_frame.winfo_children():
                w.destroy()
        else:
            self.profile_content_frame = tk.Frame(self.profile_main_area, bg="#FFFFFF")
            self.profile_content_frame.pack(fill="both", expand=True)

        frame = self.profile_content_frame

        # ---------- PROFILE HEADER (NO BLUE BAR) ----------
        header_frame = tk.Frame(frame, bg="#FFFFFF")
        header_frame.pack(fill="x")

        img = Image.open("image/profile_back.png").resize((410,185))
        backgd = ImageTk.PhotoImage(img)
        self.profile_background_img = backgd

        self.backgroundLabel = tk.Label(header_frame,image=backgd)
        self.backgroundLabel.image = backgd
        self.backgroundLabel.pack()
        self.backgroundLabel.pack_propagate(False)

        imglogo = Image.open("image/AF_header.png").resize((210,105))
        logopic = ImageTk.PhotoImage(imglogo)
        self.logo = tk.Label(self.backgroundLabel,image=logopic,bg=None)
        self.logo.image = logopic
        self.logo.pack(pady=30,side="top")
        self.logo.pack_propagate(False)
        # ---------- FOOTER (CENTER BOTTOM) ----------
        self.bottom_frame = tk.Frame(frame, bg="#FFFFFF")
        self.bottom_frame.pack(side="bottom", pady=10, fill="x")

        self.profileName = tk.Label(
           frame, text=name, bg="#FFFFFF", 
            fg="#000000", font=("Roboto", 22, "bold")
        )
        self.profileName.pack(anchor="w",pady=5, padx=10)

        self.profileAge = tk.Label(
           frame, text=f"{age}", bg="#FFFFFF", 
            fg="#000000", font=("Roboto", 12)
        ) 
        self.profileAge.pack(anchor="w",pady=5, padx=10)

        self.profileGender = tk.Label(
           frame, text=f"{gender}", bg="#FFFFFF", 
            fg="#000000", font=("Roboto", 12)
        )
        self.profileGender.pack(anchor="w",pady=5, padx=10)
       
        self.profileDesc = tk.Label(
           frame, text=desc, bg="#FFFFFF", 
            fg="#000000", font=("Roboto", 11), 
            justify="left", wraplength=250
        )
        self.profileDesc.pack(anchor="w",pady=5, padx=10)
        

        
        # Edit Profile Button
        self.profileEdit = ctk.CTkButton(
            self.bottom_frame, fg_color="#3838D5", hover_color="#6767FF", 
            text_color="#FFFFFF", text="Edit Profile", corner_radius=50, 
           width=380, height=60,font=("Comic Sans MS",30,"bold"), command=self.profile_edit
        )
        self.profileEdit.pack(anchor="w", pady=5,padx=15)
        #Copyright Button
        self.profileEdit = ctk.CTkButton(
            self.bottom_frame, fg_color="#FFFFFF", hover_color="#6767FF", 
            text_color="#000000", text="Copyright", corner_radius=30, 
            width=380, height=40,font=("Tahoma",16, "bold"), command=self.copy_right, 
            border_width = 3, border_color = "#3838D5"
        )
        self.profileEdit.pack(anchor="w", pady=5,padx=15)
        #Accuracy Button
        self.profileEdit = ctk.CTkButton(
            self.bottom_frame, fg_color="#FFFFFF", hover_color="#6767FF", 
            text_color="#000000", text="Accuracy", corner_radius=30, 
            width=380, height=40,font=("Tahoma",16, "bold"), command=self.accuracy, 
            border_width = 3, border_color = "#3838D5"
        )
        self.profileEdit.pack(anchor="w", pady=5,padx=15)
        #Terms & Condition Button
        self.profileEdit = ctk.CTkButton(
            self.bottom_frame, fg_color="#FFFFFF", hover_color="#6767FF", 
            text_color="#000000", text="Terms & Condition", corner_radius=30, 
            width=380, height=40,font=("Tahoma",16, "bold"), command=self.terms, 
            border_width = 3, border_color = "#3838D5"
        )
        self.profileEdit.pack(anchor="w", pady=5,padx=15)
        #Log out Button
        self.logout_but = ctk.CTkButton(
            self.bottom_frame, fg_color="#E74C3C", hover_color="#C0392B", 
            text_color="#FFFFFF", text="Log out", corner_radius=30, 
            width=380, height=40,font=("Tahoma",16,"bold"), command=self.logout 
        ) 
        self.logout_but.pack(anchor="w", pady=5, padx=15)

    def profile_edit(self):
        #Hide the profile frame and navbar
        self.profile_main_area.pack_forget()
        self.master.nav_bar.pack_forget()

        #Initialize variables
        self.name_var = tk.StringVar(value=self.profile_data[0])
        self.age_var = tk.StringVar(value=self.profile_data[1])
        self.gender_var = tk.StringVar(value=self.profile_data[2])
        self.desc_var = tk.StringVar(value=self.profile_data[3])

        #Top black frame (optional styling)
        
        self.frame_0 = tk.Frame(self, bg="#FFFFFF", height=150)
        
        self.frame_0.pack(fill="x", side="top")
        self.frame_0.pack_propagate(False)
        img = Image.open("image/profile_back.png").resize((410,150))
        image = ImageTk.PhotoImage(img)
        self.labelpic = tk.Label(self.frame_0,image=image,bg="#FFFFFF")
        self.labelpic.image = image
        self.labelpic.pack()
        self.labelpic.pack_propagate(False)

        #Main input frame
        self.frame_1 = tk.Frame(self, bg="#FFFFFF")
        self.frame_1.pack(fill="both", side="top", padx=10, pady=10)

        #---Name---
        tk.Label(self.frame_1, bg="#FFFFFF", text="Name:", font=("Arial", 13, "bold")).pack(anchor="w", padx=20, pady=2)
        tk.Entry(self.frame_1, textvariable=self.name_var, font=("Arial", 13), width=25).pack(fill="x", padx=20)

        #---Age---
        tk.Label(self.frame_1, bg="#FFFFFF", text="Age:", font=("Arial", 13, "bold")).pack(anchor="w", padx=20, pady=2)
        ttk.Combobox(self.frame_1, textvariable=self.age_var, values=[str(i) for i in range(16, 61)], state="readonly", font=("Arial", 13), width=20).pack(fill="x", padx=20)

        #---Gender---
        tk.Label(self.frame_1, bg="#FFFFFF", text="Gender:", font=("Arial", 13, "bold")).pack(anchor="w", padx=20, pady=2)
        ttk.Combobox(self.frame_1, textvariable=self.gender_var, values=("-", "Male", "Female"), state="readonly", font=("Arial", 13), width=20).pack(fill="x", padx=20)

        #---Description---
        #Description Label
        self.desc_edit = tk.Label(self.frame_1, bg="#FFFFFF", text="Description:", font=("Arial", 13, "bold"))
        self.desc_edit.pack(anchor="w", padx=20, pady=2)

        #Text box for description
        self.desc_box = tk.Text(self.frame_1, height=4, width=40, font=("Arial", 13))
        self.desc_box.pack(fill="x", padx=20)
        self.desc_box.insert("1.0", self.desc_var.get())

        #Character counter label
        self.char_count_label = tk.Label(self.frame_1, text=f"{len(self.desc_box.get('1.0', 'end-1c'))}/100", font=("Arial", 10), fg="#555555")
        self.char_count_label.pack(anchor="e", padx=20, pady=(0,5))
        
        #Function to limit text and update counter
        def limit_text(event=None):
            content = self.desc_box.get("1.0", "end-1c")
            if len(content) > 100:
                cursor_pos = self.desc_box.index(tk.INSERT)
                self.desc_box.delete("1.0", "end")
                self.desc_box.insert("1.0", content[:100])
                try:
                    self.desc_box.mark_set(tk.INSERT, cursor_pos)
                except tk.TclError:
                    self.desc_box.mark_set(tk.INSERT, "end-1c")
            #Update counter
            self.char_count_label.config(text=f"{len(self.desc_box.get('1.0', 'end-1c'))}/100")
            return "break"

        #Bind typing, paste, and middle-click paste
        self.desc_box.bind("<KeyRelease>", limit_text)
        self.desc_box.bind("<Control-v>", limit_text)
        self.desc_box.bind("<Button-2>", limit_text)  #middle-click paste

        #Save button frame
        self.frame_2 = tk.Frame(self, bg="#FFFFFF")
        self.frame_2.pack(fill="both")
        self.save_btn = ctk.CTkButton(self.frame_2, text="Save", fg_color="#3838D5",hover_color="#6767FF", text_color="white", corner_radius=60,font=("Tahoma",14,"bold"), width=120, height=40, command=self.save_profile)
        self.save_btn.pack(pady=10)

    def save_profile(self):
            # 1. Get Inputs
            new_name = self.name_var.get().strip()
            new_age = self.age_var.get()
            new_gender = self.gender_var.get()
            new_desc = self.desc_box.get("1.0", "end").strip().replace("\t", " ")
            if len(new_desc) > 100: new_desc = new_desc[:100]

            old_name = self.master.current_user

            # 2. Validation
            if not new_name:
                self.master.show_center_msg("Username cannot be empty")
                return
                
            # 3. Check for Duplicate Username (only if name actually changed)
            if new_name != old_name:
                try:
                    with open("user_info.txt", "r") as f:
                        for line in f:
                            parts = line.split("\t")
                            if parts and parts[0] == new_name:
                                self.master.show_center_msg("Username already taken")
                                return
                except FileNotFoundError:
                    pass 

            # 4. Update user_info.txt
            lines_to_write = []
            try:
                with open("user_info.txt", "r") as f:
                    lines = f.readlines()
                
                for line in lines:
                    parts = line.strip().split("\t")
                    # Check if this line belongs to the current user (old_name)
                    if len(parts) >= 2 and parts[0] == old_name:
                        # Keep password (parts[1]), update Name, Age, Gender, Desc
                        password = parts[1]
                        # Format: NewName \t Password \t Age \t Gender \t Description
                        new_line = f"{new_name}\t{password}\t{new_age}\t{new_gender}\t{new_desc}\n"
                        lines_to_write.append(new_line)
                    else:
                        lines_to_write.append(line)
                
                with open("user_info.txt", "w") as f:
                    f.writelines(lines_to_write)
                    
            except Exception as e:
                print(f"Error updating user info: {e}")
                return

            # 5. Update workout_records.txt (Migrate logs to new username)
            if new_name != old_name:
                log_lines = []
                try:
                    with open("workout_records.txt", "r", encoding="utf-8") as f:
                        logs = f.readlines()
                    
                    for line in logs:
                        parts = line.split("\t")
                        # If the log belongs to the old name, swap it to new name
                        if parts and parts[0] == old_name:
                            # parts[1:] contains Activity, Time, Intensity
                            rest_of_line = "\t".join(parts[1:])
                            log_lines.append(f"{new_name}\t{rest_of_line}")
                        else:
                            log_lines.append(line)
                    
                    with open("workout_records.txt", "w", encoding="utf-8") as f:
                        f.writelines(log_lines)
                except FileNotFoundError:
                    pass # No logs to migrate yet

            # 6. Update Internal Session Data
            self.master.current_user = new_name
            self.profile_data = [new_name, new_age, new_gender, new_desc if new_desc else "No Description"]

            # 7. UI Refresh
            self.frame_0.pack_forget()
            self.frame_1.pack_forget()
            self.frame_2.pack_forget()

            self.master.create_navbar()
            self.master.show_pages("Profile")
            self.profile_main_area.pack(fill="both", expand=True)
            self.profile_display()

    def terms(self):
        self.profile_main_area.pack_forget()
        self.master.nav_bar.pack_forget()

        paragraph = """Welcome to the web site of Anytime Fitness, LLC (“Anytime Fitness”). Anytime Fitness is pleased to make the web sites located at anytimefitness.com (e.g. www.anytimefitness.com, blog.anytimefitness.com) but excluding shop.anytimefitness.com (the “Sites”) available for your use and benefit. By using the Sites you agree to be bound by the Terms of Use set forth below. Use of the Sites is strictly voluntary. If you do not agree to these Terms of Use and the Privacy Policy, you must immediately log off the Sites and may not use the Sites.These Terms of Use apply to your access to and use of the Sites and do not alter in any way the terms and conditions of any other agreement you may have with Anytime Fitness, unless otherwise directed by Anytime Fitness. If you breach any of these terms and conditions, your authorization to use the Sites automatically terminates and you must immediately discontinue use of the Sites."""
        
        self.frame_0 = tk.Frame(self,bg="#3838D5",height=75)
        self.frame_0.pack(fill="x",side="top")
        self.frame_0.pack_propagate(False)
        self.terms_1 = tk.Label(self.frame_0,bg="#3838D5",text="Terms & Condition",font=("Verdana",20,"bold"),fg="#000000")
        self.terms_1.pack(side="top",pady=20)
        self.back_but = ctk.CTkButton(self.frame_0,corner_radius=20,text="<",width=40,hover_color="#3838D5",height=40,text_color="#000000",fg_color="#3838D5",font=("Consolas", 40, "bold"),cursor="hand2",command=self.go_back_to_profile)
        self.back_but.place(x=30,y=35,anchor="center")

        self.frame_1 = tk.Frame(self,bg="#FFFFFF")
        self.frame_1.pack(fill="x",side="top")
        self.terms_2 = tk.Label(self.frame_1,text=paragraph,fg="#000000",justify="left",bg="#FFFFFF",font=("Arial",10),wraplength=380)
        self.terms_2.pack(padx=10, pady=10)

    def accuracy(self):
        self.profile_main_area.pack_forget()
        self.master.nav_bar.pack_forget()
        
        paragraph = """Information on the Sites may contain typographical errors, inaccuracies, or omissions in relation to services, pricing, locations, descriptions, information, and other matters. Anytime Fitness reserves the right to correct any errors, inaccuracies, or omissions and to discontinue, change or update information at any time without prior notice. If Anytime Fitness discovers price errors, they will be corrected on Anytime Fitness's systems, and the corrected price will apply to your order."""
        
        self.frame_0 = tk.Frame(self,bg="#3838D5",height=75)
        self.frame_0.pack(fill="x",side="top")
        self.frame_0.pack_propagate(False)
        self.about_1 = tk.Label(self.frame_0,bg="#3838D5",text="Accuracy",font=("Verdana",20,"bold"),fg="#000000")
        self.about_1.pack(side="top",pady=20)
        self.back_but = ctk.CTkButton(self.frame_0,corner_radius=20,text="<",width=40,height=40,hover_color="#3838D5",text_color="#000000",fg_color="#3838D5",font=("Consolas", 40, "bold"),cursor="hand2",command=self.go_back_to_profile)
        self.back_but.place(x=30,y=35,anchor="center")

        self.frame_1 = tk.Frame(self,bg="#FFFFFF")
        self.frame_1.pack(fill="x",side="top")
        self.terms_2 = tk.Label(self.frame_1,text=paragraph,fg="#000000",justify="left",bg="#FFFFFF",font=("Arial",10),wraplength=380)
        self.terms_2.pack(padx=10, pady=10)
 
    def copy_right(self):
        self.profile_main_area.pack_forget()
        self.master.nav_bar.pack_forget()

        paragraph ="""All content, software, and technology included on the Sites or used in the operation of the Sites is the owned or licensed property of Anytime Fitness or its content, software, and technology suppliers, and is protected by U.S. and international copyright laws. The compilation (meaning the collection, arrangement, and assembly) of all content on the Sites is the exclusive property of Anytime Fitness and protected by U.S. and international copyright laws. Anytime Fitness grants you permission to view and use content, software, and technology made available to you on the Sites in connection with your own personal, noncommercial use of the Sites. Any other use, including the reproduction, modification, distribution, transmission, republication, display, or performance, of the content, software, and technology on the Sites is strictly prohibited."""

        self.frame_0 = tk.Frame(self,bg="#3838D5",height=75)
        self.frame_0.pack(fill="x",side="top")
        self.frame_0.pack_propagate(False)
        self.copy_1 = tk.Label(self.frame_0,bg="#3838D5",text="Copyright",font=("Verdana",20,"bold"),fg="#000000")
        self.copy_1.pack(side="top",pady=20)
        self.back_but = ctk.CTkButton(self.frame_0,corner_radius=20,text="<",hover_color="#3838D5",width=40,height=40,text_color="#000000",fg_color="#3838D5",font=("Consolas", 40, "bold"),cursor="hand2",command=self.go_back_to_profile)
        self.back_but.place(x=30,y=35,anchor="center")

        self.frame_1 = tk.Frame(self,bg="#FFFFFF")
        self.frame_1.pack(fill="x",side="top")
        self.terms_2 = tk.Label(self.frame_1,text=paragraph,fg="#000000",justify="left",bg="#FFFFFF",font=("Arial",10),wraplength=380)
        self.terms_2.pack(padx=10, pady=10)

    def go_back_to_profile(self):
            self.frame_0.pack_forget()
            self.frame_1.pack_forget()
            
            self.master.create_navbar()
            self.master.show_pages("Profile")

            self.profile_main_area.pack(fill="both", expand=True)
            self.master.nav_bar.pack(fill="x")

    def show_center_msg(self, msg):
        # Utility function to display a centered pop-up message
        popup = tk.Toplevel(self)
        popup.title("Message")
        popup.resizable(False, False)

        width, height = 300, 150
        
        # Define the command based on the message content
        if msg == "Log out successfully":
            # If successfully logged out, the OK button closes the main window
            ok_command = lambda: self.relog_and_exit(popup)
        else:
            # Otherwise, the OK button just destroys the pop-up
            ok_command = popup.destroy

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
        
        # USE THE DYNAMIC COMMAND HERE
        ctk.CTkButton(
            popup, text="OK", fg_color="#3838D5", text_color="#FFFFFF", 
            command=ok_command, 
            width=120, height=40, corner_radius=50
        ).pack(pady=15)
        popup.grab_set()
        popup.focus_set()
        popup.transient(self)
    
    def logout(self):
        # Hide the current profile view and navbar
        self.profile_main_area.pack_forget()
        if hasattr(self.master, 'nav_bar'):
            self.master.nav_bar.pack_forget()

        # Show "Log out successfully" pop-up message
        self.master.after(100, lambda: self.show_center_msg("Log out successfully"))

    def relog_and_exit(self, popup):
        # Hides the popup, then restarts the application using subprocess."""
        # Close the success pop-up
        popup.destroy()
        
        # Get the executable and script path
        python_exe = sys.executable
        # os.path.abspath ensures we get the full, correctly resolved path
        script_path = os.path.abspath(sys.argv[0]) 
        
        # Launch a new instance of the script using subprocess.Popen
        # This correctly handles paths containing spaces.
        subprocess.Popen([python_exe, script_path] + sys.argv[1:])
        
        # Exit the current application cleanly
        self.master.quit()
        