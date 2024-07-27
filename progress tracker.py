import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import date

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
        # Project selection
        self.project_frame = ttk.Frame(self.master)
        self.project_frame.pack(pady=10)

        ttk.Label(self.project_frame, text="Project:").grid(row=0, column=0, padx=5)
        self.project_var = tk.StringVar()
        self.project_dropdown = ttk.Combobox(self.project_frame, textvariable=self.project_var)
        self.project_dropdown.grid(row=0, column=1, padx=5)
        self.project_dropdown.bind("<<ComboboxSelected>>", self.load_project)

        ttk.Button(self.project_frame, text="New Project", command=self.new_project).grid(row=0, column=2, padx=5)

        # Checkpoint frame
        self.checkpoint_frame = ttk.LabelFrame(self.master, text="Checkpoints")
        self.checkpoint_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.checkpoint_listbox = tk.Listbox(self.checkpoint_frame)
        self.checkpoint_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        checkpoint_scrollbar = ttk.Scrollbar(self.checkpoint_frame, orient=tk.VERTICAL, command=self.checkpoint_listbox.yview)
        checkpoint_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.checkpoint_listbox.config(yscrollcommand=checkpoint_scrollbar.set)

        # Checkpoint controls
        self.checkpoint_controls = ttk.Frame(self.master)
        self.checkpoint_controls.pack(pady=5)

        self.checkpoint_entry = ttk.Entry(self.checkpoint_controls, width=40)
        self.checkpoint_entry.grid(row=0, column=0, padx=5)

        ttk.Button(self.checkpoint_controls, text="Add Checkpoint", command=self.add_checkpoint).grid(row=0, column=1, padx=5)
        ttk.Button(self.checkpoint_controls, text="Complete Checkpoint", command=self.complete_checkpoint).grid(row=0, column=2, padx=5)

        # Daily log
        self.log_frame = ttk.LabelFrame(self.master, text="Daily Log")
        self.log_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.log_entry = ttk.Entry(self.log_frame, width=50)
        self.log_entry.pack(side=tk.LEFT, padx=5)

        ttk.Button(self.log_frame, text="Add Log", command=self.add_log).pack(side=tk.LEFT, padx=5)

    def new_project(self):
        project_name = tk.simpledialog.askstring("New Project", "Enter project name:")
        if project_name:
            self.projects[project_name] = {"checkpoints": [], "completed": [], "logs": []}
            self.update_project_list()
            self.project_var.set(project_name)
            self.load_project()

    def update_project_list(self):
        self.project_dropdown['values'] = list(self.projects.keys())

    def load_project(self, event=None):
        self.current_project = self.project_var.get()
        self.checkpoint_listbox.delete(0, tk.END)
        for checkpoint in self.projects[self.current_project]["checkpoints"]:
            self.checkpoint_listbox.insert(tk.END, checkpoint)
        for checkpoint in self.projects[self.current_project]["completed"]:
            self.checkpoint_listbox.insert(tk.END, f"✓ {checkpoint}")

    def add_checkpoint(self):
        checkpoint = self.checkpoint_entry.get()
        if checkpoint:
            self.projects[self.current_project]["checkpoints"].append(checkpoint)
            self.checkpoint_listbox.insert(tk.END, checkpoint)
            self.checkpoint_entry.delete(0, tk.END)

    def complete_checkpoint(self):
        selection = self.checkpoint_listbox.curselection()
        if selection:
            index = selection[0]
            checkpoint = self.checkpoint_listbox.get(index)
            if not checkpoint.startswith("✓"):
                self.projects[self.current_project]["checkpoints"].remove(checkpoint)
                self.projects[self.current_project]["completed"].append(checkpoint)
                self.checkpoint_listbox.delete(index)
                self.checkpoint_listbox.insert(tk.END, f"✓ {checkpoint}")

    def add_log(self):
        log_entry = self.log_entry.get()
        if log_entry:
            today = date.today().isoformat()
            self.projects[self.current_project]["logs"].append((today, log_entry))
            self.log_entry.delete(0, tk.END)
            messagebox.showinfo("Log Added", "Daily log entry has been added.")

    def save_data(self):
        with open("project_data.json", "w") as f:
            json.dump(self.projects, f)

    def load_data(self):
        try:
            with open("project_data.json", "r") as f:
                self.projects = json.load(f)
            self.update_project_list()
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