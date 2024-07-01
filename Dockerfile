
FROM python:3.9 as python_dependencies

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y ffmpeg


COPY . .

CMD ["python", "main.py"]