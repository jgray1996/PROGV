import sqlite3
from src.init_db import DBCreater
import time

class DatabaseHandler:

    """
    This class handles writing genomic data to a database
    """

    counter = 0
    inserts = []
    kingdoms = []
    phylums_kingdoms = []
    classes_phylums = []
    orders_classes = []
    families_orders = []
    genusses_families = []

    def __init__(self, batch_size=50000):
        """
        Database handler initialize
        """
        self.path = None
        self.connection = None
        self.cursor = None
        self.batch_size = batch_size
    
    def connect(self, path):
        """
        Connect to specified database
        """
        self.connection = sqlite3.connect(path)
        self.cursor = self.connection.cursor()
        print(f"Connected to: {path}")

    def insert_ncbi_data(self, record, last_iter=False):
        """
        Writes and handles data parsed from record and writes to database
        """

        if last_iter:

            self.cursor.executemany("INSERT OR IGNORE INTO kingdom (kingdom_name) VALUES (?)", set(self.kingdoms))
            self.cursor.executemany("INSERT OR IGNORE INTO phylum (phylum_name, kingdom_name) VALUES (?, ?)", set(self.phylums_kingdoms))
            self.cursor.executemany("INSERT OR IGNORE INTO class (class_name, phylum_name) VALUES (?, ?)", set(self.classes_phylums))
            self.cursor.executemany("INSERT OR IGNORE INTO `order` (order_name, class_name) VALUES (?, ?)", set(self.orders_classes))
            self.cursor.executemany("INSERT OR IGNORE INTO family (family_name, order_name) VALUES (?, ?)", set(self.families_orders))
            self.cursor.executemany("INSERT OR IGNORE INTO genus (genus_name, family_name) VALUES (?, ?)", set(self.genusses_families))

            self.cursor.executemany("""
            INSERT OR IGNORE INTO species (
            species_name, genus_name, sub_accession, accession_number, genome_size, 
            assembly_id, bioproject_id, biosample_id, pubmed_id, 
            first_article_year, genbank_version_year, total_genes, coding_genes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, self.inserts)
            self.connection.commit()
            print("Remaining records parsed!")
            return

        taxonomy = record['taxonomy']

        try:
            kingdom, phylum, class_, order, family, genus = taxonomy
        except ValueError as e:
            try:
                kingdom, phylum, class_, order, family, genus_group, genus = taxonomy
            except ValueError as e:
                return
        species = record['organism']

        # store all new taxonomy entries
        self.kingdoms.append((kingdom,))
        self.phylums_kingdoms.append((phylum, kingdom))
        self.classes_phylums.append((class_, phylum))
        self.orders_classes.append((order, class_))
        self.families_orders.append((family, order))
        self.genusses_families.append((genus, family))

        
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

        self.counter += 1

        self.inserts.append((species, genus, sub_accession, accession_number, genome_size, assembly_id, 
            bioproject_id, biosample_id, pubmed_id, first_article_year, 
            genbank_version_year, total_genes, coding_genes))

        if self.counter > self.batch_size:

            self.cursor.executemany("INSERT OR IGNORE INTO kingdom (kingdom_name) VALUES (?)", set(self.kingdoms))
            self.cursor.executemany("INSERT OR IGNORE INTO phylum (phylum_name, kingdom_name) VALUES (?, ?)", set(self.phylums_kingdoms))
            self.cursor.executemany("INSERT OR IGNORE INTO class (class_name, phylum_name) VALUES (?, ?)", set(self.classes_phylums))
            self.cursor.executemany("INSERT OR IGNORE INTO `order` (order_name, class_name) VALUES (?, ?)", set(self.orders_classes))
            self.cursor.executemany("INSERT OR IGNORE INTO family (family_name, order_name) VALUES (?, ?)", set(self.families_orders))
            self.cursor.executemany("INSERT OR IGNORE INTO genus (genus_name, family_name) VALUES (?, ?)", set(self.genusses_families))

            self.kingdoms = []
            self.phylums_kingdoms = []
            self.classes_phylums = []
            self.orders_classes = []
            self.families_orders = []
            self.genusses_families = []

            self.cursor.executemany("""
                INSERT OR IGNORE INTO species (
                    species_name, genus_name, sub_accession, accession_number, genome_size, 
                    assembly_id, bioproject_id, biosample_id, pubmed_id, 
                    first_article_year, genbank_version_year, total_genes, coding_genes
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, self.inserts)
            self.connection.commit()
            self.inserts = []
            self.counter = 0
