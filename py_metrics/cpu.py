#!/usr/bin/env python3

"""
    needs python3 ad psutil (python3-psutil on debian:12 or psutil on pypi)
"""

import datetime, csv, sys, argparse, psutil, os, time

def now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

def main():
    parser = argparse.ArgumentParser(description="Write cpu metrics into csv file")
    parser.add_argument('--csv', help="output file", metavar="cpu.csv")
    parser.add_argument('--interval', help="scanning interval", type=float, default=1.0)
    parser.add_argument('--timeout', help="run until timeout", type=float, default=0.0)
    parser.add_argument('--percpu', action='store_true', default=False, help="include metrics per logical cpu")
    parser.add_argument('metrics', metavar="metrics", type=str, nargs='*')
    args = parser.parse_args()
    no_headers: bool = args.csv and os.path.exists(args.csv)
    
    def work():
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
            f = open(args.csv, 'a')

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
            if not no_headers:
                w.writeheader()
            w.writerows(data)

    start_time = time.time()
    while True:
        work()
        no_headers = True
        if time.time() - start_time > args.timeout:
            break

if __name__ == '__main__':
    main()