#!/bin/bash

. config.sh

docker run -it --rm \
    -e GOOGLE_APPLICATION_CREDENTIALS="/workspace/etc/service_account.json" \
    -w "/workspace" \
    -v "$(pwd):/workspace" \
    -v "${ETC_DIR}:/workspace/etc" \
    "${FUNCTION}"
