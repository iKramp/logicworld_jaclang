class StackManager:
    def __init__(self):
        self.top = 0

    def allocate(self):
        self.top += 1
        return self.top - 1

    def getSize(self):
        return self.top