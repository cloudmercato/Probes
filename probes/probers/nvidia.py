"""Retrieve NVIDIA GPU data from pynvml"""
# WIP
# TODO: Check minimum interval
from collections import defaultdict
import pynvml
from probes.probers import base

# https://developer.download.nvidia.com/compute/DevZone/NVML/doxygen/group__group4.html
FUNCS = {
    'name': pynvml.nvmlDeviceGetName,
    'memory_info': pynvml.nvmlDeviceGetMemoryInfo,
    'pci_info': pynvml.nvmlDeviceGetPciInfo,
    'persistence_mode': pynvml.nvmlDeviceGetPersistenceMode,
    'power_capping_mode': pynvml.nvmlDeviceGetPowerCappingMode,
    'power_state': pynvml.nvmlDeviceGetPowerState,
    'power_usage': pynvml.nvmlDeviceGetPowerUsage,
    'temperature': pynvml.nvmlDeviceGetTemperature,
    'total_ecc_errors': pynvml.nvmlDeviceGetTotalEccErrors,
    'utilization_rates': pynvml.nvmlDeviceGetUtilizationRates,
    'fan_speed': pynvml.nvmlDeviceGetFanSpeed,
}


class NvidiaGpuProber(base.BaseProber):
    """
    Retrieve informations for NVIDIA GPUs.
    Values are selectable with the option `funcs`, a list with:
    - name:
    - memory_info:
    - pci_info:
    - persistence_mode:
    - power_capping_mode:
    - power_state:
    - power_usage:
    - temperature:
    - total_ecc_errors:
    - utilization_rates:
    - fan_speed:
    """
    id = "nvidia_gpu"

    def set_options(self, options):
        self.funcs = options.get('funcs') or list(FUNCS)

    def pre_start(self):
        pynvml.nvmlInit()

    def post_stop(self):
        pynvml.nvmlShutdown()

    def get_gpu_info(self, idx):
        """Retrive info for a single GPU"""
        infos = {}
        handle = pynvml.nvmlDeviceGetHandleByIndex(idx)
        for func_name in self.funcs:
            func = FUNCS[func_name]
            try:
                data = func(handle)
                infos[func_name] = vars(data)
            except Exception as err:
                self._append_error(err)
        return infos

    def run_probe(self):
        result = defaultdict(dict)
        device_count = pynvml.nvmlDeviceGetCount()
        for idx in range(device_count):
            result[idx] = self.get_gpu_info(idx)
        return result
