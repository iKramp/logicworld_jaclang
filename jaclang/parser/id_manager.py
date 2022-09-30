class IdManager:
    def __init__(self):
        self.curr_id = 0

    def requestId(self):
        result = self.curr_id
        self.curr_id += 1
        return result
