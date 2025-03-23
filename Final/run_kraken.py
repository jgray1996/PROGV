from mpi4py import MPI

import numpy as np
from glob import glob

from src.config_handler import ConfigHandler
from src.kraken_runner import KrakenRunner

ch = ConfigHandler()

config = ch.read_config("config.yaml")

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

FILES = glob(f"{config.get('raw_fastq')}*.fastq")

CHUNKS = np.array_split(FILES, size)

assigned = comm.scatter(CHUNKS, root=0)
for job in assigned:
    kr = KrakenRunner(config.get("reference_index"),
                      job,
                      config.get("kraken_output"),
                      cores=4)
    del kr

results = comm.gather(f"Rank {rank} done {len(assigned)}.", root=0)

if rank == 0:
    for res in results:
        print(res)
