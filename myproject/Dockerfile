# 使用 python 3.9
FROM python:3.9

# 安装netcat
RUN apt-get update && apt install -y netcat-traditional 

# Python 環境變數
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# 建立資料夾，並設定工作目錄
ENV APP_HOME=/var/www/html/myproject
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

# 將當前專案資料複製到容器內
ADD . $APP_HOME

# 更新 pip
RUN /usr/local/bin/python -m pip install --upgrade pip

# 安裝函式庫
RUN pip install -r requirements.txt

# 移除\r in windows
RUN sed -i 's/\r//' ./start.sh

# 给start.sh可执行权限
RUN chmod +x ./start.sh

# 資料庫遷移，啟動
ENTRYPOINT /bin/bash ./start.sh