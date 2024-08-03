import time
import contextlib
import importlib
import logging

DEFAULT_PROBERS = (
    'probes.probers.system.CpuProber',
    'probes.probers.system.MemoryProber',
)

logger = logging.getLogger('probes.manager')


class ProbeManager:
    """
    Tool for manage simultaneously several Probers.

    After instantiation, the manager can be use manually:::

        manager.start()
        mystuff()
        manager.stop()
        manager.get_results()

    Or as a context manager:::

        with manager.run():
            mystuff()
        manager.get_results()
    """
    def __init__(
        self,
        probers=DEFAULT_PROBERS,
        interval=2,
        delay=0,
        decay=0,
    ):
        self.running = False
        self.delay = delay
        self.decay = decay
        self.probers = []
        for prober in probers:
            if isinstance(prober, str):
                path = prober
                module_path = '.'.join(path.split('.')[:-1])
                class_name = path.rsplit('.', maxsplit=1)[-1]
                module = importlib.import_module(module_path)
                prober_class = getattr(module, class_name)
                prober = prober_class(
                    interval=interval,
                )
            self.probers.append(prober)

    def start(self):
        """Start all Probers"""
        for prober in self.probers:
            prober.start()
        self.running = True

    def stop(self):
        """Stop all Probers"""
        for prober in self.probers:
            prober.stop()
        self.running = False

    def get_results(self):
        """Retrieve all Probers resutls"""
        return {
            prober.id: prober.get_result()
            for prober in self.probers
        }

    @contextlib.contextmanager
    def run(self):
        logger.debug("Wait delay %s", self.delay)
        time.sleep(self.delay)
        try:
            self.start()
            yield
        finally:
            logger.debug("Wait decay %s", self.delay)
            time.sleep(self.decay)
            self.stop()
