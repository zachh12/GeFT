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
    vm.apply_to_detector([5068054.82, 4988240.69, 6538435.34, 5925515.5], detector)
    hp.apply_to_detector([34336.51273333012], detector)
    fs.apply_to_detector([-1.6726791950686515, 0.8668817247858145, -4.752247247699966], detector)
    al.apply_to_detector([0.8081722376640458, 0.11022819946140337], detector)
    oshoot.apply_to_detector([-4.781231221813979, 0.4360771327659954], detector)
    osc.apply_to_detector([-1.7145995461740187, 3.002188106849415, -1.3480151900941126, 4.9442560336492445], detector)
    im.apply_to_detector([-0.19525537473916815, -1.906570916850837 ], detector)
    #tp.apply_to_detector(935, detector)
    '''
    #626
    vm.apply_to_detector([5060949, 4998461, 6540686, 5911641], detector)
    #hp.apply_to_detector([35040.50], detector)
    fs.apply_to_detector([-1.6466, 0.84437, -4.7535], detector)
    al.apply_to_detector([0.797979, 0.1095046], detector)
    oshoot.apply_to_detector([-4.83454, 0.49837], detector)
    osc.apply_to_detector([-1.69987, 3.003310, -1.1292170, 4.983754], detector)
    im.apply_to_detector([-0.19515, -1.9196440519], detector)
    #tm.apply_to_detector(1222, detector)
    '''
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
