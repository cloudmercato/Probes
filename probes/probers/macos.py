"""Retrieve Apple macos data from powermetrics"""
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
    """
    Retrieve informations for Apple systems.
    Values are selectable with the option `samples`, a list with:
    - cpu_power: cpu power and frequency info
    - thermal: thermal pressure notifications
    - gpu_power: gpu power and frequency info
    - ane_power: dedicated rail ane power and frequency info
    """
    id = 'macos'

    def check(self):
        self._check_is_root()
        if self.interval < 4:
            msg = f"{self.interval} is a low interval for powermetrics."\
                    " Use at least 4."
            self.logger.warning(msg)

    def set_options(self, options):
        self.samplers = options.get('samplers') or DEFAULT_SAMPLERS

    def run_command(self):
        """Compose and run the powermetrics command"""
        command = ['powermetrics', '--sample-count', '1', '--format', 'plist']
        command += ['--samplers'] + self.samplers
        self.logger.debug("Run %s", " ".join(command))
        process = subprocess.Popen(
            command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        stdout, stderr = process.communicate()
        if process.returncode:
            msg = f"Invalid return code {process.returncode}"
            err = base.ProberError(msg)
            raise err

        try:
            data = plistlib.loads(stdout)
        except plistlib.InvalidFileException:
            msg = "Invalid powermetrics plist output"
            err = base.ProberError(msg)
            raise err
        return data

    def run_probe(self):
        try:
            data = self.run_command()
            return data
        except base.ProberError:
            return {}
