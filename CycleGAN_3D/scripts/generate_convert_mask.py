import os
import shutil

root = '/data/hohokam/Yanxi/Data/mri2pet/adni/wmparc'

for f in os.listdir(root):
    job_file = os.path.join('sbatch_jobs', 'job_convert_mask_' + f + '.sh')
    with open(job_file, 'w') as fout:
        lines = []
        lines.append('#!/bin/bash\n')

        lines.append('#SBATCH -n 1                        # number of cores')
        lines.append('#SBATCH --mem=32G')
        lines.append('#SBATCH -p general')
        lines.append('#SBATCH -t 0-01:00:00                 # wall time (D-HH:MM:SS)')
        lines.append('#SBATCH -o /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.out             # STDOUT (%j = JobId)')
        lines.append('#SBATCH -e /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.err             # STDERR (%j = JobId)')
        lines.append('#SBATCH --mail-type=NONE             # Send a notification when the job starts, stops, or fails')
        lines.append('#SBATCH --mail-user=ychen855@asu.edu # send-to address\n')

        lines.append('module purge    # Always purge modules to ensure a consistent environment\n')

        lines.append('module load freesurfer-7.3.0-gcc-11.2.0\n')
        lines.append('export FS_LICENSE=/data/hohokam/Yanxi/Data/fs_license/license.txt\n')

        lines.append('source ~/.bashrc')
        lines.append('conda activate tetcnn\n')
        lines.append('cd ' + os.path.join(root, f) + '\n')
        lines.append('mri_convert --in_type mgz --out_type nii wmparc.nii wmparc.nii')

        fout.write('\n'.join(lines))
