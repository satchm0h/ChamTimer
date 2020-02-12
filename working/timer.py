
'''
What we are trying to do here is support simple periodic wall clock timers.
They come in two forms. First is a simple periodic timer. It runs the provided
callback Every N seconds. Second is a nested timer. It runs the provided
last_callback every N seconds (primary period), then again M seconds later
(secondary period). this allows for use cases like "Turn on the humidifyer for
five minutes every hour". TODO : Allow for optional secondary callback...should
just do the primary calback if not defined

'''

from sys import stderr
from time import time
from datetime import datetime, time as dt_time
import logging

# Custom Exception
class TimerInvalidSecondaryPeriod (ValueError):
    def __init__(self, period, message=None):
        if not message:
            message = "Invalid secondary timer provided to Timer: "+ period.str()
        self.message = message
        print(message, file=stderr)
        pass

# Factory functiuon to create wall-clock based timers.
def new_wall_clock_timer(name, callback, period, on_hour=0, on_min=0, on_sec=0, secondary_period=None):
    # figure out when the next valid primary period trigger time is.
    right_now = datetime.now()
    logging.info("New Timer Creation: '%s' OnHour: %d, OnMin: %d, Primary: %d, Secondary: %s"
                % (name, on_hour, on_min, period, str(secondary_period)))
    logging.info("\tNow: " + right_now.strftime('%Y-%m-%d %H:%M:%S'))
    initial_start = first_trigger = datetime.combine(right_now.date(), dt_time(on_hour, on_min, on_sec)).timestamp()

    # If right now is in the middle of period, run the last_callback
    if secondary_period:
        if right_now.timestamp() > initial_start and \
           right_now.timestamp() < initial_start + secondary_period:
            logging.info("\tStarting up in the middle of SECONDARY timer cycle - Triggering")
            callback()
        while first_trigger <= right_now.timestamp():
            first_trigger += secondary_period

    elif right_now.timestamp() > initial_start and \
          right_now.timestamp() < initial_start + period:
        logging.info("\tStarting up in the middle of PRIMARY timer cycle - Triggering")
        callback()
        while first_trigger <= right_now.timestamp():
            first_trigger += period

    logging.info("\tNext Trigger: " + datetime.fromtimestamp(first_trigger).strftime('%Y-%m-%d %H:%M:%S'))
    return Timer(name, first_trigger, period, callback, secondary_period)

class Timer:
    def __init__(self, name, next_trigger, primary_period, callback, secondary_period=None):
        self.name = name
        self.next_trigger = next_trigger
        self.primary_period = primary_period
        self.secondary_period = secondary_period
        self.active_timer = "PRIMARY"
        self.callback = callback

        if secondary_period and secondary_period > primary_period:
            raise TimerInvalidSecondaryPeriod(self.name, self.secondary_period)


    def get_as_dict(self):
        return {
            'name': self.name,
            'next_trigger': self.next_trigger,
            'primary_period': self.primary_period,
            'secondary_period': self.secondary_period,
            'active_timer': self.active_timer,
            }


    def is_time_to_run(self):
        if time() > self.next_trigger:
            return True
        else:
            return False

    def run(self, force=False):
        # This is a no-op if it is not yet time to run.
        if force is False and self.is_time_to_run() is False:
            logging.warning("Running %s, but it's not time yet\n" % (self.name))
            return

        # First things first, lets run the callback
        #   We'll return the value of the callback if it does not raise exception
        rval = self.callback()

        if self.active_timer == "PRIMARY":
            if self.secondary_period:
                self.next_trigger += self.secondary_period
                self.active_timer = "SECONDARY"
            else:
                self.next_trigger += self.primary_period
        elif self.active_timer == "SECONDARY":
            self.next_trigger += self.primary_period - self.secondary_period
            self.active_timer = "PRIMARY"
        else:
            logging.warning("WARNING : Timer found in unknown state, resetting to PRIMARY", file=stderr)
            self.active_timer = "PRIMARY"

        #logging.info("\tNext Run Trigger: " + datetime.fromtimestamp(datetime.now().timestamp() + self.next_trigger).strftime('%Y-%m-%d %H:%M:%S'))
        return rval
