import tempfile
import unittest
from pathlib import Path
from database import count_sales, get_sales
from generar_datos import seed


class DatabaseTests(unittest.TestCase):
    def test_seed_and_calculations(self):
        with tempfile.TemporaryDirectory() as tmp:
            db = Path(tmp) / 'ventas.db'
            self.assertEqual(seed(db, rows=30), 30)
            self.assertEqual(seed(db, rows=30), 0)
            self.assertEqual(count_sales(db), 30)
            df = get_sales(db)
            self.assertEqual(len(df), 30)
            self.assertTrue((df['ingresos'] >= df['costos']).all())
            self.assertTrue((df['beneficio'] >= 0).all())
            self.assertTrue((df['cantidad'] > 0).all())


if __name__ == '__main__':
    unittest.main()
