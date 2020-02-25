#!/bin/bash

#SBATCH -J h12_2deg
#SBATCH -n 20
#SBATCH -N 1
#SBATCH -p mb
#SBATCH -o output_%j.out
#SBATCH -e errors_%j.err

FOAM_INST_DIR=/opt/OpenFOAM
./Allrun
