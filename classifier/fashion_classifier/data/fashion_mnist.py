"""FashionMNIST DataModule."""
import argparse

import torch
from torch.utils.data import random_split
from torchvision.datasets import FashionMNIST as TorchFashionMNIST

from fashion_classifier.data.base_data_module import BaseDataModule, load_and_print_info
import fashion_classifier.data.config as settings
from torchvision import transforms as T


class FashionMNIST(BaseDataModule):
    """FashionMNIST DataModule."""

    def __init__(self, args: argparse.Namespace) -> None:
        super().__init__(args)
        self.data_dir = settings.DOWNLOADED_DATA_DIRNAME
        self.transform = T.Compose([
                T.ToTensor(),
                T.Normalize((0.2861,), (0.3530,))
            ])
        self.input_dims = settings.DIMS
        self.output_dims = settings.OUTPUT_DIMS
        self.mapping = settings.MAPPING

    def prepare_data(self, *args, **kwargs) -> None:
        """Download train and test MNIST data from PyTorch canonical source."""
        TorchFashionMNIST(self.data_dir, train=True, download=True)
        TorchFashionMNIST(self.data_dir, train=False, download=True)

    def setup(self, stage=None) -> None:
        """Split into train, val, test, and set dims."""
        fashion_mnist_full = TorchFashionMNIST(self.data_dir, train=True, transform=self.transform)
        self.data_train, self.data_val = random_split(fashion_mnist_full, [settings.TRAIN_SIZE, settings.VAL_SIZE])  # type: ignore
        self.data_test = TorchFashionMNIST(self.data_dir, train=False, transform=self.transform)


if __name__ == "__main__":
    load_and_print_info(FashionMNIST)
