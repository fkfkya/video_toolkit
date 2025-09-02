#  Video Toolkit

**Video Toolkit** — это Python CLI-инструмент и библиотека для работы с видео:  
- сжатие видео (CRF, preset),  
- извлечение каждого N-го кадра,  
- сборка кадров обратно в видео.  

Поддерживает запуск как из командной строки (CLI), так и через графический интерфейс (GUI на Tkinter).

---

## Как скачать проект

1. Откройте терминал или командную строку
2. Клонируйте репозиторий:

```bash
git clone https://github.com/your-username/video_toolkit.git
cd video_toolkit
```

(или скачайте `.zip` на GitHub и распакуйте)

---

## Установка зависимостей

### Python-библиотеки

Проект использует:

- `opencv-python-headless`
- `numpy==1.24.4`
- `natsort`

Установите их из файла `requirements.txt`.

### Системная зависимость: `ffmpeg`

`ffmpeg` нужен для сжатия видео — он не устанавливается через pip

---

### Установка на разных платформах

#### macOS

```bash
brew install ffmpeg
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

#### Ubuntu / Debian

```bash
sudo apt update
sudo apt install ffmpeg python3-venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

####  Windows (в PowerShell или CMD)

1. Скачайте ffmpeg с https://ffmpeg.org/download.html  
2. Распакуйте и добавьте путь к `bin/ffmpeg.exe` в `PATH`
3. Далее:

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## Как запускать проект

### GUI

```bash
python gui/app.py
```

### CLI

```bash
python main.py \
  --input /полный/путь/к/video.mp4 \
  --output /путь/к/папке/для/результатов \
  --compress \
  --extract \
  --n 10
```

### Аргументы:

| Аргумент      | Описание                                                  |
|---------------|-----------------------------------------------------------|
| `--input`     | Путь к исходному видеофайлу (обязательно)                |
| `--output`    | Папка для результатов (default: `./output/`)        |
| `--compress`  | Включает сжатие видео (кодек H.264, имя файла: `<имя>_compressed.mp4`)  |
| `--crf` | CRF (качество: меньше -> лучше качество, больше размер; default: 28) |
| `--preset` | Preset скорости сжатия (ultrafast … veryslow; default: medium) |
| `--extract`   | Включает извлечение кадров                                |
| `--n`         | Извлекает каждый N-й кадр (default: 10)              |
| `--assemble` | Собирает кадры обратно в видео |
| `--fps` | FPS для сборки видео (default: 30) |
| `--ratio` | Показывает коэффициент сжатия (размер до/после) |

---

## Примеры использования

- Сжать видео с `CRF=23`, `preset=fast`:
    ```bash
    python -m video_toolkit.main -i input.mp4 -o out --compress --crf 23 --preset fast
    ```
    
- Извлечь каждый **15-й** кадр:
    ```bash
    python -m video_toolkit.main -i input.mp4 -o out --extract --n 15
    ```
    
- Собрать видео из кадров:
    ```bash
    python -m video_toolkit.main -i input.mp4 -o out --assemble --fps 24
    ```
