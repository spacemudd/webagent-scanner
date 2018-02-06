from pyScanLib import pyScanLib
from StringIO import StringIO
import tornado.httpserver
import tornado.ioloop
import tornado.web
import uuid
import base64

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
        self.write("Hello, world")

class ScanHandler(BaseHandler):
    def get(self):
        image = scan()
        buffer = StringIO()
        image.save(buffer, format="jpeg")
        img_str = base64.b64encode(buffer.getvalue())
        self.write(img_str)

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/scan", ScanHandler)
    ])

def main():
    app = make_app()
    server = tornado.httpserver.HTTPServer(app, ssl_options = {
            "certfile": "cert/localhost_cert.crt",
            "keyfile": "cert/localhost_cert.key",
        })
    server.listen(8087)
    print "Serving on 8087..."
    tornado.ioloop.IOLoop.current().start()


def scan():
    loadScanner = pyScanLib() # load scanner library
    devices = loadScanner.getScanners()
    loadScanner.setScanner(devices[0])

    loadScanner.setDPI(300)

    # A4 Example
    loadScanner.setScanArea(width=8.26,height=11.693) # (left,top,width,height) in inches

    loadScanner.setPixelType("color") # bw/gray/color

    pil = loadScanner.scan()

    loadScanner.closeScanner() # unselect selected scanner, set in setScanners()
    loadScanner.close() # Destory whole class

    return pil

if __name__ == '__main__':
    main()
