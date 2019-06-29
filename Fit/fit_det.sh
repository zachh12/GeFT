#!/bin/sh
#PBS -N Fit_Detector_672
#PBS -l nodes=1:ppn=1
#PBS -l walltime=48:00:00
#PBS -V
#PBS -o output580.log
#PBS -e error580.log
#source .bash_rc

cd Software/GeFT/GeFT
python do_fit.py 580
