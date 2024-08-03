"""Base Prober module"""
import os
import logging
import threading
import time
from probes import utils


class ProberError(utils.ProbesError):
    """Error related to Probers"""


class BaseProber:
    """
    Base class for with all the required behavior.
    Just left to subclass and write `run_probe`

    Other methods allows flexibility of usage:
    - check
    - set_options
    """
    id = None

    def __init__(self, interval=2, **options):
        self.interval = interval
        self.running = False
        self._results = {}
        self._errors = {}
        self.thread = threading.Thread(target=self.run, name=self.id)
        self.logger = logging.getLogger(f'probes.{self.id}')
        self.set_options(options)
        self.check()

    def check(self):
        """Raise a `ProberError` for wrong configuration"""

    def _check_is_root(self):
        """Check if superuser else raise an error"""
        if os.geteuid() != 0:
            msg = "Must be invoked as the superuser"
            raise ProberError(msg)

    def set_options(self, options):
        """Configure the options specific to this Prober"""

    def _append(self, result):
        """Add values to the results"""
        self._results[time.time()] = result

    def _append_error(self, error):
        """Add an error to the list"""
        self._errors[time.time()] = error

    def run(self):
        """
        Run the probe until stopped with an interval between each launch.
        This method is run in a thread allowing an external stopper.
        """
        while self.running:
            self.logger.debug('Running probe')
            try:
                result = self.run_probe()
                self.logger.debug('Collected probe')
                self._append(result)
            except ProberError as err:
                self._append_error(err)
            self.logger.debug('Wait %d seconds', self.interval)
            time.sleep(self.interval)
        self.post_stop()

    def run_probe(self):
        """Main function retrieving values as a dict"""
        raise NotImplementedError()

    def pre_start(self):
        """Subclass method for pre-start actions"""

    def post_start(self):
        """Subclass method for post-start actions"""

    def start(self):
        """Start the probe loop in background"""
        self.pre_start()
        self.running = True
        self.thread.start()
        self.post_start()

    def post_stop(self):
        """Subclass method for post-stop actions"""

    def stop(self):
        """Stop the probe loop"""
        self.running = False

    def clear_results(self):
        """Flush results and errors"""
        self._results = {}
        self._errors = {}

    def get_result(self):
        """Retrieve probes' results"""
        return self._results.copy()

    def get_errors(self):
        """Retrieve probes' errors"""
        return self._errors.copy()
