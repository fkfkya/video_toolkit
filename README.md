#  Video Toolkit

**Video Toolkit** — это Python CLI-инструмент и библиотека для сжатия видео и извлечения каждого N-го кадра. Поддерживает работу как из командной строки, так и в виде модулей в других проектах.

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

### Базовая команда:

python gui/app.py   #в корне проекта с файлом main.py


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
| `--output`    | Папка для результатов (по умолчанию: `./output/`)        |
| `--compress`  | Включает сжатие видео (кодек H.265)                       |
| `--extract`   | Включает извлечение кадров                                |
| `--n`         | Извлекает каждый N-й кадр (по умолчанию: 10)              |

---



