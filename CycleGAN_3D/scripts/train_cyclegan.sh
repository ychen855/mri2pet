# module load cuda-11.7.0-gcc-11.2.0

# source ~/.bashrc
# conda activate tetcnn

NAME=adni_cyclegan_base_test
FOLD=0
DATA_PATH=/data/hohokam/Yanxi/Data/mri2pet/adni
VAL_PATH=/data/hohokam/Yanxi/Data/mri2pet/adni
MODEL=cycle_gan
DATA_SPLIT=/data/hohokam/Yanxi/Data/mri2pet/adni/data_split.csv
PYTHON_PATH=/scratch/ychen855/mri2pet/CycleGAN_3D/train.py
CHECKPOINTS_DIR=/scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check

python ${PYTHON_PATH} --name ${NAME} --data_path ${DATA_PATH} --val_path ${VAL_PATH} --model ${MODEL} --workers 4 --batch_size 8 --save_epoch_freq 20 --niter 100 --niter_decay 100 --checkpoints_dir ${CHECKPOINTS_DIR} --netG resnet_9blocks --ngf 64 --ndf 64 --cross_validation --data_split ${DATA_SPLIT} --fold ${FOLD}