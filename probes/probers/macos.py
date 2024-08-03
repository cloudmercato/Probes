import subprocess
import plistlib
from probes.probers import base

DEFAULT_SAMPLERS = [
    'cpu_power',
    'thermal',
    'gpu_power',
    'ane_power',
]


class MacosProber(base.BaseProber):
    id = 'macos'

    def set_options(self, options):
        self.samplers = options.get('samplers') or DEFAULT_SAMPLERS

    def run_command(self):
        command = ['powermetrics', '--sample-count', '1', '--format', 'plist']
        command += ['--samplers'] + self.samplers
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()
        data = plistlib.loads(stdout.encode())
        return data

    def run_probe(self):
        data = self.run_command()
        return data
