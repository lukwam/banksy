#!/bin/bash

. config.sh

docker run -it --rm \
    --expose 8080 \
    -e GOOGLE_APPLICATION_CREDENTIALS="/etc/service_account.json" \
    -e GOOGLE_CLOUD_PROJECT="${GCP_PROJECT}" \
    -p 8080:8080 \
    -v "$(pwd):/workspace" \
    -v "${ETC_DIR}/service_account.json:/etc/service_account.json" \
    -w "/workspace" \
    "${IMAGE}"
