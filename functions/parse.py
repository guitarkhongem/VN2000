import re

def parse_coordinates(text):
    """
    Giải mã văn bản đầu vào thành danh sách tọa độ (x, y, h).
    Các định dạng hỗ trợ:
      - 'STT X Y' (3 thành phần, STT là số hoặc chữ, H mặc định = 0.0)
      - 'X Y H' (3 thành phần)
      - 'X Y' (2 thành phần, H mặc định = 0.0)
      - 'STT X Y H' (4 thành phần, bỏ qua STT đầu)
      - Định dạng có 'X=...','Y=...' (có thể trên cùng dòng hoặc nhiều dòng)
      - Định dạng 'E ...', 'N ...', tương tự 'X','Y'
      - Định dạng 3 dòng riêng biệt: X, Y, H (mỗi giá trị trên một dòng)
    """
    points = []
    # Tách các dòng và loại bỏ dòng trống
    lines = [line.strip() for line in text.splitlines() if line.strip()]

    # Định dạng 3 dòng liên tiếp (X, Y, H)
    # Nếu tổng số dòng chia hết cho 3 và mỗi dòng chỉ có 1 số
    if len(lines) >= 3 and len(lines) % 3 == 0:
        valid = True
        for line in lines:
            if not re.match(r'^-?\d+(\.\d+)?$', line):
                valid = False
                break
        if valid:
            for i in range(0, len(lines), 3):
                try:
                    x = float(lines[i])
                    y = float(lines[i+1])
                    h = float(lines[i+2])
                except ValueError:
                    continue
                points.append((x, y, h))
            # Trả kết quả ngay nếu khớp định dạng 3 dòng liên tiếp
            if points:
                return points

    i = 0
    while i < len(lines):
        line = lines[i]

        # Định dạng 'X=... Y=...' hoặc nhiều dòng 'X=...', 'Y=...'
        if '=' in line:
            parts = re.split('[,\\s]+', line.replace(',', ' '))
            coords = {}
            for part in parts:
                if '=' in part:
                    key, val = part.split('=', 1)
                    key = key.strip().upper().rstrip(':')
                    try:
                        coords[key] = float(val)
                    except ValueError:
                        continue
            if 'X' in coords and 'Y' in coords:
                x = coords['X']; y = coords['Y']
                # Nếu có 'Z' hoặc 'H' thì lấy, ngược lại H = 0.0
                h = coords.get('Z', coords.get('H', 0.0))
                points.append((x, y, h))
            i += 1
            continue

        # Định dạng Easting/Northing ('E ...', 'N ...')
        match_e = re.match(r'^[Ee]\s*[:=]?\s*([-\d\.]+)', line)
        if match_e:
            try:
                x = float(match_e.group(1))
            except ValueError:
                i += 1
                continue
            # Tìm dòng tiếp theo cho 'N ...'
            if i + 1 < len(lines):
                match_n = re.match(r'^[Nn]\s*[:=]?\s*([-\d\.]+)', lines[i+1])
                if match_n:
                    try:
                        y = float(match_n.group(1))
                    except ValueError:
                        i += 2
                        continue
                    # Tìm H ở dòng sau nếu có
                    h = 0.0
                    if i + 2 < len(lines):
                        match_h = re.match(r'^[Hh]\s*[:=]?\s*([-\d\.]+)', lines[i+2])
                        if match_h:
                            try:
                                h = float(match_h.group(1))
                            except ValueError:
                                h = 0.0
                            i += 3
                        else:
                            i += 2
                    else:
                        i += 2
                    points.append((x, y, h))
                    continue

        tokens = line.split()
        if len(tokens) == 2:
            # Định dạng 'X Y' (không có H)
            try:
                x = float(tokens[0]); y = float(tokens[1]); h = 0.0
                points.append((x, y, h))
            except ValueError:
                pass
            i += 1
            continue
        if len(tokens) == 3:
            first, second, third = tokens
            # Nếu token đầu là STT (toàn chữ hoặc toàn số nguyên)
            if first.isalpha() or first.isdigit():
                try:
                    x = float(second); y = float(third); h = 0.0
                    points.append((x, y, h))
                    i += 1
                    continue
                except ValueError:
                    pass
            # Nếu không phải STT, coi là X Y H
            try:
                x = float(first); y = float(second); h = float(third)
                points.append((x, y, h))
            except ValueError:
                # Nếu đầu tiên không thể chuyển thành số (STT ký tự)
                # và đã thất bại ở trên, bỏ qua
                pass
            i += 1
            continue
        if len(tokens) == 4:
            # Định dạng 'STT X Y H' (bỏ qua STT đầu)
            try:
                x = float(tokens[1]); y = float(tokens[2]); h = float(tokens[3])
                points.append((x, y, h))
            except ValueError:
                pass
            i += 1
            continue

        i += 1

    return points
