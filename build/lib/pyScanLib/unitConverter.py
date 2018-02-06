
#======================================================================
#	File Name:	    unitConverter
#   Location:       https://github.com/soachishti/pyScanLib
#	License:        BSD 2-Clause License
#======================================================================


class unitConverter(object):

    def pixelToInch(self, pixel):
        """Convert pixels to Inch using current dpi set
        It must be called after setDPI function otherwise dpi = 200
        """
        return (pixel / float(self.dpi))

    def cmToInch(self, cm):
        """Convert Centimetre(cm) to Inch
        """
        return (cm * 0.39370)

    def inchTomm(self, inch):
        """Convert inch to millimeter
        """
        return (inch / 0.039370)

    def mmToInch(self, mm):
        """Convert millimeter to inch
        """
        return mm * 0.039370
