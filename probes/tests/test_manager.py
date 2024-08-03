from unittest import TestCase
from probes.manager import ProbeManager
from probes.tests import utils


class ProberManagerTest(TestCase):
    def test_init_with_custom_prober(self):
        manager = ProbeManager(
            probes=(utils.DummyProber, )
        )
        self.assertIsInstance(manager.probers[0], utils.DummyProber)

    def test_init_with_custom_prober_path(self):
        manager = ProbeManager(
            probes=(utils.DUMMY_PROBER_PATH, )
        )
        self.assertIsInstance(manager.probers[0], utils.DummyProber)

    def test_interval(self):
        interval = 42
        manager = ProbeManager(
            interval=interval,
        )
        for prober in manager.probers:
            self.assertEqual(prober.interval, interval)
