#!/bin/bash

BASE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
ETC_DIR="${BASE_DIR}/etc"
GCP_PROJECT="lukwam-banksy"
INCOMING_BUCKET="${GCP_PROJECT}-incoming"
SERVICE_ACCOUNT="${ETC_DIR}/service_account.json"
export BASE_DIR ETC_DIR GCP_PROJECT INCOMING_BUCKET SERVICE_ACCOUNT

# check for service account key
if [ ! -e "${SERVICE_ACCOUNT}" ] ; then
  IAM_ACCOUNT="${GCP_PROJECT}@appspot.gserviceaccount.com"
  echo "Getting servicea account key for ${IAM_ACCOUNT}..."
  gcloud iam service-accounts keys create \
    --format json \
    --iam-account="${IAM_ACCOUNT}" \
    "${SERVICE_ACCOUNT}"
fi
