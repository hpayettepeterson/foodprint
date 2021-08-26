#!/usr/bin/env python



gcloud run deploy \
    --image eu.gcr.io/$PROJECT_ID/$DOCKER_IMAGE_NAME \
    --platform managed \
    --region europe-west1 \
    --set-env-vars "GOOGLE_APPLICATION_CREDENTIALS=/credentials.json"
