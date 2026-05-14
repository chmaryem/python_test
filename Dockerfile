# Dockerfile genere par Code Auditor
# Python 3.11

FROM python:3.11-slim
WORKDIR /app
RUN addgroup --system appgroup && adduser --system --group appuser
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
USER appuser
EXPOSE 8000
CMD ["python", "main.py"]
