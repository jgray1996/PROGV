import os
from glob import glob

PATH_RAW_READS = "./dir_raw_reads/rumen/rumen_miseq/"
fastq_in_dir = glob(PATH_RAW_READS+"*.fastq")

print(f"All fastq\n{fastq_in_dir}", sep='\n')