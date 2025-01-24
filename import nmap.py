import nmap
import sqlite3
import json
import pandas as pd
from typing import Dict, List, Any

class NmapAnalyzer:
    def __init__(self, database_path: str = 'nmap_results.db'):
        """
        Nmap tarama sonuçları için analiz sınıfı
        
        Args:
            database_path (str): SQLite veritabanı dosyası yolu
        """
        self.database_path = database_path
        self.conn = sqlite3.connect(database_path)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Gerekli veritabanı tablolarını oluştur"""
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS nmap_scans (
                scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                target TEXT,
                scan_date DATETIME DEFAULT CURRENT_TIMESTAMP,
                scan_type TEXT
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS host_results (
                host_id INTEGER PRIMARY KEY AUTOINCREMENT,
                scan_id INTEGER,
                ip_address TEXT,
                hostname TEXT,
                status TEXT,
                FOREIGN KEY (scan_id) REFERENCES nmap_scans(scan_id)
            )
        ''')
        
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS port_results (
                port_id INTEGER PRIMARY KEY AUTOINCREMENT,
                host_id INTEGER,
                port_number INTEGER,
                protocol TEXT,
                state TEXT,
                service TEXT,
                version TEXT,
                FOREIGN KEY (host_id) REFERENCES host_results(host_id)
            )
        ''')
        self.conn.commit()

    def perform_scan(self, target: str, scan_type: str = '-sV') -> Dict:
        """
        Hedef üzerinde Nmap taraması gerçekleştir

        Args:
            target (str): Taranacak IP/Alan adı
            scan_type (str): Nmap tarama tipi

        Returns:
            Dict: Tarama sonuçları
        """
        nm = nmap.PortScanner()
        nm.scan(target, arguments=scan_type)

        # Tarama bilgilerini kaydet
        self.cursor.execute(
            'INSERT INTO nmap_scans (target, scan_type) VALUES (?, ?)', 
            (target, scan_type)
        )
        scan_id = self.cursor.lastrowid

        results = {}
        for host in nm.all_hosts():
            # Host bilgilerini kaydet
            self.cursor.execute(
                'INSERT INTO host_results (scan_id, ip_address, status) VALUES (?, ?, ?)',
                (scan_id, host, nm[host].state())
            )
            host_id = self.cursor.lastrowid

            # Port bilgilerini kaydet
            for proto in nm[host].all_protocols():
                ports = nm[host][proto].keys()
                for port in ports:
                    port_state = nm[host][proto][port]['state']
                    service = nm[host][proto][port].get('name', 'unknown')
                    version = nm[host][proto][port].get('version', 'unknown')

                    self.cursor.execute(
                        '''INSERT INTO port_results 
                        (host_id, port_number, protocol, state, service, version) 
                        VALUES (?, ?, ?, ?, ?, ?)''',
                        (host_id, port, proto, port_state, service, version)
                    )

        self.conn.commit()
        return results

    def analyze_vulnerabilities(self, scan_id: int) -> List[Dict]:
        """
        Belirli bir taramadaki potansiyel zafiyetleri analiz et

        Args:
            scan_id (int): Analiz edilecek tarama ID'si

        Returns:
            List[Dict]: Tespit edilen zafiyetler
        """
        self.cursor.execute('''
            SELECT h.ip_address, p.port_number, p.service, p.version 
            FROM host_results h
            JOIN port_results p ON h.host_id = p.host_id
            WHERE h.scan_id = ? AND p.state = 'open'
        ''', (scan_id,))

        vulnerabilities = []
        for result in self.cursor.fetchall():
            ip, port, service, version = result
            # Basit bir versiyon bazlı zafiyet kontrolü
            # Gerçek dünyada bu kısım bir CVE veritabanı ile genişletilmelidir
            if 'old' in version.lower() or 'vulnerable' in version.lower():
                vulnerabilities.append({
                    'ip': ip,
                    'port': port,
                    'service': service,
                    'version': version,
                    'risk_level': 'Yüksek'
                })

        return vulnerabilities

    def generate_report(self, scan_id: int) -> Dict:
        """
        Tarama için detaylı rapor oluştur

        Args:
            scan_id (int): Raporu oluşturulacak tarama ID'si

        Returns:
            Dict: Tarama raporu
        """
        self.cursor.execute('SELECT target, scan_date FROM nmap_scans WHERE scan_id = ?', (scan_id,))
        scan_info = self.cursor.fetchone()

        self.cursor.execute('''
            SELECT h.ip_address, COUNT(p.port_id) as open_ports, 
                   GROUP_CONCAT(DISTINCT p.service) as services
            FROM host_results h
            JOIN port_results p ON h.host_id = p.host_id
            WHERE h.scan_id = ? AND p.state = 'open'
            GROUP BY h.ip_address
        ''', (scan_id,))

        hosts = self.cursor.fetchall()
        vulnerabilities = self.analyze_vulnerabilities(scan_id)

        return {
            'scan_id': scan_id,
            'target': scan_info[0],
            'scan_date': scan_info[1],
            'hosts': [
                {
                    'ip': host[0], 
                    'open_ports': host[1], 
                    'services': host[2]
                } for host in hosts
            ],
            'vulnerabilities': vulnerabilities
        }

    def close(self):
        """Veritabanı bağlantısını kapat"""
        self.conn.close()

# Örnek kullanım
if __name__ == '__main__':
    analyzer = NmapAnalyzer()
    
    # Örnek bir tarama yap
    scan_result = analyzer.perform_scan('8.8.8.8/24')
    
    # Son taramanın raporunu oluştur
    report = analyzer.generate_report(1)
    print(json.dumps(report, indent=2))
    
    analyzer.close()