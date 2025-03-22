import os

class KrakenRunner:

    """
    python wrapper for executing a kraken2 run
    """

    def __init__(self, idx, fastq, 
                 output, records, cores=1):
        """
        Init class
        """
        
        self.command = f"""kraken2 \
                            --threads {cores} \
                            --db {idx} \
                            --use-names \
                            --report {records} \
                            {fastq} 1> /dev/null"""
        self.run_kraken()

    def run_kraken(self):
        """
        Execute local installation of kraken2
        """
        os.system(self.command)