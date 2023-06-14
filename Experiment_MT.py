from ConstituencyInvariance.translate_sent import translate
from ConstituencyInvariance.detect_bug import detect
import argparse
import os


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file-name',
                        default='business')
    parser.add_argument('--sid',
                        type=int,
                        default=0)
    parser.add_argument('--eid',
                        type=int,
                        default=1)
    return parser.parse_args()


def main():
    args = parse_args()
    file_name = args.file_name
    s_id = args.sid
    e_id = args.eid
    path = './Data/Experiment_MT/'+file_name
    if os.path.exists(path):
        print("文件夹{}已存在！".format(path))
    else:
        os.mkdir(path)
    translate(file_name, s_id, e_id)
    detect(file_name, s_id, e_id)


if  __name__ == '__main__':
    main()

