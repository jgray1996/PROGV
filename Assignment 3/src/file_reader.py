import gzip
from glob import glob
from Bio import SeqIO
from src.config_handler import ConfigHandler

class GenbankReader:

    """
    read genbank files
    """

    def __init__(self, config_file="config.yaml"):
        ch = ConfigHandler()
        self.config = ch.read_config(config_file)
    
    def get_files(self):
        """
        Get compressed genbank files from configured directory
        """
        return glob(f"{self.config['data_dir']}*.gbff.gz")
    
    def read_files(self):
        """
        Makes a generator which yields
        genbank records

        returns: GENERATOR [Genbank.record]
        """
        for file in self.get_files():
            with gzip.open(file, "rt") as f_in:
                for record in SeqIO.parse(f_in, "genbank"):
                    yield record

    def read_file(self, file):
        """
        Reads in a single genbank file and returns the SeqIO
        object
        """
        with gzip.open(file, "rt") as f_in:
            return SeqIO.parse(f_in, "genbank")
        
    def read_records(self, file):
        """
        Makes a generator which yields
        genbank records from a single genbank file

        returns: GENERATOR [Genbank.record]
        """
        for record in self.read_file(file):
            yield record
