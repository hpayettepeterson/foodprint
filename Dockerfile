FROM python:3.8.6-buster

COPY api /api
COPY foodprint /foodprint
COPY models /models
COPY predict_neighbors.py /predict_neighbors.py
COPY predict_similarities.py /predict_similarities.py
COPY models/nneighbors_model.joblib /models/nneighbors_model.joblib
COPY le-wagon-chris-13ef0fd8fa08.json /credentials.json
COPY requirements.txt /requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

CMD uvicorn api.clusterapi:app --host 0.0.0.0 --port $PORT
