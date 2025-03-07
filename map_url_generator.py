import math
import yaml
import json

# YAML yapılandırma dosyasını oku
def load_config(file_path):
    try:
        with open(file_path) as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Hata: {file_path} bulunamadı!")
        return None
    except yaml.YAMLError as e:
        print(f"Hata: YAML dosyası okunurken hata olustu: {e}")
        return None

# Koordinatları donduren fonksiyon
def lat_lng_to_tile(lat_lng_coordinates, zoom):
    lat, lng = lat_lng_coordinates
    n = 2.0 ** zoom
    x = int((lng + 180.0) / 360.0 * n)
    y = int(
        (1.0 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2.0 * n
    )
    return x, y

# URL olusturma fonksiyonu
def generate_tile_urls(top_left, bottom_right, map_type, zoom_levels):
    json_data = []
    count = 0

    for z in zoom_levels:
        tl_x, tl_y = lat_lng_to_tile(top_left, z)
        br_x, br_y = lat_lng_to_tile(bottom_right, z)

        print(f"Zoom: {z} | TL: ({tl_x}, {tl_y}) | BR: ({br_x}, {br_y})")
        print(f"X diff: {br_x - tl_x}, Y diff: {br_y - tl_y}")
        print("-" * 50)

        for x in range(tl_x, br_x + 1):
            for y in range(tl_y, br_y + 1):
                url = (
                    f"https://mts1.google.com/vt/lyrs={map_type}@186112443&hl=x-local&src=app&"
                    f"x={x}&y={y}&z={z}&s=Galile"
                )
                json_data.append({"x": x, "y": y, "z": z, "url": url})
                count += 1

    return json_data, count

# JSON verisini dosyaya yazan fonksiyon
def save_to_json(data, file_name):
    try:
        with open(file_name, 'w') as json_file:
            json.dump(data, json_file, indent=4)
    except IOError as e:
        print(f"Hata: JSON dosyası yazılırken hata olustu: {e}")

# Ana calısma fonksiyonu
def main():
    config = load_config('./config/config.yaml')
    if not config:
        return
    
    try:
        top_left = config['top_left']
        bottom_right = config['bottom_right']
        map_type = config['map_type']
    except KeyError as e:
        print(f"Hata: YAML dosyasında eksik anahtar: {e}")
        return
    
    zoom_levels = range(0, 22)
    tile_data, count = generate_tile_urls(top_left, bottom_right, map_type, zoom_levels)

    save_to_json(tile_data, '/data/urls.json')
    print(f"Toplam olusturulan URL sayısı: {count}")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Beklenmeyen bir hata olustu: {e}")
