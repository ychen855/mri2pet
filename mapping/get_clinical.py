import os
import shutil

def get_clinical():
    with open('clinical_raw.csv', 'w') as fout:
        fout.write(','.join(['mri', 'pet', 'age', 'sex', 'apoe', 'abeta']) + '\n')
        with open('bai_abeta_use_new.csv') as f:
            f.readline()
            for line in f:
                linelist = line.split('\n')[0].split(',')
                mri_id = linelist[22]
                pet_id = linelist[23]
                age = linelist[5]
                sex = linelist[6]
                apoe_geno = linelist[8]
                abeta = linelist[4]
                if apoe_geno == 'NC':
                    apoe = '0'
                elif apoe_geno == 'HT':
                    apoe = '1'
                elif apoe_geno == 'HM':
                    apoe = '2'
                else:
                    apoe = ''
                if mri_id != '' and pet_id != '':
                    fout.write(','.join([mri_id, pet_id, age, sex, apoe, abeta]) + '\n')

def remove_dup():
    with open('clinical_raw.csv') as f:
        with open('clinical.csv', 'w') as fout:
            fout.write(f.readline())
            pet = ''
            for line in f:
                linelist = line.split('\n')[0].split(',')
                cur_pet = linelist[1]
                if cur_pet == pet:
                    continue
                else:
                    fout.write(','.join([linelist[0] + '.nii', linelist[1] + '.nii'] + linelist[2:]) + '\n')
                    pet = cur_pet

def trivial():
    mri_set = set()

    with open('clinical_final.csv', 'w') as fout:
        with open('clinical_652_new.csv') as f:
            for line in f:
                fout.write(line)
                linelist = line.split('\n')[0].split(',')
                mri_set.add(linelist[0])
        with open('clinical_159_new.csv') as f:
            f.readline()
            for line in f:
                linelist = line.split('\n')[0].split(',')
                if linelist[0] not in mri_set:
                    fout.write(line)

def check():
    image_root = '/data/hohokam/Yanxi/Data/mri2pet/adni/images'
    label_root = '/data/hohokam/Yanxi/Data/mri2pet/adni/labels'
    n = 0
    with open('clinical_final.csv') as f:
        f.readline()
        for line in f:
            linelist = line.split('\n')[0].split(',')
            if linelist[0] in os.listdir(image_root) and linelist[1] in os.listdir(label_root):
                n += 1
            else:
                print(linelist[0], ' ', linelist[1])
    print(n)

if __name__ == '__main__':
    # get_clinical()
    # remove_dup()
    # trivial()
    check()