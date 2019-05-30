#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil
import numpy as np

import dnest4

from waffle.management import WaveformFitManager
from waffle.models import VelocityModel, LowPassFilterModel, HiPassFilterModel, ImpurityModelEnds
from waffle.models import FirstStageFilterModel, AntialiasingFilterModel
from waffle.models import OvershootFilterModel,OscillationFilterModel, TrappingModel
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

def main(wf, doPlot=False):

    align_point = 0.95
    wf_idx = int(wf)

    chan = 626
    datadir= os.environ['DATADIR']
    directory = "../../Data/Waveform/chan{}_wfs".format(chan)

    wf_file = datadir + "/Detector/chan{}_8wfs_DS1-1.npz".format(chan)
    conf_name = "{}.conf".format( chan_dict[chan] )
    conf_file = datadir +"/siggen/config_files/" + conf_name

    detector = PPC( conf_file, wf_padding=100)

    vm = VelocityModel(include_beta=False)
    #hp = HiPassFilterModel(detector)
    fs = FirstStageFilterModel(detector)
    al = AntialiasingFilterModel(detector)
    oshoot = OvershootFilterModel(detector)
    osc = OscillationFilterModel(detector)
    im = ImpurityModelEnds(detector)
    #tm = TrappingModel()

    vm.apply_to_detector([6.329044e+06, 7.070545190569272265e+06, 6.3290662440e+06, 7.320139440024248324e+06], detector)
    fs.apply_to_detector([-1.51087, 9.790192e-01, -2.10403], detector)
    al.apply_to_detector([7.99097e-01, .0091], detector)
    oshoot.apply_to_detector([-5.2901815, 1.80], detector)
    osc.apply_to_detector([-2.181, 7, -2.2, 5.], detector)
    im.apply_to_detector([-.12, -1.54175], detector)

    data = np.load(wf_file, encoding="latin1")
    wfs = data['wfs']

    wf = wfs[wf_idx]
    wf_directory = os.path.join(directory, "wf{}".format(wf_idx))
    if os.path.isdir(wf_directory):
        if len(os.listdir(wf_directory)) >0:
            raise OSError("Directory {} already exists: not gonna over-write it".format(wf_directory))
    else:
        os.makedirs(wf_directory)

    wf.window_waveform(time_point=align_point, early_samples=100, num_samples=125)

    fm = WaveformFitManager(wf, align_percent=align_point, detector=detector, align_idx=100)

    fm.fit(numLevels=1000, directory = wf_directory, new_level_interval=1000, numParticles=3)


if __name__=="__main__":
    main(*sys.argv[1:])
