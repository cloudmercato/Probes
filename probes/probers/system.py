import psutil
from probes.probers import base


class CpuProber(base.BaseProber):
    id = 'cpu'

    def run_probe(self):
        result = {
            'cpu_percent': psutil.cpu_percent(),
            'cpu_percent_per_cpu': psutil.cpu_percent(percpu=True),

            'cpu_times': psutil.cpu_times()._asdict(),
            'cpu_times_per_cpu': [
                t._asdict() for t in psutil.cpu_times(percpu=True)
            ],

            'cpu_times_percent': psutil.cpu_times_percent()._asdict(),
            'cpu_times_percent_per_cpu': [
                t._asdict() for t in psutil.cpu_times_percent(percpu=True)
            ],

            'cpu_stats': psutil.cpu_stats()._asdict(),
            'cpu_freq': psutil.cpu_freq()._asdict(),

            'load_avg': psutil.getloadavg(),
        }

        cpu_freq = psutil.cpu_freq()
        if cpu_freq:
            result.update(
                cpu_freq=cpu_freq._asdict(),
                cpu_freq_per_cpu=psutil.cpu_freq(percpu=True),
            )

        return result


class MemoryProber(base.BaseProber):
    id = 'memory'

    def run_probe(self):
        result = {
            'virtual_memory': psutil.virtual_memory()._asdict(),
            'swap_memory': psutil.swap_memory()._asdict(),
        }
        return result
