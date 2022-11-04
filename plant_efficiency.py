# ------------------------------------------------------------------
from ipyleaflet import Map, Marker, Circle, LayerGroup
from ipywidgets import HTML
from colour import Color
# ------------------------------------------------------------------




# ------------------------------------------------------------------
df = depot.table('testers/lng-emissions')
# ------------------------------------------------------------------




# ------------------------------------------------------------------
plants = []
for row in df.collect():
    eff = row.co2_emissions * 2204.64 / row.lng_gen
    plants.append({'eff': eff, 'year': row.year, 'pos': (row.Lat_WGS84, row.Lon_WGS84)})
# ------------------------------------------------------------------





# ------------------------------------------------------------------
colors = list(zip(range(500, 3500, 30), Color('green').range_to(Color('red'), 100)))

plants.sort(key=lambda p: p['eff'])
years = {}
for idx, plant in enumerate(plants):
    year = plant['year']
    if year not in years: years[year] = []
    popup = HTML()
    popup.value = f"{int(plant['eff'])} lbs CO2/MWh"
    c = 'red'
    for color in colors:
        if plant['eff'] < color[0]:
            c = color[1].hex
            break
    c = Circle(location=plant['pos'], radius=50, color=c, popup=popup)
    years[year].append(c)
# ------------------------------------------------------------------




# ------------------------------------------------------------------
clusters = {}
for year, plants in years.items():
    clusters[year] = LayerGroup(layers=plants)

m = Map(center=(37, -120), zoom=5)
l_2020 = clusters[2020]
m.add_layer(l_2020)
m
# ------------------------------------------------------------------
