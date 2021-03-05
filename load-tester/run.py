import logging
import os
import time
from multiprocessing import Pool

import requests

URL = os.environ.get("TEST_URL", "http://127.0.0.1:8090")

logging.basicConfig(level=logging.DEBUG)

# Non-empty body
event = {
    "key_{}".format(x): "value_{}".format(x) for x in range(20)
}

def send_request():
    s = requests.Session()
    s.post(URL, data=event)
    s.close()


if __name__ == "__main__":
    for _ in range(10000):
        send_request()
