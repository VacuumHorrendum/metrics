#!/usr/bin/env python3

"""
    needs python3 ad psutil (python3-psutil on debian:12 or psutil on pypi)
"""

import datetime, csv, sys, argparse, psutil

def now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

def main():
    parser = argparse.ArgumentParser(description="Write memory metrics into csv file")
    parser.add_argument('--csv', help="output file", metavar="mem.csv")
    parser.add_argument('metrics', metavar="metrics", type=str, nargs='*')
    args = parser.parse_args()

    f = sys.stdout
    if args.csv:
        f = open(args.csv, 'w')
    row = {"now.iso": now()}
    for k, v in psutil.virtual_memory()._asdict().items():
        if args.metrics and k not in args.metrics:
            continue
        row[k] = v
    
    data = [row]

    if len(data) > 0:
        w = csv.DictWriter(f, data[0].keys())
        w.writeheader()
        w.writerows(data)

if __name__ == '__main__':
    main()