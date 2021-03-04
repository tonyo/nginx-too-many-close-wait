# nginx-too-many-close-wait

In this repository we demonstrate how the CLOSE_WAIT leak issue in Nginx can be reproduced.

## Description

In some cases, Nginx doesn't close downstream connections properly, and as a result, lots of "hanging" CLOSE_WAIT sockets can be seen e.g. when checking `netstat`.

One of these cases: Envoy sitting in front of Nginx, and Nginx responds (unconditionally) with some status code via a `return` statement.

## Requirements

`docker` and `docker-compose`

## Steps

- Build all images and start Envoy and Nginx (in the first tab):

      docker-compose up

- Start the load tester (in the second tab). This will send some traffic to the Envoy container:

      ./run_load_tester.sh

- Check the CLOSE_WAIT sockets in the Nginx container:

      docker-compose exec nginx watch 'netstat -atunpl | grep CLOSE_WAIT'
