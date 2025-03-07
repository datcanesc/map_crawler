
# Google Maps Fotoğraf İndirme Uygulaması

Bu uygulama, Google Maps üzerindeki fotoğrafları belirli bir bölge için URL'ler aracılığıyla üretir ve bunları PNG formatında indirir. Uygulama, belirli bir alanı (dikdörtgen şeklinde) tarayarak bu alan içerisindeki fotoğrafları toplar.

## Özellikler

- Belirtilen koordinatlar arasındaki fotoğraflar indirilir.
- Fotoğraflar, bölgeye ve zoom seviyelerine göre organize edilmiştir.
- Başarısız indirmeler `failed_downloads.json` dosyasına kaydedilir.

## Gereksinimler

- Docker ve Docker Compose kurulu olmalıdır.

## Kurulum

1. **Config Dosyasının Düzenlenmesi**

   `config` klasöründeki `config.yaml` dosyasını açın ve taramak istediğiniz bölgenin koordinatlarını girin. Bu koordinatlar, bölgenin sol üst ve sağ alt köşelerinin enlem ve boylam değerleri olacaktır. 
   **Not:** Bu şuan koordinatlar, Ankara için ayarlanmıştır.

3. **Map Fotoğraf URL'lerinin Oluşturulması**

   İlk adımda, fotoğrafları almak istediğiniz bölge için URL'leri oluşturmalısınız. Aşağıdaki komutu çalıştırarak bu URL'leri oluşturabilirsiniz:

   ```bash
   docker compose -f docker-compose.1.yaml up --build
   ```

   Bu işlem, `data` klasöründe `urls.json` dosyasını oluşturacaktır. Bu dosya, fotoğraf URL'lerini içerecektir.

4. **Fotoğrafların İndirilmesi**

   URL'ler oluşturulduktan sonra, bu URL'lerden fotoğrafları indirmek için aşağıdaki komutu çalıştırın:

   ```bash
   docker compose -f docker-compose.2.yaml up --build
   ```

   İndirilen fotoğraflar, `data/images` klasörüne kaydedilecektir. Fotoğraflar, zoom seviyelerine göre alt klasörlere ayrılacaktır. İndirilemeyen fotoğraflar ise `failed_downloads.json` dosyasına kaydedilecektir.

## Yapılandırma

- **coordinates:** Tarama yapılacak bölgenin sol üst ve sağ alt köşe koordinatları.
- **map_type:** Fotoğrafların hangi türde alınacağını belirten parametre. Bu parametre, fotoğrafların görsel kalitesini ve türünü kontrol eder.