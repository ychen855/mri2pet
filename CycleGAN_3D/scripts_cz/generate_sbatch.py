import os
import shutil

datasets = ['adni']
training = False

lr = 0.0002
pool_size = 20
lmd = 2.0
lmdidt = 0.5
init_type = 'xavier'
batch_size = 8
strides = 16

condition = False
if condition:
    feature = 'abeta'
    model = 'mask' if training else 'mask_test'
    netg = 'condition'
    if training:
        python_path = '/scratch/czhu62/yc/mri2pet/CycleGAN_3D/train_mask.py'
    else:
        python_path = '/scratch/czhu62/yc/mri2pet/CycleGAN_3D/test_mask.py'
else:
    model = 'cycle_gan' if training else 'test'
    netg = 'resnet_9blocks'
    if training:
        python_path = '/scratch/czhu62/yc/mri2pet/CycleGAN_3D/train.py'
    else:
        python_path = '/scratch/czhu62/yc/mri2pet/CycleGAN_3D/test.py'

n_fold = 5
n_workers = 8
netd = 'basic' # basic/n_layers/pixel

ngf = 64
ndf = 64
continue_train = False
which_epoch = 200
epoch_count = which_epoch
n_epoch = 200
save_freq = 20
test_epoch = 200
data_root = '/data/hohokam/Yanxi/Data/mri2pet'
checkpoints_dir = '/scratch/czhu62/yc/mri2pet/CycleGAN_3D/CycleGAN3D_check'

for dataset in datasets:
    exp_name = 'baseline'
    for i in range(n_fold):
        data_folder = os.path.join(data_root, dataset)
        if training:
            job_file = 'sbatch_jobs/' + dataset + '_' + exp_name + '_' + str(which_epoch) + '_' + str(i) + '.sh'
        else:
            job_file = 'sbatch_jobs/' + dataset + '_' + exp_name + '_test_' + str(test_epoch) + '_' + str(i) + '_' + str(n_epoch) + 'epoch.sh'
        with open(job_file, 'w') as f:
            lines = list()
            lines.append('#!/bin/bash\n')

            lines.append('#SBATCH -n 8                        # number of cores')
            lines.append('#SBATCH -N 1                        # number of nodes')
            lines.append('#SBATCH --mem=128G')
            lines.append('#SBATCH -p general')
            lines.append('#SBATCH -q grp_rwang133')
            lines.append('#SBATCH -G h100:1')
            if training:
                lines.append('#SBATCH -t 1-00:00:00                 # wall time (D-HH:MM:SS)')
            else:
                lines.append('#SBATCH -t 0-04:00:00                 # wall time (D-HH:MM:SS)')
            lines.append('#SBATCH -o /scratch/czhu62/yc/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.out             # STDOUT (%j = JobId)')
            lines.append('#SBATCH -e /scratch/czhu62/yc/mri2pet/CycleGAN_3D/scripts/job_logs/slurm.%j.err             # STDERR (%j = JobId)')
            lines.append('#SBATCH --mail-type=END             # Send a notification when the job starts, stops, or fails')
            lines.append('#SBATCH --mail-user=ychen855@asu.edu # send-to address\n')

            lines.append('module purge    # Always purge modules to ensure a consistent environment\n')

            lines.append('module load cuda-12.1.1-gcc-12.1.0\n')

            lines.append('source ~/.bashrc')
            lines.append('conda activate cu121\n')
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
                lines.append('LR=' + str(lr))
                lines.append('LAMBDA=' + str(lmd))
                lines.append('LAMBDA_IDT=' + str(lmdidt))
                lines.append('INIT_TYPE=' + str(init_type))
                lines.append('POOL_SIZE=' + str(pool_size))
                lines.append('NWORKERS=' + str(n_workers))
                lines.append('BATCH_SIZE=' + str(batch_size))
                lines.append('DATA_SPLIT=' + os.path.join(data_root, dataset, 'data_split.csv'))
                lines.append('PYTHON_PATH=' + python_path)
                lines.append('CHECKPOINTS_DIR=' + checkpoints_dir)
                lines.append('SAVE_FREQ=' + str(save_freq))
                
                if continue_train:
                    lines.append('WHICH_EPOCH=' + str(which_epoch))
                    lines.append('EPOCH_COUNT=' + str(epoch_count))
                    if condition:
                        lines.append('FEATURE=' + feature)
                        lines.append('python ${PYTHON_PATH} --init_type ${INIT_TYPE} --lambda_A ${LAMBDA} --lambda_B ${LAMBDA} --lambda_identity ${LAMBDA_IDT} --pool_size ${POOL_SIZE} --feature ${FEATURE} --name ${NAME} --lr ${LR} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq ${SAVE_FREQ} --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --continue_train --which_epoch ${WHICH_EPOCH} --epoch_count ${EPOCH_COUNT} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                    else:
                        lines.append('python ${PYTHON_PATH} --init_type ${INIT_TYPE} --lambda_A ${LAMBDA} --lambda_B ${LAMBDA} --lambda_identity ${LAMBDA_IDT} --pool_size ${POOL_SIZE} --name ${NAME} --lr ${LR} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq ${SAVE_FREQ} --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --continue_train --which_epoch ${WHICH_EPOCH} --epoch_count ${EPOCH_COUNT} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                else:
                    if condition:
                        lines.append('FEATURE=' + feature)
                        lines.append('python ${PYTHON_PATH} --init_type ${INIT_TYPE} --lambda_A ${LAMBDA} --lambda_B ${LAMBDA} --lambda_identity ${LAMBDA_IDT} --pool_size ${POOL_SIZE} --feature ${FEATURE} --name ${NAME} --lr ${LR} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq ${SAVE_FREQ} --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
                    else:
                        lines.append('python ${PYTHON_PATH} --init_type ${INIT_TYPE} --lambda_A ${LAMBDA} --lambda_B ${LAMBDA} --lambda_identity ${LAMBDA_IDT} --pool_size ${POOL_SIZE} --name ${NAME} --lr ${LR} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers ${NWORKERS} --batch_size ${BATCH_SIZE} --save_epoch_freq ${SAVE_FREQ} --niter ' + str(n_epoch//2) + ' --niter_decay ' + str(n_epoch//2) + ' --checkpoints_dir ${CHECKPOINTS_DIR} --netG ${NETG} --ngf ${NGF} --ndf ${NDF} --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}')
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
                lines.append('DATA_SPLIT=' + os.path.join(data_root, dataset, 'data_split.csv'))
                
                if condition:
                    lines.append('IMG_DIR=' + os.path.join(data_root, dataset))
                    lines.append('FOLD=' + str(i))
                    lines.append('FEATURE=' + feature)
                    lines.append('python ${PYTHON_PATH} --data_split ${DATA_SPLIT} --name ${NAME} --feature ${FEATURE} --image ${IMG_DIR} --result ${RES_DIR} --workers ${NWORKERS} --netG ${NETG} --model ${MODEL} --ngf ${NGF} --checkpoints_dir ${CHECKPOINTS_DIR} --which_epoch ${WHICH_EPOCH} --fold ${FOLD}')
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
                    lines.append('\tpython ${PYTHON_PATH} --data_split ${DATA_SPLIT} --name ${NAME} --image ${IMG_DIR}/${subj} --result ${RES_DIR}/${subj} --workers ${NWORKERS} --netG ${NETG} --model ${MODEL} --ngf ${NGF} --checkpoints_dir ${CHECKPOINTS_DIR} --which_epoch ${WHICH_EPOCH}')
                    # lines.append('\tpython ${PYTHON_PATH} --stride_inplane 16 --stride_layer 16 --data_split ${DATA_SPLIT} --name ${NAME} --image ${IMG_DIR}/${subj} --result ${RES_DIR}/${subj} --workers ${NWORKERS} --netG ${NETG} --model ${MODEL} --ngf ${NGF} --checkpoints_dir ${CHECKPOINTS_DIR} --which_epoch ${WHICH_EPOCH}')
                    lines.append('done')

            f.write('\n'.join(lines))
