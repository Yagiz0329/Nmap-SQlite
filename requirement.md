# Nmap Analyzer

Nmap Analyzer, ağ taramaları yapmak, sonuçları bir SQLite veritabanında saklamak ve detaylı raporlar oluşturmak için kullanılan bir Python uygulamasıdır.

## Özellikler
- Hedef IP veya ağ aralığı için Nmap taramaları yapar.
- Açık portlar, kullanılan protokoller ve servisleri kaydeder.
- Potansiyel zafiyetleri analiz eder.
- Tarama raporlarını JSON formatında oluşturur.

## Gereksinimler
- Python 3.8+
- `nmap` kütüphanesi (`pip install python-nmap`)
- SQLite

## Kurulum
1. Bu projeyi klonlayın:
   ```bash
   git clone https://github.com/kullaniciadi/nmap-analyzer.git
   cd nmap-analyzer

2. Gerekli kütüphaneleri yükleyin:
   ```bash
   pip install python-nmap pandas

## Kullanım

NmapAnalyzer sınıfını oluşturun:

![image](https://github.com/user-attachments/assets/45c5e38c-10f2-4564-af0b-03641d24140e)

Bir ağ taraması gerçekleştirin:

![image](https://github.com/user-attachments/assets/834de4e9-f71c-49e0-ad01-1931f6df4991)

Rapor oluşturun:

![image](https://github.com/user-attachments/assets/cdc55f58-02aa-49ea-aa17-ccb11c99adee)





