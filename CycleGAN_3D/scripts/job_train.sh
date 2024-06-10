#!/bin/bash

#SBATCH -n 4                        # number of cores
#SBATCH --mem=32G
#SBATCH -p general
#SBATCH -G a100:1
##SBATCH -q wildfire
#SBATCH -t 1-00:00:00                 # wall time (D-HH:MM:SS)
#SBATCH -o /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.out             # STDOUT (%j = JobId)
#SBATCH -e /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.err             # STDERR (%j = JobId)
#SBATCH --mail-type=NONE             # Send a notification when the job starts, stops, or fails
#SBATCH --mail-user=ychen855@asu.edu # send-to address

module purge    # Always purge modules to ensure a consistent environment

module load cuda-11.7.0-gcc-11.2.0

source ~/.bashrc
conda activate cyclegan

NAME=674_cross_0_80epoch
FOLD=0
DATA_PATH=/scratch/ychen855/Data/mri2pet/674/warped/raw
VAL_PATH=/scratch/ychen855/Data/mri2pet/674/warped/raw
DATA_SPLIT=/scratch/ychen855/Data/mri2pet/674/warped/raw/data_split.csv

PYTHON_PATH=/scratch/ychen855/mri2pet/CycleGAN_3D/train.py
CHECKPOINTS_DIR=/scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check

# python /scratch/ychen855/mri2pet/CycleGAN_3D/train.py --name 674_cross_0_80epoch --data_path /scratch/ychen855/Data/mri2pet/674/warped/raw --val_path /scratch/ychen855/Data/mri2pet/674/warped/raw --workers 4 --batch_size 8 --save_epoch_freq 40 --niter 40 --niter_decay 40 --checkpoints_dir /scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check --netG resnet_6blocks --ngf 8
python ${PYTHON_PATH} --name ${NAME} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --workers 4 --batch_size 8 --save_epoch_freq 40 --niter 40 --niter_decay 40 --checkpoints_dir ${CHECKPOINTS_DIR} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}