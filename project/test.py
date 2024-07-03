import unittest
import os
import sqlite3
import pipeline
class Test(unittest.TestCase):
    path = None
    table = None
    
    @classmethod
    def setUpClass(cls):
        try:
            data = pipeline.main()
            cls.path = data[0]
            cls.table = data[1]
            
        except SystemExit:
            return
            
            
        except Exception as e:
            raise
    
    
    def setUp(self):
        if(self.path is not None and len(self.path) > 0):
            self.conn = sqlite3.connect(self.path)
            self.cursor = self.conn.cursor()
            
        else:
            self.conn = self.cursor = None
        
    
    def tearDown(self):
        if(self.conn is not None):
            self.conn.close()
     
     
    def test_pipeline(self):
        self.assertIsNotNone(self.path, f"Pipeline Error.")  
    
    
    def test_fileExists(self):
        if(self.path is None):
            self.assertIsNotNone(self.path, f"This file is not available.")
            
        else:
            self.assertTrue(os.path.exists(self.path), f"This file '{self.path}' is not available.")

    
    def test_tableExists(self):
        if(self.table is None):
            self.assertIsNotNone(self.table, f"This table is not available.")
            
        else:
            self.cursor.execute(f'''
                                SELECT      name 
                                FROM        sqlite_master 
                                WHERE       type='table' 
                                            AND name='{self.table}';
            ''')
            
            table_exists = self.cursor.fetchone()
            
            self.assertIsNotNone(table_exists, f"This table '{self.table}' is not available.")
            
    
            
    @classmethod
    def tearDownClass(cls):
        if(hasattr(cls, 'cursor') and cls.cursor):
            cls.cursor.close()
        if(hasattr(cls, 'conn') and cls.conn):
            cls.conn.close()
        if(cls.path and os.path.exists(cls.path)):
           
            os.remove(cls.path)
            if(os.path.exists(cls.path) == False):
                cls.path = None
                cls.table = None
            
if __name__ == '__main__':
    unittest.main(verbosity=1)