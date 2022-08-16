FROM python:3
RUN mkdir dashboard
ADD . /dashboard
WORKDIR dashboard
RUN pip install -r requirements.txt
ENV PORT=$port
EXPOSE $PORT
RUN ls
CMD gunicorn --bind 0.0.0.0:$PORT dashboard:server --log-level DEBUG --timeout 20 -w 4



