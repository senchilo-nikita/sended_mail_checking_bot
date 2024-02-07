FROM python:3.10

COPY bot.py bot-requirements.txt  ./
COPY .env ./
RUN pip install --upgrade pip
RUN pip install -r bot-requirements.txt

# COPY . ./

CMD ["python","bot.py"]