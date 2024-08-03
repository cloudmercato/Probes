import contextlib
import importlib

DEFAULT_PROBERS = (
    'probes.probers.system.CpuProber',
    'probes.probers.system.MemoryProber',
)


class ProbeManager:
    def __init__(
        self,
        probers=DEFAULT_PROBERS,
        interval=2,
    ):
        self.running = False
        self.probers = []
        for prober in probers:
            if isinstance(prober, str):
                path = prober
                module_path = '.'.join(path.split('.')[:-1])
                class_name = path.split('.')[-1]
                module = importlib.import_module(module_path)
                prober_class = getattr(module, class_name)
                prober = prober_class(
                    interval=interval,
                )
            self.probers.append(prober)

    def start(self):
        for prober in self.probers:
            prober.start()
        self.running = True

    def stop(self):
        for prober in self.probers:
            prober.stop()
        self.running = False

    def get_results(self):
        return {
            prober.id: prober.get_result()
            for prober in self.probers
        }

    @contextlib.contextmanager
    def run(self):
        try:
            self.start()
            yield
        finally:
            self.stop()
