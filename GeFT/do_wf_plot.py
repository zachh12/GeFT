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
580: "P42661C",
600: "B8482",
626: "P42574A",
630: "P42661B",
672: "P42661A",
680: "B8477",
690: "P42662A",
692: "B8474",
694: "B8465",
1106: "B8594",
}

def main(dir_name, wf_idx, num_samples=10 ):
    wf_idx = int(wf_idx)

    align_point = 0.95
    chan = 626
    datadir= os.environ['DATADIR']
    directory = "../../Data/Waveform/chan{}_wfs".format(chan)

    wf_directory = os.path.join(directory, "wf{}".format(wf_idx))

    wf_file = datadir + "/Detector/chan{}_8wfs_DS1-1.npz".format(chan)
    conf_name = "{}.conf".format( chan_dict[chan] )

    datadir= os.environ['DATADIR']
    conf_file = datadir +"/siggen/config_files/" + conf_name

    data = np.load(wf_file, encoding="latin1")
    wfs = data['wfs']

    wf = wfs[wf_idx]
    wf.window_waveform(time_point=0.95, early_samples=100, num_samples=125)
    detector = PPC( conf_file, wf_padding=100)

    vm = VelocityModel(include_beta=False)
    hp = HiPassFilterModel(detector)
    fs = FirstStageFilterModel(detector)
    al = AntialiasingFilterModel(detector)
    oshoot = OvershootFilterModel(detector)
    osc = OscillationFilterModel(detector)
    im = ImpurityModelEnds(detector)
    #tm = TrappingModel()

    vm.apply_to_detector([5.113175887585735880e+06, 4.931135374698639847e+06 6.582017554250035435e+06 5.973647864047872834e+06], detector)
    hp.apply_to_detector([7.034677287318628805e+04 ], detector)
    fs.apply_to_detector([-1.613713407466759397e+00, 8.961780932196099503e-01 -3.570576615818913169e+00 ], detector)
    al.apply_to_detector([9.632021736944443857e-01, 1.092491237580749397e-01 ], detector)
    oshoot.apply_to_detector([-5.132649715387167078e+00, 6.836889886576967834e-01 ], detector)
    osc.apply_to_detector([-1.683230727845734354e+00, 3.003407309583828511e+00, -9.148622525552410067e-01, 5.120352824921794443e+00], detector)
    im.apply_to_detector([-6.569293239164863962e-02, -2.749414433346664577e+00 ], detector)
    '''
    #626
    vm.apply_to_detector([5060949, 4998461, 6540686, 5911641], detector)
    hp.apply_to_detector([35040.50], detector)
    fs.apply_to_detector([-1.6466, 0.84437, -4.7535], detector)
    al.apply_to_detector([0.797979, 0.1095046], detector)
    oshoot.apply_to_detector([-4.83454, 0.49837], detector)
    osc.apply_to_detector([-1.69987, 3.003310, -1.1292170, 4.983754], detector)
    im.apply_to_detector([-0.19515, -1.9196440519], detector)
    #tm.apply_to_detector(1222, detector)
    '''
    wfm = WaveformModel(wf, align_percent=align_point, detector=detector, align_idx=100)
    plotter = WaveformFitPlotter(wf_directory, int(num_samples), wfm)
    plotter.plot_waveform()
    #plotter.plot_trace()

    plt.show()


if __name__=="__main__":
    main(*sys.argv[1:] )
