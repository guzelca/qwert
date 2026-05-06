import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Предопределённые задачи с типами
PREDEFINED_TASKS = [
    {"name": "Прочитать статью", "type": "учёба"},
    {"name": "Сделать зарядку", "type": "спорт"},
    {"name": "Написать отчёт", "type": "работа"},
    {"name": "Посмотреть лекцию", "type": "учёба"},
    {"name": "Сходить на пробежку", "type": "спорт"},
    {"name": "Провести встречу", "type": "работа"},
]

HISTORY_FILE = "tasks.json"

class TaskGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Task Generator")
        self.history = self.load_history()
        self.current_task = None

        # Виджеты
        self.task_label = tk.Label(root, text="Ваша задача появится здесь", font=("Arial", 14))
        self.task_label.pack(pady=10)

        self.generate_btn = tk.Button(root, text="Сгенерировать задачу", command=self.generate_task)
        self.generate_btn.pack(pady=5)

        self.filter_var = tk.StringVar(value="все")
        filter_frame = tk.Frame(root)
        filter_frame.pack(pady=5)
        tk.Label(filter_frame, text="Фильтр по типу:").pack(side=tk.LEFT)
        ttk.Combobox(filter_frame, textvariable=self.filter_var,
                     values=["все", "учёба", "спорт", "работа"], state="readonly").pack(side=tk.LEFT)

        self.history_listbox = tk.Listbox(root, width=50, height=10)
        self.history_listbox.pack(pady=10)

        self.add_task_entry = tk.Entry(root, width=40)
        self.add_task_entry.pack(pady=5)
        self.add_type_entry = ttk.Combobox(root, values=["учёба", "спорт", "работа"], state="readonly")
        self.add_type_entry.set("учёба")
        self.add_type_entry.pack(pady=5)
        self.add_btn = tk.Button(root, text="Добавить задачу", command=self.add_custom_task)
        self.add_btn.pack(pady=5)

    def generate_task(self):
        filter_type = self.filter_var.get()
        if filter_type == "все":
            pool = PREDEFINED_TASKS + [t for t in self.history]
        else:
            pool = [t for t in PREDEFINED_TASKS + self.history if t["type"] == filter_type]

        if not pool:
            messagebox.showwarning("Нет задач", "Нет задач для выбранного фильтра.")
            return

        task = random.choice(pool)
        self.current_task = task
        self.task_label.config(text=f"Задача: {task['name']} ({task['type']})")

    def add_custom_task(self):
        name = self.add_task_entry.get().strip()
        task_type = self.add_type_entry.get()
        if not name:
            messagebox.showerror("Ошибка", "Название задачи не может быть пустым.")
            return
        new_task = {"name": name, "type": task_type}
        self.history.append(new_task)
        self.save_history()
        self.update_history_listbox()
        self.add_task_entry.delete(0, tk.END)

    def load_history(self):
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_history(self):
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(self.history, f, ensure_ascii=False, indent=2)

    def update_history_listbox(self):
        self.history_listbox.delete(0, tk.END)
        for task in self.history:
            self.history_listbox.insert(tk.END, f"{task['name']} ({task['type']})")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskGeneratorApp(root)
    root.mainloop()