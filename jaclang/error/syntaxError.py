class JaclangSyntaxError(Exception):
    def __init__(self, pos: int, message: str):
        self.pos = pos
        self.message = message

    def printError(self, file_contents: str):
        print(f"SyntaxError: {self.message}")
        right = self.pos
        left = self.pos

        while right < len(file_contents) and file_contents[right] != '\n':
            right += 1

        while left >= 0 and file_contents[left - 1] != '\n':
            left -= 1

        print(file_contents[left:right].replace("\t", " "))
        print(" " * (self.pos - left) + "^")
