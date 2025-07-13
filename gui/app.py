import tkinter as tk
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import threading

from video_toolkit.core import compressor, extractor
from video_toolkit.utils.video_utils import frames_to_video


def run_processing():
    input_path = input_var.get()
    output_path = output_var.get()
    n = int(n_var.get())

    if not os.path.exists(input_path):
        messagebox.showerror("Ошибка", "Файл не найден")
        return

    os.makedirs(output_path, exist_ok=True)

    compressed_path = os.path.join(output_path, "compressed.mp4")
    frames_dir = os.path.join(output_path, "frames")
    assembled_path = os.path.join(output_path, "assembled.mp4")

    try:
        if compress_var.get():
            compressor.compress_video(input_path, compressed_path)

        if extract_var.get():
            extractor.extract_frames(
                compressed_path if compress_var.get() else input_path,
                frames_dir,
                n
            )

        if assemble_var.get():
            frames_to_video(frames_dir, assembled_path, fps=24)

        messagebox.showinfo("Готово", "Обработка завершена!")
    except Exception as e:
        messagebox.showerror("Ошибка", str(e))


# ---------- UI ----------
root = tk.Tk()
root.title("Video Toolkit")

tk.Label(root, text="Входной файл:").pack()
input_var = tk.StringVar()
tk.Entry(root, textvariable=input_var, width=60).pack()
tk.Button(root, text="Выбрать файл", command=lambda: input_var.set(filedialog.askopenfilename())).pack()

tk.Label(root, text="Выходная папка:").pack()
output_var = tk.StringVar()
tk.Entry(root, textvariable=output_var, width=60).pack()
tk.Button(root, text="Выбрать папку", command=lambda: output_var.set(filedialog.askdirectory())).pack()

tk.Label(root, text="Извлекать каждый n-й кадр:").pack()
n_var = tk.StringVar(value="10")
tk.Entry(root, textvariable=n_var).pack()

compress_var = tk.BooleanVar()
extract_var = tk.BooleanVar()
assemble_var = tk.BooleanVar()

tk.Checkbutton(root, text="Сжать видео", variable=compress_var).pack()
tk.Checkbutton(root, text="Извлечь кадры", variable=extract_var).pack()
tk.Checkbutton(root, text="Собрать из кадров видео", variable=assemble_var).pack()

tk.Button(root, text="Запустить обработку", command=run_processing).pack(pady=10)

root.mainloop()
