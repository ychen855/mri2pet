import os
import shutil
import argparse

def copy_pw(src, dst, flist):
    with open(flist) as f:
        for line in f:
            pid = line.split('\n')[0]
            if pid not in os.listdir(dst):
                os.mkdir(os.path.join(dst, pid))
            if pid not in os.listdir(os.path.join(dst, pid)):
                os.mkdir(os.path.join(dst, pid, pid))
            shutil.copy(os.path.join(src, pid, 'surf', 'lh.pial'), os.path.join(dst, pid, pid))
            shutil.copy(os.path.join(src, pid, 'surf', 'lh.white'), os.path.join(dst, pid, pid))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--src', type=str)
    parser.add_argument('--dst', type=str)
    parser.add_argument('--flist', type=str)
    args = parser.parse_args()

    copy_pw(args.src, args.dst, args.flist)