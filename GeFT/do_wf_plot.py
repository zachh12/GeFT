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
    hp2 = HiPassFilterModel(detector)
    fs = FirstStageFilterModel(detector)
    al = AntialiasingFilterModel(detector)
    oshoot = OvershootFilterModel(detector)
    osc = OscillationFilterModel(detector)
    im = ImpurityModelEnds(detector)
    tm = TrappingModel()

    vm.apply_to_detector([5068054.82, 4988240.69, 6538435.34, 5925515.5], detector)
    hp.apply_to_detector([72.9], detector)
    hp2.apply_to_detector([34336.51273333012], detector)
    fs.apply_to_detector([-1.6726791950686515, 0.8668817247858145, -4.752247247699966], detector)
    al.apply_to_detector([0.8081722376640458, 0.11022819946140337], detector)
    oshoot.apply_to_detector([-4.781231221813979, 0.4360771327659954], detector)
    osc.apply_to_detector([-1.7145995461740187, 3.002188106849415, -1.3480151900941126, 4.9442560336492445], detector)
    im.apply_to_detector([-0.19525537473916815, -1.906570916850837 ], detector)
    tm.apply_to_detector(935, detector)

    wfm = WaveformModel(wf, align_percent=align_point, detector=detector, align_idx=100)
    plotter = WaveformFitPlotter(wf_directory, int(num_samples), wfm)
    plotter.plot_waveform()
    #plotter.plot_trace()

    plt.show()


if __name__=="__main__":
    main(*sys.argv[1:] )
