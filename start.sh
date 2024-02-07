# docker build --no-cache -t check_forecasts_bot .
# docker run -dp 8003:8003 --name check_forecasts_container check_forecasts_bot

# docker build -t mail_sender -f mail.Dockerfile .
# docker run -dp 8004:8004 --name mail_sender_container mail_sender
docker-compose up -d