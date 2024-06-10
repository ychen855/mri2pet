import os
import random

def split_data_5(root, f_mapping):
    flist = []
    with open(f_mapping) as f:
        f.readline()
        for line in f:
            flist.append(line.split('\n')[0])
        random.shuffle(flist)
        with open(os.path.join(root, 'data_split.csv'), 'w') as f:
            for i, ele in enumerate(flist):
                if i < len(flist) / 5:
                    f.write(ele + ',0\n')
                elif i < len(flist) / 5 * 2:
                    f.write(ele + ',1\n')
                elif i < len(flist) / 5 * 3:
                    f.write(ele + ',2\n')
                elif i < len(flist) / 5 * 4:
                    f.write(ele + ',3\n')
                else:
                    f.write(ele + ',4\n')

if __name__ == '__main__':
    root = '/data/hohokam/Yanxi/Data/mri2pet/adni'
    f_mapping = '/data/hohokam/Yanxi/Data/mri2pet/adni/clinical.csv'
    split_data_5(root, f_mapping)