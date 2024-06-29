import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageOps, ImageDraw
import cv2
import numpy as np

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")
        self.image_path = None
        self.image = None
        self.original_image = None

        self.canvas = tk.Canvas(root, width=800, height=600)
        self.canvas.pack()

        self.create_buttons()
        self.create_entries()

    def create_buttons(self):
        btn_load_image = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        btn_load_image.pack(side=tk.LEFT)

        btn_load_from_camera = tk.Button(root, text="Загрузить изображение с камеры", command=self.load_from_camera)
        btn_load_from_camera.pack(side=tk.LEFT)

        btn_show_negative = tk.Button(root, text="Show negative", command=self.show_negative)
        btn_show_negative.pack(side=tk.LEFT)

        btn_rotate = tk.Button(root, text="Вращение изображения", command=self.rotate_image)
        btn_rotate.pack(side=tk.LEFT)

        btn_draw_circle = tk.Button(root, text="Нарисовать красный круг", command=self.draw_circle)
        btn_draw_circle.pack(side=tk.LEFT)

        btn_clear = tk.Button(root, text="Clear", command=self.clear)
        btn_clear.pack(side=tk.LEFT)

        btn_exit = tk.Button(root, text="Exit", command=root.quit)
        btn_exit.pack(side=tk.LEFT)

    def create_entries(self):
        self.angle_entry = tk.Entry(root)
        self.angle_entry.pack(side=tk.LEFT)
        self.angle_entry.insert(0, "Угол вращения")

        self.circle_params_entry = tk.Entry(root)
        self.circle_params_entry.pack(side=tk.LEFT)
        self.circle_params_entry.insert(0, "Координаты x, y и диаметр")

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg")])
        if not self.image_path:
            messagebox.showerror("Ошибка", "Не удалось загрузить изображение.")
            return
        self.image = Image.open(self.image_path)
        self.original_image = self.image.copy()
        self.display_image(self.image)

    def load_from_camera(self):
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Ошибка", "Не удалось подключиться к веб-камере.")
            return
        ret, frame = cap.read()
        if not ret:
            messagebox.showerror("Ошибка", "Не удалось сделать снимок.")
            cap.release()
            return
        self.image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        self.original_image = self.image.copy()
        self.display_image(self.image)
        cap.release()

    def display_image(self, image):
        img = ImageTk.PhotoImage(image.resize((800, 600), Image.ANTIALIAS))
        self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        self.canvas.image = img

    def show_negative(self):
        if self.image:
            if self.image.mode != 'RGB':
                self.image = self.image.convert('RGB')
            self.image = ImageOps.invert(self.image)
            self.display_image(self.image)

    def rotate_image(self):
        angle = self.angle_entry.get()
        try:
            angle = float(angle)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректный угол.")
            return
        if self.image:
            self.image = self.image.rotate(angle, expand=True)
            self.display_image(self.image)

    def draw_circle(self):
        params = self.circle_params_entry.get().split(',')
        try:
            x, y, diameter = map(int, params)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные координаты и диаметр.")
            return
        if self.image:
            draw = ImageDraw.Draw(self.image)
            draw.ellipse((x, y, x + diameter, y + diameter), outline="red", width=3)
            self.display_image(self.image)

    def clear(self):
        if self.original_image:
            self.image = self.original_image.copy()
            self.display_image(self.image)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
