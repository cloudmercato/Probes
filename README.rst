Probes
~~~~~~

probes is handy tool to monitor systems during workloads. It aims to collect metrics about:

- CPU
- RAM
- Network
- NVIDIA GPU
- VPU
- Apple Silicon
- IPMI

Get started
===========

Install
-------

Simple as::

  pip install https://github.com/cloudmercato/probes/archive/refs/heads/main.zip

Basic usage
-----------

probes can be used though its Python API for code measurement or with command line.
Both method will return a ``dict`` or JSON in the following format::

  {
    "<prober_id>": {
      "<timestamp": {
        "<value1>": 42,
        "<value2>": [4, 2]
      }
    }
  }


  
Take a look at the probers documentation to get samples of collected data.

Python API
@@@@@@@@@@

You can use the ``ProbeManager`` manually::

  from probes import ProbeManager

  manager.start()
  mystuff()
  manager.stop()
  manager.get_results()

Or as a context manager::

  with manager.run():
    mystuff()
  manager.get_results()

Command line
@@@@@@@@@@@@

Nothing easiest than::

  $ probes sleep 1
  {
    "cpu": {
      "1722896625.775925": {
        "cpu_percent": 0.0,
        "cpu_percent_per_cpu": [
          0.0,
  ...
  }

The output is a JSON with the same format the Python one.

All the basic monitoring options are available::

  $ probes --help
  usage: probes [-h] [-i INTERVAL] [-p PROBERS] [-d DELAY] [-D DECAY] [-q] [-o OUTPUT] [-] [-I] [-t TIMEOUT] [-v {0,1,2}] [-V] ...

  positional arguments:
    command

  optional arguments:
    -h, --help            show this help message and exit
    -i INTERVAL, --interval INTERVAL
    -p PROBERS, --probers PROBERS
    -d DELAY, --delay DELAY
    -D DECAY, --decay DECAY
    -q, --quiet
    -o OUTPUT, --output OUTPUT
    -, --stdin
    -I, --do-not-ignore-error
    -t TIMEOUT, --timeout TIMEOUT
    -v {0,1,2}, --verbosity {0,1,2}
    -V, --version


Configuration
=============

Probers
-------

Probers are Python classes allowing to collect a particular set of data. We already provides the following:

probes.prober.system.CpuProber
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Metrics about CPU usage, global and per CPU, frequency and load average. This prober is powered by psutil.

Sample::

  {
    "cpu": {
      "1722897347.6944609": {
        "cpu_percent": 0.0,
        "cpu_percent_per_cpu": [
          0.0
        ],
        "cpu_times": {
          "user": 1543773.15,
          "nice": 0.0,
          "system": 683447.71,
          "idle": 12162731.0
        },
        "cpu_times_per_cpu": [
          {
            "user": 346659.43,
            "nice": 0.0,
            "system": 200543.88,
            "idle": 1216883.2
          }
        ],
        "cpu_times_percent": {
          "user": 0.0,
          "nice": 0.0,
          "system": 0.0,
          "idle": 1.0
        },
        "cpu_times_percent_per_cpu": [
          {
            "user": 0.0,
            "nice": 0.0,
            "system": 0.0,
            "idle": 0.0
          }
        ],
        "cpu_stats": {
          "ctx_switches": 3613,
          "interrupts": 147674,
          "soft_interrupts": 3913649281,
          "syscalls": 274251
        },
        "cpu_freq": {
          "current": 2400,
          "min": 2400,
          "max": 2400
        },
        "load_avg": [
          1.849609375,
          1.9775390625,
          1.962890625
        ],
        "cpu_freq_per_cpu": [
          [
            2400,
          ]
        ]
      }
    }
  }

probes.prober.system.MemoryProber
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Metrics about RAM and swap usage. It uses psutil under the hood.

Sample::

  {
    "memory": {
      "1722897258.003343": {
        "virtual_memory": {
          "total": 17179869184,
          "available": 1101221888,
          "percent": 93.6,
          "used": 1745637376,
          "free": 25284608,
          "active": 1140215808,
          "inactive": 1074270208,
          "wired": 605421568
        },
        "swap_memory": {
          "total": 8589934592,
          "used": 7384530944,
          "free": 1205403648,
          "percent": 86.0,
          "sin": 279234916352,
          "sout": 17371725824
        }
      }
    }
  }


probes.prober.system.NetworkProber
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

Metrics about network usage. It uses psutil under the hood.

Sample::

  {
    "network": {
      "1724063994.340725": {
        "bytes_sent": 5046946816,
        "bytes_recv": 6862913536,
        "packets_sent": 145665481,
        "packets_recv": 349973714,
        "errin": 0,
        "errout": 0,
        "dropin": 400863614200,
        "dropout": 0
      },
      "1724063996.3488991": {
        "bytes_sent": 5046956032,
        "bytes_recv": 6862915584,
        "packets_sent": 145665496,
        "packets_recv": 349973730,
        "errin": 0,
        "errout": 0,
        "dropin": 400863614200,
        "dropout": 0,
        "bytes_sent_diff": 9216,
        "bytes_sent_speed": 4608.0,
        "bytes_recv_diff": 2048,
        "bytes_recv_speed": 1024.0,
        "packets_sent_diff": 15,
        "packets_sent_speed": 7.5,
        "packets_recv_diff": 16,
        "packets_recv_speed": 8.0,
        "errin_diff": 0,
        "errin_speed": 0.0,
        "errout_diff": 0,
        "errout_speed": 0.0,
        "dropin_diff": 0,
        "dropin_speed": 0.0,
        "dropout_diff": 0,
        "dropout_speed": 0.0
      },
      ...
    }
  }

probes.prober.nvidia.NvidiaGpuProber
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

For NVIDIA GPU, it providers metrics about power usage, VRAM, temperature and more. This prober requires `pynvml <https://pypi.org/project/pynvml/>`_.

Sample::

  WIP


probes.prober.macos.MacosProber
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

For Apple macos system, it uses the command line tool `powermetrics <https://firefox-source-docs.mozilla.org/performance/powermetrics.html>`_ to provides CPU power, thermal, GPU power and ANE power data.

Sample::

  {
    "macos": {
      "1722897929.421819": {
        "is_delta": true,
        "elapsed_ns": 5005696583,
        "hw_model": "MacBookPro18,3",
        "kern_osversion": "23F79",
        "kern_bootargs": "",
        "kern_boottime": 1719733635,
        "timestamp": "2024-08-05T22:45:29",
        "processor": {
          "clusters": [
            {
              "name": "E-Cluster",
              "hw_resid_counters": true,
              "freq_hz": 1224990000.0,
              "idle_ns": 2735840291,
              "idle_ratio": 0.546236,
              "dvfm_states": [
                {
                  "freq": 600,
                  "used_ns": 0,
                  "used_ratio": 0.0
                }
              ],
              "online_ratio": 1.0,
              "cpus": [
                {
                  "cpu": 0,
                  "freq_hz": 1297740000.0,
                  "idle_ns": 3357356833,
                  "idle_ratio": 0.670184,
                  "dvfm_states": [
                    {
                      "freq": 600,
                      "used_ns": 0,
                      "used_ratio": 0.0
                    }
                  ]
                }
              ]
            },
            {
              "name": "P0-Cluster",
              "hw_resid_counters": true,
              "freq_hz": 1293200000.0,
              "idle_ns": 3730712166,
              "idle_ratio": 0.744864,
              "dvfm_states": [
                {
                  "freq": 600,
                  "used_ns": 2271138000,
                  "used_ratio": 0.453449
                }
              ],
              "online_ratio": 1.0,
              "cpus": [
                {
                  "cpu": 1,
                  "freq_hz": 1998340000.0,
                  "idle_ns": 4056568333,
                  "idle_ratio": 0.809749,
                  "dvfm_states": [
                    {
                      "freq": 600,
                      "used_ns": 7131166,
                      "used_ratio": 0.00142348
                    }
                  ]
                }
              ]
            },
            {
              "name": "P1-Cluster",
              "hw_resid_counters": true,
              "freq_hz": 973859000.0,
              "idle_ns": 4702986666,
              "idle_ratio": 0.938975,
              "dvfm_states": [
                {
                  "freq": 600,
                  "used_ns": 3619404416,
                  "used_ratio": 0.722632
                }
              ],
              "online_ratio": 1.0,
              "cpus": [
                {
                  "cpu": 7,
                  "freq_hz": 1979210000.0,
                  "idle_ns": 4764940000,
                  "idle_ratio": 0.951136,
                  "dvfm_states": [
                    {
                      "freq": 600,
                      "used_ns": 5151166,
                      "used_ratio": 0.00102823
                    }
                  ]
                }
              ]
            }
          ],
          "cpu_energy": 3212,
          "cpu_power": 641.669,
          "gpu_energy": 255,
          "gpu_power": 50.942,
          "ane_energy": 0,
          "ane_power": 0.0,
          "combined_power": 692.611
        }
      }
    }
  }

External links
--------------

Probes is used by different other projects:

- `ollama-benchmark <https://github.com/cloudmercato/ollama-benchmark>`_
- `os-benchmark <https://github.com/cloudmercato/os-benchmark>`_
- `yolo-benchmark <https://github.com/cloudmercato/yolo-benchmark>`_
- `whisper-benchmark <https://github.com/cloudmercato/whisper-benchmark>`_

Contribute
----------

This project is created with ❤️ for free by `Cloud Mercato`_ under BSD License. Feel free to contribute by submitting a pull request or an issue.

.. _`Cloud Mercato`: https://www.cloud-mercato.com/
