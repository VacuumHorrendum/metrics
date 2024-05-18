#!/usr/bin/env python3

"""
    needs python3 (tested with python3-minimal on debian:12)
"""

import datetime, csv, sys, argparse, shutil, os

parser = argparse.ArgumentParser(description="Write filesystem metrics into csv file")
parser.add_argument('mounts', metavar="fs", type=str, nargs='*', help="mounts")
parser.add_argument('--csv', help="output file", metavar="fs.csv")

args = parser.parse_args()

def now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

def getMounts() -> list[str]:
    if not os.path.exists("/proc/mounts"):
        return list("/")
    with open('/proc/mounts','r') as f:
        return [line.split()[1] for line in f.readlines()]

fallback = False
mounts = args.mounts
f = sys.stdout

if args.csv:
    f = open(args.csv, 'w')

if len(mounts) == 0:
    fallback = True
    mounts = getMounts()

data = list()

for m in mounts:
    total, used, free = shutil.disk_usage(m)
    if fallback and (total == 0 or used == 0): continue
    data.append({"now.iso": now(), "fs": m, "total":total, "used":used, "free":free})

if len(data) > 0:
    w = csv.DictWriter(f, data[0].keys())
    w.writeheader()
    w.writerows(data)

def poetry():
    return True