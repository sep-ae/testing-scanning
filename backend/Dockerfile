FROM python:3.11-slim

WORKDIR /app

# Install dependencies dulu (cache layer)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy semua file
COPY . .

# Buat folder uploads
RUN mkdir -p uploads instance

EXPOSE 5000

CMD ["gunicorn", "-w", "2", "-b", "0.0.0.0:5000", "app:create_app()"]