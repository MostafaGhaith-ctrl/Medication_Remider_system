import customtkinter as ctk
from tkinter import messagebox
import threading
import schedule
import time
import datetime
from plyer import notification
import os

# UI Appearance Settings
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MedicationApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Medical Scheduler System - Mostafa Ghaith")
        self.geometry("600x450")

        self.label = ctk.CTkLabel(self, text="💊 Medication Management System", font=("Arial", 24, "bold"))
        self.label.pack(pady=20)

        self.info_box = ctk.CTkTextbox(self, width=500, height=200, font=("Arial", 14))
        self.info_box.pack(pady=10)
        self.info_box.insert("0.0", "--- System Logs Active ---\n")

        self.status_label = ctk.CTkLabel(self, text="Status: Monitoring Active ✅", text_color="#50C878")
        self.status_label.pack(pady=10)

        self.open_btn = ctk.CTkButton(self, text="View Report File", command=self.open_report)
        self.open_btn.pack(pady=10)

        threading.Thread(target=self.run_scheduler, daemon=True).start()

    def save_log(self, med, status):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("medication_report.txt", "a", encoding="utf-8") as f:
            f.write(f"[{now}] Medication: {med} | Status: {status}\n")
        self.info_box.insert("end", f"[{now}] {med}: {status}\n")
        self.info_box.see("end")

    def alert_patient(self, med):
        """This function handles the reminder and the 'Zannnan' (Snooze) logic."""
        taken = False

        while not taken:
            # 1. Show System Notification
            try:
                notification.notify(
                    title="URGENT: Medication Reminder",
                    message=f"Please take your: {med} now!",
                    timeout=10
                )
            except:
                pass

            # 2. Beep sound (Windows only)
            try:
                import winsound
                winsound.Beep(1000, 500)  # Frequency: 1000Hz, Duration: 500ms
            except:
                pass

            # 3. Ask the user
            ans = messagebox.askyesno("Medical Alert",
                                      f"Did you take your ({med})?\n\nSelecting 'No' will trigger a reminder again in 30 seconds.")

            if ans:
                self.save_log(med, "Taken ✅")
                taken = True
            else:
                self.save_log(med, "Skipped - Retrying in 30s ⏳")
                # Wait for 30 seconds before 'Zann' again
                time.sleep(30)

    def open_report(self):
        if os.path.exists("medication_report.txt"):
            os.startfile("medication_report.txt")
        else:
            messagebox.showinfo("Information", "No report logs found yet.")

    def run_scheduler(self):
        # ⚠️ Adjust the time for testing
        schedule.every().day.at("15:17").do(
            lambda: threading.Thread(target=self.alert_patient, args=("Panadol",)).start())

        while True:
            schedule.run_pending()
            time.sleep(1)


if __name__ == "__main__":
    app = MedicationApp()
    app.mainloop()