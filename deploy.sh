#!/bin/bash

# 設定
PROJECT_ID="your-project-id"
REGION="asia-northeast1"
SERVICE_NAME="gcs-mount-test"
BUCKET_NAME="your-bucket-name"
MOUNT_PATH="/gcs"

# Cloud Runにデプロイ（GCSマウント付き）
gcloud run deploy $SERVICE_NAME \
  --source . \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --set-env-vars GCS_MOUNT_PATH=$MOUNT_PATH \
  --execution-environment gen2 \
  --add-volume name=gcs,type=cloud-storage,bucket=$BUCKET_NAME \
  --add-volume-mount volume=gcs,mount-path=$MOUNT_PATH

echo "Deployed to Cloud Run with GCS bucket mounted at $MOUNT_PATH"
