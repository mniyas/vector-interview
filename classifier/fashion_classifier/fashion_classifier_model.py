import argparse
from pathlib import Path
from typing import Sequence, Union

from fashion_classifier.lit_models import BaseLitModel
from fashion_classifier.models import ResNet
from fashion_classifier.data.config import MAPPING, DOWNLOADED_DATA_DIRNAME
import util
from torchvision import transforms as T
from PIL import Image
import torch

from torchvision.datasets import FashionMNIST as TorchFashionMNIST


STAGED_MODEL_DIRNAME = Path(__file__).resolve().parent / "artifacts" / "classifier"
MODEL_FILE = "model.pt"


class FashionClassifierModel:
    def __init__(self, model_path=None):
        if model_path is None:
            model_path = STAGED_MODEL_DIRNAME / MODEL_FILE
        self.transform = T.Compose([T.ToTensor(), T.Normalize((0.2861,), (0.3530,))])
        model = ResNet({"mapping": MAPPING})
        self.lit_model = BaseLitModel.load_from_checkpoint(checkpoint_path=model_path, model=model)
        self.lit_model.eval()
        self.scripted_model = self.lit_model.to_torchscript(method="script", file_path=None)

    @torch.no_grad()
    def predict(self, image: Union[str, Image.Image]) -> str:
        """Predict/infer class of input image."""
        image_pil = image
        if not isinstance(image, Image.Image):
            image_pil = util.read_image_pil(image, grayscale=True)

        image_tensor = self.transform(image_pil)
        y_pred = self.scripted_model(image_tensor.unsqueeze(axis=0))[0]
        return MAPPING[torch.argmax(y_pred).item()]


if __name__ == "__main__":
    model = FashionClassifierModel("artifacts/epoch=0004-validation.loss=0.247.ckpt")
    data_dir = DOWNLOADED_DATA_DIRNAME
    data = TorchFashionMNIST(data_dir, train=False, download=True)
    prediction = model.predict(data[0][0])
    print(data[0][1], prediction)
