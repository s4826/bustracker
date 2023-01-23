"""Function call cache decorator"""

import time


class Cache():
    """
    Cache the results of a function call for a certain amount of time
    """
    def __init__(self, seconds=float('inf')):
        """
        Initialize a decorator instance

        :param int seconds: return cached result for this many seconds
        """
        self.most_recent = time.time()
        self.res = None
        self.seconds = seconds

    def __call__(self, func):
        def wrapper():
            if abs(time.time() - self.most_recent) < self.seconds and \
                    self.res is not None:
                return self.res
            self.res = func()
            self.most_recent = time.time()
            return self.res
        return wrapper
