from pydsm import dsm, seismicmodel
from pydsm.event import Event
from pydsm.station import Station
from pydsm.utils.cmtcatalog import read_catalog
import time

if __name__ == '__main__':
    # load gcmt catalog
    catalog = read_catalog()
    # get event from catalog
    event = Event.event_from_catalog(
        catalog, '200707211534A')
    # define station FCC
    stations = [
        Station(
            name='FCC', network='CN',
            latitude=58.7592, longitude=-94.0884), 
        ]
    stations *= 100
    # load (anisotropic) PREM model
    seismic_model = seismicmodel.SeismicModel.prem()
    tlen = 1638.4 #3276.8 # duration of synthetics (s)
    nspc = 128 #512 # number of points in frequency domain
    sampling_hz = 20 # sampling frequency for sythetics
    # create input parameters for pydsm
    input = dsm.PyDSMInput.input_from_arrays(
        event, stations, seismic_model, tlen, nspc, sampling_hz)
    # compute synthetics in frequency domain calling DSM Fortran
    start = time.time()
    output = dsm.compute(input, mode=2)
    end = time.time()
    print('DSM finished in {} s'.format(end - start))
    output.to_time_domain() # perform inverse FFT
    us = output.us # synthetics. us.shape = (3,nr,tlen)
    ts = output.ts # time points [0, tlen]