#!/usr/bin/env bash

#PBS -J 1-10
#PBS -lselect=1:ncpus=1:mem=4gb
#PBS -lwalltime=04:00:00
#PBS -e /rds/general/user/ppd19/home/cx1_am_kit/multiscale_tests/logs/errors/
#PBS -o /rds/general/user/ppd19/home/cx1_am_kit/multiscale_tests/logs/outputs/

module load intel-suite anaconda3/personal
. ~/anaconda3/etc/profile.d/conda.sh
conda activate base

python -u /rds/general/user/ppd19/home/cx1_am_kit/multiscale_tests/solve_system.py
