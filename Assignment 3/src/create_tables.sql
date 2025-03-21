CREATE TABLE kingdom (
    kingdom_name TEXT PRIMARY KEY
);
CREATE TABLE phylum (
    phylum_name TEXT,
    kingdom_name TEXT NOT NULL,
    PRIMARY KEY (phylum_name),
    FOREIGN KEY (kingdom_name) REFERENCES kingdom(kingdom_name)
);
CREATE TABLE class (
    class_name TEXT,
    phylum_name TEXT NOT NULL,
    PRIMARY KEY (class_name),
    FOREIGN KEY (phylum_name) REFERENCES phylum(phylum_name)
);
CREATE TABLE "order" (
    order_name TEXT,
    class_name TEXT NOT NULL,
    PRIMARY KEY (order_name),
    FOREIGN KEY (class_name) REFERENCES class(class_name)
);
CREATE TABLE family (
    family_name TEXT,
    order_name TEXT NOT NULL,
    PRIMARY KEY (family_name),
    FOREIGN KEY (order_name) REFERENCES "order"(order_name)
);
CREATE TABLE genus (
    genus_name TEXT,
    family_name TEXT NOT NULL,
    PRIMARY KEY (genus_name),
    FOREIGN KEY (family_name) REFERENCES family(family_name)
);
CREATE TABLE species (
    species_name TEXT,
    genus_name TEXT NOT NULL,
    sub_accession TEXT UNIQUE,
    accession_number TEXT,
    genome_size INTEGER,
    assembly_id TEXT,
    bioproject_id TEXT,
    biosample_id TEXT,
    pubmed_id TEXT,
    first_article_year INTEGER,
    genbank_version_year INTEGER,
    total_genes INTEGER,
    coding_genes INTEGER,
    PRIMARY KEY (sub_accession),
    FOREIGN KEY (genus_name) REFERENCES genus(genus_name)
);