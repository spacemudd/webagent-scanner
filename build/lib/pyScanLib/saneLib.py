import sane

#======================================================================
#	Name:	    saneLib
#   Location:   https://github.com/soachishti/pyScanLib
#	License:    BSD 2-Clause License
#======================================================================

class saneLib(object):

    """The is main class of SANE API (Linux)
    """

    def __init__(self):
        self.dpi = 200
        self.layout = False

    def getScanners(self):
        """Get available scanner from sane module
        """
        sane.init()
        devices = sane.get_devices()[0]
        if len(devices) > 0:
            return devices
        else:
            return None

    def setScanner(self, scannerName):
        """Connected to Scanner using Scanner Name

        Arguments:
        scannerName -- Name of Scanner return by getScanners()
        """
        self.scanner = sane.open(scannerName)

    def setDPI(self, dpi):
        """Set DPI to selected scanner and dpi to self.dpi
        """
        self.dpi = dpi
        self.scanner.resolution = self.dpi

    def setScanArea(self, left=0.0, top=0.0, width=8.267, height=11.693):
        """Set Custom scanner layout to selected scanner in Inches

        Arguments:
        left -- Left position of scanned Image in scanner 
        top -- Top position of scanned Image in scanner
        width(right) -- Width of scanned Image
        bottom(height) -- Height of scanned Image
        """

        # http://www.sane-project.org/html/doc014.html#f5
        # (left, top, right, bottom)
        # top left x axis          left
        self.scanner.tl_x = float(inchTomm(left))
        # top left y axis           top
        self.scanner.tl_y = float(inchTomm(top))
        # bottom left x axis      width
        self.scanner.br_x = float(inchTomm(width))
        # bottom left y axis     height
        self.scanner.br_y = float(inchTomm(height))

    def getScannerSize(self):
        """Return Scanner Layout as Tuple (left, top, right, bottom) in Inches      
        """
        return (mmToInch(self.scanner.tl_x), mmToInch(self.scanner.tl_y), mmToInch(self.scanner.br_x), mmToInch(self.scanner.br_y))

    def setPixelType(self, pixelType):
        """Set pixelType to selected scanner

        Arguments:
        pixelType -- Pixel type - bw (Black & White), gray (Gray) and color(Colored)

        """
        self.scanner.mode = pixelType.lower()

    def scan(self):
        """Scan and return PIL object if success else return False
        """
        try:
            self.scanner.start()
            image = self.scanner.snap()
            return image
        except:
            return False

    def closeScanner(self):
        """ Destory 'self.scanner' class of sane module generated in setScanner function
        """
        if self.scanner:
            self.scanner.close()
            del self.scanner

    def scanPreview(self):
        """Pray for this function ;)
        """
        raise NotImplementedError

    def close(self):
        """
        Destory 'sane' class of sane module generated in getScanners function ie sane.init()
        Destory 'self.scanner' class of sane module generated in setScanner function
        """
        if self.scanner:
            self.scanner.close()
        sane.exit()
