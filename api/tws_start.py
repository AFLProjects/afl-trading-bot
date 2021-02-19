import os, time
import pyautogui
import threading
import api.tws_api as tws_api

_USERNAME_ = ''
_PASSWORD_ = ''

class _start_(threading.Thread):
    def run(self):
        _VERSION_ = 978
        _PATH_ = f'C:\\Jts\\{_VERSION_}\\tws.exe'
        os.system(_PATH_);
        pass

def _init_api_():
    global _USERNAME_
    global _PASSWORD_
    thread = _start_()
    thread.daemon = True
    thread.start()
    time.sleep(5)
    pyautogui.typewrite(_USERNAME_)
    pyautogui.press('tab')
    pyautogui.typewrite(_PASSWORD_)
    pyautogui.press('enter')
    time.sleep(20)
    api = tws_api.init_api()
    time.sleep(5)
    return api



