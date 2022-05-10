#!/usr/bin/env bash

#PBS -J 1-200
#PBS -lselect=1:ncpus=1:mem=4gb
#PBS -lwalltime=03:00:00

module load intel-suite anaconda3/personal
. ~/anaconda3/etc/profile.d/conda.sh
conda activate koala

python -u /rds/general/user/tch14/home/many_systems/many_systems.py