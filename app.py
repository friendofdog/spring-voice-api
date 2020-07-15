from flask import Flask, jsonify


app = Flask(__name__)
VERSION = "v1"


@app.route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck():
    return {"success": True}


if __name__ == '__main__':
    app.run(debug=True)
