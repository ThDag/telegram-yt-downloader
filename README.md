# Telegram bot that batch downloads video sections that you choose

You send it a youtube (or any other video platform) with timestamps (preferebly). And choose the length of the video. And it downloads the video starting from the time stamp with the length you chose.

You can host the Telegram bot yourself

## dependencies

In order for the code to run correctly you need the dependencies inside requirements.txt file and also ffmpeg

```
brew install ffmpeg # for mac
```

```
your-favirote-package-manager install ffmpeg
```

## installation

1.

```
git clone https://github.com/ThDag/telegram-yt-downloader.git
```

> clone the repository

2. Put your telegram bot token obtained with Botfather in telegram into .env file with the name `TELEGRAM_TOKEN`

3.

```
docker-compose up --build
# or (idk which one)
docker compose up --build
```

## Me

i made this code.
