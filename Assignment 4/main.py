import random, sys, time
sys.path.append('/opt/spark/python')
sys.path.append('/opt/spark/python/lib/py4j-0.10.9.7-src.zip')
from pyspark.sql import SparkSession
from pyspark.sql.functions import min, max, avg, count, col, sum

spark = SparkSession.builder.appName("assignment4_JamesGray").master("spark://spark.bin.bioinf.nl:7077").getOrCreate()
sc = spark.sparkContext

import pickle

import pandas as pd

import re
from src.file_reader import GenbankReader
from src.genbank_parser import GenbankParser
from src.config_handler import ConfigHandler


CONFIG_PATH = "config.yaml"

regex = re.compile(r'\d+')

def parse_proteins(record_generator):
    


    for record in reader.read_files():
        column_names = ["id", "species", "tax_id", "locus_tag", "protein_id", "location", "length", "sequence", "AA_seq", "product"]
        entries = []

        first = True

        id = record.id
        annotations = parser.get_annotations(record)
        species = parser.get_species(annotations)
        features = record.features
        
        tax_id = ""

        for feature in features:

            if "db_xref" in feature.qualifiers:
                qualifiers = feature.qualifiers
                tax_id = qualifiers.get("db_xref")[0].strip("taxon:")

        for feature in features:

            locus_tag = ""
            protein_id = ""
            location = ""
            product = ""

            try:
                sequence = str(feature.extract(record.seq))
            except:
                sequence = ""

            if feature.type == "CDS":
                position = list(re.findall(regex, str(feature.location)))
                position.sort()
                try:
                    start, stop = position
                    length = abs(int(stop) - int(start))
                except:
                    start, stop = [0, 0]
                    lenght = 0

                # tags
                if "translation" in feature.qualifiers:
                        AA_seq = feature.qualifiers["translation"][0]

                if "locus_tag" in feature.qualifiers:
                    locus_tag = feature.qualifiers["locus_tag"][0]

                if "protein_id" in feature.qualifiers:
                    protein_id = feature.qualifiers["protein_id"][0]
                
                if "product" in feature.qualifiers:
                        product = feature.qualifiers["product"][0]
        
                meta_points = [id, species, tax_id, locus_tag, protein_id, location, length, sequence, AA_seq, product]

                     
                entries.append(meta_points)

        if first:
            spark_df = spark.createDataFrame([meta_points], column_names)
            first = False
        else:
            new_row = spark.createDataFrame([meta_points], column_names)
            spark_df = spark_df.union(new_row)

    # result = {key: [value_set[i] for value_set in entries] for i, key in enumerate(column_names)}
    return spark_df


if __name__ == "__main__":
    config_h = ConfigHandler()
    config = config_h.read_config(CONFIG_PATH)

    reader = GenbankReader(config_object=config)
    parser = GenbankParser()

    print("Parsing genbank records...")
    spark_df = parse_proteins(reader.get_files())
    # # # with open('resultsdict.pickle', 'wb') as handle:
    # # #     pickle.dump(results_dict, handle, protocol=pickle.HIGHEST_PROTOCOL)

    # with open("resultsdict.pickle", 'rb') as handle:
    #      results_dict = pickle.load(handle)


    # pandas_df = pd.DataFrame(results_dict)
    # spark_df = spark.createDataFrame(pandas_df)
    # spark_df = spark_df.withColumn("length", col("length").cast("int"))

    # Vraag 1
    spark_df.select(
        min("length").alias("Shortest protein"),
        max("length").alias("Longest protein"),
        avg("length").alias("Average protein length")
    ).show()

    # Vraag 2
    spark_df.groupBy("species") \
        .agg(count("*").alias("Protein count")) \
        .orderBy("Protein count", ascending=False) \
        .limit(1) \
        .show()
    
    # Vraag 3
    spark_df.groupBy("species") \
    .agg(sum("length").alias("Total genome size")) \
    .orderBy("Total genome size", ascending=False) \
    .limit(1) \
    .show()
