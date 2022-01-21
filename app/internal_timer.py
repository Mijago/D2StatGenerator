import time


class Timer:
    """
    Allows you to easily time how long a piece of code takes.
    Logs the result in the console.

    Example
    -------------
    with Timer("get pgcrs"):
        calculateStuff()
    """
    def __init__(self, name):
        self._name = name

    def __enter__(self):
        print("Start Timer '%s'" % (self._name))
        self._start = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("Stop  Timer '%s' - %f" % (self._name, time.time() - self._start))
