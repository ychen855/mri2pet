#!/bin/bash

#SBATCH -n 1                        # number of cores
#SBATCH --mem=64G
#SBATCH -p general
#SBATCH -t 0-04:00:00                 # wall time (D-HH:MM:SS)
#SBATCH -o /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/evaluate_%j.out             # STDOUT (%j = JobId)
#SBATCH -e /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/evaluate_%j.err             # STDERR (%j = JobId)
#SBATCH --mail-type=END             # Send a notification when the job starts, stops, or fails
#SBATCH --mail-user=ychen855@asu.edu # send-to address

module purge    # Always purge modules to ensure a consistent environment

source ~/.bashrc
conda activate tetcnn

python /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/evaluate.py --dataset adni --exp resnet_6blocks --epoch 200 --map /data/hohokam/Yanxi/Data/mri2pet/adni/data_split.csv
