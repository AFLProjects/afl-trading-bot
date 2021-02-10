from contextlib import contextmanager
from math import *
import os, sys

@contextmanager
def suppress_stdout():
    with open(os.devnull, "w") as devnull:
        old_stdout = sys.stdout
        sys.stdout = devnull
        try:  
            yield
        finally:
            sys.stdout = old_stdout

def write_progress_bar(i, m, toolbar_width):
    p = f'{round(i / m * 100)}.'
    p += '0' * (5 - len(p))
    sys.stdout.write(f'{p}% |')
    sys.stdout.flush()
    c = ceil(round(toolbar_width * (i / m)))
    for j in range(c):
        sys.stdout.write("█")
        sys.stdout.flush()
    sys.stdout.write(' ' * (toolbar_width - c))
    sys.stdout.write(f'| {i}/{m} \r')
    sys.stdout.flush()
