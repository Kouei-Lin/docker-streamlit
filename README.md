# Streamlit + Docker

## 安裝Docker

參訪以下連結來安裝[Docker](https://docs.docker.com/engine/install/)和[Docker Compose](https://docs.docker.com/compose/install/)。

## 下載Repo
`$ git clone https://github.com/Kouei-Lin/docker-streamlit`

## 進入文件夾

`$ cd docker-streamlit`

`$ cd yf`

## 建Image並運作容器
`$ docker compose up -d --build`

## 當地參訪
參訪[http://localhost:8501](http://localhost:8501)。

`Port`如有衝突可於`docker-compose.yml`自行變更`xxx(希望Port):8501`。

## 刪除容器
`$ docker compose down -v`

## 刪除Image
`$ docker images`查看`image_id`

`$ docker image rm image_id`
