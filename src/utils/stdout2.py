from contextlib import contextmanager
from math import *
import os, sys, time

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def write(str):
	sys.stdout.write(str)
	sys.stdout.flush()

def write_line(str):
	sys.stdout.write(str + "\n")
	sys.stdout.flush()
   
def write_progress_bar(i, m, toolbar_width):
    p = f'{round(i / m * 100)}.'
    p += '0' * (5 - len(p))
    sys.stdout.write(f'{p}% |')
    c = ceil(round(toolbar_width * (i / m)))
    for j in range(c):
        sys.stdout.write("█")
    sys.stdout.write(' ' * (toolbar_width - c))
    sys.stdout.write(f'| {i}/{m} \r')
    if i == m:
    	sys.stdout.write('\n')
    sys.stdout.flush()

def pause_progress_bar(seconds):
    for i in range(seconds * 100):
        time.sleep(seconds / 100)
        write_progress_bar(i+1, seconds * 100, 40)
