#!/bin/sh
##Set name of job
#PBS -N Testing
##Pass thru local environment variables
#PBS -V
#PBS -oe outlog.log

cd Software/GeFT/Geft

python fit_waveform.py