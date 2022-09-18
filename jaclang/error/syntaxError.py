class JaclangSyntaxError(Exception):
    def __init__(self, pos: int, message: str):
        self.pos = pos
        self.message = message

    def printError(self, file_contents: str):
        print(f"SyntaxError: {self.message}")
        r = self.pos
        l = self.pos

        while r < len(file_contents) and file_contents[r] != '\n':
            r += 1

        while l >= 0 and file_contents[l] != '\n':
            l += 1

        print(file_contents[l:r])
