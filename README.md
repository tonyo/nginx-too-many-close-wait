# nginx-too-many-close-wait

In this repository we demonstrate how the CLOSE_WAIT leak issue in Nginx can be reproduced.

## Description

In some cases, Nginx doesn't close downstream connections properly, and as a result, lots of "hanging" CLOSE_WAIT sockets can be seen e.g. when checking `netstat`.

One of these cases: Envoy sitting in front of Nginx, and Nginx responds (unconditionally) with some status code via a `return` statement (see `nginx/nginx.conf` for an example configuration).

### Components

On the high-level, the setup is the following:

      load-tester -> Envoy (port 8090) -> Nginx (port 8080)

The components are:

* **load-tester** - a Python script that sends POST requests with a non-empty body
* **Envoy** - [Envoy proxy](https://www.envoyproxy.io/), version 1.16.0
* **Nginx** - [Nginx web server](https://nginx.org/), version 1.19.7

## Requirements

`docker` and `docker-compose`

## Steps to Reproduce

- Build all images and start Envoy and Nginx (in the first tab):

      docker-compose up

- Start the load tester (in the second tab). This will send some traffic to the Envoy container:

      ./run_load_tester.sh

- Check the CLOSE_WAIT sockets in the Nginx container (in another tab):

      docker-compose exec nginx watch 'netstat -atunpl | grep CLOSE_WAIT'
      
  You will see something like this:
  
  ```
  Every 1.0s: netstat -atunpl | grep CLOSE_WAIT                                                                                                                                                                               

  tcp        0      0 172.20.0.3:8080         172.20.0.4:36124        CLOSE_WAIT  -
  tcp        0      0 172.20.0.3:8080         172.20.0.4:60178        CLOSE_WAIT  -
  tcp        0      0 172.20.0.3:8080         172.20.0.4:57830        CLOSE_WAIT  -
  tcp        0      0 172.20.0.3:8080         172.20.0.4:34660        CLOSE_WAIT  -
  tcp        0      0 172.20.0.3:8080         172.20.0.4:35056        CLOSE_WAIT  -
  tcp        0      0 172.20.0.3:8080         172.20.0.4:32968        CLOSE_WAIT  -
  ```
  
  
## Additional Information

### What is CLOSE_WAIT?

From [here](https://blog.cloudflare.com/this-is-strictly-a-violation-of-the-tcp-specification/):


> CLOSE_WAIT - Indicates that the server has received the first FIN signal from the client and the connection is in the process of being closed. This means the socket is waiting for the application to execute close(). A socket can be in CLOSE_WAIT state indefinitely until the application closes it. Faulty scenarios would be like a file descriptor leak: server not executing close() on sockets leading to pile up of CLOSE_WAIT sockets.

So in this case, it's Nginx who doesn't close the connection immediately after receiving the FIN packet from the downstream (Envoy).

### Show me some traffic

This is how one of the TCP streams look like in Wireshark:

![image](https://user-images.githubusercontent.com/1120468/110104729-d286eb80-7da7-11eb-89ca-59ac78cbe023.png)


As we see, the second response (in blue) sent before reading the full request body, which might hint at the specific situation when the issue is triggered.

### Q&A

* Do these CLOSE_WAIT sockets disappear at some point?

  Yes, for example when the keep-alive timeout expires on Nginx side.


* Is the issue present when keep-alive is disabled in Nginx (`keepalive_timeout 0`)?

  No, I couldn't reproduce the issue in that situation.
  
  




