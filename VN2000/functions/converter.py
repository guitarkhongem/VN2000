# province_lon0 bảng chuẩn hóa
province_lon0 = {
    "104.5": ["Kiên Giang", "Cà Mau"],
    "104.75": ["Lào Cai", "Phú Thọ", "Nghệ An", "An Giang"],
    "105.0": ["Vĩnh Phúc", "Hà Nam", "Ninh Bình", "Thanh Hóa", "Đồng Tháp", "TP. Cần Thơ", "Hậu Giang", "Bạc Liêu"],
    "105.5": ["Hà Giang", "Bắc Ninh", "Hải Dương", "Hưng Yên", "Nam Định", "Thái Bình", "Hà Tĩnh", "Tây Ninh", "Vĩnh Long", "Trà Vinh"],
    "105.75": ["TP. Hải Phòng", "Bình Dương", "Long An", "Tiền Giang", "Bến Tre", "TP. Hồ Chí Minh"],
    "106.0": ["Tuyên Quang", "Hòa Bình", "Quảng Bình"],
    "106.25": ["Quảng Trị", "Bình Phước"],
    "106.5": ["Bắc Kạn", "Thái Nguyên"],
    "107.0": ["Bắc Giang", "Thừa Thiên – Huế"],
    "107.25": ["Lạng Sơn"],
    "107.5": ["Kon Tum"],
    "107.75": ["TP. Đà Nẵng", "Quảng Nam", "Đồng Nai", "Bà Rịa – Vũng Tàu", "Lâm Đồng"],
    "108.0": ["Quảng Ngãi"],
    "108.25": ["Bình Định", "Khánh Hòa", "Ninh Thuận"],
    "108.5": ["Gia Lai", "Đắk Lắk", "Đắk Nông", "Phú Yên", "Bình Thuận"]
}

def get_lon0_from_province(province_name: str) -> float:
    for lon0, provinces in province_lon0.items():
        if province_name.strip().lower() in [p.strip().lower() for p in provinces]:
            return float(lon0)
    return 106.25  # mặc định Quảng Trị

# Dummy placeholder thuật toán
def vn2000_to_wgs84_baibao(x, y, h, lon0):
    # Thay bằng thuật toán thực tế của bạn
    return x/100000, y/100000, h

def wgs84_to_vn2000_baibao(lat, lon, h, lon0):
    # Thay bằng thuật toán thực tế của bạn
    return lat*100000, lon*100000, h
