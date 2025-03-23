import os

class KrakenRunner:

    """
    python wrapper for executing a kraken2 run
    """

    def __init__(self, idx, fastq, 
                 out, cores=1):
        """
        Init class
        """

        record = fastq.split("/")[-1].strip(".fastq")+".report"
        
        self.command = f"""kraken2 \
                            --db {idx} \
                            --threads {cores} \
                            --use-names \
                            --report {f"{out}/{record}"} \
                            {fastq} 1> /dev/null"""
        self.run_kraken()

    def run_kraken(self):
        """
        Execute local installation of kraken2
        """
        os.system(self.command)