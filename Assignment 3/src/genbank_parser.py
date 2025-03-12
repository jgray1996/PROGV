import re

class GenbankParser:

    """
    This class puls apart genbank records into their tiniest smithereens
    """

    def __init__(self):
        """
        Init Class
        """
        pattern = r"\((20\d{2})\)"
        self.regex = re.compile(pattern)
        pass

    def parse_record(self, record):
        """
        This function accepts a record and parses Martijn's wishes to a dict
        """
        annotations = self.get_annotations(record)
        accession_number = self.get_accessions(annotations)
        genome_size = self.get_genome_size(record)
        db_codes = self.get_db_codes(record)
        publication = self.get_publication(annotations)
        pubmed, year = self.parse_publication(publication, annotations)
        current_version_gb = self.get_version(annotations)
        organism = self.get_species(annotations)
        taxonomy = self.get_taxonomy(annotations)
        n_features = self.get_num_features(record)
        n_coding = self.get_num_coding(record)

        return {"accession_numbers": accession_number,
                "genome_size": genome_size,
                "db_codes": db_codes,
                "publication": publication,
                "pubmed_id": pubmed,
                "publication_year": year,
                "current_version": current_version_gb,
                "organism": organism,
                "taxonomy": taxonomy,
                "n_features": n_features,
                "n_coding": n_coding}
    
    def get_species(self, annotations):
        """
        Return organism
        """
        return annotations["organism"]
    
    def get_num_features(self, record):
        """
        Counts the amount of genes in the features 
        object of genbank record
        """
        total_genes = sum(1 for feature in record.features 
                          if feature.type == "gene")
        return total_genes
    
    def get_num_coding(self, record):
        """
        Counts the amount of coding regions in features 
        object of genbank record
        """
        coding_genes = sum(1 for feature in record.features
                           if feature.type == "CDS")
        return coding_genes
    
    def get_taxonomy(self, annotations):
        """
        Return taxonomy layers
        """
        return annotations["taxonomy"]
        
    def get_genome_size(self, record):
        """
        This function returns the recorded genome size
        """
        return len(record.features[0].location)

    def get_annotations(self, record):
        """ 
        This function recieves a genbank record and extracts the annotations object
        """
        return record.annotations
    
    def get_accessions(self, annotations):
        """
        This function recieves an annotation object and returns the genbank 
        sub and master accession number in a tuple
        """
        accessions = annotations["accessions"]
        return accessions
    
    def get_version(self, annotations):
        """
        Get the version dat of the genbank record
        """
        return annotations["date"]
        
    def get_db_codes(self, record):
        """
        This function recieves a record object and returns the
        accession numbers for BioProject, BioSample and Assembly
        """
        dbrefs = record.dbxrefs

        try:
            if len(dbrefs) != 3:
                return (dbrefs[0].strip("BioProject:"),
                        dbrefs[1].strip("BioSample:"),
                        dbrefs[3].strip("Assembly:"))
            return (dbrefs[0].strip("BioProject:"),
                    dbrefs[1].strip("BioSample:"),
                    dbrefs[2].strip("Assembly:"))
        except IndexError:
            return (None, None, None)

    def parse_publication(self, publication, annotations):
        """
        Parse obtained publication object
        """
        id = publication.pubmed_id
        year = self.get_year_publication(publication)
        if not year:
            return id, int(self.get_version(annotations)[-4:])
        return id, int(year[0]) 

    def get_publication(self, annotation):
        """
        This function attempt to extract the first publication 
        from annotation reference object
        """
        first_ref = annotation["references"][0]
        return first_ref
    
    def get_year_publication(self, publication):
        """
        This function attempts to extract the date from the
        journal string in a reference
        """
        matches = re.findall(self.regex, publication.journal)
        return matches
