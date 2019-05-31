#!/bin/sh
#PBS -N Fit_Detector
#PBS -l nodes=1:ppn=1
#PBS -l walltime=36:00:00
#PBS -V
#PBS -o output692.log
#PBS -e error692.log
#source .bash_rc

cd Software/GeFT/GeFT
python do_fit.py 692
