FROM python:3.7

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip3 install -r requirements.txt

COPY ./springapi /app/springapi

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "-m", "springapi.app" ]
