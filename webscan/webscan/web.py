from flask import Flask, Response, request
from jsonrpcserver import method, Result, Success, dispatch
from .log import logging as log


app = Flask(__name__)


@method
def ping() -> Result:
    log.info('PING => PONG')
    return Success("pong")


@app.route("/", methods=["POST"])
def index():
    return Response(
        dispatch(request.get_data().decode()),
        content_type="application/json")

def main():
    return app
