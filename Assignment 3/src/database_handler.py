import sqlite3
from src.init_db import DBCreater
import time

class DatabaseHandler:

    """
    This class handles writing genomic data to a database
    """

    counter = []
    inserts = []

    def __init__(self):
        """
        Database handler initialize
        """
        self.path = None
        self.connection = None
        self.cursor = None
        self.batch_size = 1
    
    def connect(self, path):
        """
        Connect to specified database
        """
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        print(f"Connected to: {path}")
        time.sleep(2)

    def insert_ncbi_data(self, record):
        """
        Writes and handles data parsed from record and writes to database
        """

        taxonomy = record['taxonomy']
        try:
            kingdom, phylum, class_, order, family, genus = taxonomy
        except ValueError as e:
            try:
                kingdom, phylum, class_, order, family, genus_group, genus = taxonomy
            # Insert custom exception for missing family etc.
            except ValueError as e:
                # print(f"Organism with altered taxonomy from record:\n{record.get('accession_numbers')}")
                return
        species = record['organism']

        # write all new taxonomy entries
        self.cursor.execute("INSERT OR IGNORE INTO kingdom (kingdom_name) VALUES (?)", (kingdom,))
        self.cursor.execute("INSERT OR IGNORE INTO phylum (phylum_name, kingdom_name) VALUES (?, ?)", (phylum, kingdom))
        self.cursor.execute("INSERT OR IGNORE INTO class (class_name, phylum_name) VALUES (?, ?)", (class_, phylum))
        self.cursor.execute("INSERT OR IGNORE INTO `order` (order_name, class_name) VALUES (?, ?)", (order, class_))
        self.cursor.execute("INSERT OR IGNORE INTO family (family_name, order_name) VALUES (?, ?)", (family, order))
        self.cursor.execute("INSERT OR IGNORE INTO genus (genus_name, family_name) VALUES (?, ?)", (genus, family))
        
        # get parsed data
        try:
            sub_accession, accession_number = record['accession_numbers']
        except ValueError as e:
            try:
                sub_accession, accession_number = record['accession_numbers'], record['accession_numbers']
            except ValueError as e:
                return
        
        genome_size = record['genome_size']
        assembly_id, bioproject_id, biosample_id = record['db_codes']
        pubmed_id = record.get('pubmed_id')
        first_article_year = record.get('publication_year')
        genbank_version_year = int(record['current_version'].split('-')[-1])
        total_genes = record['n_features']
        coding_genes = record['n_coding']

        self.cursor.execute("""
            INSERT INTO species (
                species_name, genus_name, sub_accession, accession_number, genome_size, 
                assembly_id, bioproject_id, biosample_id, pubmed_id, 
                first_article_year, genbank_version_year, total_genes, coding_genes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (species, genus, sub_accession, accession_number, genome_size, assembly_id, 
            bioproject_id, biosample_id, pubmed_id, first_article_year, 
            genbank_version_year, total_genes, coding_genes))
        self.connection.commit()
