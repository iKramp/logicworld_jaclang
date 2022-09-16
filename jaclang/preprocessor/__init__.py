def removeSingleLineComments(code: str) -> str:
    new_code = ""
    is_in_comment = False
    for i, c in enumerate(code):
        if i < len(code) - 1 and c == '/' and code[i + 1] == '/':
            is_in_comment = True

        if c == '\n':
            is_in_comment = False

        if not is_in_comment:
            new_code += c

    return new_code


def removeMultilineComments(code: str) -> str:
    new_code = ""
    comment_nesting = 0
    for i, c in enumerate(code):
        if i < len(code) - 1 and c == '/' and code[i + 1] == '*':
            comment_nesting += 1
            new_code += " "

        if i > 1 and code[i - 2] == '*' and code[i - 1] == '/' and comment_nesting > 0:
            comment_nesting -= 1

        if comment_nesting == 0:
            new_code += c

    return new_code


def preprocess(file_contents: str, debug_output: bool = False) -> str:
    file_contents = removeSingleLineComments(file_contents)
    file_contents = removeMultilineComments(file_contents)

    if debug_output:
        print("Preprocessed code:")
        print("---------------------------------")
        print(file_contents)
        print("---------------------------------")

    file_contents = file_contents.replace("\n", " ").replace("\t", " ")
    return file_contents
