#!/bin/sh
#PBS -N Testing
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:00:20
#PBS -V
#PBS -oe outlog.log
source .bash_rc
cd Software/GeFT/Geft

python fit_waveform.py