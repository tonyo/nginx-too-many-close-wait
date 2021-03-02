import logging
import os
import time
from multiprocessing import Pool

import requests

URL = os.environ.get("TEST_URL", "http://127.0.0.1:8090")

logging.basicConfig(level=logging.DEBUG)

event = {
    "key_{}".format(x): "value_{}".format(x) for x in range(20)
}

def send_few(x):
    s = requests.Session()
    res = s.post(URL, data=event)
    _ = res.text
    s.close()


if __name__ == "__main__":
    with Pool(20) as p:
        p.map(send_few, range(10000))
