import pyautogui
import time
pyautogui.PAUSE = 0.5  # Sets a 0.5 second pause after each PyAutoGUI call

#pyautogui.write('Automate my tasks', interval=0.1)


# Open the start menu
pyautogui.press('win')
time.sleep(1)
# Type the name of the browser (e.g., "firefox") and press enter
pyautogui.write('remote', interval=0.25)
pyautogui.press('enter')
time.sleep(2)  # Wait for the browser to open

pyautogui.write('', interval=0.25)
pyautogui.press('enter')
