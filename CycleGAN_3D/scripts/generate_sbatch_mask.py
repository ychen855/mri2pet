import os
import shutil

datasets = ['adni']
training = True
if training:
    python_path = '/scratch/ychen855/mri2pet/CycleGAN_3D/train_mask.py'
else:
    python_path = '/scratch/ychen855/mri2pet/CycleGAN_3D/test_mask.py'
baseline = False
n_fold = 5
model = 'mask' if training else 'mask_test'
exp_name = 'abeta'
feature = 'abeta'
continue_train = False
start_epoch = 10
n_epoch = 200
n_test_epoch = 100
data_root = '/data/hohokam/Yanxi/Data/mri2pet'

for dataset in datasets:
    for i in range(n_fold):
        data_folder = os.path.join(data_root, dataset)
        if training:
            job_file = 'sbatch_jobs/' + dataset + '_' + exp_name + '_' + str(i) + '.sh'
        else:
            job_file = 'sbatch_jobs/' + dataset + '_' + exp_name + '_test_' + str(i) + '_' + str(n_test_epoch) + '.sh'
        with open(job_file, 'w') as f:
            lines = list()
            lines.append('#!/bin/bash\n')

            lines.append('#SBATCH -n 4                        # number of cores')
            lines.append('#SBATCH --mem=64G')
            lines.append('#SBATCH -p general')
            lines.append('#SBATCH -G a100:1')
            if training:
                lines.append('#SBATCH -t 1-00:00:00                 # wall time (D-HH:MM:SS)')
            else:
                lines.append('#SBATCH -t 0-04:00:00                 # wall time (D-HH:MM:SS)')
            lines.append('#SBATCH -o /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.out             # STDOUT (%j = JobId)')
            lines.append('#SBATCH -e /scratch/ychen855/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.err             # STDERR (%j = JobId)')
            lines.append('#SBATCH --mail-type=END             # Send a notification when the job starts, stops, or fails')
            lines.append('#SBATCH --mail-user=ychen855@asu.edu # send-to address\n')

            lines.append('module purge    # Always purge modules to ensure a consistent environment\n')

            lines.append('module load cuda-11.7.0-gcc-11.2.0\n')

            lines.append('source ~/.bashrc')
            lines.append('conda activate tetcnn\n')
            if training:
                lines.append('NAME=' + dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch')
                lines.append('FOLD=' + str(i))
                lines.append('DATA_PATH=' + os.path.join(data_root, dataset))
                lines.append('VAL_PATH=' + os.path.join(data_root, dataset))
                lines.append('MODEL=' + model)
                lines.append('FEATURE=' + feature)
                lines.append('DATA_SPLIT=' + os.path.join(data_root, dataset, 'data_split.csv'))
                lines.append('PYTHON_PATH=/scratch/ychen855/mri2pet/CycleGAN_3D/train_mask.py')
                lines.append('CHECKPOINTS_DIR=/scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check\n')
                if baseline:
                    if continue_train:
                        lines.append('python ${PYTHON_PATH} --name ${NAME} --feature ${FEATURE} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers 4 --batch_size 8 --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG condition --ngf 8 --ndf 16 --continue_train --epoch_count 40 --which_epoch ' + str(start_epoch) + ' --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                    else:
                        lines.append('python ${PYTHON_PATH} --name ${NAME} --feature ${FEATURE} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers 4 --batch_size 8 --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG condition --ngf 8 --ndf 16 --clinical ' + os.path.join(data_root, dataset, 'clinical.csv') + ' --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                else:
                    if continue_train:
                        lines.append('python ${PYTHON_PATH} --name ${NAME} --feature ${FEATURE} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers 4 --batch_size 8 --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG condition --ngf 64 --ndf 64 --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                    else:
                        lines.append('python ${PYTHON_PATH} --name ${NAME} --feature ${FEATURE} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers 4 --batch_size 8 --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG condition --ngf 64 --ndf 64 --clinical ' + os.path.join(data_root, dataset, 'data_split.csv') + ' --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
            else:
                lines.append('EPOCH=' + str(n_test_epoch))
                lines.append('FOLD=' + str(i))
                lines.append('MODEL=' + model)
                lines.append('FEATURE=' + feature)
                if str(n_test_epoch) + '_net_G.pth' not in os.listdir(os.path.join('../CycleGAN3D_check', dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch')):
                    shutil.move(os.path.join('../CycleGAN3D_check', dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch', str(n_test_epoch) + '_net_G_A.pth'), os.path.join('../CycleGAN3D_check', dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch', str(n_test_epoch) + '_net_G.pth'))
                lines.append('NAME=' + dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch')
                lines.append('IMG_DIR=' + os.path.join(data_root, dataset))

                if 'gen_' + exp_name + '_' + str(i) + '_' + str(n_test_epoch) not in os.listdir(os.path.join(data_root, dataset, 'gen')):
                    os.mkdir(os.path.join(data_root, dataset, 'gen', 'gen_' + exp_name + '_' + str(i) + '_' + str(n_test_epoch)))
                gen_folder = os.path.join(data_root, dataset, 'gen', 'gen_' + exp_name + '_' + str(i) + '_' + str(n_test_epoch))

                lines.append('RES_DIR=' + gen_folder)
                lines.append('PYTHON_DIR=/scratch/ychen855/mri2pet/CycleGAN_3D/test_mask.py')

                if baseline:
                    lines.append('\tpython ${PYTHON_DIR} --name ${NAME} --feature ${FEATURE} --image ${IMG_DIR} --result ${RES_DIR} --workers 4 --netG condition --model ${MODEL} --ngf 8 --ndf 16 --clinical ' + os.path.join(data_root, dataset, 'data_split.csv') + ' --checkpoints_dir /scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check --which_epoch ${EPOCH} --fold ${FOLD}')
                else:
                    lines.append('\tpython ${PYTHON_DIR} --name ${NAME} --feature ${FEATURE} --image ${IMG_DIR} --result ${RES_DIR} --workers 4 --netG condition --model ${MODEL} --ngf 64 --ndf 64 --clinical ' + os.path.join(data_root, dataset, 'data_split.csv') + ' --checkpoints_dir /scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check --which_epoch ${EPOCH} --fold ${FOLD}')


            f.write('\n'.join(lines))
