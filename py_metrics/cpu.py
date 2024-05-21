#!/usr/bin/env python3

"""
    needs python3 ad psutil (python3-psutil on debian:12 or psutil on pypi)
"""

import datetime, csv, sys, argparse, psutil, os

def now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

def main():
    parser = argparse.ArgumentParser(description="Write cpu metrics into csv file")
    parser.add_argument('--csv', help="output file", metavar="mem.csv")
    parser.add_argument('--interval', help="scanning interval", type=float, default=1.0)
    parser.add_argument('--percpu', action='store_true', default=False, help="include metrics per logical cpu")
    parser.add_argument('metrics', metavar="metrics", type=str, nargs='*')
    args = parser.parse_args()
    
    data: list[dict[str,str]] = list()

    def append_row(row:dict[str,str]):
        new_row = {"now.iso": now()}
        for k, v in row.items():
            if args.metrics and k not in args.metrics:
                continue
            new_row[k] = v
        data.append(new_row)

    f = sys.stdout
    if args.csv:
        os.makedirs(os.path.dirname(args.csv), exist_ok=True)
        f = open(args.csv, 'w')

    times = psutil.cpu_times_percent(interval=args.interval)
    load = round(100.0 - times.idle, 1)
    metrics = {'cpu': 'all'} | times._asdict()
    metrics['load'] = load
    append_row(metrics)

    if args.percpu:
        all_times = psutil.cpu_times_percent(interval=args.interval, percpu=True)
        core:int = 0
        for times in all_times:
            load = round(100.0 - times.idle, 1)
            metrics = {'cpu': core} | times._asdict()
            metrics['load'] = load
            append_row(metrics)
            core += 1

    if len(data) > 0:
        w = csv.DictWriter(f, data[0].keys())
        w.writeheader()
        w.writerows(data)

if __name__ == '__main__':
    main()