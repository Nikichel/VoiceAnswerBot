# Stage 1: Установка зависимостей Python
FROM python:3.9 as python_dependencies

COPY requirements.txt .
RUN pip install -r requirements.txt

FROM ubuntu:latest as ffmpeg_installation

RUN apt-get update && apt-get install -y ffmpeg

FROM python_dependencies as final_image

COPY --from=ffmpeg_installation /usr/bin/ffmpeg /usr/bin/ffmpeg

COPY . .

CMD ["python", "main.py"]