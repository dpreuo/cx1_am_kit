#!/usr/bin/env bash

#PBS -J 1-512
#PBS -lselect=1:ncpus=9:mem=4gb
#PBS -lwalltime=04:00:00
#PBS -e /rds/general/user/ppd19/home/kitaev_systems/many_systems/logs/errors/
#PBS -o /rds/general/user/ppd19/home/kitaev_systems/many_systems/logs/outputs/

module load intel-suite anaconda3/personal
. ~/anaconda3/etc/profile.d/conda.sh
conda activate base

python -u /rds/general/user/ppd19/home/kitaev_systems/many_systems/many_systems.py
