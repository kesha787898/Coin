FROM python:3
ARG port
ARG BD_CONNECTION
ENV PORT=$port
ENV BD_CONNECTION=$BD_CONNECTION
EXPOSE $PORT
ADD . /
RUN pip install -r requirements.txt
CMD [ "python", "./order_collector.py" ]

