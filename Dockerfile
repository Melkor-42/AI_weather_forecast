FROM python:3.11-alpine
LABEL maintainer="michal.macej@proton.me" \
      maintainerVersion="1.0.0.28.09.24" \
      maintainerChange="Implement AI weather app with secrets"

RUN apk update && \
    apk add --no-cache gcc musl-dev libffi-dev && \
    mkdir -p /app/weather_bot && \
    mkdir -p /app/weather_bot/logs

WORKDIR /app/weather_bot

COPY . .

RUN pip install --upgrade pip && \
    pip install -r ./requirements.txt


RUN addgroup --gid 10042 weather_bot_group && \
    adduser --uid 10042 --disabled-password --ingroup weather_bot_group weather_bot && \
    chown -R weather_bot:weather_bot_group /app/weather_bot

USER weather_bot

CMD ["python", "/app/weather_bot/app.py"]