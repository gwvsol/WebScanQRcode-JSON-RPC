import imutils
import time
from imutils.video import VideoStream
from imutils.video import FPS
from pyzbar import pyzbar
from threading import Thread
from pathlib import PosixPath
from datetime import datetime
from .log import logging as log


class WebScanDev(object):
    """ Сканирование и распознавание QR кодов """
    def __init__(self, webcam: PosixPath, barcodes: set, db: dict) -> None:
        self.log = log
        self.cam = webcam
        self.barcodes = barcodes
        self.db = db
        self.scanoff = 60

    def getWebCam(self):
        """ Подключаемся к web камере """
        self.log.info(f"PORT OPEN {self.cam.absolute()}")
        cam = str(self.cam.absolute())
        vs = VideoStream(src=cam,
                         resolution=(640, 480),
                         framerate=30).start()
        time.sleep(2.0)
        fps = FPS().start()
        return vs, fps

    def scan(self):
        """ Cканирование и распознавание QR кодов """
        vs, fps = self.getWebCam()
        scantime, lastbarcode = datetime.now(), datetime.now()

        while self.db.get('status') == "ScanON":
            try:
                time.sleep(0.6)  # Задержка  для фокусировки камеры
                frame = vs.read()
                frame = imutils.resize(frame, width=640)
                barcodes = pyzbar.decode(frame)  # Декодируем изображение
                # Распознаем баркоды
                for barcode in barcodes:
                    # Декодируем баркоды в строку
                    bdata = barcode.data.decode("utf-8")
                    # btype = barcode.type
                    if bdata not in self.barcodes:
                        self.barcodes.add(bdata)
                        lastbarcode = datetime.now()

                deltascan = datetime.now() - scantime
                deltabarcode = datetime.now() - lastbarcode
                # Если найден хотя бы один баркод и прошло более 0,5с или
                # С момента сканирования прошло времени более установленного
                # в scanoff завершаем сканирование
                if (len(self.barcodes) >= 1 and
                        deltabarcode.microseconds > 500000) or \
                        deltascan.seconds > self.scanoff:
                    self.db.update({'status': 'ScanOFF',
                                    'scan': list(self.barcodes)})
                    self.log.info('=> AUTOSTOP')
                    self.log.info(f'=> BARCODE {self.db.get("scan")}')
                    break
                fps.update()
            except AttributeError as err:
                self.barcodes.clear()
                self.log.error(f"ERROR SCAN {err}")
                break
        vs.stop()

    def start(self):
        """ Включаем сканирование """
        self.barcodes.clear()
        self.db.update({'status': 'ScanON', 'scan': list()})
        Thread(target=self.scan).start()

    def stop(self):
        """ Выключаем скнирование """
        self.db.update({'status': 'ScanOFF'})
        self.db.update({'scan': list(self.barcodes)})
        self.barcodes.clear()
