FROM python:2.7
LABEL maintainer="Michael Akouwa"

ADD ./techtrends/ /app

WORKDIR /app

RUN python init_db.py

RUN pip install -r requirements.txt

EXPOSE 3111

# command to run on container start
CMD [ "python", "app.py" ]
