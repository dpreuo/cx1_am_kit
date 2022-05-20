#!/usr/bin/env bash

#PBS -J 19-23, 28
#PBS -lselect=1:ncpus=2:mem=4gb
#PBS -lwalltime=06:00:00
#PBS -e /rds/general/user/ppd19/home/cx1_am_kit/state_scaling/logs/errors
#PBS -o /rds/general/user/ppd19/home/cx1_am_kit/state_scaling/logs/outputs

module load intel-suite anaconda3/personal
. ~/anaconda3/etc/profile.d/conda.sh
conda activate base

python -u /rds/general/user/ppd19/home/cx1_am_kit/state_scaling/solve_systems.py

