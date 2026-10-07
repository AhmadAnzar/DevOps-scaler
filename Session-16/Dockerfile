FROM python:3.12-slim

WORKDIR /app

COPY app/ app/

# calculator.py asks for input, so run the container with -it
CMD ["python", "app/calculator.py"]
