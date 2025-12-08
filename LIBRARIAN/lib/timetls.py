""" Time tools 

	Domeu - Dec 2, 2025 - sourced from https://github.com/capella-ben/microPython_MCP2515
"""

from time import ticks_ms

class TimeoutTimer:
    """A reusable class to track timeouts, like an egg timer"""

    def __init__(self, timeout=0.0):
        self._timeout = 0.0 
        self._start_time = 0.0
        if timeout:
            self.setTimer(timeout)

    @property
    def expired(self):
        """Returns the expiration status of the timer

        Returns:
            bool: True if more than `timeout` seconds has past since it was set
        """
        return ((ticks_ms()/1000) - self._start_time) > self._timeout

    def setTimer(self, new_timeout: float):
        """Set the length of the timer"""
        self._timeout = float(new_timeout)
        self._start_time = ticks_ms()/1000

        