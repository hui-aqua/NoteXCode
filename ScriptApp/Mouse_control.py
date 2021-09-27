from pynput.mouse import Button, Controller
import time

mouse = Controller()
print(mouse.position)
print("Starting...")
# a tool to click the left button artificially.
k = 0  # Counter
while k < 300:
    k += 1
    time.sleep(0.5) # pause
    mouse.position = (-420, 359) # position of Cursor on screen
    mouse.click(Button.left, 1) # action, click left button.

print("finish")