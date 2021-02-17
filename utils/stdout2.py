from contextlib import contextmanager
from math import *
import os, sys, time

# Supress console output
@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

# Append text to console
def write(str, start='', end=''):
	sys.stdout.write(start + str + end)
	sys.stdout.flush()

# Write new line
def write_line(str, start='', end=''):
	sys.stdout.write(start + str + "\n" + end)
	sys.stdout.flush()

# Append text and complete with spaces to a certain length
def write_autocomplete(str, length):
    sys.stdout.write(str + " " * (length - len(str)))
    sys.stdout.flush()

# Write line and complete with spaces to a certain length
def write_line_autocomplete(str, length):
    sys.stdout.write(str + " " * (length - len(str)) + "\n")
    sys.stdout.flush()

# Draw a progress bar
def write_progress_bar(i, m, toolbar_width, start='', end=''):
    p = f'{round(i / m * 100)}.'
    p += '0' * (5 - len(p))
    sys.stdout.write(f'{start}{p}% |')
    c = ceil(round(toolbar_width * (i / m)))
    for j in range(c):
        sys.stdout.write("█")
    sys.stdout.write(' ' * (toolbar_width - c))
    sys.stdout.write(f'| {i}/{m}{end}\r')
    if i == m:
    	sys.stdout.write('\n')
    sys.stdout.flush()

# Draw a progress bar while waiting
def pause_progress_bar(seconds, start='', end=''):
    for i in range(seconds * 100):
        time.sleep(seconds / 100)
        write_progress_bar(i+1, seconds * 100, 40, start=start, end=end)
