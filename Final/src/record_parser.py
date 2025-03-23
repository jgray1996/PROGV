import sqlite3

class RecordCorrector:

    """
    Corrects technical and biological error of kraken2 reports
    """

    def __init__(self, record, config):
        self.connector = sqlite3.connect(config.get("species_database"))
        self.cursor = self.connector.cursor()
        self.record = record

    def get_genome_length(self, species):
        """
        Data base was built without taxid so queries are made based on species name and 
        average genome length for that species. The average is computed by aggregating 
        the accession numbers.
        """

        query = f"""SELECT species_name, AVG(total_genome_size) AS average_genome_size
        FROM (
        SELECT species_name, accession_number, SUM(genome_size) AS total_genome_size
        FROM species
        WHERE species_name like '%{species}%'
        GROUP BY accession_number
        ) AS genome_sums
        GROUP BY species_name;"""

        self.cursor.execute(query)
        res = self.cursor.fetchone()
        return res


    def parse_record(self):
        """
        Find species which are present in the database and correct for coverage
        """ 

        with open(self.record, 'r') as f_in, open(self.record+".corrected", "w") as f_out:
            for line in f_in:
                line = line.strip().split(None, 5)
                species = line[-1]
                percentage = float(line[0])
                reads = int(line[1])
                identifyer = line[3]
                if identifyer == 'S' and percentage > 0.01 and reads > 1:
                    correction_value = self.get_genome_length(species)
                    if correction_value:
                        _, size = correction_value
                        coverage = str(reads / size)
                        line[1] = coverage
                        # write output
                        print(", ".join(line), file=f_out)
