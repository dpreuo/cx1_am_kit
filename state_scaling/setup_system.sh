#!/usr/bin/env bash

#PBS -lselect=1:ncpus=9:mem=4gb
#PBS -lwalltime=01:00:00
#PBS -e /rds/general/user/ppd19/home/cx1_am_kit/state_scaling/logs/errors
#PBS -o /rds/general/user/ppd19/home/cx1_am_kit/state_scaling/logs/outputs

module load intel-suite anaconda3/personal
. ~/anaconda3/etc/profile.d/conda.sh
conda activate base

python -u /rds/general/user/ppd19/home/cx1_am_kit/state_scaling/setup_system.py

