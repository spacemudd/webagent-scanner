import twain
from PIL import Image
from StringIO import StringIO

#======================================================================
#	Name:	    twainLib
#   Location:   https://github.com/soachishti/pyScanLib
#	License:    BSD 2-Clause License
#======================================================================

class twainLib(object):

    """The is main class of Twain API (Win32)
    """

    def __init__(self):
        self.dpi = 200  # Define for use in pixeltoInch function
        self.scannedImages = []

    def getScanners(self):
        """Get available scanner from twain module
        """
        self.sourceManager = twain.SourceManager(0)
        scanners = self.sourceManager.GetSourceList()
        if scanners:
            return scanners
        else:
            return None

    def setScanner(self, scannerName):
        """Connected to Scanner using Scanner Name

        Arguments:
        scannerName -- Name of Scanner return by getScanners()
        """
        self.scanner = self.sourceManager.OpenSource(scannerName)

    def setDPI(self, dpi):
        """Set DPI to selected scanner and dpi to self.dpi
        """
        self.dpi = dpi
        self.scanner.SetCapability(
            twain.ICAP_XRESOLUTION, twain.TWTY_FIX32, float(self.dpi))
        self.scanner.SetCapability(
            twain.ICAP_YRESOLUTION, twain.TWTY_FIX32, float(self.dpi))

    def setScanArea(self, left=0.0, top=0.0, width=8.267, height=11.693):
        """Set Custom scanner layout to selected scanner in Inches

        Arguments:
        left -- Left position of scanned Image in scanner 
        top -- Top position of scanned Image in scanner
        width(right) -- Width of scanned Image
        bottom(height) -- Height of scanned Image
        """
        #((left, top, width, height) document_number, page_number, frame_number)
        width = float(width)
        height = float(height)
        left = float(left)
        top = float(top)
        self.scanner.SetImageLayout((left, top, width, height), 1, 1, 1)

    #size in inches
    def getScannerSize(self):
        """Return Scanner Layout as Tuple (left, top, right, bottom) in Inches       
        """
        return self.scanner.GetImageLayout()

    def setPixelType(self, pixelType):
        """Set pixelType to selected scanner

        Args:
        pixelType: String  bw / gray / color
        """
        pixelTypeMap = {'bw': twain.TWPT_BW,
                        'gray': twain.TWPT_GRAY,
                        'color': twain.TWPT_RGB}
        try:
            pixelType = pixelTypeMap[pixelType]
        except:
            pixelType = twain.TWPT_RGB
        self.scanner.SetCapability(
            twain.ICAP_PIXELTYPE, twain.TWTY_UINT16, pixelType)

    def setDuplex(self, boolEnabled):
        """ Set the duplex to be enabled or not.
        :param enabled: Boolean
        """
        try:
            self.scanner.SetCapability(twain.CAP_DUPLEXENABLED, twain.TWTY_BOOL, boolEnabled)
        except:
            print("Couldn't set duplex")


    def scan(self):
        """Scan and return PIL object if success else return False
        """
        self.scanner.RequestAcquire(0, 1)
        info = self.scanner.GetImageInfo()
        try:
            self.handle = self.scanner.XferImageNatively()[0]
            image = twain.DIBToBMFile(self.handle)
            twain.GlobalHandleFree(self.handle)
            return Image.open(StringIO(image))
        except:
            return False

    def multiScan(self):
        """ Scan and return an array of PIL objects 
            If no images, will return an empty array
        """
        if self.scanner == None:
            raise ScannerNotSet

        try:
            self.scanner.RequestAcquire(0, 0) # RequestAcquire(ShowUI, ShowModal)
        except:
            print("RequestAcquire Error")


        while self.next():
            image = self.capture()
            if not image:
                print("Capture didnt find any images")

        return self.scannedImages

    def next(self):
        try:
            print("next()")
            self.scanner.GetImageInfo()
            print("image_info()")
            return True
        except twain.excTWCC_SEQERROR:
            print("next() fired an exception()")
            return False

    def capture(self):
        try:
            print("capture()")
            (handle, more_to_come) = self.scanner.XferImageNatively()
        except twain.excDSTransferCancelled:
            return None
        self.scannedImages.append(Image.open(StringIO(twain.DIBToBMFile(handle))))
        twain.GlobalHandleFree(handle)
        return True
        

    def detectBlankPages(self):
        try:
            self.scanner.SetCapability(twain.ICAP_AUTODISCARDBLANKPAGES, twain.TWTY_UINT16, False)
        except twain.excTWCC_CAPUNSUPPORTED:
            print "Blank page detection not supported"


    def closeScanner(self):
        """ Destory 'self.scanner' class of twain module generated in setScanner function
        """
        if self.scanner:
            self.scanner.destroy()
        self.scanner = None

    def scanPreview(self):
        """Pray for this function ;)
        """
        raise NotImplementedError

    def close(self):
        """
        Destory 'self.sourceManager' class of twain module generated in getScanners function
        Destory 'self.scanner' class of twain module generated in setScanner function
        """
        if self.scanner:
            self.scanner.destroy()
        if self.sourceManager:
            self.sourceManager.destroy()
        (self.scanner, self.sourceManager) = (None, None)
