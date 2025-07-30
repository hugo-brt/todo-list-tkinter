import tkinter as tk
from tkinter import messagebox
import json
import os

TASKS_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)

class TodoApp:
    def __init__(self, master):
        self.master = master
        master.title("To-Do List")

        self.tasks = load_tasks()
        self.displayed_task_indices = []

        # === Dictionnaires de couleurs light/dark ===
        self.colors_light = {
            "bg": "#f0f0f0",
            "fg": "#222",
            "entry_bg": "#fff",
            "entry_fg": "#000",
            "select_bg": "#cce2ff",
            "button_bg": "#e0e0e0",
            "button_fg": "#222"
        }
        self.colors_dark = {
            "bg": "#21222c",
            "fg": "#f7f7f7",
            "entry_bg": "#2e2e38",
            "entry_fg": "#f7f7f7",
            "select_bg": "#51516a",
            "button_bg": "#282a36",
            "button_fg": "#f7f7f7"
        }
        self.dark_mode = True

        # ---------- Fenêtre principale : grid pour le responsive ----------
        master.grid_rowconfigure(2, weight=1)
        master.grid_columnconfigure(0, weight=1)

        # ----------- Section Saisie tâche/priorité -------------
        entry_frame = tk.Frame(master)
        entry_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 0))
        entry_frame.columnconfigure(1, weight=1)

        self.label_task = tk.Label(entry_frame, text="Task:")
        self.label_task.grid(row=0, column=0, sticky='w')
        self.entry = tk.Entry(entry_frame)
        self.entry.grid(row=0, column=1, padx=(0, 10), sticky="ew")

        self.label_priority = tk.Label(entry_frame, text="Priority (number):")
        self.label_priority.grid(row=0, column=2, sticky='w')

        vcmd = (master.register(self.validate_priority), '%P')
        self.entry_priority = tk.Entry(entry_frame, width=5, validate='key', validatecommand=vcmd)
        self.entry_priority.grid(row=0, column=3, padx=(0, 10))

        # ----------- Boutons d'ajout et modification ----------
        btn_frame_top = tk.Frame(master)
        btn_frame_top.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))

        self.add_button = tk.Button(btn_frame_top, text="Add Task", width=12, command=self.add_task)
        self.add_button.pack(side=tk.LEFT, padx=2)

        self.modify_priority_button = tk.Button(btn_frame_top, text="Modify Priority", width=15, command=self.modify_priority)
        self.modify_priority_button.pack(side=tk.LEFT, padx=2)

        # ----------- Bascule Dark mode --------
        self.theme_button = tk.Button(btn_frame_top, text="Light mode", width=12, command=self.toggle_theme)
        self.theme_button.pack(side=tk.LEFT, padx=8)

        # ---------------- Liste des tâches --------------------
        self.frame = tk.Frame(master)
        self.frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0,10))
        self.frame.rowconfigure(0, weight=1)
        self.frame.columnconfigure(0, weight=1)

        self.listbox = tk.Listbox(self.frame)
        self.listbox.grid(row=0, column=0, sticky="nsew")
        self.scrollbar = tk.Scrollbar(self.frame)
        self.scrollbar.grid(row=0, column=1, sticky="ns")
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox.yview)

        self.listbox.bind('<<ListboxSelect>>', self.on_select_task)
        self.update_listbox()

        # ---------- Boutons d'actions sur la sélection ----------
        btn_frame_bottom = tk.Frame(master)
        btn_frame_bottom.grid(row=3, column=0, pady=(0, 10), sticky="ew", padx=10)

        self.complete_button = tk.Button(btn_frame_bottom, text="Mark as Completed", width=18, command=self.complete_task)
        self.complete_button.pack(side=tk.LEFT, padx=2)

        self.uncomplete_button = tk.Button(btn_frame_bottom, text="Mark as Uncompleted", width=18, command=self.uncomplete_task)
        self.uncomplete_button.pack(side=tk.LEFT, padx=2)

        self.remove_button = tk.Button(btn_frame_bottom, text="Remove Task", width=14, command=self.remove_task)
        self.remove_button.pack(side=tk.LEFT, padx=2)

        # Appliquer le thème au lancement
        self.apply_theme()

    # ------------------------ Thème / Dark mode --------------------------
    def apply_theme(self):
        colors = self.colors_dark if self.dark_mode else self.colors_light
        # Fenêtre principale
        self.master.configure(bg=colors["bg"])
        # Parcourir tous les widgets manuellement pour appliquer les couleurs
        for widget in self.master.winfo_children():
            self._set_widget_theme(widget, colors)
        # Appliquer aussi à la frame de la liste
        self._set_widget_theme(self.frame, colors)
        self.listbox.config(bg=colors["entry_bg"], fg=colors["entry_fg"],
                            selectbackground=colors["select_bg"],
                            selectforeground=colors["entry_fg"])
        self.scrollbar.config(bg=colors["bg"])
        # Appliquer au contenu de la frame (listbox/scrollbar)
        for widget in self.frame.winfo_children():
            self._set_widget_theme(widget, colors)

    def _set_widget_theme(self, widget, colors):
        # Fonction utilitaire pour tous les types de widgets
        classname = widget.winfo_class()
        if classname in ("Frame",):
            widget.config(bg=colors["bg"])
            for child in widget.winfo_children():
                self._set_widget_theme(child, colors)
        elif classname in ("Label",):
            widget.config(bg=colors["bg"], fg=colors["fg"])
        elif classname in ("Entry",):
            widget.config(bg=colors["entry_bg"], fg=colors["entry_fg"],
                          insertbackground=colors["entry_fg"])
        elif classname in ("Button",):
            widget.config(bg=colors["button_bg"], fg=colors["button_fg"],
                          activebackground=colors["select_bg"], activeforeground=colors["button_fg"])
        # Listbox et Scrollbar déjà traités ailleurs

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        # Changer le texte du bouton selon le mode
        self.theme_button.config(text="Light mode" if self.dark_mode else "Dark mode")
        self.apply_theme()

    # ------------------- Fonctions classiques -------------------
    def validate_priority(self, value_if_allowed):
        return value_if_allowed.isdigit() or value_if_allowed == ""

    def update_listbox(self):
        self.listbox.delete(0, tk.END)
        self.displayed_task_indices = []
        indexed_tasks = list(enumerate(self.tasks))
        sorted_indexed_tasks = sorted(
            indexed_tasks,
            key=lambda t: (t[1]['priority'] == "" or t[1]['priority'] is None, t[1]['priority'] if t[1]['priority'] != "" else float('inf'))
        )
        for orig_idx, task in sorted_indexed_tasks:
            priority = f"(Priority: {task.get('priority', '')})" if task.get('priority') != "" else ""
            status = "[x]" if task.get('completed') else "[ ]"
            self.listbox.insert(tk.END, f"{status} {task.get('title', '')} {priority}")
            self.displayed_task_indices.append(orig_idx)

    def add_task(self):
        title = self.entry.get().strip()
        priority = self.entry_priority.get().strip()
        if not title:
            messagebox.showwarning("Input Error", "Please enter a task.")
            return
        priority_val = int(priority) if priority else ""
        self.tasks.append({'title': title, 'priority': priority_val, 'completed': False})
        save_tasks(self.tasks)
        self.entry.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)
        self.update_listbox()

    def complete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to mark as completed.")
            return
        displayed_idx = selection[0]
        real_idx = self.displayed_task_indices[displayed_idx]
        self.tasks[real_idx]['completed'] = True
        save_tasks(self.tasks)
        self.update_listbox()

    def uncomplete_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to mark as uncompleted.")
            return
        displayed_idx = selection[0]
        real_idx = self.displayed_task_indices[displayed_idx]
        self.tasks[real_idx]['completed'] = False
        save_tasks(self.tasks)
        self.update_listbox()

    def remove_task(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to remove.")
            return
        displayed_idx = selection[0]
        real_idx = self.displayed_task_indices[displayed_idx]
        del self.tasks[real_idx]
        save_tasks(self.tasks)
        self.update_listbox()
        self.entry.delete(0, tk.END)
        self.entry_priority.delete(0, tk.END)

    def modify_priority(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showwarning("Selection Error", "Please select a task to modify its priority.")
            return
        displayed_idx = selection[0]
        real_idx = self.displayed_task_indices[displayed_idx]
        priority = self.entry_priority.get().strip()
        if priority == "":
            self.tasks[real_idx]['priority'] = ""
        else:
            self.tasks[real_idx]['priority'] = int(priority)
        save_tasks(self.tasks)
        self.update_listbox()

    def on_select_task(self, event):
        selection = self.listbox.curselection()
        if selection:
            displayed_idx = selection[0]
            real_idx = self.displayed_task_indices[displayed_idx]
            task = self.tasks[real_idx]
            self.entry.delete(0, tk.END)
            self.entry.insert(0, task.get('title', ''))
            self.entry_priority.delete(0, tk.END)
            prio = str(task.get('priority')) if task.get('priority') != "" else ""
            self.entry_priority.insert(0, prio)

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.minsize(400, 300)
    root.mainloop()
