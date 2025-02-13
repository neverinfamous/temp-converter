FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create templates directory and copy files
RUN mkdir templates
COPY templates/* templates/
COPY . .

EXPOSE 3000

CMD ["python", "app.py"]