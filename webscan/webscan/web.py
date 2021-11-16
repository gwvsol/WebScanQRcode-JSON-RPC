from flask import Flask, Response, request
from jsonrpcserver import method, Result, Success, dispatch
from .config import WEBSCAN_DATA as db
from .config import WEBSCAN_HELP as helps
from .config import WEBSCAN_BARCODES as barcodes
from .config import WEBSCAN_DEV as cam
from .scan import WebScanDev
from .log import logging as log


app = Flask(__name__)

scan = WebScanDev(webcam=cam, barcodes=barcodes, db=db)


@method
def ping() -> Result:
    """ Метод для проверки сервиса
        Запрос вида { "jsonrpc": "2.0", "method": "ping", "id": "13" }
    """
    log.info('=> PONG')
    return Success(dict(ping=db.get('ping')))


@method
def enable():
    """ Метод для включения WEB сканера
        Запрос вида { "jsonrpc": "2.0", "method": "enable", "id": "15" }
    """
    status = db.get('status')
    if status == 'ScanOFF':
        scan.start()
    log.info(f"=> {db.get('status')}")
    return Success(dict(status=db.get('status'), scan=db.get('scan')))


@method
def disable() -> Result:
    """ Метод для выключения WEB сканера
        Запрос вида { "jsonrpc": "2.0", "method": "disable", "id": "15" }
    """
    status = db.get('status')
    if status == 'ScanON':
        scan.stop()
    log.info(f"=> {db.get('status')}")
    return Success(dict(status=db.get('status'), scan=db.get('scan')))


@method
def getscan() -> Result:
    """ Метод считывания сканированных данных
        Запрос вида { "jsonrpc": "2.0", "method": "getscan", "id": "12" }
    """
    log.info(f"=> {db.get('scan')}")
    return Success(dict(status=db.get('status'), scan=db.get('scan')))


@method
def help() -> Result:
    """ Метод для получения информации по работе с сервисом
        Запрос вида { "jsonrpc": "2.0", "method": "help", "id": "12" }
    """
    log.info('=> HELP')
    return Success(dict(helps))


@app.route("/", methods=["POST"])
def index():
    return Response(
        dispatch(request.get_data().decode()),
        content_type="application/json")


def main():
    log.info('=> START WEBCAM SERVICE')
    return app
