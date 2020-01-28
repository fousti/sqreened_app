from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=("POST",))
def http_backend():
    notifications = request.get_json()
    print("Received dispatch notification from webhooks app, msg: %s" % notifications)
    return 'Ok', 200

app.run(host="localhost", port=8080)
