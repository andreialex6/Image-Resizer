import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageOps
import os

def select_image():
    global img_path
    img_path = filedialog.askopenfilename(
        filetypes=[("Images", "*.jpg *.jpeg *.png *.bmp *.gif")]
    )
    if img_path:
        lbl_file.config(text=os.path.basename(img_path))

def process_image():
    if not img_path:
        messagebox.showerror("Error", "No image selected!")
        return

    try:
        width = int(entry_width.get())
        height = int(entry_height.get())
        ext = combo_ext.get().lower()

        # Open image
        img = Image.open(img_path)

        # Resize the image while maintaining proportions 
        img = ImageOps.contain(img, (width, height))

        # Create white background
        background = Image.new("RGB", (width, height), (255, 255, 255))

        # Center the image on the background
        offset = ((width - img.width) // 2, (height - img.height) // 2)
        background.paste(img, offset)

        # Choose location save
        save_path = filedialog.asksaveasfilename(
            defaultextension=f".{ext}",
            filetypes=[("Image", f"*.{ext}")]
        )

        if save_path:
            background.save(save_path)
            messagebox.showinfo("Success", f"Image was saved as {save_path}")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===== Tkinter Interface =====
root = tk.Tk()
root.title("Image resizer")

img_path = None

# Select file
btn_select = tk.Button(root, text="Choose image", command=select_image)
btn_select.pack(pady=5)

lbl_file = tk.Label(root, text="No image selected")
lbl_file.pack()

# Enter the desired image size
frame_size = tk.Frame(root)
frame_size.pack(pady=5)

tk.Label(frame_size, text="Width:").grid(row=0, column=0, padx=5)
entry_width = tk.Entry(frame_size, width=6)
entry_width.insert(0, "1024")
entry_width.grid(row=0, column=1, padx=5)

tk.Label(frame_size, text="Height:").grid(row=0, column=2, padx=5)
entry_height = tk.Entry(frame_size, width=6)
entry_height.insert(0, "768")
entry_height.grid(row=0, column=3, padx=5)

# Choose extension
tk.Label(root, text="Save extension:").pack()
combo_ext = ttk.Combobox(root, values=["png", "jpg", "jpeg", "bmp"], state="readonly")
combo_ext.current(0)
combo_ext.pack(pady=5)

# Processing button
btn_process = tk.Button(root, text="Processing and saving", command=process_image)
btn_process.pack(pady=10)

root.mainloop()
