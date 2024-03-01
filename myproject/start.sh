#!/bin/bash

# 等待 MYSQL 啟動才進行遷移
# while ! nc -z db 3306 ; do
#     echo "Waiting for the MySQL Server"
#     sleep 3
# done

# # 搜集靜態檔案到 static 資料夾
# python manage.py collectstatic --noinput&&
# 產生資料庫執行文件
python manage.py makemigrations&&
# 使用執行文件修改資料庫
python manage.py migrate&&
# 啟動 django
python3 manage.py runserver 0.0.0.0:8000&&
# tail 空命令 防止執行腳本後退出
tail -f /dev/null

exec "$@"