FROM python:3.11-slim

WORKDIR /opt/stone

ENV TZ=America/Sao_Paulo

RUN apt update && apt install -y gcc

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "main:app", "-c", "gunicorn_configs.py", "--bind", "0.0.0.0:80", "--workers", "8", "--worker-class", "uvicorn.workers.UvicornWorker"]