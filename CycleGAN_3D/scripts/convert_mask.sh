# module load freesurfer-7.3.0-gcc-11.2.0
# export FS_LICENSE=/data/hohokam/Yanxi/Data/fs_license/license.txt

ROOT=/data/hohokam/Yanxi/Data/mri2pet/adni/wmparc

for folder in `ls ${ROOT}`; do
    # echo ${folder}
    mri_convert --in_type mgz --out_type nii ${ROOT}/${folder}/wmparc.mgz ${ROOT}/${folder}/wmparc.nii
done
