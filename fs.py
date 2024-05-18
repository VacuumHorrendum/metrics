#!/usr/bin/env python3

"""
    needs python3 (works fine with python3-minimal on debian 12)
    usage: fs.py [paths...]

    write data for all known mounts into csv file (only works on linux)
    $ ./fs.py > /tmp/fs.csv

    write data for specific paths into csv file (works on linux and windows)
    $ ./fs.py / /dev/shm > /tmp/fs.csv
    $ python fs.py C: > /tmp/fs.csv
"""

import datetime, csv, sys
import shutil

def now() -> str:
    return datetime.datetime.now().astimezone().replace(microsecond=0).isoformat()

def getMounts() -> list[str]:
    with open('/proc/mounts','r') as f:
        return [line.split()[1] for line in f.readlines()]

fallback = False
mounts = sys.argv[1:]

if len(mounts) == 0:
    fallback = True
    mounts = getMounts()

data = list()

for m in mounts:
    total, used, free = shutil.disk_usage(m)
    if fallback and (total == 0 or used == 0): continue
    data.append({"now.iso": now(), "fs": m, "total":total, "used":used, "free":free})

if len(data) > 0:
    w = csv.DictWriter(sys.stdout, data[0].keys())
    w.writeheader()
    w.writerows(data)
