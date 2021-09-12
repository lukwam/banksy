#!/bin/bash

. config.sh

docker run -it --rm \
    -e GOOGLE_APPLICATION_CREDENTIALS="/etc/service_account.json" \
    -w "/workspace" \
    -v "$(pwd):/workspace" \
    -v "${ETC_DIR}/service_account.json:/etc/service_account.json" \
    "${FUNCTION}"
