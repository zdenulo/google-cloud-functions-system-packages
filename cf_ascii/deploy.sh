#!/bin/bash

if [ -z "$GCP_PROJECT" ]; then
  echo "Set GCP_PROJECT variable for your shell"
  exit
fi

gcloud functions deploy ascii \
  --project $GCP_PROJECT \
  --entry-point main \
  --runtime python37 \
  --trigger-http
