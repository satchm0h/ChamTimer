"""
This brings together the Timer object and the Relay object. Pretty much just
a simple wrapper class.

"""

from timer import new_wall_clock_timer
from relay import Relay
import logging




class RelayTimer(Relay):
    def __init__(self, name, relay_pin, period, on_hour, on_min=0, on_sec=0, relay_state=False, secondary_period=None):
        super().__init__(relay_pin, relay_state)
        self.timer = new_wall_clock_timer(name + "_timer", self.toggle, period,
                                          on_hour, on_min, on_sec, secondary_period)
        self.name = name
        logging.info("Created RelayTimer: %s" % self.name)
        logging.debug(str(self.timer.get_as_dict()))

    def is_time_to_run(self):
        return self.timer.is_time_to_run()

    def run(self):
        logging.info("Running RelayTimer: %s in state %s" % (self.name, str(self.state)))
        return self.timer.run()
