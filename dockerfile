FROM python

WORKDIR /test
COPY ./ .
RUN apt update
RUN apt install tor -y
RUN pip install -r requirements.txt
RUN python app.py
