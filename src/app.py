from flask import Flask, request, jsonify, make_response
from flask.helpers import url_for
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
app.config['RATELIMIT_HEADER_REMAINING'] = True
limiter = Limiter(app, headers_enabled=True, key_func=get_remote_address, retry_after=True )

def limit_x_secret_key():
    return request.headers.get("x-secret-key")

def host_scope(endpoint_name):
    return request.host
host_limit = limiter.shared_limit("2/second", scope=host_scope)

@app.route("/ping")
@limiter.limit("10/minute", limit_x_secret_key)
@host_limit
def pong():
    if "x-secret-key" in request.headers and isinstance(limit_x_secret_key(), str) :
        return "pong"
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401


#In next release we will available to get the headers of the elapsed time https://github.com/alisaifee/flask-limiter/issues/276
@app.errorhandler(429)
def ratelimit_handler(e):
    return  make_response(
            jsonify(message="request throttled request", throttle_age = "%s" % e.description)
            , 429
        )

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)