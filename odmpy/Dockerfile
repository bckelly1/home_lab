FROM python

RUN apt update && apt install -y ffmpeg

WORKDIR /usr/src/app

COPY ./requirements.txt /usr/src/app
RUN pip install -r requirements.txt

COPY . .

CMD ["tail", "-f", "/dev/null"]

