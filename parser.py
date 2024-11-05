def parse(feet_inches_local):
    parts = feet_inches_local.split(" ")
    feet = float(parts[0])
    inches = float(parts[1])
    return {"feet":feet,"inches":inches}
