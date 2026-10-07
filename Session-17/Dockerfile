FROM python:3.12-slim

# links the image on ghcr.io to this repo
LABEL org.opencontainers.image.source=https://github.com/AhmadAnzar/DevOps-scaler

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

# don't run as root inside the container
RUN useradd --create-home appuser
USER appuser

EXPOSE 5001

CMD ["python", "app/app.py"]
