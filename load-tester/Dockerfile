FROM python:3.8-slim

WORKDIR /work
COPY requirements.txt run.py /work/
RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "run.py" ]
