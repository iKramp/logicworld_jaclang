import time
import keyboard

WORD_KEYS = "IUYTREWQ87654321"


def writeBinary(binary_code):
    print("Waiting for key 'p' to be pressed. Then the compiler will start the writing process.")
    keyboard.wait("p")

    keyboard.press("o")
    time.sleep(0.1)
    keyboard.release("o")
    time.sleep(0.1)
    for byte_index in range(0, len(binary_code), 2):
        word = binary_code[byte_index] + (binary_code[byte_index + 1] << 8)
        keys_to_press = []
        for i in range(16):
            if (word >> i) & 1 == 1:
                keys_to_press.append(WORD_KEYS[i])

        for key in keys_to_press:
            keyboard.press(key)
        time.sleep(0.1)
        for key in keys_to_press:
            keyboard.release(key)
        keyboard.press("0")
        time.sleep(0.1)
        keyboard.release("0")
        time.sleep(0.1)

    keyboard.press("l")
    time.sleep(0.1)
    keyboard.release("l")
