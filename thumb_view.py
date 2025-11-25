# ChatGPT program to view png thumbnails and sort them based on how active they look
# Run the program in the command line python thumb_view.py path
# This path should be the path to the directory full of the pngs you want to look at
# Use arrow keys to flip back and forth
# Enter skips 100 images forward, space 100 back
# If you press 1-5 when viewing an image, it will copy the image into a folder named that number
# Pressing c copies to "cool" and o copies it to "other"

import os
import sys
import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import shutil


class ImageViewer:
    def __init__(self, root, image_dir):
        self.root = root
        self.image_dir = image_dir
        # Alphabetical order
        self.image_files = sorted(
        (f for f in os.listdir(image_dir) if f.lower().endswith(".png")),
            key=str.lower)

        self.index = 0
        self.cache = {}  # cache to hold preloaded images

        self.label = Label(root)
        self.label.pack()

        # Key bindings
        root.bind("<Left>", self.prev_image)
        root.bind("<Right>", self.next_image)
        root.bind("<Return>", self.skip_forward)  # Enter key
        root.bind("<space>", self.skip_back)      # Space key
        root.bind("c", self.copy_to_cool)         # 'c' key
        root.bind("o", self.copy_to_other)        # 'o' key
        for i in range(1, 6):
            root.bind(str(i), self.copy_to_folder)

        # Initial load
        self.show_image()

    def preload_images(self):
        """Keep next and previous 5 images loaded into memory."""
        to_keep = range(max(0, self.index - 5), min(len(self.image_files), self.index + 6))

        # Load needed
        for i in to_keep:
            if i not in self.cache:
                path = os.path.join(self.image_dir, self.image_files[i])
                img = Image.open(path)
                self.cache[i] = ImageTk.PhotoImage(img)

        # Drop unused
        for i in list(self.cache.keys()):
            if i not in to_keep:
                del self.cache[i]

    def show_image(self):
        self.preload_images()
        if 0 <= self.index < len(self.image_files):
            self.label.config(image=self.cache[self.index])
            self.root.title(f"{self.image_files[self.index]} ({self.index+1}/{len(self.image_files)})")

    def prev_image(self, event=None):
        if self.index > 0:
            self.index -= 1
            self.show_image()

    def next_image(self, event=None):
        if self.index < len(self.image_files) - 1:
            self.index += 1
            self.show_image()

    def skip_forward(self, event=None):
        """Jump ahead 100 images."""
        if self.index < len(self.image_files) - 1:
            self.index = min(self.index + 100, len(self.image_files) - 1)
            self.show_image()

    def skip_back(self, event=None):
        """Jump back 100 images."""
        if self.index > 0:
            self.index = max(self.index - 100, 0)
            self.show_image()

    def copy_to_folder(self, event):
        folder_name = event.char
        self._copy_current_image(folder_name)

    def copy_to_cool(self, event=None):
        self._copy_current_image("cool")

    def copy_to_other(self, event=None):
        self._copy_current_image("other")

    def _copy_current_image(self, folder_name):
        folder_path = os.path.join(self.image_dir, folder_name)
        os.makedirs(folder_path, exist_ok=True)

        src = os.path.join(self.image_dir, self.image_files[self.index])
        dst = os.path.join(folder_path, self.image_files[self.index])
        shutil.copy2(src, dst)
        print(f"Copied {self.image_files[self.index]} -> {folder_path}")


if __name__ == "__main__":
    # Use command line argument if given, otherwise current working directory
    if len(sys.argv) > 1:
        image_directory = sys.argv[1]
    else:
        image_directory = os.getcwd()

    if not os.path.isdir(image_directory):
        print(f"Error: {image_directory} is not a valid directory")
        sys.exit(1)

    root = tk.Tk()
    app = ImageViewer(root, image_directory)
    root.mainloop()