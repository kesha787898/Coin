FROM python:3
RUN mkdir dashboard
ADD . /dashboard
WORKDIR dashboard
RUN pip install -r requirements.txt
EXPOSE 8050
RUN ls
CMD python dashboard.py


