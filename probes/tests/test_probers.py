from unittest import TestCase
from probes.probers import system


class BaseProberTestCase:
    def setUp(self):
        self.prober = self.prober_class()

    def test_run(self):
        self.prober.running = True
        self.prober.run()

    def test_run_running_false(self):
        self.prober.running = False
        self.prober.run()

    def test_run_probe(self):
        self.prober.run_probe()


class CpuProberTest(BaseProberTestCase, TestCase):
    prober_class = system.CpuProbe


class MemoryProberTest(BaseProberTestCase, TestCase):
    prober_class = system.MemoryProbe
