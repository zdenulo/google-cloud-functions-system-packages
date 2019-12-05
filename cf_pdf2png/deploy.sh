#!/bin/bash

if [ -z "$GCP_PROJECT" ]; then
  echo "Set GCP_PROJECT variable for your shell"
  exit
fi

if [ -z "$GCS_INPUT_BUCKET" ]; then
  echo "Set GCP_INPUT variable for your shell for input bucket (with out gs:// prefix)"
  exit
fi

if [ -z "$GCS_OUTPUT_BUCKET" ]; then
  echo "Set GCP_OUTPUT variable in your shell for output bucket (with out gs:// prefix)"
  exit
fi

gcloud functions deploy pdf2png \
  --project $GCP_PROJECT \
  --entry-point main \
  --runtime python37 \
  --trigger-resource "gs://$GCS_INPUT_BUCKET" \
  --trigger-event google.storage.object.finalize \
  --set-env-vars=GCS_OUTPUT_BUCKET=$GCS_OUTPUT_BUCKET
