#!/usr/bin/env python
"""
Simple script for example and test.
"""
import argparse
import json
import subprocess
import sys

from probes import utils
from probes import __version__
from probes.manager import ProbeManager, DEFAULT_PROBERS
from probes.loggers import logger


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', type=int, default=2)
    parser.add_argument('-p', '--probers', action='append')

    parser.add_argument('-d', '--delay', type=int, default=0)
    parser.add_argument('-D', '--decay', type=int, default=0)

    parser.add_argument('-q', '--quiet', action="store_true")
    parser.add_argument('-o', '--output', default="/dev/stdout")
    parser.add_argument('-', '--stdin', action="store_true")
    parser.add_argument('-I', '--do-not-ignore-error', action="store_false",
                        dest="ignore_errors")
    parser.add_argument('-t', '--timeout', type=int, default=None, required=False)
    parser.add_argument('-v', '--verbosity', type=int, default=0,
                        choices=(0, 1, 2))
    parser.add_argument('-V', '--version', action="store_true")

    parser.add_argument('command', nargs='...')

    args, _ = parser.parse_known_args()

    if args.version:
        sys.stdout.write(f"{__version__}\n")
        sys.exit(0)

    if not args.command:
        msg = "No specified command"
        sys.stderr.write(msg)
        parser.print_help()
        sys.exit(1)

    logger.setLevel(40-(10+args.verbosity*10))

    manager = ProbeManager(
        interval=args.interval,
        probers=args.probers or DEFAULT_PROBERS,
        delay=args.delay,
        decay=args.decay,
    )
    cmd_input = None
    if args.stdin:
        try:
            cmd_input = sys.stdin.read()
        except KeyboardInterrupt:
            sys.stderr.write("Stopped stdin reading\n")
            sys.exit(1)

    try:
        with manager.run():
            process = subprocess.Popen(
                args.command,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
            )
            stdout, stderr = process.communicate(
                input=cmd_input,
                timeout=args.timeout,
            )
            if not args.ignore_errors and process.returncode:
                if not args.quiet:
                    sys.stdout.write(stdout)
                    msg = f"Invalid return code: {process.returncode}\n"
                    sys.stderr.write(msg)
                    sys.stderr.write(stderr)
                sys.exit(1)
    except subprocess.TimeoutExpired as err:
        if not args.quiet:
            msg = f"Timeout after {err.timeout} seconds\n"
            sys.stderr.write(msg)
        sys.exit(1)
    except FileNotFoundError as err:
        if not args.quiet:
            msg = f"Invalid command path {err.filename}\n"
            sys.stderr.write(msg)
        sys.exit(1)
    except KeyboardInterrupt:
        pass

    if not args.quiet:
        sys.stdout.write(stdout)
        sys.stderr.write(stderr)

    with open(args.output, 'w') as fd:
        fd.write(json.dumps(
            manager.get_results(),
            indent=2,
            cls=utils.JSONEncoder,
        ))


if __name__ == '__main__':
    main()
