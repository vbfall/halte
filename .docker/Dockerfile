FROM us.gcr.io/atlas-ce/worker:latest

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --requirement /tmp/requirements.txt
RUN rm /tmp/requirements.txt

ENTRYPOINT ["python"]
