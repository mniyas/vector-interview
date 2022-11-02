import argparse
from typing import Any, Dict

import torch
from torch import nn
import torch.nn.functional as F
import torch
import torchvision.models as models
import pytorch_lightning as pl


class ResNet(pl.LightningModule):
    def __init__(self, data_config: Dict[str, Any], args: argparse.Namespace = None) -> None:
        super().__init__()
        self.args = vars(args) if args is not None else {}
        self.data_config = data_config

        _, input_height, input_width = self.data_config["input_dims"]
        assert (
            input_height == input_width
        ), f"input height and width should be equal, but was {input_height}, {input_width}"
        self.input_height, self.input_width = input_height, input_width

        num_classes = len(self.data_config["mapping"])

        # init a pretrained resnet
        backbone = models.resnet18(pretrained=True)
        num_filters = backbone.fc.in_features
        layers = list(backbone.children())[:-1]
        self.feature_extractor = nn.Sequential(*layers)
        self.classifier = nn.Linear(num_filters, num_classes)

    def forward(self, x):
        self.feature_extractor.eval()
        with torch.no_grad():
            representations = self.feature_extractor(x).flatten(1)
        x = self.classifier(representations)
        return x
    
    @staticmethod
    def add_to_argparse(parser):
        return parser
