FROM python:3.8.6-buster

COPY api /api
COPY fooodprintai /fooodprintai
COPY models/nneighbors_model.joblib /models/nneighbors_model.joblib
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.clusterapi:app --host 0.0.0.0 --port $PORT
