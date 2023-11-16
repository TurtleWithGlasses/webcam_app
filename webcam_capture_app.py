import tkinter as tk
from tkinter import ttk, messagebox
import cv2
from PIL import Image, ImageTk
import os
import subprocess
from datetime import datetime
import numpy as np

class WebcamApp:
    def __init__(self, window, window_title):
        self.window = window
        self.window.title(window_title)
        self.window.geometry("700x700")

        self.style = ttk.Style()
        self.style.theme_use("vista")

        # Create a button to capture an image
        self.capture_button = ttk.Button(self.window, text="Capture Image", command=self.capture_image, style="TButton")
        self.capture_button.pack(side=tk.BOTTOM, pady=10)

        # Create a button to open the folder
        self.open_folder_button = ttk.Button(self.window, text="Open Folder", command=self.open_folder, style="TButton")
        self.open_folder_button.pack(side=tk.BOTTOM, pady=10)

        # Create a button to start/stop the webcam
        self.start_button = ttk.Button(self.window, text="Start", command=self.toggle_webcam, style="TButton")
        self.start_button.pack(side=tk.BOTTOM, pady=10)

        # Define the folder to save captured images
        self.save_folder = "C:/Users/mhmts/captured_images"  # Change this path as needed

        # Ensure the folder exists, create it if necessary
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)

        # Initialize the webcam
        self.cap = None

        # Create a label to display the webcam feed
        self.video_label = tk.Label(self.window, background="dark gray")
        self.video_label.pack(side=tk.TOP, expand=True)

        # Display a black image initially
        black_image = np.zeros((480, 640, 3), dtype=np.uint8)
        black_pil_image = Image.fromarray(black_image)
        black_imgtk = ImageTk.PhotoImage(image=black_pil_image)
        self.video_label.configure(image=black_imgtk)
        self.video_label.imgtk = black_imgtk

        # Variable to track whether the webcam is currently running
        self.webcam_running = False

    def toggle_webcam(self):
        # Toggle between starting and stopping the webcam
        if not self.webcam_running:
            self.start_webcam()
        else:
            self.stop_webcam()

    def start_webcam(self):
        # Start the webcam
        if self.cap is None or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            messagebox.showinfo("Webcam Started", "Webcam is now running.")
            self.webcam_running = True
            self.update()
            self.start_button.config(text="Stop")
        else:
            messagebox.showinfo("Webcam Already Started", "Webcam is already running.")

    def stop_webcam(self):
        # Stop the webcam
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()
            messagebox.showinfo("Webcam Stopped", "Webcam has been stopped.")
            self.webcam_running = False
            self.start_button.config(text="Start")
            # Display a black image when the webcam is stopped
            black_image = np.zeros((480, 640, 3), dtype=np.uint8)
            black_pil_image = Image.fromarray(black_image)
            black_imgtk = ImageTk.PhotoImage(image=black_pil_image)
            self.video_label.imgtk = black_imgtk
            self.video_label.configure(image=black_imgtk, background="dark gray")

    def update(self):
        # Get a frame from the webcam
        ret, frame = self.cap.read()

        # Convert the frame to RGB format
        if ret:
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Convert the frame to a PIL Image
            img = Image.fromarray(frame_rgb)

            # Convert the PIL Image to a Tkinter PhotoImage
            imgtk = ImageTk.PhotoImage(image=img)

            # Update the label with the new PhotoImage and set the background color
            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk, background="dark gray")

        # Repeat this process after 10 milliseconds if the webcam is running
        if self.webcam_running:
            self.window.after(10, self.update)

    def capture_image(self):
        # Get a frame from the webcam
        ret, frame = self.cap.read()

        # Save the captured image to the specified folder with a timestamp in the filename
        if ret:
            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
            image_name = f"captured_image_{timestamp}.jpg"
            image_path = os.path.join(self.save_folder, image_name)
            cv2.imwrite(image_path, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            messagebox.showinfo("Image Saved", f"Your image is saved as '{image_name}'")

    def open_folder(self):
        # Open the specific folder using the default file explorer
        folder_path = os.path.abspath(self.save_folder)
        subprocess.Popen(['explorer', folder_path])

    def __del__(self):
        # Release the webcam when the window is closed
        if self.cap is not None and self.cap.isOpened():
            self.cap.release()

# Create the main window
root = tk.Tk()
root.configure(bg="gray")
app = WebcamApp(root, "Webcam App")

# Run the Tkinter event loop
root.mainloop()