# Name: Fares Elbermawy
# Description: An app which makes a colored image black and white. Firstly, the user choses which image to work on.
# Secondly, we do a grayscale to the image. We simply make the image gray according to the user's choice.
# They chose to have the red, green or blue color and we simply give every pixel the corresponding value of this color.
# Then we do the dithering which is making it black and white totally.
# Also depends on the user's choice there's threshold and random modes.
# For the threshold, we take the specified threshold value of the user and see each pixel if it is greater than or equal
# this value we make it white else black. If it was random option, it takes a random value for each pixel and
# make it as the threshold value then do the same thing.
# We then display the generated image and there is a button if the user wants to save this generated image.
# If you found that the photo is not complete try to extend the gui display.

import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog
import threading
import random


class Dithering:
    def __init__(self, root):
        self.root = root
        self.root.title("Dithering")
        self.root.geometry("700x700")
        # Making the button for the image path and storing the path in a string.
        self.image_path = tk.StringVar()
        self.image_entry = tk.Entry(root, textvariable=self.image_path, width=50)
        self.image_entry.pack()
        self.image_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.image_button.pack()
        # Setting a frame for the settings and buttons for the dithering.
        self.settings_frame = tk.Frame(root)
        self.settings_frame.pack(pady=40)

        self.mode_label = tk.Label(self.settings_frame, text="Chose mode")
        self.grayscale_label = tk.Label(self.settings_frame, text="Chose grayscale channel")
        self.threshold_label = tk.Label(self.settings_frame, text="Threshold")
        self.mode_string = tk.StringVar()
        self.mode_string.set("Threshold")
        self.mode = tk.OptionMenu(self.settings_frame, self.mode_string, "Threshold", "Random")

        self.grayscale_string = tk.StringVar()
        self.grayscale_string.set("Red")
        self.grayscale = tk.OptionMenu(self.settings_frame, self.grayscale_string, "Red", "Green", "Blue")

        self.threshold_value = tk.IntVar(value=50)
        self.threshold = tk.Spinbox(self.settings_frame, from_=0, to=255, textvariable=self.threshold_value)

        self.generate_button = tk.Button(self.settings_frame, text="Generate photo", command=self.generate_photo)
        self.save_button = tk.Button(self.settings_frame, text="Save Generated photo", command=self.save_image)

        self.mode.grid(row=1, column=0, padx=5)
        self.mode_label.grid(row=0, column=0, padx=5)
        self.grayscale_label.grid(row=0, column=1, padx=5)
        self.grayscale.grid(row=1, column=1, padx=5)
        self.threshold_label.grid(row=0, column=2, padx=5)
        self.threshold.grid(row=1, column=2, padx=5)
        self.generate_button.grid(row=1, column=3, padx=10)
        self.save_button.grid(row=1, column=4, padx=10)
        # The frame which will contain both the original and generated images.
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(pady=40)
        # A container for the generated image.
        self.generated_image = None

    # A function to let the user select an image then it leads to the open_image function.
    def select_image(self):
        image_path = filedialog.askopenfilename()
        if image_path:
            self.image_path.set(image_path)
            self.open_image(image_path)

    # A function which opens the original image and put it in the image frame.
    def open_image(self, path):
        try:
            self.original_image = Image.open(path)
            self.original_image.thumbnail((300, 300))
            self.img = ImageTk.PhotoImage(self.original_image)
            self.original_image_display = tk.Label(self.image_frame, image=self.img)
            self.original_image_display.grid(row=0, column=0, padx=5)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    # A function which starts the tread for generating the dithered photo.
    def generate_photo(self):
        thread = threading.Thread(target=self.run_dithering)
        thread.start()

    # The function which starts the grayscale of the image then making it B&W.
    def run_dithering(self):
        try:
            grayscale_image = self.grayscale_function(self.original_image)
            self.dithered_image = self.dither(grayscale_image)
            self.dithered_image.thumbnail((400, 400))
            self.generated_image = ImageTk.PhotoImage(self.dithered_image)
            self.root.after(0, self.update_image_display)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load image: {e}")

    # The function to display the dithered image or update it if it there was an existing one
    def update_image_display(self):
        self.dithered_image_display = tk.Label(self.image_frame, image=self.generated_image)
        self.dithered_image_display.grid(row=0, column=1, padx=5)

    # The function which makes it grayscale according to the user's input.
    def grayscale_function(self, image):
        r, g, b = image.split()
        grayscale_value = self.grayscale_string.get()
        if grayscale_value == "Red":
            return r
        elif grayscale_value == "Green":
            return g
        else:
            return b

    # The dither function which changes the grayscale image to a B&W image.
    def dither(self, image):
        grayscale_array = np.array(image)
        height, width = grayscale_array.shape
        threshold_mode = self.mode_string.get()
        threshold_value = self.threshold_value.get()
        if threshold_mode == "Threshold":
            for i in range(height):
                for j in range(width):
                    if grayscale_array[i][j] >= threshold_value:
                        grayscale_array[i][j] = 255
                    else:
                        grayscale_array[i][j] = 0
        else:
            for i in range(height):
                for j in range(width):
                    random_threshold = random.randint(0, 255)
                    if grayscale_array[i, j] >= random_threshold:
                        grayscale_array[i, j] = 255
                    else:
                        grayscale_array[i, j] = 0
        dithered_image = Image.fromarray(grayscale_array)
        return dithered_image

    # The function to save the image with the extension .tif"
    def save_image(self):
        if self.generated_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".tif")
            if file_path:
                self.dithered_image.save(file_path)
        else:
            messagebox.showerror("Error", "Failed to save image: No image is generated!")


root = tk.Tk()
pic = Dithering(root)
root.mainloop()
