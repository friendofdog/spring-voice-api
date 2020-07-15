from flask import Flask


app = Flask(__name__)
app.config.from_object("config")
VERSION = "v1"


@app.route(f"/api/{VERSION}/healthcheck", methods=['GET'])
def healthcheck():
    return {"success": True}


if __name__ == '__main__':
    app.run(debug=True)
