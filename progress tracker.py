import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json

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

        ttk.Button(button_frame_top, text="Select Project", command=self.select_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_top, text="New Project", command=self.new_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_top, text="Remove Project", command=self.remove_project).pack(side=tk.LEFT, padx=5)

        self.checkpoint_frame = ttk.LabelFrame(self.master, text="Checkpoints")
        self.checkpoint_frame.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

        self.checkpoint_listbox = tk.Listbox(self.checkpoint_frame, bg="black", fg="white")
        self.checkpoint_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.master)
        self.button_frame.pack(pady=10, fill=tk.X)

        button_frame_bottom = ttk.Frame(self.button_frame)
        button_frame_bottom.pack(expand=True)

        ttk.Button(button_frame_bottom, text="Add Checkpoint", command=self.add_checkpoint).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_bottom, text="Remove Checkpoint", command=self.remove_checkpoint).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame_bottom, text="Complete Checkpoint", command=self.complete_checkpoint).pack(side=tk.LEFT, padx=5)

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
            self.projects[project_name] = {"checkpoints": [], "completed": []}
            self.current_project = project_name
            self.load_project()
        elif project_name in self.projects:
            messagebox.showerror("Error", "Project already exists")

    def remove_project(self):
        if self.current_project:
            if messagebox.askyesno("Remove Project", f"Are you sure you want to remove the project '{self.current_project}'?"):
                del self.projects[self.current_project]
                self.current_project = None
                self.checkpoint_listbox.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "No project selected")

    def load_project(self):
        if self.current_project:
            self.master.title(f"Project Manager - {self.current_project}")
            self.update_checkpoint_list()

    def update_checkpoint_list(self):
        self.checkpoint_listbox.delete(0, tk.END)
        for checkpoint in self.projects[self.current_project]["checkpoints"]:
            self.checkpoint_listbox.insert(tk.END, checkpoint)
        for checkpoint in self.projects[self.current_project]["completed"]:
            self.checkpoint_listbox.insert(tk.END, f"✓ {checkpoint}")

    def add_checkpoint(self):
        if not self.current_project:
            messagebox.showerror("Error", "Please select a project first")
            return
        checkpoint = simpledialog.askstring("Add Checkpoint", "Enter checkpoint name:")
        if checkpoint:
            self.projects[self.current_project]["checkpoints"].append(checkpoint)
            self.update_checkpoint_list()

    def remove_checkpoint(self):
        if not self.current_project:
            messagebox.showerror("Error", "Please select a project first")
            return
        selection = self.checkpoint_listbox.curselection()
        if selection:
            index = selection[0]
            checkpoint = self.checkpoint_listbox.get(index)
            if checkpoint.startswith("✓ "):
                checkpoint = checkpoint[2:]
                self.projects[self.current_project]["completed"].remove(checkpoint)
            else:
                self.projects[self.current_project]["checkpoints"].remove(checkpoint)
            self.update_checkpoint_list()
        else:
            messagebox.showerror("Error", "Please select a checkpoint to remove")

    def complete_checkpoint(self):
        if not self.current_project:
            messagebox.showerror("Error", "Please select a project first")
            return
        selection = self.checkpoint_listbox.curselection()
        if selection:
            index = selection[0]
            checkpoint = self.checkpoint_listbox.get(index)
            if not checkpoint.startswith("✓"):
                self.projects[self.current_project]["checkpoints"].remove(checkpoint)
                self.projects[self.current_project]["completed"].append(checkpoint)
                self.update_checkpoint_list()
        else:
            messagebox.showerror("Error", "Please select a checkpoint to complete")

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