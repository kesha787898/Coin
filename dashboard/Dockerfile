FROM python:3
ADD . /
RUN pip install -r requirements.txt
#CMD [ "python", "./dashboard.py" ]
CMD ["gunicorn --bind 0.0.0.0:5000 ./dashboard:app"]