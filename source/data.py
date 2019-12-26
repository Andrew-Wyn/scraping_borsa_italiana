import enum

class Status(enum.Enum): 
    BUY = "BUY"
    SELL = "SELL"
    NOTHING = "NOTHING"

class Action(object):
    def __init__(self, title, aperture, max_oggi, min_oggi, max_anno, min_anno):
        self.title = title
        self.aperture = aperture
        self.max_oggi = max_oggi
        self.min_oggi = min_oggi
        self.max_anno = max_anno
        self.min_anno = min_anno
        self.status = None

    def setStatus(self, status):
        self.status = status

    def toString(self): # bad practice
        return "name: " + self.title + " -> aperture: " + str(self.aperture) + " - max_oggi:" + str(self.max_oggi) + " - min_oggi: " + str(self.min_oggi) + " - max_anno: " + str(self.max_anno) + " - min_anno: " + str(self.min_anno) + " - status: " + self.status.name

actions = []
