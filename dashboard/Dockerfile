FROM python:3
ARG port
ARG BD_CONNECTION
ENV PORT=$port
ENV BD_CONNECTION=$BD_CONNECTION
RUN mkdir dashboard
COPY . /dashboard
WORKDIR dashboard
EXPOSE $PORT
RUN ls
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils \
    && apt-get -y install curl \
    && apt-get install libgomp1

RUN chgrp -R 0 /dashboard \
    && chmod -R g=u /dashboard \
    && pip install pip --upgrade \
    && pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:$PORT dashboard:server --preload --log-level info



