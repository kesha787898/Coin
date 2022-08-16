FROM python:3
ARG port
RUN mkdir dashboard
COPY . /dashboard
WORKDIR dashboard
RUN pip install -r requirements.txt
ENV PORT=$port
EXPOSE $PORT
RUN ls
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install curl \
    && apt-get install libgomp1

RUN chgrp -R 0 /dashboard \
    && chmod -R g=u /dashboard \
    && pip install pip --upgrade \
    && pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT dashboard:server --preload



