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

def make_compressed_name(input_path: str, output_dir: str) -> str:
    base = os.path.basename(input_path)
    name, ext = os.path.splitext(base)
    return os.path.join(output_dir, f"{name}_compressed{ext}")


def run_processing():
    # запуск в отдельном потоке
    def worker():
        try:
            # валидация ввода
            input_path = input_var.get().strip()
            output_path = output_var.get().strip()
            if not os.path.exists(input_path):
                messagebox.showerror("Ошибка", "Входной файл не найден")
                return
            if not output_path:
                messagebox.showerror("Ошибка", "Не указана выходная папка")
                return

            try:
                n = int(n_var.get())
                if n < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "N должно быть целым числом ≥ 1")
                return

            try:
                crf = int(crf_var.get())
            except ValueError:
                messagebox.showerror("Ошибка", "CRF должно быть целым числом")
                return

            try:
                fps = int(fps_var.get())
                if fps < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Ошибка", "FPS должно быть целым числом ≥ 1")
                return

            os.makedirs(output_path, exist_ok=True)

            compressed_path = make_compressed_name(input_path, output_path)
            frames_dir = os.path.join(output_path, "frames")
            assembled_path = os.path.join(output_path, "assembled.mp4")

            # считаем, сколько этапов выбрано для прогресса
            total_steps = sum([compress_var.get(), extract_var.get(), assemble_var.get()])
            step_done = 0

            # сжатие
            if compress_var.get():
                set_status("Сжатие...", step_done, total_steps)
                compressor.compress_video(
                    input_path=input_path,
                    output_path=compressed_path,
                    crf=crf,
                    preset=preset_var.get(),
                    codec="h264"
                )
                step_done += 1
                update_progress(step_done, total_steps)

            # извлечение кадров
            if extract_var.get():
                set_status("Извлечение кадров...", step_done, total_steps)
                src_for_extract = compressed_path if compress_var.get() else input_path
                extractor.extract_every_nth_frame(
                    video_path=src_for_extract,
                    output_folder=frames_dir,
                    n=n
                )
                step_done += 1
                update_progress(step_done, total_steps)

            # сборка видео из кадров
            if assemble_var.get():
                set_status("Сборка видео...", step_done, total_steps)
                frames_to_video(frames_dir, assembled_path, fps=fps)
                step_done += 1
                update_progress(step_done, total_steps)

            set_status("Готово", total_steps, total_steps)
            messagebox.showinfo("Готово", "Обработка завершена!")
        except Exception as e:
            set_status("Ошибка", 0, 1)
            messagebox.showerror("Ошибка", str(e))
        finally:
            # кнопки в нормальное состояние
            run_btn.config(state=tk.NORMAL)

    # заблокировать кнопку на время обработки
    run_btn.config(state=tk.DISABLED)
    # сброс прогресса и статуса
    update_progress(0, max(1, sum([compress_var.get(), extract_var.get(), assemble_var.get()])))
    set_status("Готово к запуску", 0, 1)
    threading.Thread(target=worker, daemon=True).start()


def update_progress(done, total):
    # прогресс по числу завершенных этапов
    if total <= 0:
        progress_var.set(0)
    else:
        progress_var.set(int(done * 100 / total))


def set_status(text, done, total):
    status_var.set(text)
    update_progress(done, total)


# UI
root = tk.Tk()
root.title("Video Toolkit")

main_frame = ttk.Frame(root, padding=10)
main_frame.pack(fill="both", expand=True)

ttk.Label(main_frame, text="Входной файл:").pack(anchor="w")
input_var = tk.StringVar()
ttk.Entry(main_frame, textvariable=input_var, width=60).pack(fill="x")
ttk.Button(main_frame, text="Выбрать файл",
           command=lambda: input_var.set(filedialog.askopenfilename())).pack(pady=(0,8), anchor="w")

ttk.Label(main_frame, text="Выходная папка:").pack(anchor="w")
output_var = tk.StringVar()
ttk.Entry(main_frame, textvariable=output_var, width=60).pack(fill="x")
ttk.Button(main_frame, text="Выбрать папку",
           command=lambda: output_var.set(filedialog.askdirectory())).pack(pady=(0,8), anchor="w")

params_frame = ttk.Frame(main_frame)
params_frame.pack(fill="x", pady=(4,8))

ttk.Label(params_frame, text="Каждый n-й кадр:").grid(row=0, column=0, sticky="w")
n_var = tk.StringVar(value="10")
ttk.Entry(params_frame, textvariable=n_var, width=8).grid(row=0, column=1, padx=(6,18), sticky="w")

ttk.Label(params_frame, text="CRF:").grid(row=0, column=2, sticky="w")
crf_var = tk.StringVar(value="23")
ttk.Entry(params_frame, textvariable=crf_var, width=8).grid(row=0, column=3, padx=(6,18), sticky="w")

ttk.Label(params_frame, text="Preset:").grid(row=0, column=4, sticky="w")
preset_var = tk.StringVar(value="medium")
preset_box = ttk.Combobox(params_frame, textvariable=preset_var, width=12, state="readonly",
                          values=["ultrafast","superfast","veryfast","faster","fast","medium","slow","slower","veryslow"])
preset_box.grid(row=0, column=5, padx=(6,0), sticky="w")
preset_box.current(5)  # medium

ttk.Label(params_frame, text="FPS (assemble):").grid(row=0, column=6, padx=(18,0), sticky="w")
fps_var = tk.StringVar(value="30")
ttk.Entry(params_frame, textvariable=fps_var, width=8).grid(row=0, column=7, padx=(6,0), sticky="w")


flags_frame = ttk.Frame(main_frame)
flags_frame.pack(fill="x", pady=(0,8))

compress_var = tk.BooleanVar()
extract_var = tk.BooleanVar()
assemble_var = tk.BooleanVar()

ttk.Checkbutton(flags_frame, text="Сжать видео", variable=compress_var).grid(row=0, column=0, sticky="w", padx=(0,18))
ttk.Checkbutton(flags_frame, text="Извлечь кадры", variable=extract_var).grid(row=0, column=1, sticky="w", padx=(0,18))
ttk.Checkbutton(flags_frame, text="Собрать видео", variable=assemble_var).grid(row=0, column=2, sticky="w", padx=(0,18))

progress_var = tk.IntVar(value=0)
progress_bar = ttk.Progressbar(main_frame, variable=progress_var, maximum=100)
progress_bar.pack(fill="x", pady=(6,2))

status_var = tk.StringVar(value="Готово к запуску")
ttk.Label(main_frame, textvariable=status_var).pack(anchor="w")

run_btn = ttk.Button(main_frame, text="Запустить обработку", command=run_processing)
run_btn.pack(pady=10)

root.mainloop()
