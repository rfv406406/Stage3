# 使用官方 Python 映像作為基本映像
FROM python:3.12.0

# 設定工作目錄，所有複製後的文件會在此資料夾下
WORKDIR /app

# 複製 requirements.txt 到容器中
COPY requirements.txt .

# 安裝應用程式相依套件
RUN pip install -r requirements.txt

# 複製應用程式程式碼到容器中
COPY . .

# 應用程式執行的預設指令
CMD ["python", "app.py"]