import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ProjectManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Project Manager")
        self.master.geometry("1000x900")

        self.projects = {}
        self.current_project = None

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        self.style = ttk.Style()
        self.style.configure("TButton", background="#1c0b9c", foreground="white")

        self.project_frame = ttk.Frame(self.master)
        self.project_frame.pack(pady=10, fill=tk.X)

        button_frame_top = ttk.Frame(self.project_frame)
        button_frame_top.pack(expand=True)

        ttk.Button(button_frame_top, text="New Project", command=self.new_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_top, text="Select Project", command=self.select_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_top, text="Remove Project", command=self.remove_project).pack(side=tk.LEFT, padx=5)

        self.status_frame = ttk.LabelFrame(self.master, text="Project Progress")
        self.status_frame.pack(pady=10, padx=10, fill=tk.X)

        self.status_bar = ttk.Progressbar(self.status_frame, length=900, mode='determinate')
        self.status_bar.pack(pady=10)

        self.status_label = ttk.Label(self.status_frame, text="No project selected")
        self.status_label.pack()

        self.task_frame = ttk.LabelFrame(self.master, text="Tasks")
        self.task_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.task_canvas = tk.Canvas(self.task_frame, bg="#323232")
        self.task_canvas.pack(fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10, fill=tk.X)

        button_frame_bottom = ttk.Frame(self.button_frame)
        button_frame_bottom.pack(expand=True)

        ttk.Button(button_frame_bottom, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_bottom, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_bottom, text="Remove Task", command=self.remove_task).pack(side=tk.LEFT, padx=5)

        self.charts_frame = ttk.LabelFrame(self.master, text="Statistics")
        self.charts_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.pie_chart_frame = ttk.Frame(self.charts_frame)
        self.pie_chart_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.bar_chart_frame = ttk.Frame(self.charts_frame)
        self.bar_chart_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def select_project(self):
        project_list = list(self.projects.keys())
        if not project_list:
            messagebox.showinfo("No Projects", "There are no projects. Please add a project first.")
            return
        project_name = simpledialog.askstring("Select Project", "Choose a project:", initialvalue=project_list[0])
        if project_name in self.projects:
            self.current_project = project_name
            self.load_project()
        elif project_name:
            messagebox.showerror("Error", "Project does not exist")

    def new_project(self):
        project_name = simpledialog.askstring("New Project", "Enter project name:")
        if project_name and project_name not in self.projects:
            self.projects[project_name] = {"tasks": [], "completed": []}
            self.current_project = project_name
            self.load_project()
            self.update_charts()
            self.update_status_bar()
        elif project_name in self.projects:
            messagebox.showerror("Error", "Project already exists")

    def remove_project(self):
        if self.current_project:
            if messagebox.askyesno("Remove Project", f"Are you sure you want to remove the project '{self.current_project}'?"):
                del self.projects[self.current_project]
                self.current_project = None
                self.task_canvas.delete("all")
                self.master.title("Project Manager")
                self.update_charts()
                self.update_status_bar()
        else:
            messagebox.showerror("Error", "No project selected")

    def load_project(self):
        if self.current_project:
            self.master.title(f"Project Manager - {self.current_project}")
            self.update_task_list()
            self.update_charts()
            self.update_status_bar()

    def update_task_list(self):
        self.task_canvas.delete("all")
        y_offset = 10
        for task in self.projects[self.current_project]["tasks"]:
            self.draw_task(task, y_offset, completed=False)
            y_offset += 40
        for task in self.projects[self.current_project]["completed"]:
            self.draw_task(task, y_offset, completed=True)
            y_offset += 40

    def draw_task(self, task, y_offset, completed=False):
        x1, y1 = 10, y_offset
        x2, y2 = 100, y_offset + 30
        fill_color = "#1c0b9c"
        self.task_canvas.create_rectangle(x1, y1, x2, y2, fill=fill_color, outline="black", width=2, tags="task")
        text = f"{task} ✓" if completed else task
        self.task_canvas.create_text(x1 + 10, (y1 + y2) / 2, text=text, anchor="w", tags="task")

    def add_task(self):
        if not self.current_project:
            messagebox.showerror("Error", "Please select a project first")
            return
        task = simpledialog.askstring("Add Task", "Enter task name:")
        if task:
            self.projects[self.current_project]["tasks"].append(task)
            self.update_task_list()
            self.update_charts()
            self.update_status_bar()

    def remove_task(self):
        if not self.current_project:
            messagebox.showerror("Error", "Please select a project first")
            return
        task = simpledialog.askstring("Remove Task", "Enter task name to remove:")
        if task:
            if task in self.projects[self.current_project]["tasks"]:
                self.projects[self.current_project]["tasks"].remove(task)
            elif task in self.projects[self.current_project]["completed"]:
                self.projects[self.current_project]["completed"].remove(task)
            else:
                messagebox.showerror("Error", "Task not found")
                return
            self.update_task_list()
            self.update_charts()
            self.update_status_bar()

    def complete_task(self):
        if not self.current_project:
            messagebox.showerror("Error", "Please select a project first")
            return
        task = simpledialog.askstring("Complete Task", "Enter task name to complete:")
        if task and task in self.projects[self.current_project]["tasks"]:
            self.projects[self.current_project]["tasks"].remove(task)
            self.projects[self.current_project]["completed"].append(task)
            self.update_task_list()
            self.update_charts()
            self.update_status_bar()
        else:
            messagebox.showerror("Error", "Task not found or already completed")

    def update_charts(self):
        self.update_pie_chart()
        self.update_bar_chart()

    def update_pie_chart(self):
        for widget in self.pie_chart_frame.winfo_children():
            widget.destroy()

        if self.current_project:
            completed = len(self.projects[self.current_project]["completed"])
            uncompleted = len(self.projects[self.current_project]["tasks"])
            
            fig, ax = plt.subplots(figsize=(4, 3))
            ax.pie([completed, uncompleted], labels=['Completed', 'Uncompleted'], autopct='%1.1f%%')
            ax.set_title(f"Task Status for {self.current_project}")

            canvas = FigureCanvasTkAgg(fig, master=self.pie_chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_bar_chart(self):
        for widget in self.bar_chart_frame.winfo_children():
            widget.destroy()

        project_names = list(self.projects.keys())
        task_counts = [len(project["tasks"]) + len(project["completed"]) for project in self.projects.values()]

        fig, ax = plt.subplots(figsize=(4, 3))
        ax.bar(project_names, task_counts)
        ax.set_title("Tasks per Project")
        ax.set_xlabel("Projects")
        ax.set_ylabel("Number of Tasks")
        plt.xticks(rotation=45, ha='right')

        canvas = FigureCanvasTkAgg(fig, master=self.bar_chart_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def update_status_bar(self):
        if self.current_project:
            completed = len(self.projects[self.current_project]["completed"])
            total = completed + len(self.projects[self.current_project]["tasks"])
            if total > 0:
                progress = (completed / total) * 100
                self.status_bar['value'] = progress
                self.status_label.config(text=f"Progress: {completed}/{total} tasks completed ({progress:.1f}%)")
            else:
                self.status_bar['value'] = 0
                self.status_label.config(text="No tasks in this project")
        else:
            self.status_bar['value'] = 0
            self.status_label.config(text="No project selected")

    def save_data(self):
        with open("project_data.json", "w") as f:
            json.dump(self.projects, f)

    def load_data(self):
        try:
            with open("project_data.json", "r") as f:
                self.projects = json.load(f)
        except FileNotFoundError:
            pass

    def on_closing(self):
        self.save_data()
        self.master.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ProjectManager(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()