from relay_timer import RelayTimer
from relay import invert_relay_states
import time
import logging
import logging.handlers
import signal
import os
import sys

TimerList = []


def main():

    # Setup the Logging System
    configure_logging()

    # Setup the relay timers we want
    configure_relay_timers()
    logger.info("Initialization complete: Entering main loop")

    # Main event loop
    while True:
        logging.debug("Top of the main event loop")
        # Woke up, we might have work to do. Lets walk through the list of RelayTimers.
        next_run = TimerList[0].timer.next_trigger
        for relay_timer in TimerList:
            logging.debug("Evaluating RelayTimer : %s" % relay_timer.name)

            # If it is time to run...um run
            if relay_timer.timer.is_time_to_run():
                relay_timer.run()

            # Always find the soonest next_trigger
            if relay_timer.timer.next_trigger < next_run:
                next_run = relay_timer.timer.next_trigger

        # Sleep until we need to run again
        sleep_secs = next_run - time.time() + 1
        if sleep_secs > 0:
            logging.debug("Sleeping for %d seconds" % sleep_secs)
            time.sleep(sleep_secs)


def configure_relay_timers():
    # TODO : This should be config file driven

    # Static variables
    LIGHT_PIN = 7
    WATER_PIN = 13
    OTHER_PIN = 15
    TWENTY_FOUR_HOURS = 60 * 60 * 24
    THIRTEEN_HOURS = 60 * 60 * 13
    TWELVE_HOURS = 60 * 60 * 12
    NINE_HOURS = 60 * 60 * 9
    FOUR_HOURS = 60 * 60 * 4
    TWO_HOURS = 60 * 60 * 2

    # Setup the set of timers we need to run stuff
    global TimerList
    # TimerList = [RelayTimer("Lights", LIGHT_PIN, TWELVE_HOURS, 7),
    TimerList = [RelayTimer("Lights", LIGHT_PIN, TWENTY_FOUR_HOURS, 7, secondary_period=THIRTEEN_HOURS),
                 RelayTimer("Water", WATER_PIN, TWO_HOURS, 7, secondary_period=15)]


# Setup the logging system
class LessThanFilter(logging.Filter):
    def __init__(self, exclusive_maximum, name=""):
        super(LessThanFilter, self).__init__(name)
        self.max_level = exclusive_maximum

    def filter(self, record):
        # non-zero return means we log this message
        return 1 if record.levelno < self.max_level else 0


def configure_logging():
    # Have to set the root logger level, it defaults to logging.WARNING
    logger.setLevel(logging.NOTSET)

    # Define the log format
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Lets send DEBUG to stdout
    logging_handler_out = logging.StreamHandler(sys.stdout)
    logging_handler_out.setLevel(logging.DEBUG)
    logging_handler_out.addFilter(LessThanFilter(logging.WARNING))
    logging_handler_out.setFormatter(formatter)
    logger.addHandler(logging_handler_out)

    # Lets send WARNING and above to stderr
    logging_handler_err = logging.StreamHandler(sys.stderr)
    logging_handler_err.setLevel(logging.WARNING)
    logging_handler_err.setFormatter(formatter)
    logger.addHandler(logging_handler_err)

    # demonstrate the logging levels
    '''
    logger.debug('Starting up test log - DEBUG')
    logger.info('Starting up test log - INFO')
    logger.warning('Starting up test log - WARNING')
    logger.error('Starting up test log - ERROR')
    logger.critical('Starting up test log - CRITICAL')
    '''
    logging.info("Logging system configured")


    ### BEGIN __main__ ###
# Define runfile
with open("ChamDaemon.run", "w") as run_file:
    print(str(os.getpid()), file=run_file)

# Instantiate the global logger object
logger = logging.getLogger()


# Enter the main event loop
if __name__ == '__main__':
    main()

    ### END __main__ ###
