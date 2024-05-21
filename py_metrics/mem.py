#!/usr/bin/env python3

"""
    needs python3 and psutil (python3-psutil on debian:12 or psutil on pypi)
"""

import datetime, csv, sys, argparse, psutil, os, time

def now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

def main():
    parser = argparse.ArgumentParser(description="Write memory metrics into csv file")
    parser.add_argument('--csv', help="output file", metavar="mem.csv")
    parser.add_argument('--interval', type=float, default=1.0)
    parser.add_argument('--timeout', type = float, default=0.0)
    parser.add_argument('metrics', metavar="available", type=str, nargs='*')
    args = parser.parse_args()

    no_headers: bool = args.csv and os.path.exists(args.csv)

    def work():

        f = sys.stdout
        if args.csv:
            f = open(args.csv, 'a')
        row = {"now.iso": now()}
        for k, v in psutil.virtual_memory()._asdict().items():
            if args.metrics and k not in args.metrics:
                continue
            row[k] = v
    
        data = [row]
        
        if len(data) > 0:
            w = csv.DictWriter(f, data[0].keys())
            if not no_headers:
                w.writeheader()
            w.writerows(data)

    start_time = time.time()
    while True:
        work()
        no_headers = True
        if time.time() - start_time > args.timeout:
            break
        time.sleep(args.interval)

if __name__ == '__main__':
    main()