import cv2
import os
import time
import tkinter as tk
from tkinter import filedialog
from datetime import datetime
from PIL import Image, ImageTk

# Initialize the camera (0 is the default camera)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    raise Exception("Could not open video device")

# Global variable to store the current image path
current_image_path = None

def capture_image():
    global current_image_path
    ret, frame = cap.read()
    if ret:
        # Define image save path (e.g., Desktop directory)
        desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
        filename = datetime.now().strftime("captured_%Y%m%d_%H%M%S.jpg")
        image_path = os.path.join(desktop_path, filename)
        
        # Save the captured frame as an image file
        cv2.imwrite(image_path, frame)
        current_image_path = image_path

        status_label.config(text=f"Image saved: {filename}")

        # Convert the image from BGR (OpenCV default) to RGB and create a PIL image for preview
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(frame_rgb)
        preview = img.copy()
        preview.thumbnail((250, 250))
        preview_img = ImageTk.PhotoImage(preview)
        preview_panel.config(image=preview_img)
        preview_panel.image = preview_img
    else:
        status_label.config(text="Failed to capture image!")

def import_photo():
    global current_image_path
    file_path = filedialog.askopenfilename(
        title="Select an Image", 
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.bmp;*.gif")]
    )
    if file_path:
        current_image_path = file_path
        status_label.config(text=f"Imported image: {os.path.basename(file_path)}")
        
        # Load the image and create a thumbnail for preview
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
        img_label.image = full_img  # keep a reference to avoid garbage collection
        img_label.pack()
    else:
        status_label.config(text="No image available to display.")

# Create the main GUI window
root = tk.Tk()
root.title("OpenCV Camera Capture")
root.geometry("500x500")

# Button to capture a new image from the camera
capture_btn = tk.Button(root, text="Capture Image", command=capture_image, font=("Arial", 14))
capture_btn.pack(pady=10)

# Button to import an existing image file
import_btn = tk.Button(root, text="Import Photo", command=import_photo, font=("Arial", 14))
import_btn.pack(pady=10)

# Button to view the full resolution of the current image
view_btn = tk.Button(root, text="View Full Resolution", command=view_full_resolution, font=("Arial", 14))
view_btn.pack(pady=10)

# Status label for messages
status_label = tk.Label(root, text="Capture or import an image", font=("Arial", 12))
status_label.pack(pady=10)

# Panel to display image preview (thumbnail)
preview_panel = tk.Label(root)
preview_panel.pack(pady=10)

# Run the application
root.mainloop()

# Release the camera and close any OpenCV windows when done
cap.release()
cv2.destroyAllWindows()
