from pyScanLib import pyScanLib
from StringIO import StringIO

import tornado.httpserver
import tornado.ioloop
import tornado.web
from threading import Thread
import base64
import sysTrayIcon

class BaseHandler(tornado.web.RequestHandler):
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Headers", "x-requested-with")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

class MainHandler(BaseHandler):
    def get(self):
        self.write("Scanner Web-Agent")

class ScanHandler(BaseHandler):
    def get(self):
        scannerName = self.get_argument('scanner', default=None)
        try:
            image = scan(scannerName)
        except transferCancelled:
            self.write('Transfer cancelled')

        buffer = StringIO()
        image.save(buffer, format = "jpeg")
        img_str = base64.b64encode(buffer.getvalue())
        self.write(img_str)

class MultiScanHandler(BaseHandler):
    def get(self):
        scannerName = self.get_argument('scanner', default=None)
        resolution = self.get_argument('resolution', default=100)
        pixelType = self.get_argument('pixel-type', default="color")
        duplex = self.get_argument('duplex', default="0")
        images = multiScan(scannerName, resolution, pixelType, duplex)
        self.write(images)

class GetScannersHandler(BaseHandler):
    def get(self):
        loadScanner = pyScanLib()
        devices = loadScanner.getScanners()

        devicesDict = {}
        for device in devices:
            devicesDict[device] = device

        self.write(devicesDict)

class CloseServerHandler(BaseHandler):
    def get(self):
        self.write('Closing...')
        tornado.ioloop.IOLoop.instance().stop()

def buildRoutes():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/scan", ScanHandler),
        (r"/multi-scan", MultiScanHandler),
        (r"/get-scanners", GetScannersHandler),
        (r"/close", CloseServerHandler),
    ])

def openWebServer():
    app = buildRoutes()
    server = tornado.httpserver.HTTPServer(app, ssl_options = {
            "certfile": "cert/localhost_cert.crt",
            "keyfile": "cert/localhost_cert.key",
        })
    server.listen(8087)
    ioloop = tornado.ioloop.IOLoop.instance()
    ioloop.start()

class transferCancelled(Exception):
    pass

def scan(scannerName=None):
    loadScanner = pyScanLib()
    devices = loadScanner.getScanners()
    print devices
    if scannerName:
        loadScanner.setScanner(scannerName)
    else:
        loadScanner.setScanner(devices[0])


    loadScanner.setDPI(100)

    # loadScanner.setScanArea(width=8.26,height=11.693) # (left,top,width,height) in inches (A4)

    loadScanner.setPixelType("color") # bw/gray/color

    pil = loadScanner.scan()

    if not pil:
        raise transferCancelled

    loadScanner.closeScanner()
    loadScanner.close()

    return pil

def multiScan(scannerName=None, resolution=100, pixelType='color', duplex="0"):
    """ Returns a list of images (PIL in Array) scanned.
    """

    loadScanner = pyScanLib()
    devices = loadScanner.getScanners()
    print devices
    if scannerName:
        loadScanner.setScanner(scannerName)
    else:
        loadScanner.setScanner(devices[0])

    loadScanner.setDPI(resolution)

    #loadScanner.setScanArea(width=8.26,height=11.693) # (left,top,width,height) in inches (A4)

    loadScanner.setPixelType(pixelType) # bw/gray/color

    if duplex == "0":
        loadScanner.setDuplex(False)
    else:
        loadScanner.setDuplex(True)

    pils = loadScanner.multiScan()

    loadScanner.closeScanner()
    loadScanner.close()

    imagesArray = []
    for pil in pils:
        buffer = StringIO()
        pil.save(buffer, format = 'JPEG')
        img_str = base64.b64encode(buffer.getvalue())
        imagesArray.append(img_str)

    imagesDict = {'images': imagesArray, 'total': len(imagesArray)}

    return imagesDict

class HttpServerThread(Thread):
    def __init__(self, name):
        Thread.__init__(self)
        self.name = name
    def run(self):
        openWebServer()

class TrayIconThread(Thread):
    def __init__(self, name, tornadoThread):
        Thread.__init__(self)
        self.name = name
        self.tornadoThread = tornadoThread
    def run(self):
        trayApp = sysTrayIcon.App(False)
        trayApp.MainLoop()

if __name__ == '__main__':
    serverThread = HttpServerThread("Connection")
    serverThread.start()

    trayIconThread = TrayIconThread("Tray icon", serverThread)
    trayIconThread.start()

