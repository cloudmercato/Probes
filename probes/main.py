#!/usr/bin/env python
import argparse
import json
import subprocess

from probes.manager import ProbeManager, DEFAULT_PROBERS
from probes.loggers import logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', type=int, default=2)
    parser.add_argument('-p', '--probers', action='append')
    parser.add_argument('-v', '--verbosity', type=int, default=0, choices=(0, 1, 2))
    parser.add_argument('command', nargs='...')

    args, _ = parser.parse_known_args()

    logger.setLevel(40-(10+args.verbosity*10))

    manager = ProbeManager(
        interval=args.interval,
        probers=args.probers or DEFAULT_PROBERS,
    )

    with manager.run():
        process = subprocess.Popen(
            args.command,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        stdout, stderr = process.communicate()

    print(json.dumps(manager.get_results()))


if __name__ == '__main__':
    main()
