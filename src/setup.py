import utils.stdout2 as std2
import pip

def import_package(package):
    try:
        __import__(package)
    except ImportError:
        pip.main(['install', package])

std2.write_line('Checking for modules and installing them...')
modules = ["ibapi", "matplotlib", "contextlib", "yfinance", "datetime", "time", "time", "csv", "os", "sys", "urllib", "math", "requests"]
for i, module in enumerate(modules):
	std2.write_progress_bar(i+1, len(modules), 40)
	with std2.suppress_stdout():
		import_package(module)
std2.write_line('Everything is up to date !')

pause = input('Press a key to exit.')

