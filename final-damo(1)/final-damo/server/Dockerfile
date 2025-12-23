FROM python:3.11-slim

# 安裝必要套件
RUN pip install --no-cache-dir flask

# 複製 Web App
COPY app.py /app.py

# 開放 HTTP 服務
EXPOSE 80

# 啟動 Web Server
CMD ["python", "/app.py"]
