FROM python:3.8-slim

WORKDIR /work
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY run.py .

ENTRYPOINT [ "python", "run.py" ]
