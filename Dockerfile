FROM python:3.11-slim

# install i2c tools
RUN apt-get update && apt-get install -y i2c-tools && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

CMD ["python", "main.py"]