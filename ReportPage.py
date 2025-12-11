import random
import tkinter as tk
from tkinter import PhotoImage, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from tkcalendar import DateEntry
from datetime import datetime

#-------------------Report Page------------------
class ReportPage(tk.Frame):
    def __init__(self, master):
        super().__init__(master, bg="#FFFFFF")
        self.log_page = None  # 用于传入 LogPage
        self.create_widgets()

    #  连接log page
    def set_log_page(self, log_page):
        self.log_page = log_page    

    # 卡路里计算
    def calculate_calories(self, activity, duration, intensity):
        duration = int(duration)
        base_rates = {
            "Arm": 4, "Leg": 5, "Chest": 4.5, "Abs": 3.5, "Back": 4.0,
            "Running": 8.0, "Walking": 3.5, "Cycling": 6.0, "Swimming": 7.0,
            "Weightlifting": 6.0, "Yoga": 3.0, "HIIT": 9.0
        }
        intensity_multiplier = {
            "Low": 0.8, "Medium": 1.0, "High": 1.3,
            "Beginner": 0.8, "Intermediate": 1.0, "Advanced": 1.3
        }
        base = base_rates.get(activity, 4)
        multi = intensity_multiplier.get(intensity, 1)
        return round(base * duration * multi, 1)

    # 创建界面
    def create_widgets(self):
        # 直接加载刷新图标
        icon_pil = Image.open("image/refresh.png").resize((30, 30), Image.LANCZOS)
        self.refresh_icon_img = ImageTk.PhotoImage(icon_pil) 

        # 创建图片按钮
        # bd=0 去掉边框, bg="#FFFFFF" 让背景透明
        self.top_refresh_btn = tk.Button(self, image=self.refresh_icon_img, 
                                         command=self.generate_report, bd=0, 
                                         bg="#FFFFFF", activebackground="#FFFFFF", cursor="hand2")

        self.top_refresh_btn.place(relx=1.0, x=-15, y=10, anchor="ne")

        # 标题
        self.title_label = tk.Label(self, text="Calories Burn Report", font=("Arial", 18, "bold"), bg="#FFFFFF")
        self.title_label.pack(pady=10)

        self.target_goal = 500 

        goal_big_frame = tk.Frame(self,bg="#FFFFFF")
        goal_big_frame.pack(padx=10)
        goal_frame = ctk.CTkFrame(goal_big_frame, fg_color="#EEEEEE",corner_radius=10)
        goal_frame.pack(fill="x", pady=5)

        # 进度文字 Label 
        self.goal_label = tk.Label(goal_frame, text=f"Goal Progress: 0 / {self.target_goal} kcal", 
                                   font=("Arial", 12, "bold"), bg="#EEEEEE", fg="#555555")
        self.goal_label.pack(anchor="w", pady=5,padx=10)

        # 创建进度条
        self.goal_bar = ctk.CTkProgressBar(goal_frame, width=400, height=15, corner_radius=10, progress_color="#3838D5", fg_color="#DDDDDD") 
        self.goal_bar.pack(fill="x",padx=10,pady=10)
        self.goal_bar.set(0) 

        # 总览 Label
        self.stats_frame = tk.Frame(self,bg="#FFFFFF")
        self.stats_frame.pack(fill="x", pady=10, padx=20)
        self.card_workouts_val = self.create_stat_card(self.stats_frame, "Workouts", "0", "#3838D5", 0)
        self.card_minutes_val = self.create_stat_card(self.stats_frame, "Minutes", "0", "#E67E22", 1)
        self.card_calories_val = self.create_stat_card(self.stats_frame, "Calories", "0", "#E74C3C", 2)

        filter_frame = tk.Frame(self,bg="#FFFFFF")
        filter_frame.pack(pady=5)
        
        tk.Label(filter_frame, text="Filter:", font=("Arial", 12, "bold"),bg="#FFFFFF").pack(side="left", padx=5)

        self.current_filter_val = "All"

        # 创建那个 "小按钮"
        self.filter_btn = ctk.CTkButton(filter_frame, text="All Activities ▼", font=("Arial", 12, "bold"),fg_color="#EEEEEE", text_color="#3838D5", hover_color="#CCCCCC", width=100, height=32, corner_radius=50, command=self.show_filter_menu)
        self.filter_btn.pack(side="left", padx=5)

        self.current_time_val = "All Time" 
        self.time_options = ["All Time", "Today", "This Week", "This Month", "This Year"]

        # 创建 Time 按钮 
        self.time_filter_btn = ctk.CTkButton(filter_frame, text="All Time ▼", font=("Arial", 12, "bold"), fg_color="#EEEEEE", text_color="#3838D5", hover_color="#CCCCCC", width=100, height=32, corner_radius=50, command=self.show_time_menu)
        self.time_filter_btn.pack(side="left", padx=5)

        # 定义选项列表
        self.activity_options = [
            "All Activities", "Running", "Walking", "Cycling", "Swimming",
            "Weightlifting", "Yoga", "HIIT",
            "Arm", "Abs", "Leg", "Chest", "Back"
        ]
        
        style = ttk.Style()
        style.theme_use("clam") # 使用 clam 主题作为基础，因为它容易自定义

        # 设置表头样式 (深蓝色背景，白色文字，加粗)
        style.configure("Treeview.Heading", 
                        font=("Arial", 11, "bold"), 
                        background="#3838D5", 
                        foreground="white", 
                        relief="flat")
        
        # 鼠标悬停在表头时的颜色
        style.map("Treeview.Heading", background=[('active', '#2C2CBA')])

        style.configure("Treeview", font=("Arial", 11), rowheight=30, background="white", fieldbackground="white", bordercolor="#DDDDDD", borderwidth=0)
        
        style.map("Treeview", background=[('selected', '#E1E1FF')], foreground=[('selected', 'black')])

        # 分类表格
        self.table_frame = tk.Frame(self)
        self.table_frame.pack(pady=10)
        columns = ("Activity", "Total (min)", "Intensity", "Total (kcal)")
        self.tree = ttk.Treeview(self.table_frame, columns=columns, show="headings", height=8)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100, anchor="center",stretch=False)
        self.tree.heading("#0", anchor='w') 
        self.tree.column("#0", width=100, anchor='w', stretch=False)
        self.tree.pack(side="left",expand=True)
        scrollbar = ttk.Scrollbar(self.table_frame, command=self.tree.yview)
        scrollbar.pack(side="right", fill="y")
        self.tree.configure(yscrollcommand=scrollbar.set)

        # 按钮
        btn_frame = tk.Frame(self,bg="#FFFFFF")
        btn_frame.pack(pady=5)
        self.progress_btn = ctk.CTkButton(btn_frame, text="Show Progress Comparison", font=("Arial", 13, "bold"), fg_color="#3838D5", text_color="#FFFFFF", hover_color="#6767FF", width=220, height=40, corner_radius=50, command=self.show_progress)
        self.progress_btn.pack(side="left", padx=5)

    # Self_Card 的函数
    def create_stat_card(self, parent, title, value, color, col_index):
        # 卡片容器 
        card = ctk.CTkFrame(parent, fg_color="#EEEEEE", corner_radius=15, width=180, height=80)
        card.grid(row=0, column=col_index, padx=10, sticky="ew")
        
        # 让 Grid 自动均分宽度
        parent.grid_columnconfigure(col_index, weight=1)
        card.pack_propagate(False) # 固定大小，不受内容影响

        # 标题 
        tk.Label(card, text=title, font=("Arial", 10, "bold"), fg="gray", bg="#EEEEEE").pack(pady=(15, 0))
        
        # 数值 
        val_label = tk.Label(card, text=value, font=("Arial", 20, "bold"), fg=color, bg="#EEEEEE")
        val_label.pack(pady=5)
        
        return val_label
    
    # 显示时间菜单
    def show_time_menu(self):
        menu = tk.Menu(self, tearoff=0, font=("Arial", 10))
        for option in self.time_options:
            menu.add_command(label=option, command=lambda opt=option: self.apply_time_filter(opt))
        
        x = self.time_filter_btn.winfo_rootx()
        y = self.time_filter_btn.winfo_rooty() + self.time_filter_btn.winfo_height()
        menu.post(x, y)

    # 应用时间筛选
    def apply_time_filter(self, time_opt):
        self.current_time_val = time_opt
        self.time_filter_btn.configure(text=f"{time_opt} ▼")
        self.generate_report() 

    # 刷新报告
    def generate_report(self):
        # 引入必要的日期工具

        # 检查是否有数据
        if self.log_page is None or not self.log_page.exercise_log:
            self.summary_label.config(text="No records found.")
            # 清零卡片
            self.card_workouts_val.config(text="0")
            self.card_minutes_val.config(text="0")
            self.card_calories_val.config(text="0.0")
            # 清零进度条
            self.goal_bar.set(0)
            self.goal_label.config(text=f"Goal Progress: 0 / {self.target_goal} kcal")
            # 清空表格
            for i in self.tree.get_children():
                self.tree.delete(i)
            return

        all_logs = self.log_page.exercise_log
        filtered_logs = []

        # 获取筛选状态 (Activity)
        selected_activity = getattr(self, "current_filter_val", "All")
        # 获取筛选状态 (Time) 
        selected_time = getattr(self, "current_time_val", "All Time")
        
        # 获取当前时间 
        now = datetime.now()

        # 筛选逻辑
        for log in all_logs:
            # Activity
            if selected_activity != "All" and log["activity"] != selected_activity:
                continue 
            
            # 筛选 Time 
            if "date" in log and selected_time != "All Time":
                try:
                    # 把字符串转成日期对象
                    log_date = datetime.strptime(log["date"], "%Y-%m-%d %H:%M:%S")
                    
                    if selected_time == "Today":
                        if log_date.date() != now.date(): continue
                    
                    elif selected_time == "This Week":
                        # 判断是否在同一周
                        if log_date.isocalendar()[:2] != now.isocalendar()[:2]: continue
                    
                    elif selected_time == "This Month":
                        if (log_date.month, log_date.year) != (now.month, now.year): continue
                        
                    elif selected_time == "This Year":
                        if log_date.year != now.year: continue

                except ValueError:
                    continue 

            # 如果通过筛选，加入结果列表
            filtered_logs.append(log)

        # 使用筛选后的数据进行计算
        logs = filtered_logs

        total_workouts = 0
        total_duration_all = 0
        total_calories_all = 0
        category_stats = {} 

        for log in logs:
            activity = log["activity"]
            intensity = log["intensity"]
            duration = log["hours"] * 60 + log["minutes"]
            calories = self.calculate_calories(activity, duration, log["intensity"])

            total_workouts += 1
            total_duration_all += duration
            total_calories_all += calories

            key = (activity, intensity) 

            if key not in category_stats:
                category_stats[key] = {"minutes": 0, "calories": 0}
        
            category_stats[key]["minutes"] += duration
            category_stats[key]["calories"] += calories

        # 更新顶部总览 (卡片)
        self.card_workouts_val.config(text=str(total_workouts))
        self.card_minutes_val.config(text=str(total_duration_all))
        self.card_calories_val.config(text=f"{total_calories_all:.1f}")

        # 计算百分比 
        if self.target_goal > 0:
            progress = total_calories_all / self.target_goal
        else:
            progress = 0

        # 更新进度条 
        self.goal_bar.set(min(progress, 1.0))

        # 更新文字和颜色反馈
        if progress >= 1.0:
            self.goal_bar.configure(progress_color="#2ECC71") 
            self.goal_label.config(text=f"🎉 Goal Reached! ({int(total_calories_all)} / {self.target_goal} kcal)", fg="#27AE60")
        else:
            # 未达成显示红色 (保留你的设置)
            self.goal_bar.configure(progress_color="#FF0000") 
            self.goal_label.config(text=f"Goal Progress: {int(total_calories_all)} / {self.target_goal} kcal", fg="#555555")

        # 更新表格
        for i in self.tree.get_children():
            self.tree.delete(i)

        for (activity, intensity), stats in category_stats.items():
            self.tree.insert("", "end", values=(activity, stats["minutes"], intensity, f"{stats['calories']:.1f}"))

    # 点击按钮时，弹出菜单
    def show_filter_menu(self):
        # 创建一个弹出式菜单
        menu = tk.Menu(self, tearoff=0, font=("Arial", 10))
        
        # 把所有选项加进去
        for option in self.activity_options:
            menu.add_command(label=option, command=lambda opt=option: self.apply_filter(opt))
        
        # 在按钮的下方弹出菜单
        x = self.filter_btn.winfo_rootx()
        y = self.filter_btn.winfo_rooty() + self.filter_btn.winfo_height()
        menu.post(x, y)

    # 选择某一项后执行
    def apply_filter(self, activity):
        self.current_filter_val = activity  # 更新变量
        self.filter_btn.configure(text=f"{activity} ▼")  # 更新按钮上的文字
        self.generate_report()  # 刷新报告

    # 显示进度对比
    def show_progress(self):
        # 检查数据是否足够 
        if self.log_page is None or len(self.log_page.exercise_log) < 2:
            self.show_popup_message("Not enough data for comparison.\nPlease add at least 2 records in Log Page.")
            return

        logs = self.log_page.exercise_log
        
        n = min(5, len(logs) // 2)
        first_period = logs[:n]   # 最早的 n 条
        last_period = logs[-n:]   # 最近的 n 条

        # 定义内部函数来计算总和
        def total_calories(logs_list):
            return sum(self.calculate_calories(log["activity"], log["hours"]*60+log["minutes"], log["intensity"]) for log in logs_list)

        def total_duration(logs_list):
            return sum(log["hours"]*60+log["minutes"] for log in logs_list)

        # 计算数值
        cal_first = total_calories(first_period)
        cal_last = total_calories(last_period)
        dur_first = total_duration(first_period)
        dur_last = total_duration(last_period)

        # 计算差异 
        cal_diff = cal_last - cal_first
        dur_diff = dur_last - dur_first

        # 生成显示的文字
        text = "--- Progress Comparison ---\n(First 5 vs Last 5)\n\n"
        text += f"Calories: {cal_first:.1f} -> {cal_last:.1f}  ({'+' if cal_diff>=0 else ''}{cal_diff:.1f})\n"
        text += f"Duration: {dur_first} -> {dur_last} min  ({'+' if dur_diff>=0 else ''}{dur_diff})"

        self.show_popup_message(text)
    
    #弹窗
    def show_popup_message(self, msg):
        popup = tk.Toplevel(self)
        popup.title("Progress")
        
        width, height = 350, 200
        x = self.winfo_rootx() + (self.winfo_width()//2) - (width//2)
        y = self.winfo_rooty() + (self.winfo_height()//2) - (height//2)
        popup.geometry(f"{width}x{height}+{x}+{y}")
        
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
        
        tk.Label(popup, text=msg, font=("Arial", 11), justify="left", pady=20).pack()
        ctk.CTkButton(popup, text="OK", command=popup.destroy, fg_color="#3838D5",hover_color="#6767FF", text_color="#FFFFFF",corner_radius=30, width=120,height=40).pack(pady=10)

        popup.grab_set()
        popup.focus_set()
        popup.transient(self)
       