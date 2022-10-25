# memory_leak_tag_bind.py
# Copyright 2022 Roger Marsh
# Licence: See LICENCE (BSD licence)

"""Demonstrate memory leak for tkinter.Text tag_bind method.

Watch top report on unix, or Task Manager on Microsoft Windows, while
running this module if psutil is not installed.

"""

import tkinter

try:
    import psutil
except ImportError:  # Not ModuleNotFoundError for Pythons earlier than 3.6
    psutil = None


if __name__ == "__main__":

    def callback(event):
        """Avoid defining a lambda in each bind call."""

    if psutil is not None:
        proc = psutil.Process()
    widget = tkinter.Text()
    print("Repeated tag_bind calls without tag_unbind (10 x 100000).")
    if psutil is not None:
        print(proc.memory_full_info())
    for j in range(10):
        for i in range(100000):
            widget.tag_bind(tkinter.SEL, "a", callback)
        print(j + 1, "of 10")
    print("tag_bind loop done.")
    if psutil is not None:
        print(proc.memory_full_info())
    print("Done")
