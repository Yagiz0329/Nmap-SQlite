# Nmap-SQlite

 # 1- Gerekli Kütüphanelerin İçe Aktarılması

![image](https://github.com/user-attachments/assets/ce885720-230f-4acb-8638-d491fdb55927)


* NMAP: Python için Nmap modülü, ağ taramaları yapmak için kullanılıyor.

* SQLITE3: Veritabanı işlemleri için SQLite kütüphanesi.

* JSON: Tarama sonuçlarını JSON formatında döndürmek için.

* PANDAS: (Şu an kullanılmamış) İleride veritabanı sonuçlarını veri analizi için kullanabilirsiniz.

* TYPING: Yazılımda tür ipuçları sağlamak için


# 2- NmapAnalyzer Sınıfının Tanımlanması

![image](https://github.com/user-attachments/assets/319bf243-18f6-41ac-95ec-36134a2fa950)

* NmapAnalyzer sınıfı, tüm tarama ve analiz işlemlerini kapsar.

* __init__ Metodu:

* Varsayılan olarak nmap_results.db isimli SQLite veritabanını oluşturur veya bağlanır.

* _create_tables metodu çağrılarak gerekli veritabanı tabloları oluşturulur.

# 3- Veritabanı Tablolarının Oluşturulması

![image](https://github.com/user-attachments/assets/f43f7160-dfe4-4c30-98ec-11e7171e16ae)

* nmap_scans: Her taramayı kaydeder (Hedef IP, tarama tarihi, tarama tipi).

* host_results: Taramada bulunan her ana bilgisayarı (IP adresi, durumu vb.) kaydeder.

* port_results: Her ana bilgisayardaki port bilgilerini (port numarası, protokol, durum, hizmet, sürüm) saklar.

# 4- Tarama Yapma (perform_scan)

![image](https://github.com/user-attachments/assets/30dcd64d-5984-43d5-8a71-bfaba9a0974d)

* Nmap kullanarak belirtilen hedefe tarama yapar.

* Hedef Bilgilerinin Kaydedilmesi:

* nmap_scans tablosuna hedef ve tarama türü kaydedilir.

* Her IP için host_results tablosuna veri eklenir.

* Açık port bilgileri port_results tablosuna kaydedilir.

* Dönen Veri: Şu an results boş dönüyor. İsterseniz tarama sonuçlarını burada döndürebilirsiniz.

# 5- Zafiyet Analizi (analyze_vulnerabilities)

![image](https://github.com/user-attachments/assets/5facd8eb-18b4-40dc-b03e-8973aef1ccf0)

* scan_id parametresi ile belirli bir taramanın açık portlarını kontrol eder.

* Basit Zafiyet Kontrolü:

* Eğer bir portun versiyonu old ya da vulnerable içeriyorsa, bu port "Yüksek Riskli" olarak işaretlenir.

* Daha gelişmiş bir kontrol için CVE (Common Vulnerabilities and Exposures) veritabanı kullanılabilir.




