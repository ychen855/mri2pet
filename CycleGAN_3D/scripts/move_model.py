import os
import shutil

def move_model(src, dst, dataset, model, fold, epoch):
    dst_folder = '_'.join([dataset, model, str(epoch) + 'epoch'])
    if dst_folder not in os.listdir(dst):
        os.mkdir(os.path.join(dst, dst_folder))
    for i in range(fold):
        shutil.copy(os.path.join(src, '_'.join([dataset, model, str(i), str(epoch) + 'epoch']), '40_net_G_A.pth'), os.path.join(dst, dst_folder, '40_net_G_A_' + str(i) + '.pth'))
        shutil.copy(os.path.join(src, '_'.join([dataset, model, str(i), str(epoch) + 'epoch']), '200_net_G_A.pth'), os.path.join(dst, dst_folder, '200_net_G_A_' + str(i) + '.pth'))

if __name__ == '__main__':
    src = '/scratch/ychen855/mri2pet/CycleGAN_3D/CycleGAN3D_check'
    dst = '/scratch/ychen855/mri2pet/CycleGAN_3D/saved_models'
    dataset = 'adni'
    model = 'resnet6'
    fold = 5
    epoch = 200
    move_model(src, dst, dataset, model, fold, epoch)