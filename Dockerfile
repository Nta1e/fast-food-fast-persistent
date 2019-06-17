FROM ubuntu:latest

WORKDIR /fff-api

RUN apt-get update -y && \
    apt-get install -y python3 python3-pip

COPY ./requirements.txt /fff-api/requirements.txt

RUN pip3 install -r requirements.txt

COPY . /fff-api

ENV DB_NAME fast-food-api
ENV DB_PASSWORD fastfoodfast
ENV DB_USER postgres
ENV DB_HOST db

ENTRYPOINT [ "python3" ]

CMD ["run.py"]
