#!/usr/bin/env bash
set -eux

IMAGE_ID=$(docker-compose images -q load-tester)


docker run --network=host --rm -it -e TEST_URL=http://localhost:8090 $IMAGE_ID
