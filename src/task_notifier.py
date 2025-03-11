import threading
import time
from datetime import datetime, timedelta
from main import Task, session
import tkinter as tk
from tkinter import messagebox


def check_deadlines():
    while True:
        now = datetime.now()
        five_minutes_later = now + timedelta(minutes=5)

        # Selectez task-urile care sunt "pending" și au deadline în mai puțin de 5 minute
        tasks = session.query(Task).filter(Task.status == "pending", Task.deadline <= five_minutes_later,
                                           Task.deadline > now).all()

        for task in tasks:
            show_notification(task)

        # Marchez task-urile ca "completed" dacă deadline-ul a trecut
        expired_tasks = session.query(Task).filter(Task.status == "pending", Task.deadline <= now).all()
        for task in expired_tasks:
            task.status = "completed"
        session.commit()

        time.sleep(60)  # Verific la fiecare minut


def show_notification(task):
    def remind_later():
        messagebox.showinfo("Amânare", "Veți fi reamintit peste 1 minut!")
        threading.Timer(60, lambda: show_notification(task)).start()
        notif_window.destroy()

    def dismiss():
        # Nu-mi mai reamintește
        notif_window.destroy()

    notif_window = tk.Toplevel()
    notif_window.title("Task Aproape Expirat!")
    tk.Label(notif_window, text=f"⚠ Task-ul '{task.title}' are deadline la {task.deadline}!").pack()
    tk.Button(notif_window, text="Reamintește-mi mai târziu", command=remind_later).pack()
    tk.Button(notif_window, text="Finalizat", command=dismiss).pack()


# Creez thread pentru notificări
daemon_thread = threading.Thread(target=check_deadlines, daemon=True)
