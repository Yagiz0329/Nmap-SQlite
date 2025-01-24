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

# Gerekli kütüphaneleri yükleyin:

pip install python-nmap pandas
