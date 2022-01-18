class Player(object):
    def __init__(self, x, y, team, shirtnumber,role, name):
        self.x = x
        self.y = y
        self.team = team
        self.name = name
        self.shirtnumber = shirtnumber
        self.role = role

    def setPosition(self, newPosition):
        self.x, self.y = newPosition

    def getPosition(self):
        return (self.x, self.y)

    def getRole(self):
        return self.role

    def getshirtnumber(self):
        return self.role

    def getteam(self):
        return self.team


