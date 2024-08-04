"""Retrieve NVIDIA GPU data from pynvml"""
# TODO: Check minimum interval
from collections import defaultdict
import pynvml
from probes.probers import base

# https://developer.download.nvidia.com/compute/DevZone/NVML/doxygen/group__group4.html
TEMPERATURE_SENSORS = (
    ('gpu', pynvml.NVML_TEMPERATURE_GPU),
    # ('memory', pynvml.NVML_TEMPERATURE_MEM),
    # ('board', pynvml.NVML_TEMPERATURE_BOARD),
    # ('vr1', pynvml.NVML_TEMPERATURE_VR1),
    # ('vr2', pynvml.NVML_TEMPERATURE_VR2),
    # ('vr3', pynvml.NVML_TEMPERATURE_VR3),
    # ('vr4', pynvml.NVML_TEMPERATURE_VR4),
)
def get_temperatures(handle):
    data = {}
    for key, sensor in TEMPERATURE_SENSORS:
        data[key] = pynvml.nvmlDeviceGetTemperature(handle, sensor)
    return data


ERROR_BIT_TYPES = (
    ('single', pynvml.NVML_SINGLE_BIT_ECC),
    ('double', pynvml.NVML_DOUBLE_BIT_ECC),
)
COUNTER_TYPES = (
    ('volatile', pynvml.NVML_VOLATILE_ECC),
    ('aggregate', pynvml.NVML_AGGREGATE_ECC),
)
def get_ecc_errors(handle):
    data = {}
    for b_key, error_type in ERROR_BIT_TYPES:
        for c_key, counter_type in COUNTER_TYPES:
            try: 
                data[f"{b_key}_{c_key}"] = pynvml.nvmlDeviceGetTotalEccErrors(
                    handle, error_type, counter_type)
            except pynvml.NVMLError_NotSupported:
                pass
    return data


CLOCK_TYPES = (
    # ('core', pynvml.NVML_CLOCK_CORE),
    ('sm', pynvml.NVML_CLOCK_SM),
    ('mem', pynvml.NVML_CLOCK_MEM),
)
def get_clock_info(handle):
    data = {}
    for key, clock_type in CLOCK_TYPES:
        data[key] = pynvml.nvmlDeviceGetClockInfo(handle, clock_type)
    return data

FUNCS = {
    'name': pynvml.nvmlDeviceGetName,
    'clock_info': get_clock_info,
    'memory_info': pynvml.nvmlDeviceGetMemoryInfo,
    'pci_info': pynvml.nvmlDeviceGetPciInfo,
    'persistence_mode': pynvml.nvmlDeviceGetPersistenceMode,
    # 'power_capping_mode': pynvml.nvmlDeviceGetPowerCappingMode,
    'power_state': pynvml.nvmlDeviceGetPowerState,
    'power_usage': pynvml.nvmlDeviceGetPowerUsage,
    'temperature': get_temperatures,
    'total_ecc_errors': get_ecc_errors,
    'utilization_rates': pynvml.nvmlDeviceGetUtilizationRates,
    'fan_speed': pynvml.nvmlDeviceGetFanSpeed,
}


def info_parser(data):
    return {f: getattr(data, f) for f, _ in data._fields_ }


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
                if hasattr(data, '_fields_'):
                    data = info_parser(data)
                infos[func_name] = data
            except Exception as err:
                self.logger.warning("Error: %s", err)
                self._append_error(err)
        return infos

    def run_probe(self):
        result = defaultdict(dict)
        device_count = pynvml.nvmlDeviceGetCount()
        for idx in range(device_count):
            result[idx] = self.get_gpu_info(idx)
        return result
