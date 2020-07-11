from flask import Flask, jsonify

app = Flask(__name__)
VERSION = "v1"


@app.route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck():
    try:
        return jsonify({"success": True}), 200
    except Exception as e:
        return f"An error occured: {e}"


if __name__ == '__main__':
    app.run(debug=True)
