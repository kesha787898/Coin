FROM python:3
ARG BD_CONNECTION
ENV BD_CONNECTION=$BD_CONNECTION
ADD . /
RUN pip install -r requirements.txt
CMD [ "python", "./order_collector.py" ]
