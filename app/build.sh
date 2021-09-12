#!/bin/bash

. ./config.sh

pack build "${IMAGE}" --builder gcr.io/buildpacks/builder
