import json
import hmac
import hashlib

import requests


def main():
    with open("notifications.json", "rb") as fd:
        byt = fd.read()

    sig = hmac.new(b"1234", msg=byt, digestmod=hashlib.sha256).hexdigest()
    requests.post("http://localhost:5000/webhooks/", data=byt,
                  headers={"X-Sqreen-Integrity": sig,
                           "Content-Type": "application/json"})

if __name__ == "__main__":
    main()
