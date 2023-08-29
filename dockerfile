FROM selenium/standalone-firefox

WORKDIR /home/seluser
COPY ./ .
USER root
RUN apt update
RUN apt install tor python3 pip tar libpq-dev -y
RUN pip install -r requirements.txt
RUN chown seluser /home/seluser/* -R
USER seluser
CMD ["python3", "app.py"]
