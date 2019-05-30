#!/bin/sh
#PBS -N Testing
#PBS -l nodes=1:ppn=1
#PBS -l walltime=00:03:00
#PBS -V
#PBS -o output.log
#PBS -e error.log
#source .bash_rc

echo $PWD
cd Software/GeFT/GeFT

python fit_waveform.py 0
