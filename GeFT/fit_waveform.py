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
