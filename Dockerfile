FROM python:3.9

WORKDIR /app
COPY src/app.py /app
COPY requirements.txt /app

RUN pip install -r requirements.txt
ENTRYPOINT [ "python3" ]
CMD [ "app.py" ]