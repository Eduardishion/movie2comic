FROM python:3.8
ENV PYTHONUNBUFFERED 1

RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list && \
    apt-get update && \
    apt-get install -yq \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    ffmpeg build-essential swig git libpulse-dev libasound2-dev sox libgomp1 libpthread-stubs0-dev

COPY ./requirements.txt /requirements.txt
RUN python -m pip install -r requirements.txt

COPY ./m2c /app
WORKDIR /

ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:80", "-w", "4", "app:app" ]