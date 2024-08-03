import logging
import threading
import time


class BaseProber:
    def __init__(self, interval=2):
        self.interval = interval
        self.running = False
        self.results = {}
        self.thread = threading.Thread(target=self.run)
        self.logger = logging.getLogger(f'probes.{self.id}')

    def append(self, result):
        t = time.time()
        self.results[t] = result

    def run(self):
        while self.running:
            self.logger.debug('Running probe')
            result = self.run_probe()
            self.logger.debug('Collected probe')
            self.append(result)
            self.logger.debug('Wait %d seconds', self.interval)
            time.sleep(self.interval)

    def run_probe(self):
        raise NotImplementedError()

    def start(self):
        self.running = True
        self.thread.start()

    def stop(self):
        self.running = False

    def clear_results(self):
        self.results = {}

    def get_result(self):
        return self.results.copy()
