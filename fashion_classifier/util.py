"""Utility functions for classifier module."""
from pathlib import Path
from typing import Union

from PIL import Image


def read_image_pil(image_uri: Union[Path, str], grayscale=False) -> Image:
    with open(image_uri, "rb") as image_file:
        return read_image_pil_file(image_file, grayscale)


def read_image_pil_file(image_file, grayscale=False) -> Image:
    with Image.open(image_file) as image:
        if grayscale:
            image = image.convert(mode="L")
        else:
            image = image.convert(mode=image.mode)
        return image
