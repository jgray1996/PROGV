from mpi4py import MPI

import numpy as np
from glob import glob

from src.config_handler import ConfigHandler
from src.record_parser import RecordCorrector

ch = ConfigHandler()

config = ch.read_config("config.yaml")

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.Get_size()

FILES = glob(config.get("kraken_output")+"*.report")

CHUNKS = np.array_split(FILES, size)

assigned = comm.scatter(CHUNKS, root=0)
for job in assigned:
    r = RecordCorrector(job, config)
    r.parse_record()
    del r

results = comm.gather(f"Rank {rank} done {len(assigned)}.", root=0)

if rank == 0:
    for res in results:
        print(res)