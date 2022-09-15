import time
import keyboard


def writeBinary(binary_code):
    time.sleep(3)

    keyboard.press("o")
    time.sleep(0.1)
    keyboard.release("o")
    time.sleep(0.1)
    for byte in binary_code:
        for i in range(8):
            bit = (byte >> i) & 1
            key = "0" if bit == 0 else "1"
            keyboard.press(key)
            time.sleep(0.04)
            keyboard.release(key)
            time.sleep(0.03)
        time.sleep(0.02)
    keyboard.press("l")
    time.sleep(0.1)
    keyboard.release("l")
    time.sleep(0.1)
