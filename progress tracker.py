import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

class ProjectSelectionDialog:
    def __init__(self, parent, title, projects):
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("300x200")
        self.result = None

        frame = ttk.Frame(self.top)
        frame.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.listbox = tk.Listbox(frame)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        for project in projects:
            self.listbox.insert(tk.END, project)

        self.listbox.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(frame)
        button_frame.pack(fill=tk.X, pady=10)

        ttk.Button(button_frame, text="OK", command=self.on_ok).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancel", command=self.on_cancel).pack(side=tk.RIGHT, padx=5)

    def on_double_click(self, event):
        self.on_ok()

    def on_ok(self):
        selection = self.listbox.curselection()
        if selection:
            self.result = self.listbox.get(selection[0])
            self.top.destroy()

    def on_cancel(self):
        self.top.destroy()

class ProjectManager:
    def __init__(self, master):
        self.master = master
        self.master.title("Project Manager")
        self.master.geometry("800x600")

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

        self.status_bar = ttk.Progressbar(self.status_frame, length=600, mode='determinate')
        self.status_bar.pack(pady=10)

        self.status_label = ttk.Label(self.status_frame, text="No project selected")
        self.status_label.pack()

        self.task_frame = ttk.LabelFrame(self.master, text="Tasks")
        self.task_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.task_canvas = tk.Canvas(self.task_frame, bg="#323232")
        self.task_canvas.pack(side="left", fill=tk.BOTH, expand=True)

        self.scrollbar = ttk.Scrollbar(self.task_frame, orient="vertical", command=self.task_canvas.yview)
        self.scrollbar.pack(side="right", fill="y")

        self.task_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.task_canvas.bind('<Configure>', self.on_canvas_configure)

        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10, fill=tk.X)

        button_frame_bottom = ttk.Frame(self.button_frame)
        button_frame_bottom.pack(expand=True)

        ttk.Button(button_frame_bottom, text="Add Task", command=self.add_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_bottom, text="Complete Task", command=self.complete_task).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_bottom, text="Remove Task", command=self.remove_task).pack(side=tk.LEFT, padx=5)

    def on_canvas_configure(self):
        self.task_canvas.configure(scrollregion=self.task_canvas.bbox("all"))

    def select_project(self):
        if not self.projects:
            messagebox.showinfo("No Projects", "There are no projects. Please add a project first.")
            return
        
        dialog = ProjectSelectionDialog(self.master, "Select Project", self.projects.keys())
        self.master.wait_window(dialog.top)
        
        if dialog.result:
            self.current_project = dialog.result
            self.load_project()

    def new_project(self):
        project_name = simpledialog.askstring("New Project", "Enter project name:")
        if project_name and project_name not in self.projects:
            self.projects[project_name] = {"tasks": [], "completed": []}
            self.current_project = project_name
            self.load_project()
        elif project_name in self.projects:
            messagebox.showerror("Error", "Project already exists")

    def remove_project(self):
        if not self.projects:
            messagebox.showinfo("No Projects", "There are no projects to remove.")
            return
        
        dialog = ProjectSelectionDialog(self.master, "Remove Project", self.projects.keys())
        self.master.wait_window(dialog.top)
        
        if dialog.result:
            if messagebox.askyesno("Remove Project", f"Are you sure you want to remove the project '{dialog.result}'?"):
                del self.projects[dialog.result]
                if self.current_project == dialog.result:
                    self.current_project = None
                    self.task_canvas.delete("all")
                    self.master.title("Project Manager")
                    self.update_status_bar()
                messagebox.showinfo("Project Removed", f"Project '{dialog.result}' has been removed.")

    def load_project(self):
        if self.current_project:
            self.master.title(f"Project Manager - {self.current_project}")
            self.update_task_list()
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
            self.update_status_bar()
        else:
            messagebox.showerror("Error", "Task not found or already completed")

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