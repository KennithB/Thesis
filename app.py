import os
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from picamera2 import Picamera2
from PIL import Image, ImageTk

# Initialize the camera with a full-resolution still configuration.
picam2 = Picamera2()
# Adjust the size below to your camera's native resolution.
capture_config = picam2.create_still_configuration(main={"format": "Jpeg", "size": (4056, 3040)})
picam2.configure(capture_config)
picam2.start()

# Global variable to store the current image path
current_image_path = None

def capture_image():
    global current_image_path
    # Define image save path (Desktop directory)
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    filename = datetime.now().strftime("captured_%Y%m%d_%H%M%S.jpg")
    image_path = os.path.join(desktop_path, filename)
    
    # Reset zoom before capturing
    picam2.set_controls({"ScalerCrop": (0.0, 0.0, 1.0, 1.0)})
    
    # Capture image using the active camera
    picam2.capture_file(image_path)
    current_image_path = image_path

    # Update status label
    status_label.config(text=f"Image saved: {filename}")
    
    # Load image and create a thumbnail for preview
    img = Image.open(image_path)
    preview = img.copy()
    preview.thumbnail((250, 250))
    preview_img = ImageTk.PhotoImage(preview)
    preview_panel.config(image=preview_img)
    preview_panel.image = preview_img

def import_photo():
    global current_image_path
    file_path = filedialog.askopenfilename(
        title="Select an Image", 
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        current_image_path = file_path
        status_label.config(text=f"Imported image: {os.path.basename(file_path)}")
        
        img = Image.open(file_path)
        preview = img.copy()
        preview.thumbnail((250, 250))
        preview_img = ImageTk.PhotoImage(preview)
        preview_panel.config(image=preview_img)
        preview_panel.image = preview_img

def view_full_resolution():
    if current_image_path:
        full_res_window = tk.Toplevel(root)
        full_res_window.title("Full Resolution Image")
        
        img = Image.open(current_image_path)
        full_img = ImageTk.PhotoImage(img)
        
        img_label = tk.Label(full_res_window, image=full_img)
        img_label.image = full_img
        img_label.pack()
    else:
        status_label.config(text="No image available to display.")

root = tk.Tk()
root.title("Raspberry Pi Camera")
root.geometry("500x500")

capture_btn = tk.Button(root, text="Capture Image", command=capture_image, font=("Arial", 14))
capture_btn.pack(pady=10)

import_btn = tk.Button(root, text="Import Photo", command=import_photo, font=("Arial", 14))
import_btn.pack(pady=10)

view_btn = tk.Button(root, text="View Full Resolution", command=view_full_resolution, font=("Arial", 14))
view_btn.pack(pady=10)

status_label = tk.Label(root, text="Capture or import an image", font=("Arial", 12))
status_label.pack(pady=10)

preview_panel = tk.Label(root)
preview_panel.pack(pady=10)

root.mainloop()

picam2.stop()
