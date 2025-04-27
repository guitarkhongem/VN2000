import re

def parse_coordinates(text):
    tokens = re.split(r'\s+', text.strip())
    coords = []
    i = 0
    while i < len(tokens):
        token = tokens[i]
        if re.fullmatch(r"[EN]\d{8}", token):
            prefix = token[0]
            number = token[1:]
            if prefix == "E":
                y = int(number)
            else:
                x = int(number)

            if i+1 < len(tokens) and re.fullmatch(r"[EN]\d{8}", tokens[i+1]):
                next_prefix = tokens[i+1][0]
                next_number = tokens[i+1][1:]
                if next_prefix == "E":
                    y = int(next_number)
                else:
                    x = int(next_number)
                i += 1

            coords.append([float(x), float(y), 0])
            i += 1
            continue

        chunk = []
        for _ in range(3):
            if i < len(tokens):
                try:
                    num = float(tokens[i].replace(",", "."))
                    chunk.append(num)
                except:
                    break
                i += 1
        if len(chunk) == 2:
            chunk.append(0.0)
        if len(chunk) == 3:
            coords.append(chunk)
        else:
            i += 1

    filtered = []
    for x, y, h in coords:
        if 1_000_000 <= x <= 2_000_000 and 330_000 <= y <= 670_000 and -1000 <= h <= 3200:
            filtered.append([x, y, h])
    return filtered
