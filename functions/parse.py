import re

def parse_coordinates(text):
    tokens = re.split(r'\s+', text.strip())
    coords = []
    i = 0
    while i < len(tokens):
        token = tokens[i]

        # --- Nhận dạng mã hiệu đặc biệt E/N ---
        if re.fullmatch(r"[EN]\d{8}", token):
            x, y = None, None
            prefix = token[0]
            number = token[1:]
            if prefix == "E":
                y = int(number)
            else:
                x = int(number)

            # Nếu token tiếp theo cũng là E/N
            if i+1 < len(tokens) and re.fullmatch(r"[EN]\d{8}", tokens[i+1]):
                next_prefix = tokens[i+1][0]
                next_number = tokens[i+1][1:]
                if next_prefix == "E":
                    y = int(next_number)
                else:
                    x = int(next_number)
                i += 1  # ăn thêm 1 token

            if x is not None and y is not None:
                coords.append([float(x), float(y), 0])
            i += 1
            continue

        # --- Nếu không phải E/N thì xét STT X Y Z ---
        if i + 3 < len(tokens):
            try:
                float(tokens[i+1].replace(",", "."))
                float(tokens[i+2].replace(",", "."))
                float(tokens[i+3].replace(",", "."))
                x = float(tokens[i+1].replace(",", "."))
                y = float(tokens[i+2].replace(",", "."))
                h = float(tokens[i+3].replace(",", "."))
                coords.append([x, y, h])
                i += 4
                continue
            except:
                pass

        # --- Xét bình thường 2 hoặc 3 giá trị (X Y [H]) ---
        chunk = []
        for _ in range(3):
            if i < len(tokens):
                try:
                    chunk.append(float(tokens[i].replace(",", ".")))
                except:
                    break
                i += 1
        if len(chunk) == 2:
            chunk.append(0.0)
        if len(chunk) == 3:
            coords.append(chunk)
        else:
            i += 1

    # --- Lọc theo điều kiện hợp lệ ---
    filtered = []
    for x, y, h in coords:
        if 1_000_000 <= x <= 2_000_000 and 330_000 <= y <= 670_000 and -1000 <= h <= 3200:
            filtered.append([x, y, h])
    return filtered
