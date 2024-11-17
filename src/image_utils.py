import os
from tkinter import filedialog, messagebox
from PIL import Image
import numpy as np
from enums import RGB
from constants import EXPORT_RESOLUTION


def open_image(title="Open Image"):
    filepath = filedialog.askopenfilename(
        title=title, filetypes=[("Image file", ".tif .jpg .png")])
    if filepath:
        try:
            return Image.open(filepath).convert('L')  # convert to grayscale
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open image: {e}")
    return None


def append_enum_to_filename(filepath, channel: RGB):
    """
    Appends the channel name (e.g., BLUE, GREEN, RED) to the filename
    """
    file_dir, filename = os.path.split(filepath)
    name, ext = os.path.splitext(filename)
    new_filename = f"{name}_{channel.name}{ext}"
    return os.path.join(file_dir, new_filename)


def save_image(image_blue, image_green, image_blend):
    filepath = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[
                                            ("PNG", "*.png"), ("JPEG", "*.jpg"), ("All Files", "*.*")])
    if filepath:
        try:
            image_blue.save(append_enum_to_filename(
                filepath, RGB.BLUE), dpi=EXPORT_RESOLUTION)
            image_green.save(append_enum_to_filename(
                filepath, RGB.GREEN), dpi=EXPORT_RESOLUTION)
            image_blend.save(filepath, dpi=EXPORT_RESOLUTION)
            messagebox.showinfo("Success", f"Image saved to {filepath}")
        except Exception as e:
            messagebox.showerror("Error", f"Error saving image: {e}")


def blend_images(image_1, selected_channel_1: RGB, image_2, selected_channel_2: RGB):
    """
    Blends two grayscale images by assigning each image to a separate RGB channel.
    Returns the resulting blue, green, and blended images.
    """
    image_size = image_1.size
    image_2 = image_2.resize(image_size)

    # Convert to numpy arrays for manipulation
    image_array_1 = np.array(image_1)
    image_array_2 = np.array(image_2)

    # Create empty image arrays for each channel
    image_blue = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
    image_green = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
    image_blend = np.zeros_like(image_blue)

    # Assign the grayscale image values to the corresponding channels
    image_blue[:, :, selected_channel_1.value] = image_array_1
    image_green[:, :, selected_channel_2.value] = image_array_2

    # Blend images by adding pixel values
    image_blend = np.clip(image_blue + image_green, 0,
                          255)  # Ensure no overflow

    return Image.fromarray(image_blue), Image.fromarray(image_green), Image.fromarray(image_blend)
