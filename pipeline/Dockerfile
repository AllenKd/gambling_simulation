FROM python:3

WORKDIR /app/gambling_simulation

COPY ../ /app/gambling_simulation
COPY main.py /app/gambling_simulation
RUN pip3 install --requirement /tmp/requirements.txt

CMD ["sleep", "infinity"]
