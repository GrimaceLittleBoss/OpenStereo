import os

import numpy as np
import torch
from PIL import Image

from .base_reader import BaseReader
from .readpfm import readPFM


class ETH3DReader(BaseReader):
    def __init__(self, root, list_file):
        super().__init__(root, list_file)

    def item_loader(self, item):
        full_paths = [os.path.join(self.root, x) for x in item]
        left_img_path, right_img_path, disp_img_path = full_paths
        left_img = np.array(Image.open(left_img_path).convert('RGB'), dtype=np.float32)
        right_img = np.array(Image.open(right_img_path).convert('RGB'), dtype=np.float32)
        disp_img, _ = readPFM(disp_img_path)
        # remove invalid values
        disp_img[disp_img == np.inf] = 0
        disp_img = disp_img.astype(np.float32)
        sample = {
            'left': left_img,
            'right': right_img,
            'disp': disp_img,
            # 'original_size': left_img.shape[-2:],
        }
        return sample


if __name__ == '__main__':
    dataset = ETH3DReader(root='../../data/ETH3D', list_file='../../../datasets/ETH3D/ETH3D_train.txt')
    print(dataset)
    for i in range(len(dataset)):
        sample = dataset[i]
        disp = sample['disp']
        disp = disp.squeeze()
        print(disp.max(), disp.min())