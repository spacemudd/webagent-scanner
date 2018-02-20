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
        try:
            image = scan()
        except transferCancelled:
            self.write('Damn!')

        buffer = StringIO()
        image.save(buffer, format = "jpeg")
        img_str = base64.b64encode(buffer.getvalue())
        self.write(img_str)

class MultiScanHandler(BaseHandler):
    def get(self):
        images = multiScan()
        self.write(images)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/scan", ScanHandler),
        (r"/multi-scan", MultiScanHandler),
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app, ssl_options = {
            "certfile": "cert/localhost_cert.crt",
            "keyfile": "cert/localhost_cert.key",
        })
    server.listen(8087)
    tornado.ioloop.IOLoop.current().start()

class transferCancelled(Exception):
    pass

def scan():
    loadScanner = pyScanLib()
    devices = loadScanner.getScanners()
    print devices
    loadScanner.setScanner(devices[0])

    loadScanner.setDPI(300)

    # loadScanner.setScanArea(width=8.26,height=11.693) # (left,top,width,height) in inches (A4)

    loadScanner.setPixelType("color") # bw/gray/color

    pil = loadScanner.scan()

    if not pil:
        raise transferCancelled

    loadScanner.closeScanner()
    loadScanner.close()

    return pil

def multiScan():
    """ Returns a list of images (PIL in Array) scanned.
    """
    loadScanner = pyScanLib()
    devices = loadScanner.getScanners()
    print devices
    loadScanner.setScanner(devices[0])

    loadScanner.setDPI(300)

    #loadScanner.setScanArea(width=8.26,height=11.693) # (left,top,width,height) in inches (A4)

    loadScanner.setPixelType('color') # bw/gray/color

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
        try:
            main()
        except(KeyboardInterrupt, SystemExit):
            raise
        # except:
        #     print("Error")

if __name__ == '__main__':
    serverThread = HttpServerThread("Connection")
    serverThread.start()
    trayapp = sysTrayIcon.App(False)
    trayapp.MainLoop()
