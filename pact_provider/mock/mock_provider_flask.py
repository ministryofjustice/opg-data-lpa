from flask import Flask, Response
import json

app = Flask(__name__)


# This is to test the deploy logic, not pact logic so this can be very basic
@app.route("/case/<id>")
def case(id):
    if id == "123":
        response_msg = {"name": "Joe Bloggs"}
        response_status = 200
    else:
        response_msg = {}
        response_status = 404

    response = Response(
        json.dumps(response_msg), status=response_status, mimetype="application/json"
    )
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0")
