FROM python:3-slim

COPY . /app
WORKDIR /app

# Installing a dependency directly into app source dir
RUN pip install --target=/app -r requirements.txt

ENV PYTHONPATH /app
CMD ["python", "/app/main.py"]
