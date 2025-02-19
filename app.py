import os
import tkinter as tk
from datetime import datetime
from picamera2 import Picamera2
from PIL import Image, ImageTk

def capture_image():
    # Initialize the camera
    picam2 = Picamera2()
    picam2.start()
    
    # Define image save path
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = datetime.now().strftime("captured_%Y%m%d_%H%M%S.jpg")
    image_path = os.path.join(desktop_path, filename)
    
    # Capture image
    picam2.capture_file(image_path)
    picam2.stop()
    
    # Display confirmation
    label.config(text=f"Image saved: {filename}")
    
    # Update preview
    img = Image.open(image_path)
    img.thumbnail((250, 250))
    img = ImageTk.PhotoImage(img)
    panel.config(image=img)
    panel.image = img

# Create GUI window
root = tk.Tk()
root.title("Raspberry Pi Camera")
root.geometry("400x400")

# Create a capture button
button = tk.Button(root, text="Capture Image", command=capture_image, font=("Arial", 14))
button.pack(pady=20)

# Label to show status
label = tk.Label(root, text="Click to capture image", font=("Arial", 12))
label.pack()

# Image preview panel
panel = tk.Label(root)
panel.pack()

# Run the application
root.mainloop()
