import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import torch
from torchvision import transforms
from model import YourDenseNetModel  # Import your trained model

# Load Model
model = YourDenseNetModel()
model.load_state_dict(torch.load("model.pth", map_location=torch.device("cpu")))
model.eval()

# Image Preprocessing
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])

def classify_image():
    file_path = filedialog.askopenfilename()
    if file_path:
        img = Image.open(file_path)
        img = transform(img).unsqueeze(0)
        
        with torch.no_grad():
            output = model(img)
            predicted_class = output.argmax().item()
        
        label.config(text=f"Prediction: {predicted_class}")

# UI Setup
root = tk.Tk()
root.title("Rice Leaf Disease Detection")

btn = tk.Button(root, text="Select Image", command=classify_image)
btn.pack()

label = tk.Label(root, text="Prediction: ")
label.pack()

root.mainloop()
