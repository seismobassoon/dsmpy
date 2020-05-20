from pydsm import dsm, rootdsm_psv
from pydsm.dataset import Dataset
from pydsm.seismicmodel import SeismicModel
import os
import numpy as np
import time
from mpi4py import MPI

if __name__ == '__main__':
    comm = MPI.COMM_WORLD
    n_cores = comm.Get_size()
    rank = comm.Get_rank()

    if rank == 0:
        parameter_files = [
        rootdsm_psv + 'test2.inf',
        rootdsm_psv + 'test3.inf']
        dataset = Dataset.dataset_from_files(parameter_files)
        seismic_model = SeismicModel.prem()
        tlen = 3276.8
        nspc = 64
        sampling_hz = 20
    else:
        dataset = None
        seismic_model = None
        tlen = None
        nspc = None
        sampling_hz = None
    
    start_time = time.time()
    outputs = dsm.compute_dataset_parallel(dataset, seismic_model,
                                           tlen, nspc, sampling_hz,
                                           comm, mode=1)
    end_time = time.time()

    if rank == 0:
        print('DSM on {} cores finished in {} s'
              .format(n_cores, end_time - start_time))
        
    if rank == 0 :
        for i, output in enumerate(outputs):
            filename = '{}_{}_n{}'.format(output.event, i, n_cores)
            np.save(filename, output.spcs)
    #elif rank == 0:
            if i == 1:
                spcs_n2 = np.load('20090101_1_n2.npy')
                assert np.allclose(spcs_n2, output.spcs, atol=1e-17)
                print("Same!")
