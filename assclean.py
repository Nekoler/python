import glob
import pysubs2

asses: list[str] = glob.glob("*.ass")
keys: list[str] = ["ScriptType", "PlayResX", "PlayResY"]

for ass in asses:
    sub: pysubs2.SSAFile = pysubs2.load(ass)
    sub.aegisub_project = {}
    sub.info = {i: j for i, j in sub.info.items() if i in keys}
    events: list[pysubs2.SSAEvent] = []
    for line in sub.events:
        if line.type == "Dialogue" and line.text:
            events.append(line)
    sub.events = events
    sub.sort()
    sub.save(ass)
