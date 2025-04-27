import folium
import pandas as pd

def df_to_kml(df):
    if not {"Vĩ độ (Lat)", "Kinh độ (Lon)", "H (m)"}.issubset(df.columns):
        return None
    kml = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        '  <Document>',
        '    <name>Computed Points (WGS84)</name>'
    ]
    for idx, row in df.iterrows():
        kml += [
            '    <Placemark>',
            f'      <name>Point {idx+1}</name>',
            '      <Point>',
            f'        <coordinates>{row["Kinh độ (Lon)"]},{row["Vĩ độ (Lat)"]},{row["H (m)"]}</coordinates>',
            '      </Point>',
            '    </Placemark>'
        ]
    kml += ['  </Document>', '</kml>']
    return "\n".join(kml)

def generate_map(df):
    m = folium.Map(
        location=[df["Vĩ độ (Lat)"].mean(), df["Kinh độ (Lon)"].mean()],
        zoom_start=14,
        tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
        attr="Esri.WorldImagery"
    )
    for _, row in df.iterrows():
        folium.CircleMarker(
            location=[row["Vĩ độ (Lat)"], row["Kinh độ (Lon)"]],
            radius=3,
            color="red",
            fill=True,
            fill_opacity=0.7
        ).add_to(m)
    return m
