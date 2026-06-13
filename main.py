import tkinter as tk
from tkinter import messagebox
from tkinter import simpledialog

from storage import load_data, save_data
from pomodoro import PomodoroTimer


BG = "#1e1e1e"
SIDEBAR = "#252526"
TEXT = "#d4d4d4"
ACCENT = "#007acc"


class ProductivityApp:

    def __init__(self, root):
        self.root = root

        self.root.title("Productivity")
        self.root.geometry("1100x700")
        self.root.configure(bg=BG)

        self.data = load_data()
        self.timer = PomodoroTimer()

        self.build_ui()
        self.update_timer()

    def build_ui(self):

        sidebar = tk.Frame(
            self.root,
            bg=SIDEBAR,
            width=250
        )

        sidebar.pack(side="left", fill="y")

        main = tk.Frame(
            self.root,
            bg=BG
        )

        main.pack(
            side="right",
            fill="both",
            expand=True
        )

        title = tk.Label(
            sidebar,
            text="PRODUCTIVITY",
            bg=SIDEBAR,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        )

        title.pack(pady=15)

        self.workspace_list = tk.Listbox(
            sidebar,
            bg=BG,
            fg=TEXT,
            selectbackground=ACCENT,
            relief="flat"
        )

        self.workspace_list.pack(
            fill="both",
            expand=True,
            padx=10
        )

        for workspace in self.data["workspaces"]:
            self.workspace_list.insert(
                tk.END,
                workspace["name"]
            )

        tk.Button(
            sidebar,
            text="New Workspace",
            command=self.create_workspace,
            bg=ACCENT,
            fg="white",
            relief="flat"
        ).pack(fill="x", padx=10, pady=5)

        tk.Button(
            sidebar,
            text="Launch Workspace",
            command=self.launch_workspace,
            bg=ACCENT,
            fg="white",
            relief="flat"
        ).pack(fill="x", padx=10, pady=5)

        self.timer_label = tk.Label(
            main,
            text="25:00",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 48)
        )

        self.timer_label.pack(pady=20)

        controls = tk.Frame(main, bg=BG)
        controls.pack()

        tk.Button(
            controls,
            text="Start/Pause",
            command=self.timer.toggle
        ).pack(side="left", padx=5)

        tk.Button(
            controls,
            text="Reset",
            command=self.reset_timer
        ).pack(side="left", padx=5)

        notes_label = tk.Label(
            main,
            text="Notes",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 14)
        )

        notes_label.pack(anchor="w", padx=20, pady=(20, 0))

        self.notes = tk.Text(
            main,
            bg="#252526",
            fg=TEXT,
            insertbackground=TEXT,
            relief="flat"
        )

        self.notes.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.notes.insert(
            "1.0",
            self.data["notes"]
        )

        tk.Button(
            main,
            text="Save Notes",
            command=self.save_notes,
            bg=ACCENT,
            fg="white",
            relief="flat"
        ).pack(pady=10)

    def save_notes(self):

        self.data["notes"] = self.notes.get(
            "1.0",
            tk.END
        )

        save_data(self.data)

        messagebox.showinfo(
            "Saved",
            "Notes saved."
        )

    def create_workspace(self):

        name = simpledialog.askstring(
            "Workspace",
            "Workspace name:"
        )

        if not name:
            return

        instructions = simpledialog.askstring(
            "Instructions",
            "Apps to open/close?"
        )

        workspace = {
            "name": name,
            "instructions": instructions
        }

        self.data["workspaces"].append(workspace)

        save_data(self.data)

        self.workspace_list.insert(
            tk.END,
            name
        )

    def launch_workspace(self):

        selected = self.workspace_list.curselection()

        if not selected:
            return

        workspace = self.data["workspaces"][
            selected[0]
        ]

        messagebox.showinfo(
            workspace["name"],
            workspace["instructions"]
        )

    def reset_timer(self):
        self.timer.reset()

    def update_timer(self):

        finished = self.timer.tick()

        self.timer_label.config(
            text=self.timer.time_string()
        )

        if finished:

            if self.timer.on_break:
                messagebox.showinfo(
                    "Break",
                    "Time for a break."
                )
            else:
                messagebox.showinfo(
                    "Focus",
                    "Back to work."
                )

        self.root.after(
            1000,
            self.update_timer
        )


root = tk.Tk()
app = ProductivityApp(root)
root.mainloop()