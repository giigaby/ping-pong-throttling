from flask import Flask, request, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address, headers_enabled=True)

@app.route("/ping")
@limiter.limit("2/seconds")
def pong():
    if "x-secret-key" in request.headers and isinstance(request.headers.get("x-secret-key"), str) :
        return "pong"
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401

@app.errorhandler(429)
def ratelimit_handler(e):
    return  make_response(
            jsonify(error="request throttled request %s" % e.description)
            , 429
        )
        
if __name__ == "__main__":
    app.run(host="0.0.0.0")