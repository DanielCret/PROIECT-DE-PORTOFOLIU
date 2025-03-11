
import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from main import Task, session  # Import modelul Task și sesiunea
from task_notifier import daemon_thread  # Import thread-ul de notificare


# adăug un task
def add_task():
    title = title_entry.get()
    description = description_entry.get("1.0", tk.END).strip()
    deadline_str = deadline_entry.get()

    if not title or not deadline_str:
        messagebox.showerror("Eroare", "Titlul și data limită sunt obligatorii!")
        return

    try:
        deadline = datetime.strptime(deadline_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        messagebox.showerror("Eroare", "Formatul datei trebuie să fie YYYY-MM-DD HH:MM:SS")
        return

    new_task = Task(title=title, description=description, deadline=deadline, status="pending")
    session.add(new_task)
    session.commit()

    messagebox.showinfo("Succes", "Task adăugat cu succes!")
    title_entry.delete(0, tk.END)
    description_entry.delete("1.0", tk.END)
    deadline_entry.delete(0, tk.END)



# Creez fereastră principală
root = tk.Tk()
root.title("Task Manager")
root.geometry("400x350")

# fac etichete si campuri pentru input
tk.Label(root, text="Titlu:").pack()
title_entry = tk.Entry(root)
title_entry.pack()

tk.Label(root, text="Descriere:").pack()
description_entry = tk.Text(root, height=5, width=40)
description_entry.pack()

tk.Label(root, text="Deadline (YYYY-MM-DD HH:MM:SS):").pack()
deadline_entry = tk.Entry(root)
deadline_entry.pack()

# butonul pentru a adauga task
tk.Button(root, text="Adaugă Task", command=add_task).pack()

# Eticheta pentru notificări
notification_label = tk.Label(root, text="", fg="red")
notification_label.pack()

# Pornesc thread-ul de notificare doar dacă nu rulează deja
if not daemon_thread.is_alive():
    daemon_thread.start()

# Rulez  interfața
root.mainloop()