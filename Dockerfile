FROM buildpack-deps:bullseye

RUN apt-get update -y

RUN apt-get install -y python3-pip python-dev build-essential

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

COPY . /app

RUN chmod +x ./app.py

ENTRYPOINT ["./app.py"]

CMD ["python", "app.py"]