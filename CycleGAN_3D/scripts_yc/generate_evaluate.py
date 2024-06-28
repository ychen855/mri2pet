import os
import shutil

root = '/data/hohokam/Yanxi/Data/mri2pet'
fmap = '/data/hohokam/Yanxi/Data/mri2pet/adni/data_split.csv'
dataset = 'adni'
exp_names = ['baseline256']
epoch = 40
n_fold = 5
eval_all = True
result = '/scratch/ychen855/mri2pet/CycleGAN_3D/results'

for exp_name in exp_names:
    job_file = os.path.join('sbatch_jobs', exp_name + '_' + str(epoch) + '.sh')
    with open(job_file, 'w') as f:
        lines = []
        lines.append('#!/bin/bash\n')
        lines.append('#SBATCH -n 8                        # number of cores')
        lines.append('#SBATCH -N 1                        # number of nodes')
        lines.append('#SBATCH --mem=128G')
        lines.append('#SBATCH -p general')
        lines.append('#SBATCH -q grp_rwang133')
        lines.append('#SBATCH -t 0-04:00:00                 # wall time (D-HH:MM:SS)')
        lines.append('#SBATCH -o /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.out             # STDOUT (%j = JobId)')
        lines.append('#SBATCH -e /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.err             # STDERR (%j = JobId)')
        lines.append('#SBATCH --mail-type=NONE             # Send a notification when the job starts, stops, or fails')
        lines.append('#SBATCH --mail-user=ychen855@asu.edu # send-to address\n')

        lines.append('source ~/.bashrc')
        lines.append('conda activate cu121\n')

        lines.append('ROOT=' + root)
        lines.append('DATASET=' + dataset)
        lines.append('EXP=' + exp_name)
        lines.append('EPOCH=' + str(epoch))
        lines.append('MAP=' + fmap)
        lines.append('N_FOLD=' + str(n_fold))
        lines.append('RESULT=' + result + '\n')
        
        if eval_all:
            lines.append('python /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/evaluate.py --root ${ROOT} --dataset ${DATASET} --exp ${EXP} --epoch ${EPOCH} --map ${MAP} --n_fold ${N_FOLD} --result ${RESULT} --all')
        else:
            lines.append('python /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/evaluate.py --root ${ROOT} --dataset ${DATASET} --exp ${EXP} --epoch ${EPOCH} --map ${MAP} --n_fold ${N_FOLD} --result ${RESULT}')

        f.write('\n'.join(lines))
