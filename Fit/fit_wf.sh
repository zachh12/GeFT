#!/bin/sh
#PBS -N Waveform
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:30:00
#PBS -V
#PBS -o outputwf.log
#PBS -e errorwf.log
#source .bash_rc
echo $PWD
cd Software/GeFT/GeFT
python fit_waveform.py 4

