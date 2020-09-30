import unittest 

import config
config.database_path = 'test_record.sqlite'

import chainsaw
from model import ChainsawRecord

class TestRecord(unittest.TestCase):

    def setUp(self):
        print("DELETE")
        ChainsawRecord.delete().execute()  # clear table 


    def test_add_valid_data(self):  
        chainsaw.add_record('bob', 12, 'Canada')
        query = ChainsawRecord.select().where(ChainsawRecord.name=='bob')
        self.assertEqual(query.count(), 1)
        record = query.get()
        self.assertEqual(record.name, 'bob')
        self.assertEqual(record.catches, 12)
        self.assertEqual(record.country, 'Canada')



    def test_add_invalid_no_name_data(self):  
        # expect error
        chainsaw.add_record(None, 12, 'Canada')
        

    def test_add_invalid_country_data(self):  
        # expect error
        chainsaw.add_record('bob', 12, None)


    def test_add_invalid_catches_data(self):  
        # expect error
        chainsaw.add_record('bob', -12, 'Canada')



if __name__ == '__main__':
    unittest.main()