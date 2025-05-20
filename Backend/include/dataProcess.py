import sqlite3
import sqlite3

class DataProcess:
    def __init__(self):
        self.data = []
        self.file_path = None

    def readFile(self, file_path='text.txt'):
        with open(file_path, 'r') as file:
            for line in file:
                fields = line.strip().split('\t')
                if len(fields) >= 6:
                    record = {
                        'date': fields[0],
                        'time': fields[1],
                        'Radio_number': fields[2],
                        'lat': float(fields[3]),
                        'long': float(fields[4]),
                        'info': float(fields[5].strip())
                    }
                    if len(fields) >= 7:
                        try:
                            record['extra'] = int(fields[6].strip())
                        except ValueError:
                            record['extra'] = None
                    self.data.append(record)

    def saveToDatabase(self, db_path='data.db'):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Creer la table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                Radio_number TEXT,
                lat REAL,
                long REAL,
                info REAL,
                extra INTEGER,
                UNIQUE(date, time, Radio_number) ON CONFLICT IGNORE
            )
        ''')

        # insert les données
        for record in self.data:
            cursor.execute('''
                INSERT OR IGNORE INTO records 
                (date, time, Radio_number, lat, long, info, extra)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                record['date'],
                record['time'],
                record['Radio_number'],
                record['lat'],
                record['long'],
                record['info'],
                record.get('extra')
            ))

        conn.commit()
        conn.close()

    def checkAndUpdate(self, file_path, db_path='data.db'):
    # Connect and ensure the table exists
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                time TEXT,
                Radio_number TEXT,
                lat REAL,
                long REAL,
                info REAL,
                extra INTEGER,
                UNIQUE(date, time, Radio_number) ON CONFLICT IGNORE
            )
        ''')
    
        # Read and parse new data
        new_data = []
        with open(file_path, 'r') as file:
            for line in file:
                fields = line.strip().split('\t')
                if len(fields) >= 6:
                    record = {
                        'date': fields[0],
                        'time': fields[1],
                        'Radio_number': fields[2],
                        'lat': float(fields[3]),
                        'long': float(fields[4]),
                        'info': float(fields[5].strip())
                    }
                    if len(fields) >= 7:
                        try:
                            record['extra'] = int(fields[6].strip())
                        except ValueError:
                            record['extra'] = None
                    new_data.append(record)
    
        # Insert new records
        for record in new_data:
            cursor.execute('''
                INSERT OR IGNORE INTO records 
                (date, time, Radio_number, lat, long, info, extra)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                record['date'],
                record['time'],
                record['Radio_number'],
                record['lat'],
                record['long'],
                record['info'],
                record.get('extra')
            ))
    
        conn.commit()
        conn.close()
        
    def get_last_record(self, db_path='data.db'):
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par nom
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM records ORDER BY id DESC LIMIT 1")
        row = cursor.fetchone()
        conn.close()

        if row:
            return dict(row)  # Retourne un dict avec les colonnes
        else:
            return None
    def get_all_records(self, db_path='data.db'):
        try:
            conn = sqlite3.connect(db_path)
            conn.row_factory = sqlite3.Row  # permet d'accéder aux colonnes par nom
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM records")
            rows = cursor.fetchall()
            conn.close()

            return [dict(row) for row in rows]

        except sqlite3.Error as e:
            print(f"Erreur SQLite: {e}")
            return []



if __name__ == '__main__' :
    dp = DataProcess()
    dp.checkAndUpdate('file.txt')  

