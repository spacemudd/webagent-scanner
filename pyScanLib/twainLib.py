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

        self.scanner.RequestAcquire(0, 1) # RequestAcquire(ShowUI, ShowModal)
        info = self.scanner.GetImageInfo()
        images = []
        handles = []
        try:
            handle, more = self.scanner.XferImageNatively()
            handles.append(handle)
        except twain.excDSTransferCancelled:
            return []
        while more != 0:
            try:
                handle, more = self.scanner.XferImageNatively()
                handles.append(handle)
            except twain.excDSTransferCancelled:
                more = 0

        for handle in handles:
            images.append(Image.open(StringIO(twain.DIBToBMFile(handle))))
            twain.GlobalHandleFree(handle)

        return images

    def detectBlankPages(self):
        try:
            self.scanner.SetCapability(twain.ICAP_AUTODISCARDBLANKPAGES, twain.TWTY_UINT16, False)
        except twain.excTWCC_CAPUNSUPPORTED:
            print "shit, it aint supported"


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
