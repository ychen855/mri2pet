import os
import shutil

datasets = ['adni']
training = False
if training:
    python_path = '/scratch/ychen855/mri2pet/CycleGAN_3D/train.py'
else:
    python_path = '/scratch/ychen855/mri2pet/CycleGAN_3D/test.py'

condition = False
feature = 'abeta'

n_fold = 5
n_workers = 4
batch_size = 8
model = 'cycle_gan' if training else 'test'
exp_name = 'resnet6'
netg = 'resnet_6blocks'
netd = 'basic' # basic/n_layers/pixel
ngf = 64
ndf = 64
continue_train = False
which_epoch = 140
epoch_count = which_epoch
n_epoch = 200
test_epoch = 200
data_root = '/data/hohokam/Yanxi/Data/mri2pet'
checkpoints_dir = '/scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check'

for dataset in datasets:
    for i in range(n_fold):
        data_folder = os.path.join(data_root, dataset)
        if training:
            job_file = 'sbatch_jobs/' + dataset + '_' + exp_name + '_' + str(i) + '.sh'
        else:
            job_file = 'sbatch_jobs/' + dataset + '_' + exp_name + '_test_' + str(i) + '_' + str(test_epoch) + '.sh'
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
                lines.append('NETG=' + netg)
                lines.append('NETD=' + netd)
                lines.append('NGF=' + str(ngf))
                lines.append('NDF=' + str(ndf))
                lines.append('NWORKERS=' + str(n_workers))
                lines.append('BATCH_SIZE=' + str(batch_size))
                lines.append('DATA_SPLIT=' + os.path.join(data_root, dataset, 'data_split.csv'))
                lines.append('PYTHON_PATH=' + python_path)
                lines.append('CHECKPOINTS_DIR=' + checkpoints_dir)
                
                if continue_train:
                    lines.append('WHICH_EPOCH=' + str(which_epoch))
                    lines.append('EPOCH_COUNT=' + str(epoch_count))
                    if condition:
                        lines.append('FEATURE=' + feature)
                        lines.append('python ${PYTHON_PATH} --feature ${FEATURE} --name ${NAME} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --continue_train --which_epoch ${WHICH_EPOCH} --epoch_count ${EPOCH_COUNT} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                    else:
                        lines.append('python ${PYTHON_PATH} --name ${NAME} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --continue_train --which_epoch ${WHICH_EPOCH} --epoch_count ${EPOCH_COUNT} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                else:
                    if condition:
                        lines.append('FEATURE=' + feature)
                        lines.append('python ${PYTHON_PATH} --feature ${FEATURE} --name ${NAME} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                    else:
                        lines.append('python ${PYTHON_PATH} --name ${NAME} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq 20 --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
            else:
                lines.append('MODEL=' + model)
                lines.append('NETG=' + netg)
                lines.append('WHICH_EPOCH=' + str(test_epoch))
                lines.append('NAME=' + dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch')
                # if str(test_epoch) + '_net_G.pth' not in os.listdir(os.path.join('../CycleGAN3D_check', dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch')):
                #     shutil.move(os.path.join('../CycleGAN3D_check', dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch', str(test_epoch) + '_net_G_A.pth'), os.path.join('../CycleGAN3D_check', dataset + '_' + exp_name + '_' + str(i) + '_' + str(n_epoch) + 'epoch', str(test_epoch) + '_net_G.pth'))

                if 'gen_' + exp_name + '_' + str(i) + '_' + str(test_epoch) not in os.listdir(os.path.join(data_root, dataset, 'gen')):
                    os.mkdir(os.path.join(data_root, dataset, 'gen', 'gen_' + exp_name + '_' + str(i) + '_' + str(test_epoch)))
                gen_folder = os.path.join(data_root, dataset, 'gen', 'gen_' + exp_name + '_' + str(i) + '_' + str(test_epoch))
                
                lines.append('RES_DIR=' + gen_folder)
                lines.append('NWORKERS=' + str(n_workers))
                lines.append('PYTHON_PATH=' + python_path)
                lines.append('NGF=' + str(ngf))
                lines.append('CHECKPOINTS_DIR=' + checkpoints_dir)
                
                if condition:
                    lines.append('IMG_DIR=' + os.path.join(data_root, dataset))
                    lines.append('FOLD=' + str(i))
                    lines.append('FEATURE=' + feature)
                    lines.append('python ${PYTHON_PATH} --name ${NAME} --feature ${FEATURE} --image ${IMG_DIR} --result ${RES_DIR} --workers ${NWORKERS} --netG ${NETG} --model ${MODEL} --ngf ${NGF} --checkpoints_dir ${CHECKPOINTS_DIR} --which_epoch ${WHICH_EPOCH} --fold ${FOLD}')
                else:
                    lines.append('IMG_DIR=' + os.path.join(data_root, dataset, 'images'))
                    image_list = []
                    with open(os.path.join(data_root, dataset, 'data_split.csv')) as fdata_split:
                        for line in fdata_split:
                            linelist = line.split('\n')[0].split(',')
                            if linelist[-1] == str(i):
                                image_list.append(linelist[0])
                    lines.append('for subj in ' + ' '.join(image_list))
                    lines.append('do')
                    lines.append('\tpython ${PYTHON_PATH} --name ${NAME} --image ${IMG_DIR}/${subj} --result ${RES_DIR}/${subj} --workers ${NWORKERS} --netG ${NETG} --model ${MODEL} --ngf ${NGF} --checkpoints_dir ${CHECKPOINTS_DIR} --which_epoch ${WHICH_EPOCH}')
                    lines.append('done')

            f.write('\n'.join(lines))
