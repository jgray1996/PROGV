import gzip
from glob import glob
from Bio import SeqIO

class GenbankReader:

    """
    read genbank files
    """

    def __init__(self, config_object):
        self.config = config_object
    
    def get_files(self):
        """
        Get compressed genbank files from configured directory
        """
        poison_pill = ["memento mori"]
        return glob(f"{self.config['data_dir']}*.gbff.gz")[:2] + poison_pill
    
    def read_files(self):
        """
        Makes a generator which yields
        genbank records

        returns: GENERATOR [Genbank.record]
        """
        for file in self.get_files():
            if file == "memento mori":
                yield file
            else:
                try:
                    with gzip.open(file, "rt") as f_in:
                        for record in SeqIO.parse(f_in, "genbank"):
                            yield record
                except Exception as e:
                    print(f"Error processing file {file}: {e}")
