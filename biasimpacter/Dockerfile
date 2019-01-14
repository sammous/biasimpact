FROM python:3.6
RUN apt-get update -y
RUN apt-get install -y cron
COPY . /biasimpacter
WORKDIR /biasimpacter
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["app/app.py"]