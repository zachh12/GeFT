#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import matplotlib.pyplot as plt

from waffle.plots import WaveformFitPlotter
from waffle.models import VelocityModel, LowPassFilterModel, HiPassFilterModel, ImpurityModelEnds, WaveformModel
from waffle.models import FirstStageFilterModel, AntialiasingFilterModel
from waffle.models import OvershootFilterModel,OscillationFilterModel, TrappingModel

import numpy as np
from siggen import PPC
chan_dict = {
600: "B8482",
626: "P42574A", #All there
640:"P42665A",
648:"P42664A",
672: "P42661A", #Mostly good
692: "B8474" #Have this too
}

def main(dir_name, wf_idx, num_samples=10 ):
    wf_idx = int(wf_idx)

    align_point = 0.95
    chan = 626
    directory = "chan{}_250wfs".format(chan)

    wf_directory = os.path.join(dir_name, "wf{}".format(wf_idx))

    wf_file = "training_data/datarun11510-11549chan672_250wfs.npz"
    conf_name = "{}.conf".format( chan_dict[chan] )

    datadir= os.environ['DATADIR']
    conf_file = datadir +"/siggen/config_files/" + conf_name

    data = np.load(wf_file, encoding="latin1")
    wfs = data['wfs']


    wf = wfs[wf_idx]
    wf.window_waveform(time_point=0.95, early_samples=100, num_samples=125)
    detector = PPC( conf_file, wf_padding=100)

    vm = VelocityModel(include_beta=False)

    #hp1 = HiPassFilterModel(detector)
    #hp2 = HiPassFilterModel(detector)
    fs = FirstStageFilterModel(detector)
    al = AntialiasingFilterModel(detector)
    oshoot = OvershootFilterModel(detector)
    osc = OscillationFilterModel(detector)
    im = ImpurityModelEnds(detector)
    tm = TrappingModel()

    #lp = LowPassFilterModel(detector)
    #hp = HiPassFilterModel(detector)
    '''
    #6 72
    vm.apply_to_detector([6.330448119432486594e+06, 7.070545190569272265e+06, 6.330662440609236248e+06, 7.320939440024248324e+06], detector)
    fs.apply_to_detector([-1.50887, 9.790592e-01, -2.10503], detector)
    al.apply_to_detector([7.99097e-01, 1.160481e-02], detector)
    oshoot.apply_to_detector([-5.301815, 1.8299623], detector)
    osc.apply_to_detector([-2.185584, 6.970590, -2.2064522, 5.77401], detector)
    im.apply_to_detector([-2.739048e-01, -1.54175], detector)

    #OLD
    vm.apply_to_detector([8439025,5307015,9677126,5309391], detector)
    fs.apply_to_detector([-7.062660481537297308e-01, 9.778840228405032420e-01, -7.851819989636383390e+00], detector)
    al.apply_to_detector([0.5344254, 0.135507736], detector)
    oshoot.apply_to_detector([-3.8111099842, 0.140626600], detector)
    osc.apply_to_detector([-1.6800848, 3.00040593, -1.245777055, 5.0073780147], detector)
    im.apply_to_detector([-0.015571734108306538, -5.7326715464], detector)
    '''
    vm.apply_to_detector([6.329044e+06, 7.070545190569272265e+06, 6.3290662440e+06, 7.320139440024248324e+06], detector)
    fs.apply_to_detector([-1.51087, 9.790192e-01, -2.10403], detector)
    al.apply_to_detector([7.99097e-01, .0091], detector)
    oshoot.apply_to_detector([-5.2901815, 1.80], detector)
    osc.apply_to_detector([-2.181, 7, -2.2, 5.], detector)
    im.apply_to_detector([-.12, -1.54175], detector)
    wfm = WaveformModel(wf, align_percent=align_point, detector=detector, align_idx=100)
    plotter = WaveformFitPlotter(wf_directory, int(num_samples), wfm)

    plotter.plot_waveform()
    #plotter.plot_trace()

    plt.show()


if __name__=="__main__":
    main(*sys.argv[1:] )