import tkinter as tk
from tkinter import Toplevel
from PIL import Image, ImageTk
from image_utils import open_image, blend_images, save_image
from enums import RGB


class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")

        # Initialize variables to hold images
        self.image1 = None
        self.image2 = None
        self.image_blend = None
        self.image_blue = None
        self.image_green = None

        # UI Elements for image loading
        self.thumbnail_label1 = tk.Label(self.root, text="Image (B)")
        self.thumbnail_label1.pack(pady=5)
        self.load_button1 = tk.Button(
            self.root, text="Load Image (B)", command=self.load_image1)
        self.load_button1.pack(pady=10)

        self.thumbnail_label2 = tk.Label(self.root, text="Image (G)")
        self.thumbnail_label2.pack(pady=5)
        self.load_button2 = tk.Button(
            self.root, text="Load Image (G)", command=self.load_image2)
        self.load_button2.pack(pady=10)

        # UI Elements for displaying the processed image and saving it
        self.thumbnail_label_processed = tk.Label(
            self.root, text="Processed Image")
        self.thumbnail_label_processed.pack(pady=5)

        self.process_button = tk.Button(
            self.root, text="Process Images", command=self.process_images_button, state=tk.DISABLED)
        self.process_button.pack(pady=10)

        self.save_button = tk.Button(
            self.root, text="Save Processed Image", command=self.save_image_button, state=tk.DISABLED)
        self.save_button.pack(pady=10)

    def load_image1(self):
        self.image1 = open_image("Select the first image")
        if self.image1:
            self.show_thumbnail(self.image1, self.thumbnail_label1)
            self.check_enable_process_button()

    def load_image2(self):
        self.image2 = open_image("Select the second image")
        if self.image2:
            self.show_thumbnail(self.image2, self.thumbnail_label2)
            self.check_enable_process_button()

    def check_enable_process_button(self):
        if self.image1 and self.image2:
            self.process_button.config(state=tk.NORMAL)

    def process_images_button(self):
        if self.image1 and self.image2:
            self.image_blue, self.image_green, self.image_blend = blend_images(
                self.image1, RGB.BLUE, self.image2, RGB.GREEN)
            self.show_thumbnail(
                self.image_blend, self.thumbnail_label_processed)
            self.save_button.config(state=tk.NORMAL)

    def save_image_button(self):
        if self.image_blend:
            save_image(self.image_blue, self.image_green, self.image_blend)

    def show_thumbnail(self, image, label):
        image_thumb = image.copy()
        image_thumb.thumbnail((100, 100))  # Resize to thumbnail size
        image_tk = ImageTk.PhotoImage(image_thumb)
        label.config(image=image_tk, text="")
        label.image = image_tk  # Keep reference
        label.bind("<Button-1>", lambda e: self.show_full_image(image))

    def show_full_image(self, img):
        new_window = Toplevel(self.root)
        new_window.title("Full Image View")
        new_window.geometry("800x600")

        def update_image(event):
            if event is None:
                return
            new_width = event.width
            new_height = event.height
            resized_img = img.resize(
                (new_width, new_height), Image.Resampling.LANCZOS)
            tk_img = ImageTk.PhotoImage(resized_img)
            label.config(image=tk_img)
            label.image = tk_img

        label = tk.Label(new_window)
        label.pack(fill=tk.BOTH, expand=True)
        new_window.bind("<Configure>", update_image)

        # Initially show image at default size
        update_image(None)


# Initialize the root window and app
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
