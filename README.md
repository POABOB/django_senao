# senao_network
This is an interview project for Senao Network.

- [x] Implement two RESTful HTTP APIs for creating and verifying an account and password, following the design requirements specified above.
- [x] Use Python to implement the solution.
- [x] Include error handling and input validation.
- [x] Utilize appropriate data storage solutions.
- [x] Package the solution in a Docker container and push it to Docker Hub.
- [x] Host the solution in a GitHub repository with the source code.
- [x] Provide a comprehensive API document with clear instructions on how to use the APIs, including sample request and response payloads.
- [x] Provide a detailed user guide on how to run the container with Docker, including necessary commands and configurations. It is essential to provide clear and detailed instructions to ensure the container can be successfully run using
Docker.
## 如何啟動?

### 安裝

- Clone
```bash
git clone https://github.com/POABOB/django_senao_network.git
```
- Redis Config
```bash
cd django_senao_network
# 從範例配置中，複製一份本地執行的配置
cp -R ./compose/redis/redis.conf.example ./compose/redis/redis.conf
```

### 執行

```bash
docker-compose up
```

### 打包並發布映像欓

```bash
# 登入 Docker Hub
docker login

# 打包映像欓，<username> 為登入後的使用者名稱
docker build -t <username>/senao_network:lastest ./myproject

# 部署 Docker Hub，<username> 為登入後的使用者名稱
docker push <username>/senao_network:lastest
```

- Docker Hub Repo: https://hub.docker.com/repository/docker/poabob/senao_network/general

### 如果沒有安裝 Docker 或 Docker Compose?

#### Windows

- 點擊官方網址 https://docs.docker.com/desktop/install/windows-install/ ，直接下載安裝

#### Mac

- 點擊官方網址 https://docs.docker.com/desktop/install/mac-install/ ，直接下載安裝

<!-- - Docker Compose

    使用 brew 安裝
    ```bash
    brew install docker-compose
    ``` -->

#### Linux (Ubuntu)

- Docker
```bash
# 刪除已被安裝的 Docker
sudo apt-get remove docker docker-engine docker.io

# 透過官網的 shell 來安裝
curl -sSL https://get.docker.com/ | sh

# 測試是否安裝成功
sudo docker run hello-world
```
- Docker Compose

```bash
# 從 github 上下載最新版本
sudo curl -L https://github.com/docker/compose/releases/download/v2.21.0/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose
# 讓 docker-compose 可執行
sudo chmod +x /usr/local/bin/docker-compose
```

## 如何使用?

### Swagger

1. [執行 Django 專案](https://github.com/POABOB/django_senao_network?tab=readme-ov-file#%E5%9F%B7%E8%A1%8C)
1. 點擊 http://127.0.0.1:8000/swagger/ ，進入 Restful API 的文檔。
    - 畫面示意圖
    ![API 文檔](./images/swgger.png)
    - 可以查看特定 API 的規格
    ![API 規格](./images/signup_detail.png)
1. 點擊 signup - Try it，並輸入要註冊的帳號
    - 正確
    ```json
    {
        "username": "Bob",
        "password": "Aa123456"
    }
    ```
    ![正確輸入](./images/signup_correct_input.png)
    ![正確輸入回應](./images/signup_correct_input_response.png)
    - 帳號沒有在 3~32 位
    ```json
    {
        "username": "G",
        "password": "Aa123456"
    }
    ```
    ![錯誤輸入1](./images/signup_incorrect_input1.png)
    ![錯誤輸入1回應](./images/signup_incorrect_input1_response.png)
    - 密碼沒有只少一個大寫、一個小寫和一個數字
    ```json
    {
        "username": "Alice",
        "password": "A12345678"
    }
    ```
    ![錯誤輸入2](./images/signup_incorrect_input2.png)
    ![錯誤輸入2回應](./images/signup_incorrect_input2_response.png)
1. 點擊 login - Try it，並輸入已被註冊的帳號
    - 正確
    ```json
    {
        "username": "Bob",
        "password": "Aa123456"
    }
    ```
    ![正確輸入](./images/login_correct_input.png)
    ![正確輸入回應](./images/login_correct_input_response.png)
    - 輸入錯誤的帳密 5 次
    ```json
    {
        "username": "Bob",
        "password": "Aa123777777"
    }
    ```
- 請求參數規格

- 回應參數規格