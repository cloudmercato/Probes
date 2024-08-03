import time
from probes.probers.base import BaseProber

DUMMY_PROBER_PATH = 'probes.tests.utils.DummyProber'


class DummyProber(BaseProber):
    id = "dummy"

    def run_probe(self):
        return time.time()
