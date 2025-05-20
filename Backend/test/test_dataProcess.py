import unittest
import sqlite3
import os
import sys

# Pour importer depuis ../include/dataprocess.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../include')))
from dataProcess import DataProcess

class TestDataProcessWithFile(unittest.TestCase):

    def setUp(self):
        self.input_file = 'test.txt'
        self.test_db = 'test_data.db'

        # Contenu initial pour test.txt
        self.initial_lines = [
            "2025/05/20\t14:32:52\t00000001\t45.78082\t4.87306\t14.584\t150\n",
            "2025/05/20\t14:33:52\t00000002\t45.78085\t4.87310\t14.600\t151\n"
        ]

        # Écrit les lignes initiales dans test.txt
        with open(self.input_file, 'w') as f:
            f.writelines(self.initial_lines)

        # Supprime la base de test si elle existe
        if os.path.exists(self.test_db):
            os.remove(self.test_db)

    def tearDown(self):
        # Supprimer la base de données
        if os.path.exists(self.test_db):
            os.remove(self.test_db)
        # Supprimer test.txt
        if os.path.exists(self.input_file):
            os.remove(self.input_file)

    def test_add_lines_and_update(self):
        dp = DataProcess()
        dp.checkAndUpdate(self.input_file, self.test_db)

        # Vérifie qu'on a bien 2 lignes insérées
        conn = sqlite3.connect(self.test_db)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM records")
        count_before = cursor.fetchone()[0]
        self.assertEqual(count_before, 2)

        # Ajoute une nouvelle ligne dans test.txt
        new_line = "2025/05/20\t14:34:52\t00000003\t45.78090\t4.87315\t14.620\t152\n"
        with open(self.input_file, 'a') as f:
            f.write(new_line)

        # Relance l'insertion
        dp.checkAndUpdate(self.input_file, self.test_db)

        # Vérifie qu'il y a maintenant 3 lignes
        cursor.execute("SELECT COUNT(*) FROM records")
        count_after = cursor.fetchone()[0]
        conn.close()
        self.assertEqual(count_after, 3)

if __name__ == '__main__':
    unittest.main()
