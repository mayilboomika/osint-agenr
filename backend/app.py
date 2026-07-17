from flask import Flask, jsonify, render_template
from routes import api

app = Flask(__name__, template_folder="templates")
app.register_blueprint(api, url_prefix="/api")


@app.after_request
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, OPTIONS"
    return response


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK", "message": "OSINT backend is running."})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
