import os, time
import pyautogui
import threading

_USERNAME_ = '_USERNAME_'
_PASSWORD_ = '_PASSWORD_'
class _start_(threading.Thread):
    def run(self):
        _VERSION_ = 978
        _PATH_ = f'C:\\Jts\\{_VERSION_}\\tws.exe'
        os.system(_PATH_);
        pass
thread = _start_()
thread.daemon = True
thread.start()
time.sleep(5)
pyautogui.typewrite(_USERNAME_)
pyautogui.press('tab')
pyautogui.typewrite(_PASSWORD_)
pyautogui.press('enter')

