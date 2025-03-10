import sqlite3

class DatabaseHandler:

    """
    This class handles writing genomic data to a database
    """

    def __init__(self, database_path, 
                 initialize=False):
        self.path = database_path
        self.connection = None
        self.cursor = None
        return
    
    def initialize_database(self):
        return
    
    def connect(self):
        self.connection = sqlite3.connect(self.path)
        self.cursor = self.connection()
    
    def retrieve(self, query):
        return
    
    def submit(self, query):
        return
    
    def test_existance_tables(self):
        return
    
    def test_existance_organism(self, id):
        return
    
    def write_organism(self, id):
        return
    
    def update_organism(self, query):
        return
    
    def add_value(self):
        return
    
    def parse_record(self, record):
        return
