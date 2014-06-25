#!usr/bin/python
import argparse


def parse_arguments():
    global parser
    parser = argparse.ArgumentParser(
        description="A Befunge-98 interpreter written in pygame.",
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-s", action="store", dest="SPEED", type=int,
                        help="specify the time between "
                        "each tick (default: 50 ms)",
                        default=50)
    parser.add_argument("befunge_file", action="store",
                        help="the full path to a befunge "
                        "file to be interpreted")
    helpmsg = "show the environment variables used in the y instruction"
    parser.add_argument("-y", "--sysinfo", action="version", help=helpmsg,
                        version="Version 0.9\n"
                                "t is NOT implemented\n"
                                "i is NOT implemented\n"
                                "o is NOT implemented\n"
                                "= is NOT implemented\n"
                                "Bytes per cell: 24\n"
                                "Scalars per vector: 2")
    try:
        return parser.parse_args()
    except IOError as io:
        parser.error(str(io))
