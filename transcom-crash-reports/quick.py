import glob
import json

count = 0
fatal = 0

for fn in glob.glob("*_human.json"):
    # print(fn)
    with open(fn, "r") as fd:
        data = json.load(fd)
        for k in data:
            count += 1
            if "fatal" in k["severity"]:
                fatal += 1


print(f"incidents: {count}, fatal {fatal}")
