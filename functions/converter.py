import os
import io
import cgi
import pandas as pd
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

# ------ Hàm xử lý tọa độ (bạn có thể import từ functions nếu muốn) ------

def vn2000_to_wgs84_baibao(x, y, h, lon0_deg=106.25):
    import math
    a = 6378137.0
    e2 = 0.00669437999013
    e_2 = e2 / (1 - e2)
    k0 = 0.9999
    y0 = 500000

    lon0_rad = math.radians(lon0_deg)
    M = x / k0
    mu = M / (a * (1 - e2/4 - 3*e2**2/64 - 5*e2**3/256))

    e1 = (1 - math.sqrt(1 - e2)) / (1 + math.sqrt(1 - e2))
    J1 = (3*e1/2 - 27*e1**3/32)
    J2 = (21*e1**2/16 - 55*e1**4/32)
    J3 = (151*e1**3/96)
    J4 = (1097*e1**4/512)

    fp = mu + J1*math.sin(2*mu) + J2*math.sin(4*mu) + J3*math.sin(6*mu) + J4*math.sin(8*mu)

    C1 = e_2 * math.cos(fp)**2
    T1 = math.tan(fp)**2
    R1 = a*(1 - e2) / (1 - e2 * math.sin(fp)**2)**1.5
    N1 = a / math.sqrt(1 - e2 * math.sin(fp)**2)
    D = (y - y0) / (N1 * k0)

    lat = (fp - (N1*math.tan(fp)/R1)*(D**2/2 - (5+3*T1+10*C1-4*C1**2-9*e_2)*D**4/24
          + (61+90*T1+298*C1+45*T1**2-252*e_2-3*C1**2)*D**6/720))
    lon = (lon0_rad + (D - (1+2*T1+C1)*D**3/6
          + (5-2*C1+28*T1-3*C1**2+8*e_2+24*T1**2)*D**5/120) / math.cos(fp))

    lat_deg = math.degrees(lat)
    lon_deg = math.degrees(lon)

    return lat_deg, lon_deg, h

# ------- Server Handler --------

class SimpleServer(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        html = '''
        <html><head><title>VN2000 ⇄ WGS84 Converter</title></head><body>
        <h2>Upload File TXT/CSV hoặc Dán Dữ Liệu</h2>
        <form enctype="multipart/form-data" method="post">
        <input type="file" name="file"><br><br>
        <textarea name="text_input" rows="10" cols="80" placeholder="Dán dữ liệu vào đây..."></textarea><br><br>
        <button type="submit">Chuyển đổi VN2000 ➔ WGS84</button>
        </form>
        </body></html>
        '''
        self.wfile.write(html.encode('utf-8'))

    def do_POST(self):
        ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
        if ctype == 'multipart/form-data':
            pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
            content_len = int(self.headers.get('content-length'))
            pdict['CONTENT-LENGTH'] = content_len
            fields = cgi.parse_multipart(self.rfile, pdict)
            filedata = fields.get('file')
            textdata = fields.get('text_input')

            content = ''
            if filedata:
                content = filedata[0].decode('utf-8')
            elif textdata:
                content = textdata[0]

            # Parse toạ độ
            coords = []
            for line in content.strip().splitlines():
                parts = line.strip().split()
                if len(parts) >= 2:
                    try:
                        x = float(parts[0])
                        y = float(parts[1])
                        h = float(parts[2]) if len(parts) >= 3 else 0.0
                        coords.append((x, y, h))
                    except:
                        continue

            # Chuyển đổi VN2000 ➔ WGS84
            results = []
            for x, y, h in coords:
                lat, lon, h = vn2000_to_wgs84_baibao(x, y, h)
                results.append((lat, lon, h))

            # Xuất CSV
            df = pd.DataFrame(results, columns=["Latitude", "Longitude", "Altitude"])
            output = io.StringIO()
            df.to_csv(output, index=False)
            csv_content = output.getvalue()

            self.send_response(200)
            self.send_header('Content-type', 'text/csv')
            self.send_header('Content-Disposition', 'attachment; filename="converted.csv"')
            self.end_headers()
            self.wfile.write(csv_content.encode('utf-8'))

# ------ Start Server ------

def run(server_class=HTTPServer, handler_class=SimpleServer, port=5000):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Đang chạy server tại http://127.0.0.1:{port}")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
