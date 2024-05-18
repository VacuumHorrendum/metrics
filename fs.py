#!/usr/bin/env python3

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
