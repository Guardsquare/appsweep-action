FROM python:3.13-slim

COPY . /app
WORKDIR /app

# We are installing a dependency here directly into our app source dir
RUN pip install --target=/app -r requirements.txt

ENV PYTHONPATH /app
CMD ["python", "/app/main.py"]
