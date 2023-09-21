FROM python:3.11
ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    python3-pip \
    python3-setuptools \
    python3-tk \
    python3-wheel \
    && rm -rf /var
RUN pip install --upgrade pip
# RUN pip install -r requirements.txt
RUN mkdir /app
WORKDIR /app
COPY . /app
CMD ["python", "main.py"]
