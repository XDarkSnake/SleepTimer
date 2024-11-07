import customtkinter as ctk
import os
import tkinter.messagebox as msgbox

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

time_left, sleep_type, timer_running = 0, None, False

def start_timer(action_type):
    global time_left, sleep_type, timer_running
    try:
        time_left = int(entry_time.get()) * 60
        sleep_type, timer_running = action_type, True
        btn_pause_resume.configure(state="normal", text="II")
        btn_stop_timer.pack(pady=10)
        update_timer()
    except ValueError:
        msgbox.showerror("Erreur", "Entrez un nombre valide.")

def update_timer():
    global time_left, timer_running
    if timer_running:
        mins, secs = divmod(time_left, 60)
        label_timer.configure(text=f"{mins:02}:{secs:02}")
        if time_left > 0:
            time_left -= 1
            root.after(1000, update_timer)
        else:
            timer_running = False
            btn_pause_resume.configure(state="disabled")
            btn_stop_timer.pack_forget()
            trigger_action()

def toggle_pause():
    global timer_running
    timer_running = not timer_running
    btn_pause_resume.configure(text="II" if timer_running else "||")
    if timer_running:
        update_timer()

def stop_timer():
    global timer_running
    timer_running = False
    label_timer.configure(text="00:00")
    btn_pause_resume.configure(state="disabled", text="II")
    btn_stop_timer.pack_forget()

def trigger_action():
    actions = {
        "sleep": "rundll32.exe powrprof.dll,SetSuspendState Sleep",
        "hibernate": "rundll32.exe powrprof.dll,SetSuspendState Hibernate",
        "shutdown": "shutdown /s /t 1"
    }
    os.system(actions.get(sleep_type, ""))

root = ctk.CTk()
root.title("Minuteur de mise en veille")
root.geometry("450x350")

ctk.CTkLabel(root, text="Temps :").pack(pady=10)
entry_time = ctk.CTkEntry(root, width=120)
entry_time.pack(pady=5)

button_frame = ctk.CTkFrame(root)
button_frame.pack(pady=10)

ctk.CTkButton(button_frame, text="Veille", command=lambda: start_timer("sleep")).grid(row=0, column=0, padx=5)
ctk.CTkButton(button_frame, text="Veille prolongée", command=lambda: start_timer("hibernate")).grid(row=0, column=1, padx=5)
ctk.CTkButton(button_frame, text="Arrêt", command=lambda: start_timer("shutdown")).grid(row=0, column=2, padx=5)

label_timer = ctk.CTkLabel(root, text="00:00", font=("Helvetica", 20))
label_timer.pack(pady=20)

btn_pause_resume = ctk.CTkButton(root, text="II", command=toggle_pause, state="disabled", width=50, height=50)
btn_pause_resume.pack(pady=10)

btn_stop_timer = ctk.CTkButton(root, text="■", command=stop_timer, fg_color="red", width=50, height=50)
btn_stop_timer.pack_forget()

root.mainloop()
