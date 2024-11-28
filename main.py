import cv2
from pyzbar.pyzbar import decode
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import threading

class QRCodeApp:
    def __init__(self, root):
        self.root = root
        self.root.title("QR Code Scanner")
        self.root.geometry("800x600")
        self.root.configure(bg="#282c34")

        self.label = tk.Label(self.root, text="QR Code Scanner", font=("Arial", 24), bg="#282c34", fg="white")
        self.label.pack(pady=20)

        self.video_frame = tk.Label(self.root)
        self.video_frame.pack()

        self.start_button = tk.Button(self.root, text="Start Scanning", font=("Arial", 16), bg="#4caf50", fg="white",
                                      command=self.start_scanning)
        self.start_button.pack(pady=10)

        self.stop_button = tk.Button(self.root, text="Stop Scanning", font=("Arial", 16), bg="#f44336", fg="white",
                                     command=self.stop_scanning, state=tk.DISABLED)
        self.stop_button.pack(pady=10)

        self.cap = cv2.VideoCapture(0)
        self.running = False
        self.scanning_thread = None

    def start_scanning(self):
        self.running = True
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.scanning_thread = threading.Thread(target=self.scan_qr)
        self.scanning_thread.start()

    def stop_scanning(self):
        self.running = False
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def scan_qr(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            qr_codes = decode(frame)
            for qr_code in qr_codes:
                data = qr_code.data.decode("utf-8")
                self.display_message(data)
                self.running = False
                self.stop_scanning()
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(frame)
            img_tk = ImageTk.PhotoImage(image=img)
            self.video_frame.img_tk = img_tk
            self.video_frame.config(image=img_tk)

        self.cap.release()

    def display_message(self, data):
        messagebox.showinfo("QR Code Detected", f"Data: {data}")

    def on_closing(self):
        self.running = False
        if self.cap.isOpened():
            self.cap.release()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = QRCodeApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()
